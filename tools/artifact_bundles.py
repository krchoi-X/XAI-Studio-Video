"""Read-only discovery and verified access for historical artifact bundles."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path

_SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_BUNDLE_IDS = {"reports", "standalone-runs"}
_ROLES = {"source-record", "external-input-at-archive-time"}

def _cm():
    source = Path(__file__).with_name("character_manager.py")
    spec = importlib.util.spec_from_file_location("artifact_bundles_manager", source)
    if spec is None or spec.loader is None: raise RuntimeError("Character Manager resolver is unavailable")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def _unsafe(path: Path) -> bool:
    node = path
    while True:
        try: attributes = getattr(node.lstat(), "st_file_attributes", 0)
        except FileNotFoundError: attributes = 0
        if node.is_symlink() or attributes & getattr(os, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400): return True
        if node.parent == node: return False
        node = node.parent

def _relative(raw: str) -> Path:
    value = Path(raw)
    if not raw or ":" in raw or "\\" in raw or raw != value.as_posix() or value.is_absolute() or "." in value.parts or ".." in value.parts:
        raise ValueError("bundle member path is not canonical")
    return value

def _source_key(raw: str) -> str:
    value = Path(raw)
    if not value.is_absolute() or "." in value.parts or ".." in value.parts or raw != str(value): raise ValueError("bundle source path is not canonical")
    return os.path.normcase(os.path.normpath(raw))

def _marker(archive_root: str | Path) -> tuple[Path, dict, Path]:
    root = Path(archive_root)
    if not root.is_absolute() or _unsafe(root): raise ValueError("bundle root is unsafe")
    root = root.resolve(); marker_path = root / "archive-bundle.json"
    if not marker_path.is_file() or _unsafe(marker_path): raise ValueError("bundle marker is missing or unsafe")
    try: marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise ValueError("invalid bundle marker") from exc
    if not isinstance(marker, dict) or type(marker.get("schema_version")) is not int or marker.get("schema_version") != 1 or marker.get("kind") != "historical-artifact-bundle" or marker.get("authority") != "historical-snapshot": raise ValueError("unsupported bundle marker")
    for field in ("bundle_id", "snapshot_id", "captured_at", "archive_root"):
        if not isinstance(marker.get(field), str) or not marker[field]: raise ValueError("bundle marker is incomplete")
    if marker["bundle_id"] not in _BUNDLE_IDS or not _SAFE_ID.fullmatch(marker["snapshot_id"]) or not Path(marker["archive_root"]).is_absolute() or Path(marker["archive_root"]) != root or root.parent.name != marker["bundle_id"] or root.name != marker["snapshot_id"] or root.parent.parent.name != "records": raise ValueError("bundle root or IDs do not match marker")
    roots = marker.get("source_roots")
    if not isinstance(roots, list) or not roots: raise ValueError("invalid source roots")
    root_keys = {_source_key(item) for item in roots if isinstance(item, str)}
    if len(root_keys) != len(roots): raise ValueError("invalid source roots")
    source_roots = [Path(item) for item in roots]
    files = marker.get("files")
    if not isinstance(files, list): raise ValueError("invalid bundle files")
    paths: set[str] = set(); sources: set[str] = set()
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("source_path"), str) or type(item.get("bytes")) is not int or item["bytes"] < 0 or not isinstance(item.get("sha256"), str) or not _SHA256.fullmatch(item["sha256"]) or item.get("role") not in _ROLES: raise ValueError("invalid bundle member")
        relative = _relative(item["path"]); path_key = relative.as_posix().casefold(); source = Path(item["source_path"]); source_key = _source_key(item["source_path"])
        if path_key in paths or source_key in sources or path_key in {"archive-bundle.json", ".archive-bundle.pending.json"} or not any(source.is_relative_to(parent) for parent in source_roots): raise ValueError("bundle member escapes or duplicates")
        target = root / relative
        if _unsafe(target) or not target.is_file(): raise ValueError("bundle file missing or unsafe")
        paths.add(path_key); sources.add(source_key)
    return root, marker, marker_path

def describe_bundles() -> list[dict]:
    library = _cm().shared_creation_library()
    if library is None: return []
    library = Path(library)
    if not library.is_absolute() or _unsafe(library): raise ValueError("shared Library is unsafe")
    library = library.resolve(); records = library / "records"
    if not records.is_dir(): return []
    result = []
    for marker_path in sorted(records.glob("*/*/archive-bundle.json")):
        root, marker, verified_marker = _marker(marker_path.parent)
        if root.parent.parent != records or root.parent.name != marker["bundle_id"] or root.name != marker["snapshot_id"]: raise ValueError("bundle nesting does not match marker")
        result.append({"bundle_id": marker["bundle_id"], "snapshot_id": marker["snapshot_id"], "records_path": str(root), "source_roots": marker["source_roots"], "captured_at": marker["captured_at"], "authority": marker["authority"], "record_count": len(marker["files"]), "total_bytes": sum(item["bytes"] for item in marker["files"]), "manifest_sha256": hashlib.sha256(verified_marker.read_bytes()).hexdigest()})
    return result

def resolve_source_path(archive_root: str | Path, source_path: str | Path) -> Path:
    root, marker, _ = _marker(archive_root)
    source = str(source_path); members = {item["source_path"]: item for item in marker["files"]}
    if source not in members: raise ValueError("source path is not archived")
    item = members[source]; target = root / _relative(item["path"])
    if target.stat().st_size != item["bytes"] or hashlib.sha256(target.read_bytes()).hexdigest() != item["sha256"]: raise ValueError("bundle file hash does not match marker")
    return target
