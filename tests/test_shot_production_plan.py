from __future__ import annotations

import copy
import json
from pathlib import Path

from tools.shot_production_plan import compile_h3, load_json, validate_plan


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = load_json(ROOT / "schemas" / "shot-production-plan-v1.schema.json")
FIXTURE = ROOT / "tests" / "fixtures" / "shot-production-plan" / "noa-transition-fixed.json"


def fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_noa_transition_plan_is_valid() -> None:
    result = validate_plan(fixture(), SCHEMA)
    assert result == {"ok": True, "error_count": 0, "errors": []}


def test_renderer_chunks_remain_inside_one_editorial_shot() -> None:
    compiled = compile_h3(fixture())
    first = compiled["shots"][0]
    assert first["shot_id"] == "shot_noa_cute_chain"
    assert [chunk["editorial_shot_id"] for chunk in first["chunks"]] == [
        "shot_noa_cute_chain", "shot_noa_cute_chain"
    ]
    assert all(chunk["creates_edit_cut"] is False for chunk in first["chunks"])
    assert all(chunk["model_type"] == "minimax_h3_ref2va_pruned" for chunk in first["chunks"])


def test_twenty_second_take_can_use_multiple_render_chunks_without_an_edit_cut() -> None:
    plan = fixture()
    plan["shots"][0]["duration_intent"]["estimated_seconds"] = 20
    result = validate_plan(plan, SCHEMA)
    assert result == {"ok": True, "error_count": 0, "errors": []}
    assert len(plan["shots"][0]["render_chunks"]) == 2
    assert all(chunk["creates_edit_cut"] is False for chunk in plan["shots"][0]["render_chunks"])


def test_dependent_cut_rejects_unexplained_hand_reset() -> None:
    plan = fixture()
    first, second = plan["shots"]
    first["transition_to_next"] = {
        "next_shot_id": second["shot_id"],
        "relationship": "dependent",
        "mode": "hard_cut",
        "carry_fields": ["left_hand", "right_hand", "wardrobe", "environment"],
        "allowed_changes": [],
    }
    second["entry_state"]["left_hand"] = "left hand below frame"
    second["entry_state"]["right_hand"] = "right hand below frame"
    result = validate_plan(plan, SCHEMA)
    messages = [error["message"] for error in result["errors"]]
    assert result["ok"] is False
    assert any("left_hand" in message for message in messages)
    assert any("right_hand" in message for message in messages)


def test_later_ref2va_chunk_requires_previous_boundary_frame() -> None:
    plan = fixture()
    plan["shots"][0]["render_chunks"][1]["references"] = [
        {"role": "identity_master", "asset": "asset:noa-identity"}
    ]
    result = validate_plan(plan, SCHEMA)
    assert any(error["code"] == "chunk_handoff_missing" for error in result["errors"])


def test_fl2va_requires_start_and_end_frames() -> None:
    plan = fixture()
    chunk = plan["shots"][1]["render_chunks"][0]
    chunk["route"] = "h3_fl2va"
    chunk["references"] = [{"role": "start_keyframe", "asset": "asset:start"}]
    result = validate_plan(plan, SCHEMA)
    assert any(error["code"] == "h3_fl2va_end_missing" for error in result["errors"])


def test_chunk_beat_order_must_cover_the_shot_once() -> None:
    plan = fixture()
    duplicate = copy.deepcopy(plan["shots"][0]["render_chunks"][0]["beat_ids"][0])
    plan["shots"][0]["render_chunks"][1]["beat_ids"].append(duplicate)
    result = validate_plan(plan, SCHEMA)
    assert any(error["code"] == "chunk_beat_order" for error in result["errors"])
