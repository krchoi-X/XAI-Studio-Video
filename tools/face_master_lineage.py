"""Additive lineage record for the face-first character-master workflow.

One JSON file links the exact Stable DNA, face candidates, an Xpade-sculpted copy, a body target and a head/face-swap
composite through file hashes and recorded provenance.  The writer only ever registers candidates: approval roles
(`face_master`, `body_master`, `composite_identity_master`) are rejected because only the operator's existing review
route may confer them.  It never copies, moves or modifies media, never touches the Gallery database and never edits
character records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
RECORD_KIND = "face_master_lineage"
CANDIDATE_ROLES = ("face_candidate", "sculpted_face_candidate", "body_target", "composite_candidate")
APPROVAL_ROLES = ("face_master", "body_master", "composite_identity_master")
SELECTION_ROLES = ("base_face_selection", "body_target_selection")
SWAP_OPERATIONS = ("head_swap", "face_swap", "body_swap")
# Roles each artifact may derive from; swap inputs are validated separately.
PARENT_ROLES = {
    "face_candidate": {"face_candidate"},  # a later exploration round may cite the round it adjusts
    "sculpted_face_candidate": {"face_candidate"},
    "body_target": {"body_target"},
    "composite_candidate": {"body_target", "sculpted_face_candidate", "face_candidate"},
}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


class LineageError(ValueError):
    """Raised when a lineage change cannot be represented safely."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def new_record(lineage_id: str, concept_dna: dict[str, Any], *, created_by: str, note: str = "") -> dict[str, Any]:
    """Start a record bound to the exact Stable DNA it was derived from."""
    if not lineage_id.strip():
        raise LineageError("lineage_id is required")
    for key in ("character_id", "record_path", "character_version", "stable_dna_sha256"):
        if concept_dna.get(key) in (None, ""):
            raise LineageError(f"concept_dna.{key} is required")
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": RECORD_KIND,
        "lineage_id": lineage_id.strip(),
        "created_at": now(),
        "created_by": created_by,
        "note": note,
        "concept_dna": {key: concept_dna[key] for key in concept_dna},
        "face_discovery_brief": None,
        "artifacts": [],
        "selections": [],
        "approvals": [],  # reserved: filled only by the existing review route, never by this writer
    }


def set_brief(record: dict[str, Any], brief: dict[str, Any]) -> None:
    """Attach the engine-neutral brief; per-engine prompts stay on each artifact as `prompt_sent`."""
    text = str(brief.get("text") or "").strip()
    if not text:
        raise LineageError("brief.text is required")
    record["face_discovery_brief"] = {**brief, "text": text, "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def _artifact(record: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    for item in record["artifacts"]:
        if item["id"] == artifact_id:
            return item
    raise LineageError(f"unknown artifact: {artifact_id}")


def add_artifact(
    record: dict[str, Any], *, artifact_id: str, role: str, path: str | Path, parents: list[str] | None = None,
    provenance: dict[str, Any] | None = None, asset_id: str | None = None,
) -> dict[str, Any]:
    """Register one existing file as a candidate.  Hashes are computed here, never trusted from the caller."""
    if role in APPROVAL_ROLES:
        raise LineageError(f"{role} is an operator approval; this writer registers candidates only")
    if role not in CANDIDATE_ROLES:
        raise LineageError(f"unsupported role: {role}")
    artifact_id = artifact_id.strip()
    if not artifact_id or any(item["id"] == artifact_id for item in record["artifacts"]):
        raise LineageError("artifact IDs must be non-empty and unique")
    file_path = Path(path).resolve()
    if not file_path.is_file():
        raise LineageError(f"file not found: {file_path}")
    if file_path.suffix.lower() not in IMAGE_SUFFIXES:
        raise LineageError(f"unsupported image type: {file_path.suffix}")
    digest = sha256_file(file_path)
    for item in record["artifacts"]:
        if item["path"] == str(file_path):
            raise LineageError(f"file already registered as {item['id']}; derivatives must be new files: {file_path}")
        if item["sha256"] == digest:
            raise LineageError(f"identical bytes already registered as {item['id']}; a derivative must differ")
    parents = list(dict.fromkeys(parents or []))
    allowed = PARENT_ROLES[role]
    for parent in parents:
        if _artifact(record, parent)["role"] not in allowed:
            raise LineageError(f"{role} cannot derive from {_artifact(record, parent)['role']} ({parent})")
    provenance = deepcopy(provenance or {})
    entry: dict[str, Any] = {
        "id": artifact_id, "role": role, "asset_id": asset_id, "path": str(file_path),
        "sha256": digest, "byte_count": file_path.stat().st_size, "parents": parents,
        "status": "needs_review", "registered_at": now(), "provenance": provenance,
    }
    _validate_role_rules(record, entry)
    record["artifacts"].append(entry)
    return entry


def _validate_role_rules(record: dict[str, Any], entry: dict[str, Any]) -> None:
    role, provenance = entry["role"], entry["provenance"]
    if role in ("face_candidate", "body_target"):
        for key in ("provider", "model", "prompt_sent"):
            if not str(provenance.get(key) or "").strip():
                raise LineageError(f"{role} provenance requires {key} (the exact text sent, not a summary)")
    if role == "face_candidate":
        # An external engine must say so; absent means a local engine and needs a recorded model.
        if provenance.get("external") and not str(provenance.get("requested_by") or "").strip():
            raise LineageError("external face_candidate requires requested_by")
    if role == "sculpted_face_candidate":
        if len(entry["parents"]) != 1:
            raise LineageError("sculpted_face_candidate requires exactly one face_candidate parent")
        tool = provenance.get("tool")
        if not isinstance(tool, dict) or not str(tool.get("name") or "").strip():
            raise LineageError("sculpted_face_candidate provenance requires tool.name")
        if not str(provenance.get("edit_note") or "").strip():
            raise LineageError("sculpted_face_candidate provenance requires edit_note")
        if "replayable" not in provenance:
            raise LineageError("record replayable=true only when exported parameters exist; otherwise false")
    if role == "composite_candidate":
        operation = provenance.get("operation")
        if operation not in SWAP_OPERATIONS:
            raise LineageError(f"composite_candidate provenance.operation must be one of {SWAP_OPERATIONS}")
        inputs = provenance.get("ordered_inputs")
        if not isinstance(inputs, list) or len(inputs) != 2:
            raise LineageError("composite_candidate requires two ordered_inputs (position 1 = base, 2 = reference)")
        if [item.get("position") for item in inputs] != [1, 2]:
            raise LineageError("ordered_inputs must be listed as positions 1 then 2")
        base, reference = (_artifact(record, str(item.get("artifact_id"))) for item in inputs)
        if operation == "body_swap":
            raise LineageError("body_swap is a separate experiment; record it only after its own contract review")
        if base["role"] != "body_target":
            raise LineageError("position 1 (base) must be a body_target")
        if reference["role"] not in ("sculpted_face_candidate", "face_candidate"):
            raise LineageError("position 2 (reference head/face) must be a sculpted or untouched face candidate")
        if set(entry["parents"]) != {base["id"], reference["id"]}:
            raise LineageError("parents must be exactly the two ordered inputs")
        for key in ("provider", "model", "prompt_sent"):
            if not str(provenance.get(key) or "").strip():
                raise LineageError(f"composite_candidate provenance requires {key}")
        loras = provenance.get("loras")
        if not isinstance(loras, list):
            raise LineageError("composite_candidate provenance requires loras (use [] when none)")
        for lora in loras:
            for key in ("filename", "sha256", "byte_count", "strength"):
                if lora.get(key) in (None, ""):
                    raise LineageError(f"each lora needs {key}")
        if not isinstance(provenance.get("render_settings"), dict):
            raise LineageError("composite_candidate provenance requires render_settings")


def add_selection(record: dict[str, Any], *, role: str, artifact_id: str, selected_by: str, note: str = "") -> dict[str, Any]:
    """Record the operator's choice.  A selection is not an approval and changes no artifact status."""
    if role not in SELECTION_ROLES:
        raise LineageError(f"unsupported selection role: {role}")
    expected = {"base_face_selection": "face_candidate", "body_target_selection": "body_target"}[role]
    if _artifact(record, artifact_id)["role"] != expected:
        raise LineageError(f"{role} must name a {expected}")
    if not selected_by.strip():
        raise LineageError("selected_by is required")
    selection = {"role": role, "artifact_id": artifact_id, "selected_by": selected_by, "note": note, "at": now()}
    record["selections"].append(selection)
    return selection


def validate(record: dict[str, Any]) -> list[str]:
    """Structural problems only (no file access).  Empty list means consistent."""
    problems: list[str] = []
    if record.get("kind") != RECORD_KIND or record.get("schema_version") != SCHEMA_VERSION:
        problems.append("not a face_master_lineage v1 record")
        return problems
    ids = [item["id"] for item in record.get("artifacts", [])]
    if len(ids) != len(set(ids)):
        problems.append("duplicate artifact IDs")
    seen: set[str] = set()
    for item in record.get("artifacts", []):
        if item.get("role") in APPROVAL_ROLES:
            problems.append(f"{item['id']}: approval role registered by the writer")
        if item.get("status") != "needs_review":
            problems.append(f"{item['id']}: writer-owned status must stay needs_review")
        for parent in item.get("parents", []):
            if parent not in seen:
                problems.append(f"{item['id']}: parent {parent} missing or registered later")
        seen.add(item["id"])
    if record.get("approvals"):
        problems.append("approvals must be empty; approval happens in the existing review route")
    return problems


def verify_files(record: dict[str, Any]) -> list[str]:
    """Re-hash every registered file.  Returns mismatches; an empty list proves the inputs are byte-identical."""
    problems = []
    for item in record["artifacts"]:
        path = Path(item["path"])
        if not path.is_file():
            problems.append(f"{item['id']}: file missing: {path}")
        elif path.stat().st_size != item["byte_count"] or sha256_file(path) != item["sha256"]:
            problems.append(f"{item['id']}: bytes changed since registration: {path}")
    return problems


def load(path: Path) -> dict[str, Any]:
    record = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(record, dict):
        raise LineageError("lineage file must contain one JSON object")
    return record


def save(path: Path, record: dict[str, Any]) -> None:
    problems = validate(record)
    if problems:
        raise LineageError("; ".join(problems))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _read_json_arg(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    text = Path(value[1:]).read_text(encoding="utf-8-sig") if value.startswith("@") else value
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise LineageError("JSON argument must be an object")
    return parsed


def _current_dna(character_id: str) -> dict[str, Any]:
    import character_manager as cm  # resolved from tools/ like other maintained producers
    path = cm.character_record_path(character_id).resolve()
    record = cm.load(path)
    return {"character_id": character_id, "record_path": str(path), "character_version": record["version"],
            "stable_dna_sha256": cm.stable_hash(record)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create a lineage record bound to the current Stable DNA")
    init.add_argument("file")
    init.add_argument("--lineage-id", required=True)
    init.add_argument("--character-id", required=True)
    init.add_argument("--created-by", required=True, help="the real actor, e.g. claude, codex, user")
    brief = sub.add_parser("brief", help="attach the engine-neutral discovery brief text (@file or JSON)")
    brief.add_argument("file")
    brief.add_argument("--json", required=True)
    add = sub.add_parser("add", help="register one existing candidate file")
    add.add_argument("file")
    add.add_argument("--id", required=True)
    add.add_argument("--role", required=True)
    add.add_argument("--path", required=True)
    add.add_argument("--parent", action="append", default=[])
    add.add_argument("--asset-id")
    add.add_argument("--provenance", help="JSON object or @file")
    select = sub.add_parser("select", help="record an operator selection (not an approval)")
    select.add_argument("file")
    select.add_argument("--role", required=True, choices=SELECTION_ROLES)
    select.add_argument("--artifact-id", required=True)
    select.add_argument("--selected-by", required=True)
    select.add_argument("--note", default="")
    check = sub.add_parser("verify", help="validate structure and re-hash every file")
    check.add_argument("file")
    args = parser.parse_args(argv)
    path = Path(args.file)
    try:
        if args.command == "init":
            if path.exists():
                raise LineageError(f"refusing to overwrite existing lineage file: {path}")
            save(path, new_record(args.lineage_id, _current_dna(args.character_id), created_by=args.created_by))
        elif args.command == "verify":
            record = load(path)
            problems = validate(record) + verify_files(record)
            print(json.dumps({"ok": not problems, "problems": problems, "artifacts": len(record.get("artifacts", []))}, ensure_ascii=False, indent=2))
            return 0 if not problems else 1
        else:
            record = load(path)
            if args.command == "brief":
                set_brief(record, _read_json_arg(args.json))
            elif args.command == "add":
                add_artifact(record, artifact_id=args.id, role=args.role, path=args.path, parents=args.parent,
                             provenance=_read_json_arg(args.provenance), asset_id=args.asset_id)
            else:
                add_selection(record, role=args.role, artifact_id=args.artifact_id, selected_by=args.selected_by, note=args.note)
            save(path, record)
    except (LineageError, OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
