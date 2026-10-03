#!/usr/bin/env python3
"""Validate editorial-shot plans and compile an H3 execution summary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "shot-production-plan-v1.schema.json"
SCHEMA_BY_VERSION = {
    1: DEFAULT_SCHEMA,
    2: ROOT / "schemas" / "shot-production-plan-v2.schema.json",
}
STATE_FIELDS = {
    "body_pose", "left_hand", "right_hand", "gaze", "screen_position",
    "props", "wardrobe", "environment", "camera_relation",
}
H3_MODELS = {
    "h3_ref2va": "minimax_h3_ref2va_pruned",
    "h3_fl2va": "minimax_h3_fl2va_pruned",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def schema_errors(plan: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, str]]:
    errors = sorted(Draft202012Validator(schema).iter_errors(plan), key=lambda item: list(item.path))
    return [
        {
            "code": "schema_validation_failed",
            "path": "/".join(map(str, error.path)) or "<root>",
            "message": error.message,
        }
        for error in errors
    ]


def _issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def schema_path_for(plan: dict[str, Any]) -> Path:
    version = plan.get("schema_version")
    try:
        return SCHEMA_BY_VERSION[int(version)]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"unsupported shot production plan schema_version: {version!r}") from exc


def iter_chunks(plan: dict[str, Any]):
    for shot_index, shot in enumerate(plan.get("shots", [])):
        for chunk_index, chunk in enumerate(shot.get("render_chunks", [])):
            yield shot_index, shot, chunk_index, chunk


def semantic_errors(plan: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    shots = plan.get("shots", [])
    shot_ids = [shot.get("shot_id") for shot in shots]
    if len(shot_ids) != len(set(shot_ids)):
        issues.append(_issue("duplicate_shot_id", "shots", "shot_id values must be unique"))

    by_id = {shot.get("shot_id"): shot for shot in shots}
    schema_version = plan.get("schema_version")
    character_ids: set[str] = set()
    policy: dict[str, Any] = {}
    prompt_ids: list[str] = []
    if schema_version == 2:
        contracts = plan.get("character_contracts", [])
        ids = [item.get("character_id") for item in contracts]
        if len(ids) != len(set(ids)):
            issues.append(_issue("duplicate_character_contract", "character_contracts", "character_id values must be unique"))
        character_ids = {str(value) for value in ids if value}
        policy = plan.get("reference_policy", {})
    for index, shot in enumerate(shots):
        shot_id = shot.get("shot_id", f"index-{index}")
        prefix = f"shots/{index}"
        beats = shot.get("beats", [])
        beat_ids = [beat.get("beat_id") for beat in beats]
        if len(beat_ids) != len(set(beat_ids)):
            issues.append(_issue("duplicate_beat_id", f"{prefix}/beats", f"{shot_id} beat IDs must be unique"))

        keyframes = shot.get("keyframes", [])
        keyframe_ids = [item.get("keyframe_id") for item in keyframes]
        if len(keyframe_ids) != len(set(keyframe_ids)):
            issues.append(_issue("duplicate_keyframe_id", f"{prefix}/keyframes", f"{shot_id} keyframe IDs must be unique"))
        keyframe_map = {item.get("keyframe_id"): item for item in keyframes}
        for beat_index, beat in enumerate(beats):
            for keyframe_id in beat.get("keyframe_ids", []):
                keyframe = keyframe_map.get(keyframe_id)
                if keyframe is None:
                    issues.append(_issue("unknown_keyframe", f"{prefix}/beats/{beat_index}/keyframe_ids", f"{keyframe_id} is not declared in {shot_id}"))
                elif keyframe.get("beat_id") != beat.get("beat_id"):
                    issues.append(_issue("keyframe_beat_mismatch", f"{prefix}/beats/{beat_index}/keyframe_ids", f"{keyframe_id} belongs to {keyframe.get('beat_id')}"))
        for keyframe_index, keyframe in enumerate(keyframes):
            if keyframe.get("beat_id") not in beat_ids:
                issues.append(_issue("unknown_keyframe_beat", f"{prefix}/keyframes/{keyframe_index}/beat_id", f"{keyframe.get('beat_id')} is not declared in {shot_id}"))

        chunks = shot.get("render_chunks", [])
        flattened = [beat_id for chunk in chunks for beat_id in chunk.get("beat_ids", [])]
        if flattened != beat_ids:
            issues.append(_issue("chunk_beat_order", f"{prefix}/render_chunks", "renderer chunks must cover every beat exactly once and preserve beat order"))
        for chunk_index, chunk in enumerate(chunks):
            roles = [reference.get("role") for reference in chunk.get("references", [])]
            route = chunk.get("route")
            chunk_path = f"{prefix}/render_chunks/{chunk_index}"
            if schema_version == 2:
                prompt_id = chunk.get("prompt_id")
                if prompt_id:
                    prompt_ids.append(str(prompt_id))
                chunk_characters = set(chunk.get("character_ids", []))
                unknown_characters = chunk_characters - character_ids
                if unknown_characters:
                    issues.append(_issue(
                        "unknown_chunk_character", f"{chunk_path}/character_ids",
                        f"chunk references undeclared character contracts: {sorted(unknown_characters)}",
                    ))
                identity_characters = {
                    reference.get("character_id") for reference in chunk.get("references", [])
                    if reference.get("role") == "identity_master"
                }
                missing_identity = chunk_characters - identity_characters
                if route == "h3_ref2va" and missing_identity:
                    issues.append(_issue(
                        "h3_ref2va_character_identity_missing", f"{chunk_path}/references",
                        f"H3 Ref2VA requires one identity_master per cast character: {sorted(missing_identity)}",
                    ))
                forbidden_tags = set(chunk.get("forbidden_state_tags", []))
                native_roles = set(policy.get("native_landscape_roles", []))
                for reference_index, reference in enumerate(chunk.get("references", [])):
                    reference_path = f"{chunk_path}/references/{reference_index}"
                    reference_character = reference.get("character_id")
                    if reference_character and reference_character not in character_ids:
                        issues.append(_issue(
                            "unknown_reference_character", f"{reference_path}/character_id",
                            f"reference uses undeclared character {reference_character}",
                        ))
                    if reference.get("role") in native_roles and reference.get("composition") != "native_landscape":
                        issues.append(_issue(
                            "non_native_landscape_reference", f"{reference_path}/composition",
                            f"{reference.get('role')} must use native_landscape composition",
                        ))
                    if policy.get("require_verified_laterality") and reference.get("laterality_sensitive"):
                        if reference.get("anatomical_laterality") in {"unknown", "not_applicable"} or not reference.get("verified_by"):
                            issues.append(_issue(
                                "unverified_reference_laterality", reference_path,
                                "laterality-sensitive references require subject anatomical laterality and verified_by",
                            ))
                    conflicting_tags = forbidden_tags & set(reference.get("state_tags", []))
                    if conflicting_tags:
                        issues.append(_issue(
                            "forbidden_reference_state", f"{reference_path}/state_tags",
                            f"reference carries forbidden state tags: {sorted(conflicting_tags)}",
                        ))
            if chunk.get("creates_edit_cut"):
                issues.append(_issue("renderer_chunk_is_not_edit_cut", f"{chunk_path}/creates_edit_cut", "renderer chunks inside one editorial shot must not create an edit cut"))
            if route == "h3_ref2va" and "identity_master" not in roles:
                issues.append(_issue("h3_ref2va_identity_missing", f"{chunk_path}/references", "H3 Ref2VA requires an explicit identity_master role"))
            if route == "h3_ref2va" and chunk_index > 0 and "previous_chunk_last_frame" not in roles:
                issues.append(_issue("chunk_handoff_missing", f"{chunk_path}/references", "a later Ref2VA chunk in the same shot must carry previous_chunk_last_frame"))
            if route == "h3_fl2va":
                if not ({"start_keyframe", "previous_chunk_last_frame", "previous_shot_last_frame"} & set(roles)):
                    issues.append(_issue("h3_fl2va_start_missing", f"{chunk_path}/references", "H3 FL2VA requires a start frame role"))
                if "end_keyframe" not in roles:
                    issues.append(_issue("h3_fl2va_end_missing", f"{chunk_path}/references", "H3 FL2VA requires an end_keyframe role"))
            if route == "renderer_extension" and "previous_chunk_last_frame" not in roles:
                issues.append(_issue("extension_source_missing", f"{chunk_path}/references", "renderer extension requires previous_chunk_last_frame"))

        transition = shot.get("transition_to_next", {})
        next_id = transition.get("next_shot_id")
        expected_next = shot_ids[index + 1] if index + 1 < len(shots) else None
        if next_id != expected_next:
            issues.append(_issue("nonsequential_transition", f"{prefix}/transition_to_next/next_shot_id", f"expected {expected_next!r}, found {next_id!r}"))
        relationship = transition.get("relationship")
        if expected_next is None:
            if relationship != "final" or transition.get("mode") != "none":
                issues.append(_issue("invalid_final_transition", f"{prefix}/transition_to_next", "the final shot must use relationship=final and mode=none"))
            continue
        if relationship == "final":
            issues.append(_issue("early_final_transition", f"{prefix}/transition_to_next/relationship", "only the last shot may be final"))
        carry_fields = transition.get("carry_fields", [])
        allowed_changes = set(transition.get("allowed_changes", []))
        if set(carry_fields) - STATE_FIELDS or allowed_changes - STATE_FIELDS:
            issues.append(_issue("unknown_state_field", f"{prefix}/transition_to_next", "transition fields must name known state fields"))
        if relationship == "dependent" and not carry_fields:
            issues.append(_issue("dependent_without_carry", f"{prefix}/transition_to_next/carry_fields", "dependent transitions must declare carried state"))
        if relationship == "dependent" and transition.get("mode") == "none":
            issues.append(_issue("dependent_without_transition", f"{prefix}/transition_to_next/mode", "dependent shots need an intentional edit transition"))
        target = by_id.get(next_id)
        if relationship == "dependent" and target:
            for field in carry_fields:
                if field in allowed_changes:
                    continue
                source_value = shot.get("exit_state", {}).get(field)
                target_value = target.get("entry_state", {}).get(field)
                if source_value != target_value:
                    issues.append(_issue("continuity_mismatch", f"{prefix}/transition_to_next/carry_fields", f"{shot_id} exit {field} does not match {next_id} entry {field}"))
        if schema_version == 2 and expected_next is not None and relationship == "dependent" and policy.get("continuity_boundary_required"):
            target = by_id.get(expected_next) or {}
            target_chunks = target.get("render_chunks", [])
            target_roles = {
                reference.get("role") for reference in (target_chunks[0].get("references", []) if target_chunks else [])
            }
            if not ({"previous_shot_last_frame", "start_keyframe"} & target_roles):
                issues.append(_issue(
                    "shot_handoff_missing", f"{prefix}/transition_to_next",
                    f"dependent shot {expected_next} must start from previous_shot_last_frame or start_keyframe",
                ))
    if schema_version == 2 and len(prompt_ids) != len(set(prompt_ids)):
        issues.append(_issue("duplicate_prompt_id", "shots/render_chunks/prompt_id", "prompt_id values must be unique across the plan"))
    return issues


def validate_plan(plan: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors = schema_errors(plan, schema)
    if not errors:
        errors.extend(semantic_errors(plan))
    return {"ok": not errors, "error_count": len(errors), "errors": errors}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _setting_paths(value: Any) -> list[str]:
    values = value if isinstance(value, list) else [value] if value else []
    return [str(Path(str(item)).resolve()) for item in values if str(item).strip()]


def _execution_chunk(plan: dict[str, Any], prompt_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    matches = [
        (shot, chunk) for _, shot, _, chunk in iter_chunks(plan)
        if chunk.get("prompt_id") == prompt_id
    ]
    if len(matches) != 1:
        raise ValueError(f"production plan must contain exactly one chunk for prompt_id {prompt_id!r}; found {len(matches)}")
    return matches[0]


def validate_submission_contract(
    plan: dict[str, Any],
    prompt_id: str,
    prompt: str,
    settings: dict[str, Any],
    current_characters: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Validate one execution-ready v2 chunk before a run or GPU worker is created.

    `current_characters` is resolved by the caller from the active Character Manager authority and contains
    record_path, character_version and stable_dna_sha256 for each cast member. Keeping that I/O outside this
    function makes the contract deterministic and directly testable.
    """
    if plan.get("schema_version") != 2:
        raise ValueError("a production-enforced plan must use shot-production-plan schema_version 2")
    schema = load_json(schema_path_for(plan))
    result = validate_plan(plan, schema)
    if not result["ok"]:
        first = result["errors"][0]
        raise ValueError(f"invalid production plan: {first['code']} at {first['path']}: {first['message']}")
    if plan.get("status") != "approved":
        raise ValueError("production plan must be approved before submission")
    shot, chunk = _execution_chunk(plan, prompt_id)
    contracts = {item["character_id"]: item for item in plan["character_contracts"]}
    prompt_folded = prompt.casefold()
    character_snapshot = []
    for character_id in chunk["character_ids"]:
        expected = contracts[character_id]
        current = current_characters.get(character_id)
        if not current:
            raise ValueError(f"current character authority was not resolved for {character_id}")
        for key in ("record_path", "character_version", "stable_dna_sha256"):
            expected_value = expected[key]
            current_value = current.get(key)
            if key == "record_path":
                expected_value = str(Path(str(expected_value)).resolve())
                current_value = str(Path(str(current_value)).resolve())
            if current_value != expected_value:
                raise ValueError(f"{character_id} {key} changed after plan approval: expected {expected_value!r}, found {current_value!r}")
        missing_terms = [term for term in expected["mandatory_prompt_terms"] if term.casefold() not in prompt_folded]
        if missing_terms:
            raise ValueError(f"{character_id} mandatory prompt anchors are missing: {missing_terms}")
        character_snapshot.append({**expected})

    model_type = str(settings.get("base_model_type") or settings.get("model_type") or "")
    expected_model = H3_MODELS.get(chunk["route"])
    if expected_model and model_type != expected_model:
        raise ValueError(f"chunk route {chunk['route']} requires model_type {expected_model}, found {model_type or '<missing>'}")

    references = chunk["references"]
    planned_paths = [str(Path(reference["asset"]).resolve()) for reference in references if reference.get("asset")]
    if len(planned_paths) != len(references):
        raise ValueError("execution-ready chunk references must have concrete asset paths")
    if chunk["route"] == "h3_ref2va":
        actual_paths = _setting_paths(settings.get("image_refs"))
        if actual_paths != planned_paths:
            raise ValueError(f"settings image_refs do not match the approved pack references: expected {planned_paths}, found {actual_paths}")
    elif chunk["route"] == "h3_fl2va":
        start_roles = {"start_keyframe", "previous_chunk_last_frame", "previous_shot_last_frame"}
        expected_start = [str(Path(reference["asset"]).resolve()) for reference in references if reference["role"] in start_roles]
        expected_end = [str(Path(reference["asset"]).resolve()) for reference in references if reference["role"] == "end_keyframe"]
        if _setting_paths(settings.get("image_start")) != expected_start:
            raise ValueError("settings image_start does not match the approved boundary reference")
        if _setting_paths(settings.get("image_end")) != expected_end:
            raise ValueError("settings image_end does not match the approved end keyframe")

    native_roles = set(plan["reference_policy"]["native_landscape_roles"])
    reference_snapshot = []
    for reference, value in zip(references, planned_paths):
        path = Path(value)
        if not path.is_file():
            raise ValueError(f"approved reference image not found: {path}")
        actual_hash = _sha256_file(path)
        if actual_hash != reference["sha256"]:
            raise ValueError(f"approved reference image changed after review: {path}")
        dimensions = None
        if reference["role"] in native_roles:
            try:
                from PIL import Image
                with Image.open(path) as image:
                    dimensions = [int(image.width), int(image.height)]
            except (ImportError, OSError) as exc:
                raise ValueError(f"cannot verify native-landscape reference dimensions: {path}: {exc}") from exc
            if dimensions[0] <= dimensions[1]:
                raise ValueError(f"native-landscape reference is not wider than tall: {path} ({dimensions[0]}x{dimensions[1]})")
        reference_snapshot.append({**reference, "asset": str(path), "verified_dimensions": dimensions})
    return {
        "snapshot_schema_version": 1,
        "plan_schema_version": plan["schema_version"],
        "plan_id": plan["plan_id"],
        "storyboard_id": plan["storyboard_id"],
        "shot_id": shot["shot_id"],
        "chunk_id": chunk["chunk_id"],
        "prompt_id": prompt_id,
        "route": chunk["route"],
        "characters": character_snapshot,
        "references": reference_snapshot,
        "reference_policy": plan["reference_policy"],
    }


def compile_h3(plan: dict[str, Any]) -> dict[str, Any]:
    shots = []
    warnings = list(plan.get("warnings", []))
    for shot in plan["shots"]:
        chunks = []
        for chunk in shot["render_chunks"]:
            model_type = H3_MODELS.get(chunk["route"])
            if model_type is None and chunk["route"] != "external":
                warnings.append(f"{shot['shot_id']}/{chunk['chunk_id']}: {chunk['route']} requires an adapter decision")
            chunks.append({
                "chunk_id": chunk["chunk_id"],
                "editorial_shot_id": shot["shot_id"],
                "beat_ids": chunk["beat_ids"],
                "route": chunk["route"],
                "model_type": model_type,
                "references": chunk["references"],
                "creates_edit_cut": False,
                **({
                    "prompt_id": chunk["prompt_id"],
                    "character_ids": chunk["character_ids"],
                    "forbidden_state_tags": chunk["forbidden_state_tags"],
                } if plan.get("schema_version") == 2 else {}),
            })
        shots.append({
            "shot_id": shot["shot_id"],
            "take_mode": shot["take_mode"],
            "duration_intent": shot["duration_intent"],
            "camera": shot["camera"],
            "entry_state": shot["entry_state"],
            "beats": shot["beats"],
            "exit_state": shot["exit_state"],
            "keyframes": shot["keyframes"],
            "chunks": chunks,
            "transition_to_next": shot["transition_to_next"],
        })
    compiled = {
        "schema_version": plan["schema_version"],
        "source_plan_id": plan["plan_id"],
        "storyboard_id": plan["storyboard_id"],
        "principle": "renderer chunks preserve editorial shot identity and do not imply edit cuts",
        "shots": shots,
        "warnings": warnings,
    }
    if plan.get("schema_version") == 2:
        compiled["character_contracts"] = plan["character_contracts"]
        compiled["reference_policy"] = plan["reference_policy"]
    return compiled


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "compile-h3"):
        command = subparsers.add_parser(name)
        command.add_argument("--plan", type=Path, required=True)
        command.add_argument("--schema", type=Path)
        command.add_argument("--json", action="store_true")
        if name == "compile-h3":
            command.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    plan = load_json(args.plan.resolve())
    schema_path = args.schema.resolve() if args.schema else schema_path_for(plan)
    schema = load_json(schema_path)
    result = validate_plan(plan, schema)
    if not result["ok"]:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    if args.command == "validate":
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else "shot production plan: valid")
        return 0
    compiled = compile_h3(plan)
    atomic_json(args.out.resolve(), compiled)
    print(json.dumps({"ok": True, "output": str(args.out.resolve()), "shots": len(compiled["shots"])}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
