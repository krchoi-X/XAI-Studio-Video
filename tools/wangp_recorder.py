from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TERMINAL_STATES = {"succeeded", "failed", "cancelled", "interrupted", "timed_out"}


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prompt_hash(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def normalized_prompt_hash(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    return prompt_hash(normalized)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def append_event(run_dir: Path, state: str, **details: Any) -> dict[str, Any]:
    event = {"at": now(), "state": state, **{key: value for key, value in details.items() if value is not None}}
    with (run_dir / "events.jsonl").open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    return event


def load_run(run_dir: Path) -> dict[str, Any]:
    return json.loads((run_dir / "run.json").read_text(encoding="utf-8"))


def save_run(run_dir: Path, record: dict[str, Any]) -> None:
    record["updated_at"] = now()
    write_json(run_dir / "run.json", record)


def prepare_run(args: argparse.Namespace) -> dict[str, Any]:
    prompt_path = Path(args.prompt_file).resolve()
    prompt_bytes = prompt_path.read_bytes()
    prompt_text = prompt_bytes.decode("utf-8")
    run_id = args.run_id or f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    run_dir = Path(args.runs_root).resolve() / run_id
    if run_dir.exists():
        raise ValueError(f"run already exists: {run_dir}")
    run_dir.mkdir(parents=True)
    settings: Any = None
    settings_path = None
    if args.settings_file:
        settings_path = Path(args.settings_file).resolve()
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    created_at = now()
    record = {
        "schema_version": 1,
        "run_id": run_id,
        "project_id": args.project_id,
        "prompt_id": args.prompt_id,
        "status": "queued",
        "created_at": created_at,
        "updated_at": created_at,
        "target": args.target,
        "renderer": "WanGP",
        "provider_job_id": None,
        "prompt": {
            "path": str(prompt_path),
            "sha256": sha256_bytes(prompt_bytes),
            "normalized_sha256": normalized_prompt_hash(prompt_text),
            "byte_count": len(prompt_bytes),
        },
        "settings": {"path": str(settings_path) if settings_path else None, "value": settings},
        "artifacts": [],
        "error": None,
    }
    save_run(run_dir, record)
    append_event(run_dir, "queued", prompt_sha256=record["prompt"]["sha256"], target=args.target)
    return {"run_dir": str(run_dir), **record}


def update_state(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = Path(args.run_dir).resolve()
    record = load_run(run_dir)
    if record["status"] in TERMINAL_STATES:
        raise ValueError(f"run is already terminal: {record['status']}")
    record["status"] = args.state
    if args.provider_job_id:
        record["provider_job_id"] = args.provider_job_id
    save_run(run_dir, record)
    append_event(run_dir, args.state, provider_job_id=args.provider_job_id, message=args.message)
    return record


def ffprobe_metadata(path: Path, ffprobe: str = "ffprobe") -> dict[str, Any] | None:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format_tags", "-of", "json", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "ffprobe failed").strip())
    tags = ((json.loads(result.stdout) or {}).get("format") or {}).get("tags") or {}
    for key, value in tags.items():
        if str(key).lower() in {"comment", "description"}:
            try:
                parsed = json.loads(str(value).strip().rstrip("\0"))
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    return None


def find_prompt(metadata: Any) -> str | None:
    if isinstance(metadata, dict):
        direct = metadata.get("prompt")
        if isinstance(direct, str):
            return direct
        for value in metadata.values():
            found = find_prompt(value)
            if found is not None:
                return found
    elif isinstance(metadata, list):
        for value in metadata:
            found = find_prompt(value)
            if found is not None:
                return found
    return None


def attach_artifact(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = Path(args.run_dir).resolve()
    artifact_path = Path(args.artifact).resolve()
    record = load_run(run_dir)
    if not artifact_path.is_file():
        raise ValueError(f"artifact not found: {artifact_path}")
    metadata = ffprobe_metadata(artifact_path, args.ffprobe)
    embedded_prompt = find_prompt(metadata)
    embedded_hash = prompt_hash(embedded_prompt) if embedded_prompt is not None else None
    embedded_normalized_hash = normalized_prompt_hash(embedded_prompt) if embedded_prompt is not None else None
    exact_match = embedded_hash == record["prompt"]["sha256"] if embedded_hash else False
    normalized_match = embedded_normalized_hash == record["prompt"]["normalized_sha256"] if embedded_normalized_hash else False
    artifact = {
        "path": str(artifact_path),
        "sha256": sha256_file(artifact_path),
        "byte_count": artifact_path.stat().st_size,
        "metadata_present": metadata is not None,
        "embedded_prompt_sha256": embedded_hash,
        "prompt_exact_match": exact_match,
        "prompt_normalized_match": normalized_match,
        "verified_at": now(),
    }
    record["artifacts"].append(artifact)
    record["status"] = "succeeded" if exact_match else "needs_review"
    save_run(run_dir, record)
    append_event(
        run_dir,
        record["status"],
        artifact_path=str(artifact_path),
        artifact_sha256=artifact["sha256"],
        prompt_exact_match=exact_match,
        prompt_normalized_match=normalized_match,
    )
    write_json(run_dir / "artifact-manifest.json", {"run_id": record["run_id"], "artifacts": record["artifacts"]})
    return record


def fail_run(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = Path(args.run_dir).resolve()
    record = load_run(run_dir)
    record["status"] = "failed"
    record["error"] = {"message": args.message, "last_progress": args.last_progress, "recorded_at": now()}
    save_run(run_dir, record)
    append_event(run_dir, "failed", message=args.message, last_progress=args.last_progress)
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Durably match exact WanGP prompts, runs, and artifacts")
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--runs-root", required=True)
    prepare.add_argument("--prompt-file", required=True)
    prepare.add_argument("--project-id", required=True)
    prepare.add_argument("--prompt-id", required=True)
    prepare.add_argument("--target", choices=("local", "runpod", "vast"), required=True)
    prepare.add_argument("--settings-file")
    prepare.add_argument("--run-id")
    prepare.set_defaults(handler=prepare_run)

    state = sub.add_parser("state")
    state.add_argument("--run-dir", required=True)
    state.add_argument("--state", choices=("provisioning", "starting", "running", "uploading", "interrupted", "timed_out"), required=True)
    state.add_argument("--provider-job-id")
    state.add_argument("--message")
    state.set_defaults(handler=update_state)

    attach = sub.add_parser("attach")
    attach.add_argument("--run-dir", required=True)
    attach.add_argument("--artifact", required=True)
    attach.add_argument("--ffprobe", default="ffprobe")
    attach.set_defaults(handler=attach_artifact)

    fail = sub.add_parser("fail")
    fail.add_argument("--run-dir", required=True)
    fail.add_argument("--message", required=True)
    fail.add_argument("--last-progress")
    fail.set_defaults(handler=fail_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(json.dumps(args.handler(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
