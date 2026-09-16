"""Exact historical inputs for newly shared character generation sessions."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import character_manager as cm


def snapshot_inputs(session: Path, character: dict, producer: Path, *, identity_role: str = "identity_input", skill_name: str = "character-manager", workflow: Path | None = None) -> None:
    if cm.shared_creation_library() is None:
        return
    character_path = cm.character_record_path(character["id"])
    data = character_path.read_bytes()
    if json.loads(data) != character:
        raise cm.CharacterError("character changed during session preparation; retry with fresh input")
    files = []

    def save(source: Path, relative: Path, raw: bytes | None = None):
        raw = source.read_bytes() if raw is None else raw
        target = session / "inputs" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(raw)
        files.append({"source":str(source), "snapshot":target.relative_to(session).as_posix(), "sha256":hashlib.sha256(raw).hexdigest()})

    save(character_path, Path("character.json"), data)
    if workflow is not None:
        save(workflow, Path("workflow") / workflow.name)
    skill = cm.shared_skill_path(skill_name)
    for source in sorted(skill.parent.rglob("*")):
        if source.is_file() and source.suffix in {".md", ".json", ".txt", ".yaml"}:
            resolved = source.resolve()
            if not resolved.is_relative_to(skill.parent.resolve()):
                raise cm.CharacterError("shared skill input escapes its source directory")
            save(source, Path("skills") / skill_name / source.relative_to(skill.parent))
    context = {"schema_version":1, "session_id":session.name,
               "character":{"id":character["id"],"version":character["version"],"role":identity_role},
               "producer":{"path":str(producer.resolve()),"sha256":hashlib.sha256(producer.read_bytes()).hexdigest()},
               "skill":skill_name,"inputs":files,"created_at":cm.now()}
    cm.atomic_write(session / "creation-context.json", json.dumps(context,ensure_ascii=False,indent=2)+"\n")
