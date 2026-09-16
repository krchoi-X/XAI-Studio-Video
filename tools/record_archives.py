"""Read-only discovery and verified access for historical record archives."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path

_ID = re.compile(r"ch-[a-z0-9]+(?:-[a-z0-9]+)*\Z")

def _cm():
    source = Path(__file__).with_name("character_manager.py")
    spec = importlib.util.spec_from_file_location("record_archives_manager", source)
    if spec is None or spec.loader is None: raise RuntimeError("Character Manager resolver is unavailable")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def _unsafe(path: Path, root: Path) -> bool:
    node = path
    while True:
        try: attributes = getattr(node.lstat(), "st_file_attributes", 0)
        except FileNotFoundError: attributes = 0
        if node.is_symlink() or bool(attributes & getattr(os, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)):
            return True
        if node.parent == node: return False
        node = node.parent

def _inside(root: Path, path: Path, file: bool = False) -> Path:
    if _unsafe(path, root): raise ValueError("archive path contains a symlink or junction")
    value = path.resolve(strict=False)
    if not value.is_relative_to(root) or (file and not value.is_file()): raise ValueError("archive path escapes or is missing")
    return value

def _marker(archive_root: Path) -> dict:
    archive_root = Path(archive_root)
    if not archive_root.is_absolute() or _unsafe(archive_root, archive_root): raise ValueError("archive root is unsafe")
    archive_root = archive_root.resolve()
    marker_path = _inside(archive_root, archive_root / "record-archive.json", file=True)
    try: marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise ValueError("invalid record archive marker") from exc
    if not isinstance(marker, dict) or type(marker.get("schema_version")) is not int or marker.get("schema_version") not in {1, 2} or marker.get("kind") != "historical-record-archive" or marker.get("authority") != "historical-snapshot": raise ValueError("unsupported record archive marker")
    for field in ("character_id", "session_id", "source_root", "archive_root", "captured_at", "backup_plan_sha256"):
        if not isinstance(marker.get(field), str) or not marker[field]: raise ValueError("record archive marker is incomplete")
    if marker["schema_version"] == 1 and (not isinstance(marker.get("outputs_root"), str) or not marker["outputs_root"]): raise ValueError("record archive marker is incomplete")
    if marker["schema_version"] == 2 and ("outputs_root" not in marker or (marker["outputs_root"] is not None and not isinstance(marker["outputs_root"], str))): raise ValueError("record archive marker is incomplete")
    source_root, marker_root = Path(marker["source_root"]), Path(marker["archive_root"])
    outputs_root = Path(marker["outputs_root"]) if marker.get("outputs_root") is not None else None
    if not source_root.is_absolute() or not marker_root.is_absolute() or marker_root != archive_root: raise ValueError("record archive roots do not match marker")
    if marker["schema_version"] == 1:
        if outputs_root is None or not outputs_root.is_absolute() or outputs_root != archive_root / "outputs" or not outputs_root.is_dir() or _unsafe(outputs_root, archive_root): raise ValueError("record archive roots do not match marker")
    else:
        snapshot = marker.get("snapshot_id")
        if not isinstance(snapshot, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", snapshot) or archive_root.name != snapshot or archive_root.parent.name != "historical-records" or archive_root.parent.parent.name != marker["session_id"] or archive_root.parent.parent.parent.name != "generations" or archive_root.parent.parent.parent.parent.name != marker["character_id"] or archive_root.parent.parent.parent.parent.parent.name != "characters": raise ValueError("record archive nesting does not match marker")
        if outputs_root is not None and (not outputs_root.is_absolute() or outputs_root != archive_root.parent.parent / "outputs" or not outputs_root.is_dir() or _unsafe(outputs_root, archive_root.parent.parent)): raise ValueError("record archive roots do not match marker")
    if not _ID.fullmatch(marker["character_id"]) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", marker["session_id"]) or not re.fullmatch(r"[0-9a-f]{64}", marker["backup_plan_sha256"]): raise ValueError("record archive marker IDs are invalid")
    if marker["schema_version"] == 1 and (archive_root.name != marker["session_id"] or archive_root.parent.name != "generations" or archive_root.parent.parent.name != marker["character_id"] or archive_root.parent.parent.parent.name != "characters"): raise ValueError("record archive nesting does not match marker")
    files = marker.get("files")
    if not isinstance(files, list): raise ValueError("record archive files are invalid")
    seen=set()
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) or type(item.get("bytes")) is not int or item["bytes"] < 0: raise ValueError("record archive member is invalid")
        rel=Path(item["path"])
        canonical=rel.as_posix().casefold()
        raw=item["path"]
        if not raw or ":" in raw or "\\" in raw or raw != rel.as_posix() or rel.is_absolute() or ".." in rel.parts or "." in rel.parts or canonical in seen: raise ValueError("record archive member escapes or duplicates")
        seen.add(canonical); _inside(archive_root, archive_root / rel, file=True)
    return marker

def _member(root: Path, marker: dict, relative: str, verify: bool = False) -> tuple[Path, dict]:
    members = {item["path"]: item for item in marker["files"]}
    if relative not in members: raise ValueError("recorded path is not archived")
    target = _inside(root, root / Path(relative), file=True); item = members[relative]
    if verify and (target.stat().st_size != item["bytes"] or hashlib.sha256(target.read_bytes()).hexdigest() != item["sha256"]):
        raise ValueError("archived record hash does not match marker")
    return target, item

def _library_root() -> Path:
    library = _cm().shared_creation_library()
    if library is None: raise ValueError("shared Library is unavailable")
    library = Path(library)
    if not library.is_absolute() or _unsafe(library, library): raise ValueError("shared Library is unsafe")
    return library.resolve()

def _artifact_value(value: object) -> tuple[str, str | None, int | None]:
    if not isinstance(value, dict) or not isinstance(value.get("path"), str) or not value["path"]: raise ValueError("invalid archived artifact")
    checksum, size = value.get("sha256"), value.get("byte_count")
    if checksum is not None and (not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum)): raise ValueError("invalid archived artifact checksum")
    if size is not None and (type(size) is not int or size < 0): raise ValueError("invalid archived artifact size")
    return value["path"], checksum, size

def _artifact_target(root: Path, marker: dict, recorded: str, checksum: str | None, size: int | None) -> tuple[Path | None, str, str, str | None, str | None, int | None]:
    """Resolve metadata only; callers that consume bytes must use resolve_artifact_path."""
    value = Path(recorded); source = Path(marker["source_root"])
    if not value.is_absolute() or "." in value.parts or ".." in value.parts: return None, "none", "blocked", "unsafe recorded path", checksum, size
    try: relative = value.relative_to(source)
    except ValueError: relative = None
    if relative is not None:
        key = relative.as_posix()
        try: target, member = _member(root, marker, key)
        except ValueError: return None, "none", "blocked", "unarchived historical source path", checksum, size
        if checksum is not None and checksum != member["sha256"]: raise ValueError("recorded artifact checksum conflicts with archive")
        if size is not None and size != member["bytes"]: raise ValueError("recorded artifact size conflicts with archive")
        if target.stat().st_size != member["bytes"]: return None, "archive", "missing", "archived source file size differs", member["sha256"], member["bytes"]
        return target, "archive", "available", None, member["sha256"], member["bytes"]
    library = _library_root(); character_root = library / "characters" / marker["character_id"]
    if _unsafe(character_root, library) or not value.is_relative_to(character_root): return None, "none", "blocked", "outside character Library", checksum, size
    if _unsafe(value, library): return None, "none", "blocked", "unsafe Library path", checksum, size
    resolved = value.resolve(strict=False)
    if not resolved.is_relative_to(character_root): return None, "none", "blocked", "outside character Library", checksum, size
    if not resolved.is_file(): return None, "library", "missing", "recorded Library file is missing", checksum, size
    if size is not None and resolved.stat().st_size != size: return None, "library", "missing", "recorded Library file size differs", checksum, size
    return resolved, "library", "available", None, checksum, size

def _artifact_rows(root: Path, marker: dict) -> list[dict]:
    if marker["schema_version"] != 2 or marker.get("outputs_root") is not None: return []
    rows=[]
    for item in sorted(marker["files"], key=lambda value: value["path"]):
        match=re.fullmatch(r"runs/([A-Za-z0-9][A-Za-z0-9._-]*)/run\.json", item["path"])
        if not match: continue
        record_path, _ = _member(root, marker, item["path"], verify=True)
        try: record=json.loads(record_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc: raise ValueError("invalid archived run record") from exc
        if not isinstance(record, dict) or not isinstance(record.get("status"), str) or not isinstance(record.get("artifacts"), list): raise ValueError("invalid archived run record")
        for index, artifact in enumerate(record["artifacts"]):
            recorded, checksum, size = _artifact_value(artifact)
            target, location, status, reason, checksum, size = _artifact_target(root, marker, recorded, checksum, size)
            rows.append({"run_id": match.group(1), "run_status": record["status"], "record_path": str(record_path), "artifact_index": index, "recorded_path": recorded, "resolved_path": str(target) if target is not None else None, "location": location, "status": status, "reason": reason, "sha256": checksum, "byte_count": size, "integrity": "not_checked"})
    return rows

def describe_archives(character_id: str) -> list[dict]:
    if not isinstance(character_id, str) or not _ID.fullmatch(character_id): raise ValueError("invalid character ID")
    library=_cm().shared_creation_library()
    if library is None: return []
    library=_library_root(); parent=library / "characters" / character_id / "generations"
    if not parent.is_dir(): return []
    result=[]
    for marker_path in sorted([*parent.glob("*/record-archive.json"), *parent.glob("*/historical-records/*/record-archive.json")]):
        archive=marker_path.parent
        if _unsafe(archive, library): raise ValueError("record archive contains a symlink or junction")
        marker=_marker(archive)
        if marker["character_id"] != character_id: raise ValueError("record archive IDs do not match path")
        row={"character_id": character_id, "session_id": marker["session_id"], "records_path": str(archive), "outputs_path": marker.get("outputs_root"), "source_path": marker["source_root"], "captured_at": marker["captured_at"], "record_count": len(marker["files"]), "manifest_sha256": hashlib.sha256(marker_path.read_bytes()).hexdigest(), "authority": marker["authority"]}
        if marker["schema_version"] == 2: row["snapshot_id"] = marker["snapshot_id"]
        if marker["schema_version"] == 2 and marker.get("outputs_root") is None: row["recorded_artifacts"] = _artifact_rows(archive.resolve(), marker)
        result.append(row)
    return result

def resolve_recorded_path(archive_root: str | Path, recorded_path: str | Path) -> Path:
    root=Path(archive_root); marker=_marker(root); root=root.resolve(); source=Path(marker["source_root"])
    value=Path(recorded_path)
    try: relative=value.relative_to(source)
    except ValueError as exc: raise ValueError("recorded path is outside historical source") from exc
    if relative.is_absolute() or ".." in relative.parts or "." in relative.parts: raise ValueError("recorded path is invalid")
    key=relative.as_posix(); members={item["path"]: item for item in marker["files"]}
    if key not in members: raise ValueError("recorded path is not archived")
    target, _ = _member(root, marker, key, verify=True)
    return target

def resolve_artifact_path(archive_root: str | Path, run_record_relative_path: str, artifact_index: int) -> Path:
    if type(artifact_index) is not int or artifact_index < 0: raise ValueError("invalid artifact index")
    root=Path(archive_root); marker=_marker(root); root=root.resolve(); library=_library_root()
    if not root.is_relative_to(library): raise ValueError("archive is outside configured Library")
    if marker["schema_version"] != 2 or marker.get("outputs_root") is not None: raise ValueError("archive has no recorded artifacts")
    if not isinstance(run_record_relative_path, str) or not re.fullmatch(r"runs/[A-Za-z0-9][A-Za-z0-9._-]*/run\.json", run_record_relative_path): raise ValueError("invalid archived run path")
    record_path, _ = _member(root, marker, run_record_relative_path, verify=True)
    try: record=json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise ValueError("invalid archived run record") from exc
    if not isinstance(record, dict) or not isinstance(record.get("status"), str) or not isinstance(record.get("artifacts"), list) or artifact_index >= len(record["artifacts"]): raise ValueError("invalid archived run record or index")
    recorded, checksum, size = _artifact_value(record["artifacts"][artifact_index]); target, _, status, _, checksum, size = _artifact_target(root, marker, recorded, checksum, size)
    if target is None or status != "available" or checksum is None: raise ValueError("recorded artifact is unavailable or unchecked")
    if size is not None and target.stat().st_size != size: raise ValueError("recorded artifact size differs")
    digest=hashlib.sha256()
    with target.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""): digest.update(block)
    if digest.hexdigest() != checksum: raise ValueError("recorded artifact hash differs")
    return target
