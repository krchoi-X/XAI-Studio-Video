"""Read-only model of character-independent productions.

A production is a library session folder (`<root>/<session-id>/`) that carries a `session-provenance.json`
written by `wangp_recorder.py session`. This module only reads: it never writes, moves or deletes anything, and
it never follows a request-supplied path outside a discovered production folder.

It is shared by the Control Tower `/productions` page and by `tools/productions_drive_export.py`, so what the page
shows and what the backup copies are decided in exactly one place.
"""
from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Any

PROVENANCE = "session-provenance.json"
VIDEO_SUFFIXES = {".mp4", ".webm", ".mov"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
TEXT_SUFFIXES = {".txt", ".json", ".md", ".py", ".yaml", ".yml"}
SERVABLE_SUFFIXES = VIDEO_SUFFIXES | IMAGE_SUFFIXES | TEXT_SUFFIXES
# Folders never listed or backed up: duplicate raw outputs, scratch frames and per-run machine logs.
EXCLUDED_DIRS = {"raw", "scratch", "runs", "__pycache__"}
PROVENANCE_FIELDS = (
    "session_id", "title", "requested_by", "executor", "engine", "model", "status", "character_id",
    "source_idea", "user_request_verbatim", "created_at", "updated_at",
)


def _read_provenance(session_dir: Path) -> tuple[dict[str, Any], str | None]:
    try:
        data = json.loads((session_dir / PROVENANCE).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {}, f"unreadable {PROVENANCE}: {exc}"
    if not isinstance(data, dict):
        return {}, f"{PROVENANCE} is not an object"
    return data, None


def _walk(base: Path):
    """Yield files under `base`, skipping excluded folders and anything that is not a regular file."""
    if not base.is_dir():
        return
    for path in sorted(base.rglob("*")):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(base).parts[:-1]):
            continue
        if path.is_file():
            yield path


def _entry(session_dir: Path, path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {"path": path.relative_to(session_dir).as_posix(), "name": path.name, "bytes": stat.st_size,
            "modified": stat.st_mtime}


def classify(session_dir: Path) -> dict[str, list[dict[str, Any]]]:
    """Group a production's files. Intermediates (`norm-*`), raw duplicates and run logs are left out."""
    final: list[dict[str, Any]] = []
    clips: list[dict[str, Any]] = []
    experiments: list[dict[str, Any]] = []
    images: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    for path in _walk(session_dir):
        rel = path.relative_to(session_dir)
        parts = rel.parts
        suffix = path.suffix.lower()
        if parts[0] == "outputs" and suffix in VIDEO_SUFFIXES:
            if path.name.startswith("norm-"):
                continue
            if len(parts) > 1 and parts[1] == "exp":
                experiments.append(_entry(session_dir, path))
            elif "final" in path.stem.lower():
                final.append(_entry(session_dir, path))
            else:
                clips.append(_entry(session_dir, path))
        elif parts[0] == "refs" and len(parts) == 2 and suffix in IMAGE_SUFFIXES:
            images.append(_entry(session_dir, path))
        elif parts[0] != "outputs" and suffix in TEXT_SUFFIXES and len(path.relative_to(session_dir).parts) <= 3:
            records.append(_entry(session_dir, path))
    return {"final": final, "clips": clips, "experiments": experiments, "images": images, "records": records}


def _summary(session_dir: Path) -> dict[str, Any]:
    prov, problem = _read_provenance(session_dir)
    files = classify(session_dir)
    return {
        "id": session_dir.name,
        "title": prov.get("title") or session_dir.name,
        "status": prov.get("status") or ("unknown" if not problem else "unreadable"),
        "requested_by": prov.get("requested_by"),
        "executor": prov.get("executor"),
        "engine": prov.get("engine"),
        "model": prov.get("model"),
        "character_id": prov.get("character_id"),
        "source_idea": prov.get("source_idea"),
        "created_at": prov.get("created_at"),
        "updated_at": prov.get("updated_at"),
        "problem": problem,
        "final_video": files["final"][0]["path"] if files["final"] else None,
        "clip_count": len(files["clips"]),
        "experiment_count": len(files["experiments"]),
    }


def discover(root: Path) -> list[Path]:
    """Session folders directly under `root` that carry a provenance file."""
    if not root.is_dir():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir() and not p.is_symlink() and (p / PROVENANCE).is_file())


def list_productions(root: Path) -> list[dict[str, Any]]:
    rows = [_summary(path) for path in discover(root)]
    rows.sort(key=lambda r: (r.get("created_at") or "", r["id"]), reverse=True)
    return rows


def session_dir_for(root: Path, session_id: str) -> Path | None:
    """The discovered folder for `session_id`, or None. The id must be one path component of an existing production."""
    if not session_id or session_id in {".", ".."} or "/" in session_id or "\\" in session_id:
        return None
    candidate = root / session_id
    return candidate if candidate in discover(root) else None


def get_production(root: Path, session_id: str) -> dict[str, Any] | None:
    session_dir = session_dir_for(root, session_id)
    if session_dir is None:
        return None
    prov, problem = _read_provenance(session_dir)
    detail = _summary(session_dir)
    detail["provenance"] = {k: prov.get(k) for k in PROVENANCE_FIELDS if k in prov}
    detail["files"] = classify(session_dir)
    detail["problem"] = problem
    return detail


def resolve_media(root: Path, session_id: str, relative: str) -> Path | None:
    """Resolve one servable file inside a production, or None. Never returns a path outside the session folder."""
    session_dir = session_dir_for(root, session_id)
    if session_dir is None or not relative or "\x00" in relative:
        return None
    rel = Path(relative.replace("\\", "/"))
    if rel.is_absolute() or any(part in {"", ".", ".."} for part in rel.parts):
        return None
    target = (session_dir / rel).resolve()
    try:
        target.relative_to(session_dir.resolve())
    except ValueError:
        return None
    if not target.is_file() or target.suffix.lower() not in SERVABLE_SUFFIXES:
        return None
    if any(part in EXCLUDED_DIRS for part in target.relative_to(session_dir.resolve()).parts[:-1]):
        return None
    return target


def media_type(path: Path) -> str:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return "text/plain; charset=utf-8"
    return mimetypes.guess_type(str(path))[0] or "application/octet-stream"


def backup_manifest(session_dir: Path) -> list[tuple[str, str]]:
    """(category, relative path) pairs the Drive backup copies: Videos, Images and Record."""
    files = classify(session_dir)
    manifest: list[tuple[str, str]] = []
    for group in ("final", "clips", "experiments"):
        manifest.extend(("Videos", item["path"]) for item in files[group])
    manifest.extend(("Images", item["path"]) for item in files["images"])
    manifest.extend(("Record", item["path"]) for item in files["records"])
    return manifest
