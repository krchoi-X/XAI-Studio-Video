from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import wangp_recorder


DEFAULT_WANGP_ROOT = Path(r"D:\AI\WanGP")


def write_json(path: Path, value: Any) -> None:
    wangp_recorder.write_json(path, value)


def load_settings(path: Path, prompt: str, run_id: str) -> dict[str, Any]:
    settings = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(settings, dict):
        raise ValueError("settings file must contain one JSON object")
    settings["prompt"] = prompt
    settings["output_filename"] = run_id
    return settings


def resolve_python(wangp_root: Path, explicit: str | None) -> Path:
    candidates = [Path(explicit)] if explicit else []
    candidates.extend([wangp_root / "env_uv" / "Scripts" / "python.exe", wangp_root / ".venv" / "bin" / "python"])
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise ValueError("WanGP Python was not found; pass --wangp-python")


def doctor(args: argparse.Namespace) -> dict[str, Any]:
    wangp_root = Path(args.wangp_root).resolve()
    python = resolve_python(wangp_root, args.wangp_python)
    checks = {
        "wangp_root": wangp_root.is_dir(),
        "wgp_py": (wangp_root / "wgp.py").is_file(),
        "shared_api": (wangp_root / "shared" / "api.py").is_file(),
        "python": python.is_file(),
        "ffprobe": subprocess.run(["ffprobe", "-version"], capture_output=True, check=False).returncode == 0,
    }
    import_check = subprocess.run(
        [str(python), "-c", "from shared.api import init; print('WanGP API import OK')"],
        cwd=str(wangp_root), capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    checks["api_import"] = import_check.returncode == 0
    return {"ok": all(checks.values()), "checks": checks, "api_import_output": (import_check.stdout or import_check.stderr).strip()}


def submit(args: argparse.Namespace) -> dict[str, Any]:
    wangp_root = Path(args.wangp_root).resolve()
    python = resolve_python(wangp_root, args.wangp_python)
    prompt_path = Path(args.prompt_file).resolve()
    settings_path = Path(args.settings_file).resolve()
    prompt = prompt_path.read_text(encoding="utf-8")
    run = wangp_recorder.prepare_run(
        argparse.Namespace(
            runs_root=args.runs_root,
            prompt_file=str(prompt_path),
            project_id=args.project_id,
            prompt_id=args.prompt_id,
            target="local",
            settings_file=str(settings_path),
            run_id=args.run_id,
        )
    )
    run_dir = Path(run["run_dir"])
    effective_settings = load_settings(settings_path, prompt, run["run_id"])
    effective_path = run_dir / "effective-settings.json"
    write_json(effective_path, effective_settings)
    stdout_path = run_dir / "worker.stdout.log"
    stderr_path = run_dir / "worker.stderr.log"
    command = [
        str(python), str(Path(__file__).resolve()), "worker",
        "--run-dir", str(run_dir),
        "--wangp-root", str(wangp_root),
        "--settings-file", str(effective_path),
        "--output-dir", str(Path(args.output_dir).resolve()),
        "--profile", str(args.profile),
        "--vram-safety", str(args.vram_safety),
    ]
    creationflags = 0
    popen_kwargs: dict[str, Any] = {}
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    else:
        popen_kwargs["start_new_session"] = True
    with stdout_path.open("ab") as stdout, stderr_path.open("ab") as stderr:
        process = subprocess.Popen(
            command, cwd=str(wangp_root), stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
            creationflags=creationflags, close_fds=True, **popen_kwargs,
        )
    record = wangp_recorder.load_run(run_dir)
    record["local_worker"] = {"pid": process.pid, "command": command, "stdout": str(stdout_path), "stderr": str(stderr_path)}
    wangp_recorder.save_run(run_dir, record)
    wangp_recorder.append_event(run_dir, "starting", local_worker_pid=process.pid)
    return {"run_id": run["run_id"], "run_dir": str(run_dir), "worker_pid": process.pid, "status": "starting"}


def acquire_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+b")
    try:
        if os.name == "nt":
            import msvcrt
            if path.stat().st_size == 0:
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        handle.close()
        raise RuntimeError("another XAI local WanGP worker already holds the GPU lock")
    return handle


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    fields = getattr(value, "__dataclass_fields__", None)
    if fields:
        return {name: json_safe(getattr(value, name)) for name in fields}
    return str(value)


def worker(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = Path(args.run_dir).resolve()
    wangp_root = Path(args.wangp_root).resolve()
    lock = acquire_lock(wangp_root / "outputs" / ".xai-local-worker.lock")
    try:
        sys.path.insert(0, str(wangp_root))
        from shared.api import init

        settings = json.loads(Path(args.settings_file).read_text(encoding="utf-8"))
        record = wangp_recorder.load_run(run_dir)
        record["status"] = "running"
        record["provider_job_id"] = f"local-pid-{os.getpid()}"
        wangp_recorder.save_run(run_dir, record)
        wangp_recorder.append_event(run_dir, "running", provider_job_id=record["provider_job_id"])
        session = init(
            root=str(wangp_root),
            config_path=str(wangp_root / "wgp_config.json"),
            output_dir=str(Path(args.output_dir).resolve()),
            cli_args=("--profile", str(args.profile), "--vram-safety-coefficient", str(args.vram_safety)),
            console_output=True,
            console_isatty=False,
        )
        job = session.submit(settings)
        last_progress: str | None = None
        for event in job.events.iter(timeout=0.5):
            data = json_safe(event.data)
            if event.kind == "preview" and isinstance(data, dict):
                last_progress = f"{data.get('phase') or 'generation'} {data.get('current_step')}/{data.get('total_steps')}"
                wangp_recorder.append_event(run_dir, "running", progress=last_progress, preview=data)
            elif event.kind in {"error", "completed"}:
                wangp_recorder.append_event(run_dir, event.kind, data=data)
        result = job.result(timeout=0)
        if not result.success:
            message = "; ".join(str(error) for error in result.errors) or "WanGP generation failed"
            return wangp_recorder.fail_run(argparse.Namespace(run_dir=str(run_dir), message=message, last_progress=last_progress))
        artifacts = [Path(path) for path in result.generated_files if path]
        if not artifacts:
            artifacts = [Path(item.path) for item in result.artifacts if item.path]
        if not artifacts:
            return wangp_recorder.fail_run(argparse.Namespace(run_dir=str(run_dir), message="WanGP reported success without an artifact path", last_progress=last_progress))
        final_record = None
        for artifact in artifacts:
            final_record = wangp_recorder.attach_artifact(
                argparse.Namespace(run_dir=str(run_dir), artifact=str(artifact), ffprobe="ffprobe")
            )
        return final_record or record
    except Exception as exc:
        try:
            return wangp_recorder.fail_run(
                argparse.Namespace(run_dir=str(run_dir), message=f"{type(exc).__name__}: {exc}", last_progress=None)
            )
        except Exception:
            raise
    finally:
        lock.close()


def status(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = Path(args.run_dir).resolve()
    record = wangp_recorder.load_run(run_dir)
    events_path = run_dir / "events.jsonl"
    events = []
    if events_path.is_file():
        lines = events_path.read_text(encoding="utf-8").splitlines()
        events = [json.loads(line) for line in lines[-args.event_limit:] if line.strip()]
    return {"run": record, "recent_events": events}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Persistent local WanGP submission and recording")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("doctor")
    check.add_argument("--wangp-root", default=str(DEFAULT_WANGP_ROOT))
    check.add_argument("--wangp-python")
    check.set_defaults(handler=doctor)

    start = sub.add_parser("submit")
    start.add_argument("--runs-root", required=True)
    start.add_argument("--prompt-file", required=True)
    start.add_argument("--settings-file", required=True)
    start.add_argument("--project-id", required=True)
    start.add_argument("--prompt-id", required=True)
    start.add_argument("--run-id")
    start.add_argument("--wangp-root", default=str(DEFAULT_WANGP_ROOT))
    start.add_argument("--wangp-python")
    start.add_argument("--output-dir", default=str(DEFAULT_WANGP_ROOT / "outputs"))
    start.add_argument("--profile", default="4")
    start.add_argument("--vram-safety", type=float, default=0.8)
    start.set_defaults(handler=submit)

    work = sub.add_parser("worker", help=argparse.SUPPRESS)
    work.add_argument("--run-dir", required=True)
    work.add_argument("--wangp-root", required=True)
    work.add_argument("--settings-file", required=True)
    work.add_argument("--output-dir", required=True)
    work.add_argument("--profile", required=True)
    work.add_argument("--vram-safety", required=True, type=float)
    work.set_defaults(handler=worker)

    show = sub.add_parser("status")
    show.add_argument("--run-dir", required=True)
    show.add_argument("--event-limit", type=int, default=10)
    show.set_defaults(handler=status)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = args.handler(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not isinstance(result, dict) or result.get("ok", True) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
