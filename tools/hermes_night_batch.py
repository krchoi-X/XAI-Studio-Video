#!/usr/bin/env python3
"""Create and execute durable, review-budgeted Hermes image batches."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
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
        engines = list(dict.fromkeys(raw.get("engines") or ["z-image", "krea2"]))
        count = int(raw.get("count", 2))
        if not (cm.CHARACTERS / character_id / "character.json").is_file():
            raise cm.CharacterError(f"item {position}: unknown character {character_id!r}")
        if len(prompt) < 3:
            raise cm.CharacterError(f"item {position}: prompt is too short")
        if not engines or any(engine not in ENGINES for engine in engines):
            raise cm.CharacterError(f"item {position}: unsupported engines")
        if not 1 <= count <= 10:
            raise cm.CharacterError(f"item {position}: count must be 1-10 per engine")
        generated_images += count * len(engines)
        normalized.append({
            "id": f"item-{position:02d}", "character_id": character_id, "prompt": prompt,
            "engines": engines, "count": count,
            "prompt_strategy": str(raw.get("prompt_strategy") or "strict_translation"),
            "immutable_constraints": raw.get("immutable_constraints") or {},
            "scene_spec": raw.get("scene_spec") or {},
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


def run(root: Path, sync_url: str) -> int:
    plan = load(root / "plan.json")
    completed_count = failed_count = 0
    write_json(root / "status.json", {"status": "running", "updated_at": stamp(), "total_items": len(plan["items"]),
                                        "completed_items": 0, "failed_items": 0})
    for item in plan["items"]:
        item["status"] = "running"; item["started_at"] = stamp(); write_json(root / "plan.json", plan)
        command = [sys.executable, str(SCENE_TOOL), "produce", "--character", item["character_id"],
                   "--request", item["prompt"], "--engines", ",".join(item["engines"]), "--count", str(item["count"]),
                   "--strategy", item["prompt_strategy"], "--constraints-json", json.dumps(item["immutable_constraints"], ensure_ascii=False),
                   "--scene-spec-json", json.dumps(item["scene_spec"], ensure_ascii=False), "--actor", "hermes"]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (root / f"{item['id']}.log").write_text((result.stdout or "") + "\n--- stderr ---\n" + (result.stderr or ""), encoding="utf-8")
        if result.returncode == 0:
            payload = json.loads(result.stdout); item.update({"status": "completed", "session_dir": payload.get("session_dir"), "completed_at": stamp()}); completed_count += 1
            try: urllib.request.urlopen(urllib.request.Request(sync_url, method="POST"), timeout=120).read()
            except Exception as exc: item["sync_error"] = str(exc)
        else:
            item.update({"status": "failed", "error": (result.stderr or result.stdout).strip(), "completed_at": stamp()}); failed_count += 1
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
