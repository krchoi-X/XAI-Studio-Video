"""Extract source obligations and deterministically gate a storyboard preflight plan."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator

try:
    from .storyboard_revision import ROOT, sha256
except ImportError:  # Direct script execution from tools/.
    from storyboard_revision import ROOT, sha256


SCHEMA = ROOT / "schemas" / "storyboard-preflight-plan-v1.schema.json"
SCENE_HEADING = re.compile(r"^#{3,6}\s+(?P<id>[A-Za-z]+\d+)\s*$")
ACTION_LINE = re.compile(r"^\s*(?P<number>\d+)\.\s+(?P<text>.+?)\s*$")
DURATION = re.compile(r"(?P<seconds>\d+(?:\.\d+)?)\s*(?:초|s(?:ec(?:onds?)?)?)", re.IGNORECASE)
QUOTED = re.compile(r"[\"“](.+?)[\"”]")
FIELD = re.compile(r"^-\s+\*\*(?P<name>[^*]+)\*\*:\s*(?P<value>.*)$")

ACTION_FIELDS = {"시간순 행동", "ordered actions", "ordered visible actions"}
DURATION_FIELDS = {"예상 길이", "expected duration", "duration"}
DIALOGUE_FIELDS = {"대사 및 소리", "dialogue and sound", "dialogue, sound and silence"}
MUST_FIELDS = {"반드시 유지할 요소", "must preserve", "required elements"}
FORBIDDEN_FIELDS = {"보이면 안 되는 요소", "must not show", "forbidden"}
NESTED_TERMS = ("스크린 안", "화면 안", "사진에는", "사진의 촬영", "screen inside", "inside the screen", "photograph shows")
DIRECTION_TERMS = ("우측", "좌측", "왼쪽", "오른쪽", "left", "right")


@dataclass
class Scene:
    id: str
    duration_seconds: float | None = None
    events: list[dict[str, str]] = field(default_factory=list)
    dialogue: list[dict[str, str]] = field(default_factory=list)
    constraints: list[dict[str, str]] = field(default_factory=list)


def _normal(value: str) -> str:
    return value.strip().lower()


def _split_constraints(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[,、]", value) if item.strip() and item.strip().lower() not in {"none", "없음"}]


def extract_source(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    scenes: list[Scene] = []
    current: Scene | None = None
    action_mode = False
    for raw in lines:
        heading = SCENE_HEADING.match(raw.strip())
        if heading:
            current = Scene(heading.group("id"))
            scenes.append(current)
            action_mode = False
            continue
        if current is None:
            continue
        field_match = FIELD.match(raw.strip())
        if field_match:
            name = _normal(field_match.group("name"))
            value = field_match.group("value").strip()
            action_mode = name in ACTION_FIELDS
            if name in DURATION_FIELDS:
                duration = DURATION.search(value)
                if duration:
                    current.duration_seconds = float(duration.group("seconds"))
            elif name in DIALOGUE_FIELDS:
                for text in QUOTED.findall(value):
                    current.dialogue.append({"id": f"{current.id}.D{len(current.dialogue)+1:02d}", "text": text})
            elif name in MUST_FIELDS or name in FORBIDDEN_FIELDS:
                prefix = "M" if name in MUST_FIELDS else "F"
                for text in _split_constraints(value):
                    count = sum(1 for item in current.constraints if item["id"].startswith(f"{current.id}.{prefix}")) + 1
                    current.constraints.append({"id": f"{current.id}.{prefix}{count:02d}", "text": text, "kind": "must" if prefix == "M" else "forbidden"})
            continue
        if action_mode:
            action = ACTION_LINE.match(raw)
            if action:
                text = action.group("text").strip()
                current.events.append({
                    "id": f"{current.id}.A{len(current.events)+1:02d}",
                    "text": text,
                    "nested_information": any(term in text.lower() for term in NESTED_TERMS),
                    "direction_sensitive": any(term in text.lower() for term in DIRECTION_TERMS),
                })
            elif raw.strip() and not raw.startswith(" "):
                action_mode = False
    return {
        "source": str(path),
        "sha256": sha256(path),
        "scenes": [scene.__dict__ for scene in scenes if scene.events],
    }


def _resolve(root: Path, logical_path: str) -> Path:
    logical = PurePosixPath(logical_path)
    if logical.is_absolute() or ".." in logical.parts:
        raise ValueError(f"unsafe repository-relative path: {logical_path}")
    target = (root / Path(*logical.parts)).resolve()
    target.relative_to(root.resolve())
    return target


def validate_plan(plan_path: Path, *, root: Path = ROOT, schema_path: Path = SCHEMA) -> dict[str, Any]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = [f"schema:{'/'.join(map(str, item.path)) or '<root>'}: {item.message}" for item in sorted(Draft202012Validator(schema).iter_errors(plan), key=lambda item: list(item.path))]
    if errors:
        return {"ok": False, "ready": False, "errors": errors, "repair_items": errors}

    source_path = _resolve(root, plan["source"]["path"])
    storyboard_path = _resolve(root, plan["storyboard"]["path"])
    if sha256(source_path) != plan["source"]["sha256"]:
        errors.append("source hash mismatch")
    if sha256(storyboard_path) != plan["storyboard"]["sha256"]:
        errors.append("storyboard hash mismatch")
    catalog = extract_source(source_path)
    scenes = {scene["id"]: scene for scene in catalog["scenes"]}
    included = plan["scope"]["included_scenes"]
    if plan["scope"]["mode"] == "full" and included != list(scenes):
        errors.append(f"full scope must include every source scene in order: {list(scenes)}")
    unknown_scenes = [scene for scene in included if scene not in scenes]
    if unknown_scenes:
        errors.append(f"unknown included scenes: {unknown_scenes}")

    expected_events = [event for scene_id in included if scene_id in scenes for event in scenes[scene_id]["events"]]
    expected_ids = [event["id"] for event in expected_events]
    mapped_ids = [event_id for unit in plan["units"] for event_id in unit["source_events"]]
    missing = [event_id for event_id in expected_ids if event_id not in mapped_ids]
    duplicates = sorted({event_id for event_id in mapped_ids if mapped_ids.count(event_id) > 1})
    extras = [event_id for event_id in mapped_ids if event_id not in expected_ids]
    if missing:
        errors.append(f"missing source events: {missing}")
    if duplicates:
        errors.append(f"duplicate source events: {duplicates}")
    if extras:
        errors.append(f"unknown/out-of-scope source events: {extras}")
    if not missing and not duplicates and not extras and mapped_ids != expected_ids:
        errors.append("source events are not mapped in source order")

    event_lookup = {event["id"]: event for event in expected_events}
    expected_dialogue = [
        {"source_id": line["id"], "text": line["text"]}
        for scene_id in included if scene_id in scenes for line in scenes[scene_id]["dialogue"]
    ]
    actual_dialogue = [line for unit in plan["units"] for line in unit["dialogue_lines"]]
    if actual_dialogue != expected_dialogue:
        errors.append(f"dialogue must match source exactly and in order: {expected_dialogue}")

    expected_constraints = [item["id"] for scene_id in included if scene_id in scenes for item in scenes[scene_id]["constraints"]]
    if plan["acknowledged_constraints"] != expected_constraints:
        errors.append("acknowledged_constraints must list every source must/forbidden constraint exactly once and in source order")

    durations: dict[str, float] = {scene_id: 0.0 for scene_id in included}
    for unit in plan["units"]:
        unit_id = unit["id"]
        unit_events = [event_lookup[event_id] for event_id in unit["source_events"] if event_id in event_lookup]
        scene_ids = {event_id.split(".", 1)[0] for event_id in unit["source_events"]}
        if len(scene_ids) != 1:
            errors.append(f"{unit_id}: one render unit may map events from only one source scene")
        elif next(iter(scene_ids)) in durations:
            durations[next(iter(scene_ids))] += unit["duration_seconds"]
        if plan["profile"] == "minimax-h3":
            if unit["duration_seconds"] > 7.5:
                errors.append(f"{unit_id}: H3 duration exceeds 7.5 seconds")
            if unit["visible_action_count"] > 4:
                errors.append(f"{unit_id}: H3 visible_action_count exceeds 4")
            if unit["continuation_depth"] > 4:
                errors.append(f"{unit_id}: H3 continuation_depth exceeds 4; re-anchor with a clean keyframe")
        if any(event["nested_information"] for event in unit_events) and unit["information_mode"] not in {"separate_plate", "edit_composite"}:
            errors.append(f"{unit_id}: nested screen/photo information requires separate_plate or edit_composite")
        if any(event["direction_sensitive"] for event in unit_events) and (not unit.get("start_keyframe_id") or not unit.get("blocking_anchor")):
            errors.append(f"{unit_id}: direction-sensitive action requires start_keyframe_id and blocking_anchor")
        if any(event["nested_information"] for event in unit_events) and not ({"reveal", "source"} & set(unit["preview_purposes"])):
            errors.append(f"{unit_id}: nested critical information requires reveal/source preview")

    for scene_id, total in durations.items():
        expected = scenes[scene_id]["duration_seconds"]
        if expected and not (expected * 0.8 <= total <= expected * 1.2):
            errors.append(f"{scene_id}: mapped duration {total:.1f}s is outside ±20% of source {expected:.1f}s")

    unresolved = plan["unresolved"]
    ready = not errors and not unresolved
    repair_items = list(errors)
    repair_items.extend(f"blocked:{item['source_locator']}: {item['reason']}" for item in unresolved)
    return {
        "ok": not errors,
        "ready": ready,
        "source_event_count": len(expected_ids),
        "mapped_event_count": len(mapped_ids),
        "unresolved": unresolved,
        "errors": errors,
        "repair_items": repair_items,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    extract = subparsers.add_parser("extract", help="extract deterministic source event/constraint IDs")
    extract.add_argument("--source", required=True, type=Path)
    extract.add_argument("--out", type=Path)
    validate = subparsers.add_parser("validate", help="validate a storyboard preflight sidecar")
    validate.add_argument("--plan", required=True, type=Path)
    validate.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.command == "extract":
        result = extract_source(args.source.resolve())
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.out:
            args.out.write_text(output + "\n", encoding="utf-8")
        else:
            print(output)
        return 0
    report = validate_plan(args.plan.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else "\n".join(report["repair_items"]) or "READY")
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
