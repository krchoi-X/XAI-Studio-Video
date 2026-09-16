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
DEFAULT_EXECUTOR = "local-wangp-worker"  # what runs the job; distinct from requested_by, renderer, and model_type
KREA2_EDIT_MODELS = {"krea2_raw_edit", "krea2_turbo_edit"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def write_json(path: Path, value: Any) -> None:
    wangp_recorder.write_json(path, value)


def load_settings(path: Path, prompt: str, run_id: str) -> dict[str, Any]:
    settings = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(settings, dict):
        raise ValueError("settings file must contain one JSON object")
    settings["prompt"] = prompt
    settings["output_filename"] = run_id
    return settings


def validate_reference_settings(settings: dict[str, Any]) -> list[dict[str, Any]]:
    provenance = settings.get("_xai")
    if not isinstance(provenance, dict) or provenance.get("kind") not in {"reference_variation", "reference_transformation"}:
        return []
    model_type = str(settings.get("base_model_type") or settings.get("model_type") or "")
    if model_type not in KREA2_EDIT_MODELS:
        raise ValueError("reference variation requires a Krea2 edit architecture; text-to-image fallback is disabled")
    raw_refs = settings.get("image_refs")
    refs = raw_refs if isinstance(raw_refs, list) else [raw_refs] if raw_refs else []
    if not 1 <= len(refs) <= 2:
        raise ValueError("Krea2 reference variation requires one or two reference images")
    asset_ids = provenance.get("reference_asset_ids") or []
    records = []
    for index, value in enumerate(refs):
        path = Path(str(value)).resolve()
        if not path.is_file():
            raise ValueError(f"reference image not found: {path}")
        if path.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"unsupported reference image: {path}")
        records.append({
            "asset_id": str(asset_ids[index]) if index < len(asset_ids) else None,
            "path": str(path),
            "sha256": wangp_recorder.sha256_file(path),
            "byte_count": path.stat().st_size,
        })
    return records


def _reference_values(settings: dict[str, Any]) -> list[str]:
    raw_refs = settings.get("image_refs")
    refs = raw_refs if isinstance(raw_refs, list) else [raw_refs] if raw_refs else []
    return [str(value).strip() for value in refs if str(value).strip()]


def _session_character_id(session_dir: Path) -> str | None:
    """Find the durable character ID without inferring it from a display name."""
    provenance_path = session_dir / "session-provenance.json"
    if provenance_path.is_file():
        try:
            provenance = wangp_recorder.read_json_file(provenance_path)
        except (OSError, ValueError):
            provenance = None
        if isinstance(provenance, dict) and str(provenance.get("character_id") or "").strip():
            return str(provenance["character_id"]).strip()
    # Preserve the historical directory fallback for already-existing sessions.
    if session_dir.parent.name == "02_generations" and session_dir.parent.parent.name.startswith("ch-"):
        return session_dir.parent.parent.name
    # Shared sessions carry the explicit character ID in the existing batch contract.
    batch_path = session_dir / "batch.yaml"
    if session_dir.parent.name == "generations" and batch_path.is_file():
        import character_manager as cm
        cm.validate_generation_session(session_dir)
        import yaml
        batch = yaml.safe_load(batch_path.read_text(encoding="utf-8")) or {}
        identifier = (batch.get("session") or {}).get("character_id") or batch.get("character_id")
        if identifier:
            return str(identifier)
    return None


def resolve_character_default_reference(settings: dict[str, Any], session_dir: Path) -> list[dict[str, Any]]:
    """Inject the explicitly selected identity reference for a Ref2VA character session.

    A setting-provided reference always wins.  The fallback is not a newest-file search: it reads the optional,
    durable `character.json.reference_defaults.identity` record authored for that character.
    """
    model_type = str(settings.get("base_model_type") or settings.get("model_type") or "").lower()
    if "ref2va" not in model_type or _reference_values(settings):
        return []
    character_id = _session_character_id(session_dir)
    if not character_id:
        raise ValueError("Ref2VA requires image_refs; no character_id is recorded for this session")
    import character_manager as cm
    character_path = cm.character_record_path(character_id)
    try:
        character = json.loads(character_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Ref2VA character record not found: {character_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid character record: {character_path}") from exc
    defaults = character.get("reference_defaults")
    identity = defaults.get("identity") if isinstance(defaults, dict) else None
    if not isinstance(identity, dict) or not str(identity.get("path") or "").strip():
        raise ValueError(f"Ref2VA requires image_refs; {character_id} has no reference_defaults.identity record")
    path = Path(str(identity["path"])).resolve()
    if not path.is_file():
        raise ValueError(f"character default reference not found: {path}")
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        raise ValueError(f"unsupported character default reference: {path}")
    settings["image_refs"] = [str(path)]
    return [{
        "path": str(path),
        "sha256": wangp_recorder.sha256_file(path),
        "byte_count": path.stat().st_size,
        "character_id": character_id,
        "basis": "character-default",
        "source": identity.get("source"),
    }]


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
    # Requester resolution order, all of them explicit statements by the caller or by the session record:
    #   --requested-by  ->  $XAI_REQUESTED_BY  ->  the session's own provenance record  ->  null.
    # Nothing is inferred; when every source is silent the run records null and the Control Tower falls back
    # to observing the worker process.
    session_dir = Path(args.runs_root).resolve().parent
    requested_by = wangp_recorder.normalize_actor(args.requested_by if args.requested_by is not None else os.environ.get("XAI_REQUESTED_BY"))
    if not requested_by:
        # <session>/runs/<run-id> is the layout every producer uses, so the session is the runs-root's parent.
        requested_by = wangp_recorder.normalize_actor(wangp_recorder.session_requester(session_dir))
    executor = args.executor or DEFAULT_EXECUTOR
    run = wangp_recorder.prepare_run(
        argparse.Namespace(
            runs_root=args.runs_root,
            prompt_file=str(prompt_path),
            project_id=args.project_id,
            prompt_id=args.prompt_id,
            target="local",
            settings_file=str(settings_path),
            run_id=args.run_id,
            requested_by=requested_by,
            executor=executor,
        )
    )
    run_dir = Path(run["run_dir"])
    effective_settings = load_settings(settings_path, prompt, run["run_id"])
    reference_records = resolve_character_default_reference(effective_settings, session_dir)
    reference_records.extend(validate_reference_settings(effective_settings))
    effective_path = run_dir / "effective-settings.json"
    write_json(effective_path, effective_settings)
    if reference_records:
        record = wangp_recorder.load_run(run_dir)
        record["reference_inputs"] = reference_records
        if effective_settings.get("_xai"):
            record["variation"] = effective_settings["_xai"]
        wangp_recorder.save_run(run_dir, record)
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
    if requested_by:
        # visible on the detached worker's command line for process observers; the record is the source of truth
        command += ["--requested-by", requested_by]
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
    return {"run_id": run["run_id"], "run_dir": str(run_dir), "worker_pid": process.pid, "status": "starting",
            "requested_by": requested_by, "executor": executor}


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
    lock = None
    try:
        lock = acquire_lock(wangp_root / "outputs" / ".xai-local-worker.lock")
        sys.path.insert(0, str(wangp_root))
        from shared.api import init

        settings = json.loads(Path(args.settings_file).read_text(encoding="utf-8"))
        settings.pop("_xai", None)
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
        if lock is not None:
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
    start.add_argument("--profile", type=int, default=4)
    start.add_argument("--vram-safety", type=float, default=0.8)
    start.add_argument("--requested-by", default=None,
                       help="who asked for this run (grok, claude, codex, hermes, web, user, ...); defaults to $XAI_REQUESTED_BY, else recorded as null")
    start.add_argument("--executor", default=None, help=f"what executes the run (default {DEFAULT_EXECUTOR})")
    start.set_defaults(handler=submit)

    work = sub.add_parser("worker", help=argparse.SUPPRESS)
    work.add_argument("--run-dir", required=True)
    work.add_argument("--wangp-root", required=True)
    work.add_argument("--settings-file", required=True)
    work.add_argument("--output-dir", required=True)
    work.add_argument("--profile", required=True)
    work.add_argument("--vram-safety", required=True, type=float)
    work.add_argument("--requested-by", default=None, help=argparse.SUPPRESS)  # informational; run.json is authoritative
    work.set_defaults(handler=worker)

    show = sub.add_parser("status")
    show.add_argument("--run-dir", required=True)
    show.add_argument("--event-limit", type=int, default=10)
    show.set_defaults(handler=status)
    return parser


def force_utf8_stdio() -> None:
    """Emit UTF-8 regardless of the console code page.

    Callers (character_scene, the web worker, agent orchestrators) decode this output as UTF-8, while a Windows
    console defaults to cp949 here. Korean prompts and error messages would otherwise be undecodable.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def main(argv: list[str] | None = None) -> int:
    force_utf8_stdio()
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
