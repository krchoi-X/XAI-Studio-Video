#!/usr/bin/env python3
"""Validate editorial-shot plans and compile an H3 execution summary."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "shot-production-plan-v1.schema.json"
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


def semantic_errors(plan: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    shots = plan.get("shots", [])
    shot_ids = [shot.get("shot_id") for shot in shots]
    if len(shot_ids) != len(set(shot_ids)):
        issues.append(_issue("duplicate_shot_id", "shots", "shot_id values must be unique"))

    by_id = {shot.get("shot_id"): shot for shot in shots}
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
    return issues


def validate_plan(plan: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors = schema_errors(plan, schema)
    if not errors:
        errors.extend(semantic_errors(plan))
    return {"ok": not errors, "error_count": len(errors), "errors": errors}


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
    return {
        "schema_version": 1,
        "source_plan_id": plan["plan_id"],
        "storyboard_id": plan["storyboard_id"],
        "principle": "renderer chunks preserve editorial shot identity and do not imply edit cuts",
        "shots": shots,
        "warnings": warnings,
    }


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
        command.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
        command.add_argument("--json", action="store_true")
        if name == "compile-h3":
            command.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    plan = load_json(args.plan.resolve())
    schema = load_json(args.schema.resolve())
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
