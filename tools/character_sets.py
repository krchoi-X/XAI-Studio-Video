"""Immutable shared character-set locations and lightweight set discovery."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


_CHARACTER_ID = re.compile(r"ch-[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def _character_manager():
    """Load the sibling resolver when this module is imported by file path."""
    source = Path(__file__).with_name("character_manager.py")
    spec = importlib.util.spec_from_file_location("character_sets_manager", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("Character Manager resolver is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _valid_character_id(character_id: str) -> str:
    if not isinstance(character_id, str) or not _CHARACTER_ID.fullmatch(character_id):
        raise ValueError("invalid character ID")
    return character_id


def _has_reparse_point(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        return bool(getattr(path.stat(), "st_file_attributes", 0) & getattr(os, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    except FileNotFoundError:
        return False


def _confined(root: Path, path: Path, *, file: bool = False) -> Path:
    lexical = path
    while True:
        if _has_reparse_point(lexical):
            raise ValueError(f"unsafe set path: {path}")
        if lexical == root or lexical.parent == lexical:
            break
        lexical = lexical.parent
    resolved = path.resolve(strict=False)
    if not resolved.is_relative_to(root) or (file and not resolved.is_file()):
        raise ValueError(f"set path escapes or is missing: {path}")
    return resolved


def _relative_member(set_dir: Path, value: object, *, caption: bool = False) -> Path:
    if not isinstance(value, str):
        raise ValueError("set member file is invalid")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("set member file escapes its set")
    member = _confined(set_dir, set_dir / relative, file=True)
    if caption:
        sidecar = member.with_suffix(".txt")
        _confined(set_dir, sidecar, file=True)
    return member


def _manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid set manifest: {path}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("members"), list):
        raise ValueError(f"unsupported set manifest: {path}")
    return data


def _describe_one(library: Path, character_id: str, set_dir: Path, kind: str) -> dict[str, Any]:
    manifest_name = "identity-set.json" if kind == "identity" else "dataset.json"
    manifest_path = _confined(set_dir, set_dir / manifest_name, file=True)
    manifest = _manifest(manifest_path)
    if manifest.get("character_id") != character_id:
        raise ValueError(f"set character does not match directory: {set_dir}")
    mirrored = 0
    for member in manifest["members"]:
        if not isinstance(member, dict):
            raise ValueError(f"invalid set member: {set_dir}")
        member_path = _relative_member(set_dir, member.get("file"), caption=(kind == "lora"))
        if kind == "lora":
            caption = member.get("caption")
            sidecar = member_path.with_suffix(".txt")
            # Schema-1 datasets predate manifest-level caption copies; retain them
            # while requiring exact sidecars once a caption is declared.
            if caption is not None and (not isinstance(caption, str) or sidecar.read_text(encoding="utf-8").strip() != caption):
                raise ValueError(f"dataset caption sidecar does not match manifest: {sidecar}")
        mirrored += bool(member.get("mirrored"))
    context = set_dir / "set-context.json"
    if context.exists():
        _confined(set_dir, context, file=True)
    return {
        "set_id": set_dir.relative_to(library).as_posix(),
        "kind": kind,
        "path": str(set_dir),
        "manifest_path": str(manifest_path),
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "member_count": len(manifest["members"]),
        "mirrored_count": mirrored,
        "review_state": manifest.get("review_state"),
        "context_available": context.is_file(),
    }


def describe_sets(character_id: str) -> list[dict[str, Any]]:
    """List complete schema-1 shared sets for one character; never elect a current set."""
    character_id = _valid_character_id(character_id)
    library = _character_manager().shared_creation_library()
    if library is None:
        return []
    library = Path(library).resolve()
    character_root = _confined(library, library / "characters" / character_id)
    if not character_root.is_dir():
        return []
    result: list[dict[str, Any]] = []
    for kind, parent, manifest in (
        ("identity", character_root / "imports" / "derived", "identity-set.json"),
        ("lora", character_root / "training", "dataset.json"),
    ):
        if not parent.exists():
            continue
        _confined(library, parent)
        if not parent.is_dir():
            raise ValueError(f"set parent is not a directory: {parent}")
        for set_dir in sorted(parent.iterdir()):
            if not set_dir.is_dir():
                continue
            _confined(library, set_dir)
            if (set_dir / manifest).exists():
                result.append(_describe_one(library, character_id, set_dir, kind))
    return result


def reserve_destination(kind: str, character_id: str, requested: str | Path | None) -> Path:
    """Reserve an empty immutable set directory without touching an existing one."""
    character_id = _valid_character_id(character_id)
    if kind not in {"identity", "lora"}:
        raise ValueError("unknown set kind")
    library = _character_manager().shared_creation_library()
    if library is None:
        if requested is None:
            raise ValueError("an explicit output directory is required without a shared Library")
        target = Path(requested)
    else:
        library = Path(library).resolve()
        parent = library / "characters" / character_id / ("imports/derived" if kind == "identity" else "training")
        _confined(library, parent)
        if requested is None:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            prefix = "identity-set" if kind == "identity" else "lora-dataset"
            target = parent / f"{prefix}-{stamp}"
            suffix = 1
            while target.exists():
                suffix += 1
                target = parent / f"{prefix}-{stamp}-{suffix}"
        else:
            target = Path(requested)
            if target.parent != parent:
                raise ValueError("shared set output must be an immediate child of its character parent")
            _confined(library, parent)
    if target.exists():
        raise FileExistsError(f"immutable set destination already exists: {target}")
    if ".." in target.parts or _has_reparse_point(target.parent):
        raise ValueError("set output must not use traversal, a symlink, or a junction")
    target.mkdir(parents=True, exist_ok=False)
    return target.resolve()


def write_set_context(set_dir: Path, *, character_id: str, producer: Path,
                      arguments: dict[str, object], source_manifest: Path,
                      source_bytes: bytes, output_files: list[Path]) -> None:
    """Snapshot small mutable inputs and record hashes before publishing a set manifest."""
    set_dir = Path(set_dir).resolve()
    source_manifest = Path(source_manifest).resolve()
    if not source_manifest.is_file():
        raise FileNotFoundError(f"set source manifest is missing: {source_manifest}")
    cm = _character_manager()
    dna = Path(cm.character_record_path(_valid_character_id(character_id))).resolve()
    if not dna.is_file():
        raise FileNotFoundError(f"character DNA is missing: {dna}")
    if source_manifest.read_bytes() != source_bytes:
        raise ValueError("set source manifest changed during preparation")
    dna_bytes = dna.read_bytes()
    try:
        dna_version = json.loads(dna_bytes).get("version")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"character DNA is invalid: {dna}") from exc
    inputs = set_dir / "inputs"
    inputs.mkdir(exist_ok=False)
    source_copy = inputs / f"source-manifest{source_manifest.suffix or '.bin'}"
    dna_copy = inputs / "character.json"
    source_copy.write_bytes(source_bytes)
    dna_copy.write_bytes(dna_bytes)
    members: list[dict[str, str]] = []
    for file in output_files:
        file = Path(file).resolve()
        if not file.is_relative_to(set_dir) or not file.is_file():
            raise ValueError(f"set output is missing or escapes: {file}")
        members.append({"file": file.relative_to(set_dir).as_posix(), "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
    context = {
        "schema_version": 1,
        "producer": {"path": str(producer.resolve()), "sha256": hashlib.sha256(producer.read_bytes()).hexdigest()},
        "arguments": json.loads(json.dumps(arguments, default=str, ensure_ascii=False)),
        "inputs": {
            "source_manifest": {"path": str(source_manifest), "snapshot": source_copy.relative_to(set_dir).as_posix(), "sha256": hashlib.sha256(source_copy.read_bytes()).hexdigest()},
            "character_dna": {"path": str(dna), "snapshot": dna_copy.relative_to(set_dir).as_posix(), "sha256": hashlib.sha256(dna_copy.read_bytes()).hexdigest(), "version": dna_version, "context_only": True},
        },
        "output_members": members,
        "dna_context_note": "DNA is contextual unless this producer explicitly uses it for identity.",
    }
    (set_dir / "set-context.json").write_text(json.dumps(context, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def publish_manifest(path: Path, manifest: dict) -> None:
    """Publish complete JSON only; an interrupted write stays visibly unfinished."""
    if path.exists():
        raise FileExistsError(f"immutable set manifest already exists: {path}")
    temporary = path.with_name('.' + path.name + '.pending')
    with temporary.open('x', encoding='utf-8') as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    # A same-filesystem hard link publishes atomically and refuses an existing name.
    # Remove only our newly created temporary link after publication succeeds.
    os.link(temporary, path)
    temporary.unlink()
