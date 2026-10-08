#!/usr/bin/env python3
"""Create and execute durable, review-budgeted Hermes image batches."""

from __future__ import annotations

import argparse
import ctypes
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
import gpu_runtime

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = Path(r"D:\AI_Studio\workspace\hermes-night-batches")
SCENE_TOOL = ROOT / "tools" / "character_scene.py"
MAX_ITEMS = 48
MAX_GENERATED_IMAGES = 240
ENGINES = {"z-image", "krea2", "qwen21"}
# Engines that can bind a hash-verified identity reference. A reference-bound item selects exactly one of them.
REFERENCE_ENGINES = ("krea2", "qwen21")
# Only Qwen takes references after the identity reference; the scene CLI validates roles, files and hashes.
MULTI_REFERENCE_ENGINES = ("qwen21",)
GPU_LOCK_BACKOFF_SECONDS = (10, 20, 40)
SUCCESS_STATES = {"succeeded", "needs_review"}
GPU_LOCK_MARKERS = ("gpu lock", "already holds the gpu lock")
ACTIVE_STATES = {"queued", "running", "pausing", "cancelling"}
TERMINAL_STATES = {"completed", "completed_with_errors", "failed", "cancelled"}
STALE_AFTER_SECONDS = 120


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, value: object) -> None:
    cm.atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_stamp(value: object) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def process_alive(pid: object) -> bool:
    try:
        number = int(pid)
        if number <= 0:
            return False
        if os.name == "nt":
            handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, number)
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True
            return ctypes.get_last_error() == 5  # access denied still proves the process exists
        os.kill(number, 0)
        return True
    except (TypeError, ValueError, OSError, SystemError):
        return False


def _counts(plan: dict[str, Any]) -> tuple[int, int]:
    items = plan.get("items") or []
    return (sum(item.get("status") == "completed" for item in items),
            sum(item.get("status") == "failed" for item in items))


def write_status(root: Path, status: str, *, error: str | None = None, **extra: object) -> dict[str, Any]:
    path = root / "status.json"
    previous = load(path) if path.is_file() else {}
    plan = load(root / "plan.json") if (root / "plan.json").is_file() else {"items": []}
    completed, failed = _counts(plan)
    value = {
        **previous, "status": status, "updated_at": stamp(), "heartbeat_at": stamp(),
        "total_items": len(plan.get("items") or []), "completed_items": completed,
        "failed_items": failed, **extra,
    }
    if error is not None:
        value["error"] = error
    elif status not in {"failed", "completed_with_errors"}:
        value.pop("error", None)
    if status in TERMINAL_STATES or status in {"paused", "interrupted"}:
        value.pop("current_item", None)
    write_json(path, value)
    return value


def reconcile(root: Path, *, stale_after_seconds: int = STALE_AFTER_SECONDS) -> dict[str, Any]:
    """Turn an orphaned active record into an explicit resumable state."""
    state = load(root / "status.json")
    if state.get("status") not in ACTIVE_STATES:
        return state
    updated = _parse_stamp(state.get("heartbeat_at") or state.get("updated_at") or state.get("created_at"))
    age = (datetime.now(timezone.utc) - updated).total_seconds() if updated else stale_after_seconds + 1
    pid = state.get("worker_pid")
    # A freshly queued record gets a short launch grace; running records without a
    # live recorded owner are immediately recoverable.
    stale = (state.get("status") == "running" and not process_alive(pid)) or (
        state.get("status") != "running" and age > stale_after_seconds and not process_alive(pid)
    )
    if not stale:
        return state
    plan = load(root / "plan.json")
    for item in plan.get("items") or []:
        if item.get("status") == "running":
            item["status"] = "interrupted"
            item["interrupted_at"] = stamp()
    write_json(root / "plan.json", plan)
    return write_status(root, "interrupted", error="Batch worker exited or stopped heartbeating; safe to resume.", worker_pid=None)


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
        additional_references = _normalize_additional_references(raw.get("additional_references"), position)
        seed = raw.get("seed")
        if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int) or seed < 0):
            raise cm.CharacterError(f"item {position}: seed must be a non-negative integer")
        count = int(raw.get("count", 2))
        if not cm.character_record_path(character_id).is_file():
            raise cm.CharacterError(f"item {position}: unknown character {character_id!r}")
        if len(prompt) < 3:
            raise cm.CharacterError(f"item {position}: prompt must be a direct non-empty items[] field")
        if not engines or any(engine not in ENGINES for engine in engines):
            raise cm.CharacterError(f"item {position}: unsupported engines")
        if identity_reference and (len(engines) != 1 or engines[0] not in REFERENCE_ENGINES):
            raise cm.CharacterError(
                f"item {position}: identity_reference requires exactly one engine from {list(REFERENCE_ENGINES)}"
            )
        if reference_asset_id and not identity_reference:
            raise cm.CharacterError(f"item {position}: reference_asset_id requires identity_reference")
        if additional_references and (not identity_reference or engines[0] not in MULTI_REFERENCE_ENGINES):
            raise cm.CharacterError(
                f"item {position}: additional_references require identity_reference and engines={list(MULTI_REFERENCE_ENGINES)}"
            )
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
            "additional_references": additional_references,
            "seed": seed,
            "variation_axes": raw.get("variation_axes") or {}, "status": "queued",
        })
    if generated_images > MAX_GENERATED_IMAGES:
        raise cm.CharacterError(f"generation budget exceeded: {generated_images} images requested, maximum is {MAX_GENERATED_IMAGES}")
    return {"schema_version": 1, "title": str(plan.get("title") or "Hermes night batch"),
            "source_request": str(plan.get("source_request") or ""), "generated_image_budget": generated_images,
            "items": normalized}


def _normalize_additional_references(value: Any, position: int) -> list[str]:
    """Accept `ROLE=PATH` strings or {"role", "path"} objects and keep their order as `ROLE=PATH` strings."""
    if value in (None, []):
        return []
    if not isinstance(value, list):
        raise cm.CharacterError(f"item {position}: additional_references must be a list")
    normalized = []
    for entry in value:
        if isinstance(entry, dict):
            role, path = str(entry.get("role") or "").strip(), str(entry.get("path") or "").strip()
        else:
            role, _, path = str(entry).partition("=")
            role, path = role.strip(), path.strip()
        if not role or not path:
            raise cm.CharacterError(f"item {position}: each additional reference needs a role and a path")
        normalized.append(f"{role}={path}")
    return normalized


def active_batch(queue_root: Path) -> Path | None:
    if not queue_root.is_dir():
        return None
    for path in queue_root.iterdir():
        status_path = path / "status.json"
        if status_path.is_file():
            try:
                state = reconcile(path)
            except (OSError, ValueError, json.JSONDecodeError):
                continue
            if state.get("status") in ACTIVE_STATES or state.get("status") == "paused":
                return path
    return None


def create(plan_path: Path, queue_root: Path, start: bool) -> Path:
    existing = active_batch(queue_root)
    if existing:
        raise cm.CharacterError(f"another Hermes batch is active: {existing.name}")
    plan = validate_plan(load(plan_path))
    batch_id = f"BATCH-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    root = queue_root / batch_id
    plan.update({"batch_id": batch_id, "created_at": stamp(), "created_by": "hermes"})
    write_json(root / "plan.json", plan)
    cm.atomic_write(root / "request.txt", plan["source_request"].rstrip() + "\n")
    write_json(root / "status.json", {"status": "queued", "created_at": stamp(), "updated_at": stamp(),
                                        "completed_items": 0, "failed_items": 0, "total_items": len(plan["items"])})
    if start:
        launch_worker(root)
    return root


def launch_worker(root: Path) -> int:
    stdout = (root / "worker.stdout.log").open("ab")
    stderr = (root / "worker.stderr.log").open("ab")
    flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "run", "--batch-dir", str(root)],
                                   cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                   creationflags=flags, close_fds=True)
    finally:
        stdout.close(); stderr.close()
    state = load(root / "status.json")
    if state.get("status") == "queued":
        write_status(root, "queued", worker_pid=process.pid)
    return process.pid


def _control(root: Path) -> str | None:
    path = root / "control.json"
    if not path.is_file():
        return None
    try:
        return str(load(path).get("action") or "").strip() or None
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _clear_control(root: Path) -> None:
    path = root / "control.json"
    if path.exists():
        path.unlink()


def wait_for_permission(root: Path, sleep: Any = time.sleep) -> bool:
    """Cooperatively pause between durable item operations; false means cancel."""
    while True:
        action = _control(root)
        if action == "cancel":
            write_status(root, "cancelled", worker_pid=None)
            return False
        if action != "pause":
            return True
        write_status(root, "paused", worker_pid=os.getpid())
        sleep(1)


def request_control(root: Path, action: str) -> dict[str, Any]:
    if action not in {"pause", "cancel", "resume", "retry"}:
        raise cm.CharacterError(f"unsupported batch action: {action}")
    state = reconcile(root)
    plan = load(root / "plan.json")
    if action in {"pause", "cancel"}:
        write_json(root / "control.json", {"action": action, "requested_at": stamp()})
        if not process_alive(state.get("worker_pid")):
            for item in plan.get("items") or []:
                if item.get("status") in {"queued", "running", "interrupted"}:
                    item["status"] = "interrupted" if action == "pause" else "cancelled"
            write_json(root / "plan.json", plan)
            return write_status(root, "paused" if action == "pause" else "cancelled", worker_pid=None)
        return write_status(root, "pausing" if action == "pause" else "cancelling")
    if action == "resume" and state.get("status") == "paused" and process_alive(state.get("worker_pid")):
        _clear_control(root)
        return write_status(root, "running", worker_pid=state.get("worker_pid"))
    if state.get("status") in ACTIVE_STATES and process_alive(state.get("worker_pid")):
        raise cm.CharacterError("batch already has a live worker")
    for item in plan.get("items") or []:
        if item.get("status") in ({"failed", "cancelled"} if action == "retry" else {"interrupted", "running"}):
            item["status"] = "queued"
            item.pop("error", None)
    write_json(root / "plan.json", plan)
    _clear_control(root)
    pid = launch_worker(root)
    return load(root / "status.json") | {"worker_pid": pid}


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


def verify_session(session_dir: Path, expected_engines: list[str], reference_bound: bool = False) -> dict[str, Any]:
    """Verify the durable scene/run contract before an item is called complete.

    A reference-bound item must also show the hash-bound reference in both the settings and the run record,
    so a job that silently rendered from text alone is never counted as complete.
    """
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
        if job.get("model") and settings["model_type"] != job["model"]:
            raise cm.CharacterError(f"{engine} settings model_type {settings['model_type']} differs from prepared {job['model']}")
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
        if reference_bound:
            provenance = settings.get("_xai") if isinstance(settings.get("_xai"), dict) else {}
            if provenance.get("allow_text_fallback") is not False or not settings.get("image_refs"):
                raise cm.CharacterError(f"{engine} settings are not bound to an identity reference")
            if not any(isinstance(item, dict) and item.get("sha256") for item in references):
                raise cm.CharacterError(f"{engine} run recorded no hash-verified reference input")
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
    for reference in item.get("additional_references") or []:
        command += ["--reference", reference]
    if item.get("seed") is not None:
        command += ["--seed", str(item["seed"])]
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
    _clear_control(root) if _control(root) == "resume" else None
    write_status(root, "running", worker_pid=os.getpid())
    for item in plan["items"]:
        if item.get("status") in {"completed", "failed", "cancelled"}:
            continue
        if not wait_for_permission(root, sleep):
            return 3
        item["status"] = "running"; item["started_at"] = stamp(); write_json(root / "plan.json", plan)
        write_status(root, "running", worker_pid=os.getpid(), current_item=item.get("id"))
        try:
            session_dir = Path(item["session_dir"]).resolve() if item.get("session_dir") else _prepare_item(item, root, run_command)
            write_json(root / "plan.json", plan)
            if not wait_for_permission(root, sleep):
                item["status"] = "interrupted"; write_json(root / "plan.json", plan)
                return 3
            result = _render_item(item, session_dir, root, run_command, sleep, backoff_seconds)
        except (cm.CharacterError, OSError, ValueError, json.JSONDecodeError) as exc:
            result = subprocess.CompletedProcess([], 2, "", f"{type(exc).__name__}: {exc}")
        if result.returncode == 0:
            try:
                verification = verify_session(session_dir, item["engines"], bool(item.get("identity_reference")))
            except (cm.CharacterError, OSError, ValueError, json.JSONDecodeError) as exc:
                item.update({"status": "failed", "error": f"verification failed: {exc}", "completed_at": stamp()})
                write_json(root / "plan.json", plan)
                write_status(root, "running", worker_pid=os.getpid())
                continue
            item.update({"status": "completed", "verification": verification, "completed_at": stamp()})
            try: urllib.request.urlopen(urllib.request.Request(sync_url, method="POST"), timeout=120).read()
            except Exception as exc: item["sync_error"] = str(exc)
        else:
            item.update({"status": "failed", "error": _command_text(result).strip()[-4000:], "completed_at": stamp()})
        write_json(root / "plan.json", plan)
        write_status(root, "running", worker_pid=os.getpid())
    completed_count, failed_count = _counts(plan)
    final = "completed" if failed_count == 0 else "completed_with_errors"
    write_status(root, final, worker_pid=None)
    return 0 if failed_count == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("create"); make.add_argument("--plan-file", type=Path, required=True); make.add_argument("--queue-root", type=Path, default=DEFAULT_QUEUE)
    start_mode = make.add_mutually_exclusive_group(); start_mode.add_argument("--no-start", action="store_true"); start_mode.add_argument("--wait", action="store_true", help="run the durable batch in this process so Hermes stays off the GPU until completion")
    make.add_argument("--sync-url", default="http://127.0.0.1:8787/api/sync")
    work = sub.add_parser("run"); work.add_argument("--batch-dir", type=Path, required=True); work.add_argument("--sync-url", default="http://127.0.0.1:8787/api/sync")
    inspect = sub.add_parser("reconcile"); inspect.add_argument("--batch-dir", type=Path, required=True)
    for action in ("pause", "cancel", "resume", "retry"):
        control = sub.add_parser(action); control.add_argument("--batch-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "create":
            root = create(args.plan_file.resolve(), args.queue_root.resolve(), not args.no_start and not args.wait)
            if args.wait:
                with gpu_runtime.WindowsSleepGuard():
                    result = run(root, args.sync_url)
                print(json.dumps({"batch_dir": str(root), "status": load(root / "status.json")["status"]}, ensure_ascii=False, indent=2))
                return result
            print(json.dumps({"batch_dir": str(root), "status": "queued"}, ensure_ascii=False, indent=2)); return 0
        if args.command == "reconcile":
            print(json.dumps(reconcile(args.batch_dir.resolve()), ensure_ascii=False, indent=2)); return 0
        if args.command in {"pause", "cancel", "resume", "retry"}:
            print(json.dumps(request_control(args.batch_dir.resolve(), args.command), ensure_ascii=False, indent=2)); return 0
        root = args.batch_dir.resolve()
        try:
            with gpu_runtime.WindowsSleepGuard():
                return run(root, args.sync_url)
        except Exception as exc:
            try: write_status(root, "failed", error=f"{type(exc).__name__}: {exc}", worker_pid=None)
            except Exception: pass
            raise
    except (cm.CharacterError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 2


if __name__ == "__main__": raise SystemExit(main())
