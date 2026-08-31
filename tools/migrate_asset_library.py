#!/usr/bin/env python3
"""Move generated media out of Git worktrees into the durable AI Studio library."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = Path(r"D:\AI_Studio\library")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def discover() -> list[Path]:
    paths = list((ROOT / "examples" / "character-lab" / "experiments").glob("BATCH-*/batch.yaml"))
    paths.extend((ROOT / "characters").glob("ch-*/02_generations/*/batch.yaml"))
    return sorted(path.resolve() for path in paths)


def source_outputs(manifest_path: Path, manifest: dict) -> Path | None:
    configured = (manifest.get("session") or {}).get("asset_root")
    if configured:
        return Path(str(configured)).resolve()
    candidate = manifest_path.parent / "outputs"
    return candidate.resolve() if candidate.is_dir() else None


def target_outputs(library: Path, manifest_path: Path, manifest: dict) -> Path:
    session = manifest.get("session") or {}
    character_id = str(session.get("character_id") or manifest.get("character_id") or "unassigned")
    session_id = str(session.get("id") or manifest_path.parent.name)
    return (library / "characters" / character_id / "generations" / session_id / "outputs").resolve()


def migrate(library: Path, commit: bool) -> dict:
    library = library.resolve()
    expected_root = DEFAULT_LIBRARY.resolve()
    if library != expected_root and not library.is_relative_to(expected_root):
        raise ValueError(f"library target must stay under {expected_root}")
    report = {"mode": "commit" if commit else "plan", "library": str(library), "sessions": [], "files": 0, "bytes": 0}
    for manifest_path in discover():
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        source = source_outputs(manifest_path, manifest)
        if source is None or not source.is_dir():
            continue
        target = target_outputs(library, manifest_path, manifest)
        if target == source:
            continue
        files = sorted(path for path in source.rglob("*") if path.is_file())
        entry = {"manifest": str(manifest_path), "source": str(source), "target": str(target), "files": len(files), "bytes": sum(path.stat().st_size for path in files)}
        report["sessions"].append(entry)
        report["files"] += entry["files"]
        report["bytes"] += entry["bytes"]
        if not commit:
            continue
        artifacts = []
        for src in files:
            relative = src.relative_to(source)
            dst = target / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            source_hash = digest(src)
            if dst.exists():
                if dst.stat().st_size != src.stat().st_size or digest(dst) != source_hash:
                    raise RuntimeError(f"target conflict: {dst}")
            else:
                shutil.copy2(src, dst)
            if digest(dst) != source_hash:
                raise RuntimeError(f"verification failed: {dst}")
            artifacts.append({"relative_path": relative.as_posix(), "sha256": source_hash, "byte_count": src.stat().st_size, "library_path": str(dst)})
        asset_manifest = {
            "schema_version": 1,
            "migrated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "asset_root": str(target),
            "artifacts": artifacts,
        }
        atomic_text(manifest_path.parent / "asset-manifest.json", json.dumps(asset_manifest, ensure_ascii=False, indent=2) + "\n")
        manifest.setdefault("session", {})["asset_root"] = str(target)
        atomic_text(manifest_path, yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--commit", action="store_true", help="copy, verify, and update manifests; source media remains as a backup")
    args = parser.parse_args()
    print(json.dumps(migrate(args.library, args.commit), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
