#!/usr/bin/env python3
"""Create and execute durable, review-budgeted Hermes image batches."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import character_manager as cm

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = Path(r"D:\AI_Studio\workspace\hermes-night-batches")
SCENE_TOOL = ROOT / "tools" / "character_scene.py"
MAX_ITEMS = 48
MAX_GENERATED_IMAGES = 240
ENGINES = {"z-image", "krea2"}
GPU_LOCK_BACKOFF_SECONDS = (10, 20, 40)
SUCCESS_STATES = {"succeeded", "needs_review"}
GPU_LOCK_MARKERS = ("gpu lock", "already holds the gpu lock")


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, value: object) -> None:
    cm.atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_plan(plan: dict[str, Any]) -> dict[str, Any]:
    items = plan.get("items")
    if not isinstance(items, list) or not 1 <= len(items) <= MAX_ITEMS:
        raise cm.CharacterError(f"night batch requires 1-{MAX_ITEMS} items")
    normalized = []
    generated_images = 0
    for position, raw in enumerate(items, 1):
        if not isinstance(raw, dict):
            raise cm.CharacterError(f"item {position} must be an object")
        character_id = str(raw.get("character_id", "")).strip()
        prompt = str(raw.get("prompt", "")).strip()
        if not prompt and isinstance(raw.get("scenes"), list):
            raise cm.CharacterError(
                f"item {position}: nested scenes are unsupported; move every scenes[] entry into its own "
                "items[] object with character_id, prompt, engines, and count"
            )
        engines = list(dict.fromkeys(raw.get("engines") or ["z-image", "krea2"]))
        identity_reference = str(raw.get("identity_reference") or "").strip() or None
        reference_asset_id = str(raw.get("reference_asset_id") or "").strip() or None
        count = int(raw.get("count", 2))
        if not cm.character_record_path(character_id).is_file():
            raise cm.CharacterError(f"item {position}: unknown character {character_id!r}")
        if len(prompt) < 3:
            raise cm.CharacterError(f"item {position}: prompt must be a direct non-empty items[] field")
        if not engines or any(engine not in ENGINES for engine in engines):
            raise cm.CharacterError(f"item {position}: unsupported engines")
        if identity_reference and engines != ["krea2"]:
            raise cm.CharacterError(f"item {position}: identity_reference requires engines=['krea2']")
        if reference_asset_id and not identity_reference:
            raise cm.CharacterError(f"item {position}: reference_asset_id requires identity_reference")
        if not 1 <= count <= 10:
            raise cm.CharacterError(f"item {position}: count must be 1-10 per engine")
        generated_images += count * len(engines)
        normalized.append({
            "id": f"item-{position:02d}", "character_id": character_id, "prompt": prompt,
            "engines": engines, "count": count,
            "prompt_strategy": str(raw.get("prompt_strategy") or "strict_translation"),
            "immutable_constraints": raw.get("immutable_constraints") or {},
            "scene_spec": raw.get("scene_spec") or {},
            "identity_reference": identity_reference,
            "reference_asset_id": reference_asset_id,
            "variation_axes": raw.get("variation_axes") or {}, "status": "queued",
        })
    if generated_images > MAX_GENERATED_IMAGES:
        raise cm.CharacterError(f"generation budget exceeded: {generated_images} images requested, maximum is {MAX_GENERATED_IMAGES}")
    return {"schema_version": 1, "title": str(plan.get("title") or "Hermes night batch"),
            "source_request": str(plan.get("source_request") or ""), "generated_image_budget": generated_images,
            "items": normalized}


def active_batch(queue_root: Path) -> Path | None:
    if not queue_root.is_dir():
        return None
    for path in queue_root.iterdir():
        status_path = path / "status.json"
        if status_path.is_file() and load(status_path).get("status") in {"queued", "running"}:
            return path
    return None


def create(plan_path: Path, queue_root: Path, start: bool) -> Path:
    existing = active_batch(queue_root)
    if existing:
        raise cm.CharacterError(f"another Hermes batch is active: {existing.name}")
    plan = validate_plan(load(plan_path))
    batch_id = f"NIGHT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    root = queue_root / batch_id
    plan.update({"batch_id": batch_id, "created_at": stamp(), "created_by": "hermes"})
    write_json(root / "plan.json", plan)
    cm.atomic_write(root / "request.txt", plan["source_request"].rstrip() + "\n")
    write_json(root / "status.json", {"status": "queued", "created_at": stamp(), "updated_at": stamp(),
                                        "completed_items": 0, "failed_items": 0, "total_items": len(plan["items"])})
    if start:
        stdout = (root / "worker.stdout.log").open("ab")
        stderr = (root / "worker.stderr.log").open("ab")
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "run", "--batch-dir", str(root)],
                             cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                             creationflags=flags, close_fds=True)
        finally:
            stdout.close(); stderr.close()
    return root


def _command_text(result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(part for part in (result.stdout, result.stderr) if part)


def _load_session_batch(session_dir: Path) -> dict[str, Any]:
    value = load(session_dir / "batch.yaml")
    if not isinstance(value, dict):
        raise cm.CharacterError(f"invalid session batch record: {session_dir / 'batch.yaml'}")
    return value


def _recorded_failure_text(session_dir: Path) -> str:
    """Return errors from runs currently referenced by the session jobs.

    `local_wangp.py submit` returns before its detached worker tries the GPU lock. The
    lock failure therefore often appears only in run.json, not in the submit process'
    stderr. The scene command observes that terminal record and exits non-zero; read
    the same durable evidence here before deciding whether a retry is safe.
    """
    try:
        batch = _load_session_batch(session_dir)
    except (OSError, ValueError, json.JSONDecodeError, cm.CharacterError):
        return ""
    messages: list[str] = []
    for job in batch.get("jobs") or []:
        run_dir = job.get("run_dir") if isinstance(job, dict) else None
        if not run_dir:
            continue
        try:
            record = load(Path(run_dir) / "run.json")
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        messages.append(json.dumps(record.get("error") or {}, ensure_ascii=False))
    return "\n".join(messages)


def is_gpu_lock_failure(result: subprocess.CompletedProcess[str], session_dir: Path) -> bool:
    evidence = (_command_text(result) + "\n" + _recorded_failure_text(session_dir)).lower()
    return any(marker in evidence for marker in GPU_LOCK_MARKERS)


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def verify_session(session_dir: Path, expected_engines: list[str]) -> dict[str, Any]:
    """Verify the durable scene/run contract before an item is called complete."""
    prompt_path = session_dir / "prompt.txt"
    if not prompt_path.is_file() or not prompt_path.read_text(encoding="utf-8").strip():
        raise cm.CharacterError(f"missing or empty prompt: {prompt_path}")
    batch = _load_session_batch(session_dir)
    asset_root = Path((batch.get("session") or {}).get("asset_root") or session_dir / "outputs").resolve()
    jobs = batch.get("jobs") or []
    by_engine = {Path(str(job.get("output_dir") or "")).name: job for job in jobs if isinstance(job, dict)}
    verified_runs: list[dict[str, Any]] = []
    for engine in expected_engines:
        job = by_engine.get(engine)
        if not job:
            raise cm.CharacterError(f"session has no {engine} job")
        settings_path = session_dir / str(job.get("settings_file") or "")
        if not settings_path.is_file():
            raise cm.CharacterError(f"missing settings for {engine}: {settings_path}")
        settings = load(settings_path)
        if not str(settings.get("model_type") or "").strip():
            raise cm.CharacterError(f"settings for {engine} have no model_type")
        if job.get("status") != "completed":
            raise cm.CharacterError(f"{engine} job is {job.get('status')}, not completed")
        run_dir = Path(str(job.get("run_dir") or ""))
        if not run_dir.is_dir():
            raise cm.CharacterError(f"missing run directory for {engine}: {run_dir}")
        record = load(run_dir / "run.json")
        if record.get("status") not in SUCCESS_STATES:
            raise cm.CharacterError(f"{engine} run is {record.get('status')}, not successful")
        artifacts = [Path(str(item.get("path"))).resolve() for item in (record.get("artifacts") or [])
                     if isinstance(item, dict) and item.get("path")]
        expected_count = int(job.get("count") or 1)
        if len(artifacts) < expected_count:
            raise cm.CharacterError(f"{engine} run recorded {len(artifacts)}/{expected_count} artifacts")
        output_root = (asset_root / engine).resolve()
        invalid = [str(path) for path in artifacts if not path.is_file() or not _inside(path, output_root)]
        if invalid:
            raise cm.CharacterError(f"{engine} artifacts missing or outside output directory: {invalid}")
        references = record.get("reference_inputs") or []
        verified_runs.append({
            "engine": engine, "run_id": record.get("run_id") or run_dir.name,
            "run_dir": str(run_dir.resolve()), "status": record.get("status"),
            "model_type": settings["model_type"], "artifact_count": len(artifacts),
            "output_dir": str(output_root),
            "reference_bases": [item.get("basis") for item in references if isinstance(item, dict) and item.get("basis")],
        })
    return {"verified_at": stamp(), "prompt_file": str(prompt_path.resolve()), "asset_root": str(asset_root),
            "runs": verified_runs}


def _prepare_item(item: dict[str, Any], root: Path, run_command: Any) -> Path:
    command = [sys.executable, str(SCENE_TOOL), "prepare", "--character", item["character_id"],
               "--request", item["prompt"], "--engines", ",".join(item["engines"]), "--count", str(item["count"]),
               "--strategy", item["prompt_strategy"], "--constraints-json", json.dumps(item["immutable_constraints"], ensure_ascii=False),
               "--scene-spec-json", json.dumps(item["scene_spec"], ensure_ascii=False), "--actor", "hermes"]
    if item.get("identity_reference"):
        command += ["--identity-reference", item["identity_reference"]]
    if item.get("reference_asset_id"):
        command += ["--reference-asset-id", item["reference_asset_id"]]
    result = run_command(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (root / f"{item['id']}.prepare.log").write_text(_command_text(result), encoding="utf-8")
    if result.returncode != 0:
        raise cm.CharacterError((_command_text(result).strip() or "scene preparation failed")[-4000:])
    payload = json.loads(result.stdout)
    session_dir = Path(payload["session_dir"]).resolve()
    item["session_dir"] = str(session_dir)
    return session_dir


def _render_item(item: dict[str, Any], session_dir: Path, root: Path, run_command: Any,
                 sleep: Any, backoff_seconds: tuple[int, ...]) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCENE_TOOL), "produce", "--session-dir", str(session_dir)]
    attempts = item.setdefault("attempts", [])
    for attempt_number in range(1, len(backoff_seconds) + 2):
        result = run_command(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        log_path = root / f"{item['id']}.attempt-{attempt_number}.log"
        log_path.write_text(_command_text(result), encoding="utf-8")
        lock_failure = result.returncode != 0 and is_gpu_lock_failure(result, session_dir)
        attempt = {"attempt": attempt_number, "finished_at": stamp(), "returncode": result.returncode,
                   "gpu_lock_failure": lock_failure, "log": str(log_path)}
        attempts.append(attempt)
        write_json(root / "plan.json", load(root / "plan.json") | {
            "items": [item if current.get("id") == item.get("id") else current
                      for current in load(root / "plan.json").get("items", [])]
        })
        if result.returncode == 0:
            return result
        if not lock_failure or attempt_number > len(backoff_seconds):
            return result
        delay = backoff_seconds[attempt_number - 1]
        attempt["retry_after_seconds"] = delay
        write_json(root / "plan.json", load(root / "plan.json") | {
            "items": [item if current.get("id") == item.get("id") else current
                      for current in load(root / "plan.json").get("items", [])]
        })
        sleep(delay)
    raise AssertionError("unreachable")


def run(root: Path, sync_url: str, *, run_command: Any = subprocess.run, sleep: Any = time.sleep,
        backoff_seconds: tuple[int, ...] = GPU_LOCK_BACKOFF_SECONDS) -> int:
    plan = load(root / "plan.json")
    completed_count = failed_count = 0
    write_json(root / "status.json", {"status": "running", "updated_at": stamp(), "total_items": len(plan["items"]),
                                        "completed_items": 0, "failed_items": 0})
    for item in plan["items"]:
        item["status"] = "running"; item["started_at"] = stamp(); write_json(root / "plan.json", plan)
        try:
            session_dir = Path(item["session_dir"]).resolve() if item.get("session_dir") else _prepare_item(item, root, run_command)
            write_json(root / "plan.json", plan)
            result = _render_item(item, session_dir, root, run_command, sleep, backoff_seconds)
        except (cm.CharacterError, OSError, ValueError, json.JSONDecodeError) as exc:
            result = subprocess.CompletedProcess([], 2, "", f"{type(exc).__name__}: {exc}")
        if result.returncode == 0:
            try:
                verification = verify_session(session_dir, item["engines"])
            except (cm.CharacterError, OSError, ValueError, json.JSONDecodeError) as exc:
                item.update({"status": "failed", "error": f"verification failed: {exc}", "completed_at": stamp()}); failed_count += 1
                write_json(root / "plan.json", plan)
                write_json(root / "status.json", {"status": "running", "updated_at": stamp(), "total_items": len(plan["items"]),
                                                    "completed_items": completed_count, "failed_items": failed_count})
                continue
            item.update({"status": "completed", "verification": verification, "completed_at": stamp()}); completed_count += 1
            try: urllib.request.urlopen(urllib.request.Request(sync_url, method="POST"), timeout=120).read()
            except Exception as exc: item["sync_error"] = str(exc)
        else:
            item.update({"status": "failed", "error": _command_text(result).strip()[-4000:], "completed_at": stamp()}); failed_count += 1
        write_json(root / "plan.json", plan)
        write_json(root / "status.json", {"status": "running", "updated_at": stamp(), "total_items": len(plan["items"]),
                                            "completed_items": completed_count, "failed_items": failed_count})
    final = "completed" if failed_count == 0 else "completed_with_errors"
    write_json(root / "status.json", {"status": final, "updated_at": stamp(), "total_items": len(plan["items"]),
                                        "completed_items": completed_count, "failed_items": failed_count})
    return 0 if failed_count == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("create"); make.add_argument("--plan-file", type=Path, required=True); make.add_argument("--queue-root", type=Path, default=DEFAULT_QUEUE); make.add_argument("--no-start", action="store_true")
    work = sub.add_parser("run"); work.add_argument("--batch-dir", type=Path, required=True); work.add_argument("--sync-url", default="http://127.0.0.1:8787/api/sync")
    args = parser.parse_args()
    try:
        if args.command == "create": print(json.dumps({"batch_dir": str(create(args.plan_file.resolve(), args.queue_root.resolve(), not args.no_start)), "status": "queued"}, ensure_ascii=False, indent=2)); return 0
        return run(args.batch_dir.resolve(), args.sync_url)
    except (cm.CharacterError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2


if __name__ == "__main__": raise SystemExit(main())
