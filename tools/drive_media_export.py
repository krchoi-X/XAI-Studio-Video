#!/usr/bin/env python3
"""Project Gallery-registered original media into a browsable Google Drive tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_DATABASE = Path(r"C:\Users\krcho\Documents\ChatGPT\XAI-Studio\personal-prompt-studio\data\studio.db")
DEFAULT_DESTINATION = Path(r"G:\내 드라이브\XAI-Studio Media")
DEFAULT_STATE_DIR = Path(r"D:\AI_Studio\workspace\drive-media-export")
STATE_FILE = "export-state.json"
EVENT_FILE = "export-events.jsonl"
WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


class ExportError(ValueError):
    pass


@dataclass(frozen=True)
class Asset:
    asset_id: str
    source: Path
    content_hash: str | None
    media_type: str
    byte_size: int
    relative_path: str
    created_at: str
    session_id: str | None
    session_title: str | None
    session_created_at: str | None
    engine: str | None
    character_ids: tuple[str, ...]
    character_names: tuple[str, ...]
    romanized_names: tuple[str, ...]


@dataclass(frozen=True)
class ExportItem:
    asset: Asset
    destination: Path
    action: str
    reason: str


def stamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def force_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass


def read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        for attempt in range(6):
            try:
                os.replace(temporary, path)
                return
            except PermissionError:
                if attempt == 5:
                    raise
                # Windows indexers/antivirus can briefly hold the old ledger.
                time.sleep(0.1 * (2 ** attempt))
    finally:
        if temporary.exists():
            temporary.unlink()


def append_event(state_dir: Path, event: dict[str, Any]) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir / EVENT_FILE).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"at": stamp(), **event}, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_component(value: str, *, fallback: str, limit: int = 72) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", str(value))
    value = re.sub(r"\s+", " ", value).strip(" .")
    value = value or fallback
    if value.upper() in WINDOWS_RESERVED:
        value = "_" + value
    return value[:limit].rstrip(" .") or fallback


def short_title(value: str | None) -> str:
    if not value:
        return "untitled"
    words = re.findall(r"[^\s,.;:!?]+", value)
    return safe_component("-".join(words[:8]), fallback="untitled", limit=64)


def parse_moment(asset: Asset) -> datetime:
    for value in (asset.session_id or "", asset.source.name):
        match = re.search(r"(20\d{6})[-_](\d{6})", value)
        if match:
            return datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S").astimezone()
    for value in (asset.session_created_at, asset.created_at):
        if value:
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone()
            except ValueError:
                continue
    return datetime.now().astimezone()


def character_bucket(asset: Asset) -> tuple[str, ...]:
    if len(asset.character_ids) == 1:
        name = asset.romanized_names[0] or asset.character_names[0] or asset.character_ids[0]
        folder = safe_component(f"{name} [{asset.character_ids[0]}]", fallback=asset.character_ids[0])
        return ("Characters", folder)
    if len(asset.character_ids) > 1:
        labels = []
        for position, character_id in enumerate(asset.character_ids):
            name = asset.romanized_names[position] or asset.character_names[position] or character_id
            labels.append(f"{name} [{character_id}]")
        group_hash = hashlib.sha256("|".join(asset.character_ids).encode("utf-8")).hexdigest()[:8]
        joined = f"Group {group_hash} - " + " + ".join(labels)
        return ("Multi-Character", safe_component(joined, fallback=f"group-{group_hash}", limit=180))
    return ("Unassigned",)


def destination_for(asset: Asset, destination_root: Path) -> Path:
    moment = parse_moment(asset)
    kind = "Images" if asset.media_type.startswith("image/") else "Videos"
    engine = Path(asset.relative_path).parts[0] if Path(asset.relative_path).parts else (asset.engine or "unknown")
    engine = safe_component(engine, fallback="unknown", limit=32)
    suffix = asset.source.suffix.lower()
    short_id = re.sub(r"[^A-Za-z0-9]", "", asset.asset_id)[-10:] or (asset.content_hash or "unknown")[:10]
    filename = safe_component(
        f"{moment:%Y-%m-%d_%H%M%S}__{short_title(asset.session_title)}__{engine}__{short_id}",
        fallback=asset.asset_id,
        limit=150,
    ) + suffix
    return destination_root.joinpath(*character_bucket(asset), kind, f"{moment:%Y-%m}", filename)


def _safe_source(root_text: str, relative_text: str) -> Path:
    root = Path(root_text).resolve()
    relative = Path(relative_text)
    if relative.is_absolute() or ".." in relative.parts:
        raise ExportError(f"invalid Gallery relative path: {relative_text}")
    source = (root / relative).resolve()
    try:
        source.relative_to(root)
    except ValueError as exc:
        raise ExportError(f"Gallery asset escapes its root: {relative_text}") from exc
    return source


def open_read_only(database: Path) -> sqlite3.Connection:
    if not database.is_file():
        raise ExportError(f"Gallery database not found: {database}")
    connection = sqlite3.connect(f"file:{database.resolve()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def session_character_ids(primary_id: str | None, settings_text: str | None) -> tuple[str, ...]:
    """Return explicit cast IDs without inferring identities from prompt prose."""
    identifiers: set[str] = set()
    if primary_id and primary_id.strip():
        identifiers.add(primary_id.strip())
    if settings_text:
        try:
            settings = json.loads(settings_text)
        except (json.JSONDecodeError, TypeError):
            settings = None
        if isinstance(settings, dict):
            candidates = [settings.get("character_ids")]
            session = settings.get("session")
            if isinstance(session, dict):
                candidates.append(session.get("character_ids"))
            for candidate in candidates:
                if isinstance(candidate, list):
                    identifiers.update(
                        value.strip() for value in candidate
                        if isinstance(value, str) and value.strip()
                    )
    return tuple(sorted(identifiers))


def load_assets(database: Path) -> list[Asset]:
    query = """
        SELECT a.id AS asset_id, a.relative_path, a.content_hash, a.media_type, a.byte_size,
               a.created_at, ar.absolute_path, gs.id AS session_id, gs.title AS session_title,
               gs.created_at AS session_created_at, gs.engine, gs.character_id, gs.settings_json,
               c.name AS character_name, c.romanized_name
        FROM assets a
        JOIN asset_roots ar ON ar.id=a.root_id
        LEFT JOIN session_assets sa ON sa.asset_id=a.id
        LEFT JOIN generation_sessions gs ON gs.id=sa.session_id
        LEFT JOIN characters c ON c.id=gs.character_id
        WHERE a.media_type LIKE 'image/%' OR a.media_type LIKE 'video/%'
        ORDER BY a.created_at, a.id, gs.created_at, gs.id
    """
    connection = open_read_only(database)
    try:
        rows = connection.execute(query).fetchall()
        character_rows = connection.execute(
            "SELECT id, name, romanized_name FROM characters ORDER BY id"
        ).fetchall()
    finally:
        connection.close()
    character_catalog = {
        str(row["id"]): (str(row["name"] or ""), str(row["romanized_name"] or ""))
        for row in character_rows
    }
    grouped: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        grouped.setdefault(row["asset_id"], []).append(row)
    assets: list[Asset] = []
    for asset_id, records in grouped.items():
        first = records[0]
        by_character: dict[str, tuple[str, str]] = {}
        for record in records:
            for character_id in session_character_ids(record["character_id"], record["settings_json"]):
                by_character[character_id] = character_catalog.get(character_id, ("", ""))
        character_ids = tuple(sorted(by_character))
        session_records = [record for record in records if record["session_id"]]
        session = session_records[0] if session_records else first
        assets.append(Asset(
            asset_id=asset_id,
            source=_safe_source(first["absolute_path"], first["relative_path"]),
            content_hash=str(first["content_hash"]) if first["content_hash"] else None,
            media_type=str(first["media_type"]), byte_size=int(first["byte_size"]),
            relative_path=str(first["relative_path"]), created_at=str(first["created_at"]),
            session_id=str(session["session_id"]) if session["session_id"] else None,
            session_title=str(session["session_title"]) if session["session_title"] else None,
            session_created_at=str(session["session_created_at"]) if session["session_created_at"] else None,
            engine=str(session["engine"]) if session["engine"] else None,
            character_ids=character_ids,
            character_names=tuple(by_character[item][0] for item in character_ids),
            romanized_names=tuple(by_character[item][1] for item in character_ids),
        ))
    return assets


def select_assets(assets: Iterable[Asset], args: argparse.Namespace) -> list[Asset]:
    assets = list(assets)
    asset_ids = set(args.asset_id or [])
    character_ids = set(args.character_id or [])
    session_ids = set(args.session_id or [])
    selected = []
    for asset in assets:
        if asset_ids and asset.asset_id not in asset_ids:
            continue
        if character_ids and not character_ids.intersection(asset.character_ids):
            continue
        if session_ids and asset.session_id not in session_ids:
            continue
        if args.since:
            try:
                if parse_moment(asset).date() < datetime.fromisoformat(args.since).date():
                    continue
            except ValueError as exc:
                raise ExportError("--since must be YYYY-MM-DD") from exc
        selected.append(asset)
    if asset_ids:
        known_ids = {asset.asset_id for asset in assets}
        missing_ids = sorted(asset_ids - known_ids)
        if missing_ids:
            raise ExportError(f"asset id not found in Gallery: {', '.join(missing_ids)}")
    selected.sort(key=lambda item: (parse_moment(item), item.asset_id))
    return selected


def load_state(state_dir: Path) -> dict[str, Any]:
    value = read_json(state_dir / STATE_FILE, {"schema_version": 1, "assets": {}})
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("assets"), dict):
        raise ExportError(f"invalid export state: {state_dir / STATE_FILE}")
    return value


def plan_items(assets: Iterable[Asset], destination_root: Path, state: dict[str, Any]) -> list[ExportItem]:
    items = []
    records = state["assets"]
    for asset in assets:
        destination = destination_for(asset, destination_root)
        prior = records.get(asset.asset_id)
        if not asset.source.is_file():
            items.append(ExportItem(asset, destination, "missing", "Gallery original is missing"))
        elif asset.source.stat().st_size != asset.byte_size:
            items.append(ExportItem(asset, destination, "blocked", "source size differs from Gallery record"))
        elif (prior and prior.get("content_hash") == asset.content_hash
              and Path(prior.get("destination", "")) == destination and destination.is_file()):
            items.append(ExportItem(asset, destination, "skip", "already exported"))
        elif destination.exists():
            existing_hash = sha256_file(destination) if destination.is_file() else None
            if asset.content_hash and existing_hash == asset.content_hash:
                items.append(ExportItem(asset, destination, "adopt", "matching destination already exists"))
            else:
                items.append(ExportItem(asset, destination, "conflict", "destination exists with different content"))
        else:
            items.append(ExportItem(asset, destination, "copy", "new Gallery asset"))
    return items


def item_json(item: ExportItem) -> dict[str, Any]:
    return {
        "asset_id": item.asset.asset_id, "action": item.action, "reason": item.reason,
        "source": str(item.asset.source), "destination": str(item.destination),
        "media_type": item.asset.media_type, "byte_size": item.asset.byte_size,
        "content_hash": item.asset.content_hash, "character_ids": list(item.asset.character_ids),
        "session_id": item.asset.session_id,
    }


def summarize(items: list[ExportItem]) -> dict[str, int]:
    result: dict[str, int] = {"total": len(items)}
    for item in items:
        result[item.action] = result.get(item.action, 0) + 1
    return result


def copy_item(item: ExportItem, state_dir: Path, state: dict[str, Any]) -> str:
    asset = item.asset
    if item.action in {"missing", "blocked", "conflict", "skip"}:
        return item.action
    destination = item.destination
    if item.action == "copy":
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(f".{destination.name}.{asset.asset_id}.tmp")
        if temporary.exists():
            temporary.unlink()
        try:
            shutil.copy2(asset.source, temporary)
            copied_hash = sha256_file(temporary)
            if asset.content_hash and copied_hash != asset.content_hash:
                raise ExportError(f"hash mismatch after copy: {asset.asset_id}")
            if temporary.stat().st_size != asset.byte_size:
                raise ExportError(f"size mismatch after copy: {asset.asset_id}")
            if destination.exists():
                raise ExportError(f"destination appeared during copy: {destination}")
            os.replace(temporary, destination)
        finally:
            if temporary.exists():
                temporary.unlink()
    state["assets"][asset.asset_id] = {
        "content_hash": asset.content_hash or sha256_file(destination),
        "byte_size": asset.byte_size, "source": str(asset.source), "destination": str(destination),
        "exported_at": stamp(), "session_id": asset.session_id,
        "character_ids": list(asset.character_ids), "media_type": asset.media_type,
    }
    atomic_json(state_dir / STATE_FILE, state)
    append_event(state_dir, {"event": "exported" if item.action == "copy" else "adopted", **item_json(item)})
    return "copied" if item.action == "copy" else "adopted"


def execute(args: argparse.Namespace) -> dict[str, Any]:
    database = Path(args.database).resolve()
    destination_root = Path(args.destination_root).resolve()
    state_dir = Path(args.state_dir).resolve()
    if destination_root == database.parent or destination_root.is_relative_to(database.parent):
        raise ExportError("destination must not be inside the Gallery data directory")
    assets = select_assets(load_assets(database), args)
    state = load_state(state_dir)
    items = plan_items(assets, destination_root, state)
    if args.command == "plan":
        if args.limit is not None:
            items = items[:args.limit]
        return {"ok": True, "mode": "plan", "database": str(database), "destination_root": str(destination_root),
                "summary": summarize(items), "items": [item_json(item) for item in items]}
    if not args.all and not (args.asset_id or args.character_id or args.session_id or args.since):
        raise ExportError("sync requires a selector (--asset-id/--character-id/--session-id/--since) or --all")
    if args.all:
        # A whole-catalog scheduled run must advance beyond previously exported
        # assets.  Already-exported rows therefore do not consume the batch limit.
        items = [item for item in items if item.action != "skip"]
    if args.limit is not None:
        items = items[:args.limit]
    results: dict[str, int] = {}
    for item in items:
        outcome = copy_item(item, state_dir, state)
        results[outcome] = results.get(outcome, 0) + 1
    return {"ok": not any(item.action in {"missing", "blocked", "conflict"} for item in items),
            "mode": "sync", "destination_root": str(destination_root), "summary": summarize(items),
            "results": results, "note": "filesystem copy verified; Google Drive cloud upload completion is not asserted"}


def status(args: argparse.Namespace) -> dict[str, Any]:
    state_dir = Path(args.state_dir).resolve()
    state = load_state(state_dir)
    existing = sum(1 for item in state["assets"].values() if Path(item.get("destination", "")).is_file())
    return {"ok": True, "state_dir": str(state_dir), "recorded_assets": len(state["assets"]),
            "destinations_present": existing, "destinations_missing": len(state["assets"]) - existing}


def add_selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--database", default=str(DEFAULT_DATABASE))
    parser.add_argument("--destination-root", default=str(DEFAULT_DESTINATION))
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    parser.add_argument("--asset-id", action="append")
    parser.add_argument("--character-id", action="append")
    parser.add_argument("--session-id", action="append")
    parser.add_argument("--since")
    parser.add_argument("--limit", type=int, default=100)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="show media and destinations without writing to Drive")
    add_selection_arguments(plan)
    sync = sub.add_parser("sync", help="copy selected media and update the local ledger")
    add_selection_arguments(sync)
    sync.add_argument("--all", action="store_true", help="allow an unfiltered bounded sync")
    show = sub.add_parser("status", help="summarize the local export ledger")
    show.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    return parser


def main(argv: list[str] | None = None) -> int:
    force_utf8_stdio()
    args = build_parser().parse_args(argv)
    try:
        result = status(args) if args.command == "status" else execute(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("ok") else 2
    except (ExportError, OSError, sqlite3.Error, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
