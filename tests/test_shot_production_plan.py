from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
from PIL import Image

from tools.shot_production_plan import (
    compile_h3,
    load_json,
    schema_path_for,
    validate_plan,
    validate_submission_contract,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = load_json(ROOT / "schemas" / "shot-production-plan-v1.schema.json")
FIXTURE = ROOT / "tests" / "fixtures" / "shot-production-plan" / "noa-transition-fixed.json"
V2_SCHEMA = load_json(ROOT / "schemas" / "shot-production-plan-v2.schema.json")
V2_FIXTURE = ROOT / "tests" / "fixtures" / "shot-production-plan" / "lia-pack-contract-v2.json"


def fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def fixture_v2() -> dict:
    return json.loads(V2_FIXTURE.read_text(encoding="utf-8"))


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


def test_v2_plan_freezes_character_and_reference_contracts() -> None:
    plan = fixture_v2()
    result = validate_plan(plan, V2_SCHEMA)
    assert result == {"ok": True, "error_count": 0, "errors": []}
    assert schema_path_for(plan).name == "shot-production-plan-v2.schema.json"
    compiled = compile_h3(plan)
    assert compiled["schema_version"] == 2
    assert compiled["character_contracts"] == plan["character_contracts"]
    assert compiled["shots"][0]["chunks"][1]["prompt_id"] == "pack-B"


def test_v2_rejects_missing_cast_identity_master() -> None:
    plan = fixture_v2()
    plan["shots"][0]["render_chunks"][0]["references"] = [
        reference for reference in plan["shots"][0]["render_chunks"][0]["references"]
        if reference["role"] != "identity_master"
    ]
    result = validate_plan(plan, V2_SCHEMA)
    assert any(error["code"] == "h3_ref2va_character_identity_missing" for error in result["errors"])


def test_v2_rejects_unverified_laterality_and_padded_body_reference() -> None:
    plan = fixture_v2()
    reference = plan["shots"][0]["render_chunks"][0]["references"][1]
    reference["anatomical_laterality"] = "unknown"
    reference["verified_by"] = None
    reference["composition"] = "padded_landscape"
    result = validate_plan(plan, V2_SCHEMA)
    codes = {error["code"] for error in result["errors"]}
    assert "unverified_reference_laterality" in codes
    assert "non_native_landscape_reference" in codes


def test_v2_rejects_reference_state_forbidden_in_chunk() -> None:
    plan = fixture_v2()
    plan["shots"][0]["render_chunks"][1]["references"][1]["state_tags"].append("sitting")
    result = validate_plan(plan, V2_SCHEMA)
    assert any(error["code"] == "forbidden_reference_state" for error in result["errors"])


def test_v2_requires_unique_prompt_ids() -> None:
    plan = fixture_v2()
    plan["shots"][0]["render_chunks"][1]["prompt_id"] = "pack-A"
    result = validate_plan(plan, V2_SCHEMA)
    assert any(error["code"] == "duplicate_prompt_id" for error in result["errors"])


def test_v2_dependent_shot_requires_a_boundary_reference() -> None:
    plan = fixture_v2()
    first = plan["shots"][0]
    second = copy.deepcopy(first)
    second["shot_id"] = "shot_lia_follow"
    beat_mapping = {"beat_stand": "beat_follow_stand", "beat_walk": "beat_follow_walk"}
    keyframe_mapping = {"kf_stand": "kf_follow_stand", "kf_walk": "kf_follow_walk"}
    for beat in second["beats"]:
        beat["beat_id"] = beat_mapping[beat["beat_id"]]
        beat["keyframe_ids"] = [keyframe_mapping[value] for value in beat["keyframe_ids"]]
    for keyframe in second["keyframes"]:
        keyframe["keyframe_id"] = keyframe_mapping[keyframe["keyframe_id"]]
        keyframe["beat_id"] = beat_mapping[keyframe["beat_id"]]
    for index, chunk in enumerate(second["render_chunks"], start=1):
        chunk["chunk_id"] = f"chunk_lia_follow_{index}"
        chunk["prompt_id"] = f"pack-follow-{index}"
        chunk["beat_ids"] = [beat_mapping[value] for value in chunk["beat_ids"]]
    first["transition_to_next"] = {
        "next_shot_id": second["shot_id"],
        "relationship": "dependent",
        "mode": "match_on_action",
        "carry_fields": ["wardrobe", "environment"],
        "allowed_changes": [],
    }
    plan["shots"].append(second)
    result = validate_plan(plan, V2_SCHEMA)
    assert any(error["code"] == "shot_handoff_missing" for error in result["errors"])


def test_submission_contract_hard_gates_character_prompt_and_pack_references(tmp_path: Path) -> None:
    plan = fixture_v2()
    character_record = tmp_path / "character.json"
    character_record.write_text("{}", encoding="utf-8")
    identity = tmp_path / "identity.png"
    body = tmp_path / "body.png"
    Image.new("RGB", (256, 512), "white").save(identity)
    Image.new("RGB", (640, 360), "white").save(body)

    contract = plan["character_contracts"][0]
    contract["record_path"] = str(character_record)
    refs = plan["shots"][0]["render_chunks"][0]["references"]
    for reference, path in zip(refs, (identity, body)):
        reference["asset"] = str(path)
        reference["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    current = {
        "ch-lia": {
            "record_path": str(character_record),
            "character_version": contract["character_version"],
            "stable_dna_sha256": contract["stable_dna_sha256"],
        }
    }
    settings = {
        "model_type": "minimax_h3_ref2va_pruned",
        "image_refs": [str(identity), str(body)],
    }
    prompt = "Lia has soft full bangs and three thin red-and-blue bracelets on her RIGHT wrist."
    snapshot = validate_submission_contract(plan, "pack-A", prompt, settings, current)
    assert snapshot["plan_schema_version"] == 2
    assert snapshot["references"][1]["verified_dimensions"] == [640, 360]

    with pytest.raises(ValueError, match="mandatory prompt anchors are missing"):
        validate_submission_contract(plan, "pack-A", "Lia walks on the beach.", settings, current)
    with pytest.raises(ValueError, match="do not match the approved pack references"):
        validate_submission_contract(
            plan,
            "pack-A",
            prompt,
            {**settings, "image_refs": [str(identity), str(body), str(identity)]},
            current,
        )
