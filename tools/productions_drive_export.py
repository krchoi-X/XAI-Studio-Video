#!/usr/bin/env python3
"""One-way, resumable Google Drive backup of character-independent productions.

Reads the production folders under the library (`D:\\AI_Studio\\library\\videos\\<session>` with a
`session-provenance.json`) through `control_tower.productions`, so the backup copies exactly what the Productions page
shows. It never writes, moves or deletes anything in the library and never overwrites or deletes anything on Drive.

    G:\\내 드라이브\\XAI-Studio Media\\Productions\\<title [session-id]>\\
        Videos\\   final video, clips, experiment videos
        Images\\   reference stills
        Record\\   provenance, prompts, settings and driver files (small, makes the video reproducible)

A changed record (for example a status update in `session-provenance.json`) is kept as a new revision under
`Record\\_revisions\\`; videos and images are immutable and a different file at an existing path is reported as a conflict.
The ledger lives outside Drive. A successful filesystem copy does not prove the cloud upload has finished.

    python tools/productions_drive_export.py plan --all
    python tools/productions_drive_export.py sync --session-id VIDEO-20261002-112000-rooftop-5am
    python tools/productions_drive_export.py status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from control_tower import productions  # noqa: E402

DEFAULT_ROOT = Path(r"D:\AI_Studio\library\videos")
DEFAULT_DESTINATION = Path(r"G:\내 드라이브\XAI-Studio Media\Productions")
DEFAULT_STATE = Path(r"D:\AI_Studio\workspace\productions-drive-export")
LEDGER = "ledger.json"
EVENTS = "events.jsonl"
# Files younger than this are skipped for now: a render or a recorder may still be writing them.
SETTLE_SECONDS = 120
COMPONENT_LIMIT = 60
FILENAME_BYTES = 180
PATH_BUDGET = 240
RESERVED = {"CON", "PRN", "AUX", "NUL", *{f"COM{i}" for i in range(1, 10)}, *{f"LPT{i}" for i in range(1, 10)}}


class ExportError(ValueError):
    pass


@dataclass
class Item:
    key: str
    session_id: str
    category: str
    source: Path
    destination: Path
    action: str
    reason: str
    content_hash: str | None = None
    byte_size: int = 0


def stamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_component(value: str, *, fallback: str, limit: int = COMPONENT_LIMIT) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", str(value))
    value = re.sub(r"\s+", " ", value).strip(" .") or fallback
    if value.upper() in RESERVED:
        value = "_" + value
    return value[:limit].rstrip(" .") or fallback


def fit_filename(name: str, content_hash: str, limit: int = FILENAME_BYTES) -> str:
    """Keep a filename within `limit` bytes by shortening the stem and adding a hash tag."""
    if len(name.encode("utf-8")) <= limit:
        return name
    suffix = Path(name).suffix
    stem = Path(name).stem
    room = limit - len(suffix.encode("utf-8")) - 9
    if room < 8:
        raise ExportError(f"no room left for a filename: {name}")
    return stem.encode("utf-8")[:room].decode("utf-8", errors="ignore").rstrip(" .") + "." + content_hash[:8] + suffix


def read_ledger(state_dir: Path) -> dict[str, Any]:
    path = state_dir / LEDGER
    if not path.is_file():
        return {"schema_version": 2, "files": {}, "sessions": {}}
    ledger = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(ledger, dict) or not isinstance(ledger.get("files"), dict):
        raise ExportError(f"invalid ledger structure: {path}")
    sessions = ledger.get("sessions")
    if sessions is None:
        ledger["sessions"] = {}
    elif not isinstance(sessions, dict):
        raise ExportError(f"invalid ledger sessions map: {path}")
    return ledger


def write_ledger(state_dir: Path, ledger: dict[str, Any]) -> None:
    ledger["schema_version"] = 2
    ledger.setdefault("sessions", {})
    state_dir.mkdir(parents=True, exist_ok=True)
    temporary = state_dir / f"{LEDGER}.tmp.{os.getpid()}"
    temporary.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for attempt in range(6):
        try:
            os.replace(temporary, state_dir / LEDGER)
            return
        except PermissionError:
            if attempt == 5:
                raise
            time.sleep(0.1 * (2 ** attempt))


def append_event(state_dir: Path, event: dict[str, Any]) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / EVENTS).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"at": stamp(), **event}, ensure_ascii=False) + "\n")


def _contained_production_folder(path: Path, destination_root: Path) -> Path | None:
    """Return a direct child of the configured destination root, otherwise None."""
    try:
        folder = path.resolve()
        root = destination_root.resolve()
    except OSError:
        return None
    return folder if folder.parent == root else None


def _infer_legacy_production_folder(session_id: str, destination_root: Path,
                                    ledger: dict[str, Any]) -> Path | None:
    """Recover the original folder from a v1 file ledger without moving or duplicating anything."""
    prefix = f"{session_id}/"
    for key, prior in ledger["files"].items():
        if not key.startswith(prefix) or not isinstance(prior, dict):
            continue
        destination = prior.get("destination")
        category = prior.get("category")
        if not destination or category not in {"Videos", "Images", "Record"}:
            continue
        for parent in Path(destination).parents:
            if parent.name == category:
                folder = _contained_production_folder(parent.parent, destination_root)
                if folder is not None:
                    return folder
                break
    return None


def production_folder(session_dir: Path, destination_root: Path, ledger: dict[str, Any]) -> Path:
    sessions = ledger.setdefault("sessions", {})
    stored = sessions.get(session_dir.name)
    if isinstance(stored, dict) and stored.get("destination_folder"):
        folder = _contained_production_folder(Path(stored["destination_folder"]), destination_root)
        if folder is None:
            raise ExportError(f"stored destination is outside the configured root: {session_dir.name}")
        return folder

    folder = _infer_legacy_production_folder(session_dir.name, destination_root, ledger)
    prov, _ = productions._read_provenance(session_dir)
    title = str(prov.get("title") or session_dir.name)
    if folder is None:
        safe_title = safe_component(title, fallback=session_dir.name, limit=40)
        folder = destination_root / safe_component(f"{safe_title} [{session_dir.name}]", fallback=session_dir.name,
                                                   limit=COMPONENT_LIMIT + 40)
    sessions[session_dir.name] = {"destination_folder": str(folder), "title_at_creation": title}
    return folder


def destination_path(folder: Path, category: str, relative: str, content_hash: str) -> Path:
    rel = Path(relative)
    parts = list(rel.parts)
    if category == "Videos" and parts[0] == "outputs":
        parts = parts[1:]
    elif category == "Images" and parts[0] == "refs":
        parts = parts[1:]
    directory = folder / category
    for part in parts[:-1]:
        directory = directory / safe_component(part, fallback="dir", limit=FILENAME_BYTES)
    budget = min(FILENAME_BYTES, PATH_BUDGET - len(str(directory)) - 1)
    return directory / fit_filename(safe_component(parts[-1], fallback="file", limit=4000), content_hash, budget)


def revision_path(folder: Path, relative: str, content_hash: str) -> Path:
    rel = Path(relative)
    name = fit_filename(f"{rel.stem}.{content_hash[:8]}{rel.suffix}", content_hash)
    path = folder / "Record" / "_revisions"
    for part in rel.parts[:-1]:
        path = path / safe_component(part, fallback="dir", limit=FILENAME_BYTES)
    return path / name


def plan_items(root: Path, destination_root: Path, ledger: dict[str, Any], session_ids: list[str] | None,
               now: float | None = None) -> list[Item]:
    now = time.time() if now is None else now
    items: list[Item] = []
    for session_dir in productions.discover(root):
        if session_ids is not None and session_dir.name not in session_ids:
            continue
        folder = production_folder(session_dir, destination_root, ledger)
        for category, relative in productions.backup_manifest(session_dir):
            source = session_dir / relative
            key = f"{session_dir.name}/{relative}"
            if not source.is_file():
                items.append(Item(key, session_dir.name, category, source, folder, "missing", "source disappeared"))
                continue
            stat = source.stat()
            if now - stat.st_mtime < SETTLE_SECONDS:
                items.append(Item(key, session_dir.name, category, source, folder, "wait", "modified in the last "
                                  f"{SETTLE_SECONDS}s; will be copied once it settles", None, stat.st_size))
                continue
            content_hash = sha256_file(source)
            prior = ledger["files"].get(key)
            try:
                destination = destination_path(folder, category, relative, content_hash)
            except ExportError as exc:
                items.append(Item(key, session_dir.name, category, source, folder, "blocked", str(exc), content_hash, stat.st_size))
                continue
            if prior and prior.get("content_hash") == content_hash and Path(prior["destination"]).is_file():
                items.append(Item(key, session_dir.name, category, source, Path(prior["destination"]), "skip",
                                  "already exported", content_hash, stat.st_size))
                continue
            if category == "Record" and prior and prior.get("content_hash") != content_hash:
                destination = revision_path(folder, relative, content_hash)
            if destination.exists():
                existing = sha256_file(destination) if destination.is_file() else None
                if existing == content_hash:
                    items.append(Item(key, session_dir.name, category, source, destination, "adopt",
                                      "matching destination already exists", content_hash, stat.st_size))
                else:
                    items.append(Item(key, session_dir.name, category, source, destination, "conflict",
                                      "destination exists with different content", content_hash, stat.st_size))
                continue
            if prior and prior.get("content_hash") != content_hash and category != "Record":
                items.append(Item(key, session_dir.name, category, source, destination, "conflict",
                                  "source changed after export; videos and images are immutable", content_hash, stat.st_size))
                continue
            if prior and prior.get("content_hash") == content_hash:
                reason = "destination missing; restoring the copy"
            else:
                reason = "changed record, new revision" if prior else "new production file"
            items.append(Item(key, session_dir.name, category, source, destination, "copy", reason, content_hash, stat.st_size))
    return items


def copy_item(item: Item, state_dir: Path, ledger: dict[str, Any]) -> str:
    if item.action in {"missing", "blocked", "conflict", "skip", "wait"}:
        return item.action
    if item.action == "copy":
        item.destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = item.destination.with_name(f".xai-prod-{hashlib.sha256(item.key.encode('utf-8')).hexdigest()[:16]}.tmp")
        if temporary.exists():
            temporary.unlink()
        try:
            shutil.copy2(item.source, temporary)
            if sha256_file(temporary) != item.content_hash or temporary.stat().st_size != item.byte_size:
                # The source changed while it was being copied; nothing is promoted and the next run retries.
                return "unstable"
            if item.destination.exists():
                raise ExportError(f"destination appeared during copy: {item.destination}")
            os.replace(temporary, item.destination)
        finally:
            if temporary.exists():
                temporary.unlink()
    ledger["files"][item.key] = {
        "content_hash": item.content_hash, "byte_size": item.byte_size, "source": str(item.source),
        "destination": str(item.destination), "category": item.category, "exported_at": stamp(),
    }
    write_ledger(state_dir, ledger)
    append_event(state_dir, {"event": "exported" if item.action == "copy" else "adopted", "key": item.key,
                             "destination": str(item.destination), "content_hash": item.content_hash})
    return "copied" if item.action == "copy" else "adopted"


def summarize(items: list[Item]) -> dict[str, int]:
    result: dict[str, int] = {"total": len(items)}
    for item in items:
        result[item.action] = result.get(item.action, 0) + 1
    return result


def item_json(item: Item) -> dict[str, Any]:
    return {"key": item.key, "category": item.category, "action": item.action, "reason": item.reason,
            "source": str(item.source), "destination": str(item.destination), "byte_size": item.byte_size,
            "content_hash": item.content_hash}


def run(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root)
    destination_root = Path(args.destination_root)
    state_dir = Path(args.state_dir)
    sessions = list(args.session_id) if args.session_id else None
    if args.command == "sync" and sessions is None and not args.all:
        raise ExportError("sync requires --session-id or --all")
    if destination_root.resolve() == root.resolve() or root.resolve() in destination_root.resolve().parents:
        raise ExportError("destination must not be inside the production library")
    ledger = read_ledger(state_dir)
    items = plan_items(root, destination_root, ledger, sessions)
    if args.command == "plan":
        shown = items[:args.limit] if args.limit else items
        return {"ok": True, "mode": "plan", "destination_root": str(destination_root), "summary": summarize(items),
                "items": [item_json(i) for i in shown]}
    pending = [i for i in items if i.action != "skip"]
    if args.limit:
        pending = pending[:args.limit]
    results: dict[str, int] = {}
    for item in pending:
        outcome = copy_item(item, state_dir, ledger)
        results[outcome] = results.get(outcome, 0) + 1
    # Persist newly frozen session folders even when every existing file was already a skip.
    write_ledger(state_dir, ledger)
    bad = any(i.action in {"missing", "blocked", "conflict"} for i in pending) or "unstable" in results
    return {"ok": not bad, "mode": "sync", "destination_root": str(destination_root), "summary": summarize(pending),
            "results": results, "note": "filesystem copy verified; Google Drive cloud upload completion is not asserted"}


def status(args: argparse.Namespace) -> dict[str, Any]:
    ledger = read_ledger(Path(args.state_dir))
    present = sum(1 for v in ledger["files"].values() if Path(v["destination"]).is_file())
    return {"ok": True, "state_dir": str(Path(args.state_dir)), "recorded_files": len(ledger["files"]),
            "destinations_present": present, "destinations_missing": len(ledger["files"]) - present}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--destination-root", default=str(DEFAULT_DESTINATION))
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE))
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "sync"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--session-id", action="append")
        cmd.add_argument("--all", action="store_true")
        cmd.add_argument("--limit", type=int)
    sub.add_parser("status")
    return parser


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass
    args = build_parser().parse_args(argv)
    try:
        result = status(args) if args.command == "status" else run(args)
    except (ExportError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
