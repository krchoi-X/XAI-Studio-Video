from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from tools.video_intent_contract import check, render_runtime_prompt


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def artifacts(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    storyboard = tmp_path / "storyboard.md"
    storyboard.write_text("Approved storyboard revision 3\n", encoding="utf-8")
    contract = {
        "schema_version": 2,
        "contract_id": "intent_S07_v1",
        "status": "approved",
        "source": {
            "storyboard_id": "sb_reika_departure",
            "revision": 3,
            "sha256": hashlib.sha256(storyboard.read_bytes()).hexdigest(),
        },
        "context": {
            "user_goal": "Preserve a quiet departure.",
            "viewer_should_understand": "She has decided to leave.",
            "viewer_should_feel": "Quiet finality.",
            "shot_purpose": "Hesitation then departure.",
            "rationale": {"delayed_gaze": "The final glance is the emotional punctuation."},
        },
        "locked": {
            "ordered_events": ["reach_door", "pause", "brief_final_gaze", "exit"],
            "gaze": {"before_final_moment": "away_from_lens", "final_moment": "brief_lens_contact"},
            "screen_direction": "toward_exit",
            "camera": {"movement": "static"},
            "final_state": "exited_room",
            "omitted_events": ["corridor_walk"],
            "forbidden_additions": ["object_pickup"],
            "prompt_segments": {
                "subject_definition": "One woman at the door, carrying nothing.",
                "scene_definition": "A quiet room with the exit visible.",
                "event_lines": {
                    "reach_door": "She reaches the door.",
                    "pause": "She pauses.",
                    "brief_final_gaze": "Only at the final moment, she briefly looks into the lens.",
                    "exit": "She exits the room.",
                },
                "gaze_line": "Before the final moment she looks away from the lens; lens contact occurs only at the end.",
                "direction_line": "She moves toward the exit throughout.",
                "camera_line": "Static camera; no push-in and no orbit.",
                "final_state_line": "She has exited the room.",
                "omission_line": "Do not show a corridor walk or any object pickup.",
            },
        },
        "creative_envelope": {
            "level": "L1",
            "allowed": ["lens_family", "light_softness"],
            "allowed_values": {"lens_family": ["normal"], "light_softness": ["soft", "diffused"]},
            "forbidden": ["push_in", "orbit"],
        },
        "feasibility": {"decision": "SHOW", "rationale": "One actor and one action chain."},
        "unresolved": [],
        "approval": {"approved_by": "user", "approved_at": "2026-10-03T22:00:00+09:00"},
    }
    contract_path = tmp_path / "intent-contract.json"
    write_json(contract_path, contract)
    compiler_ir = {
        "schema_version": 2,
        "source_contract_id": contract["contract_id"],
        "source_contract_sha256": hashlib.sha256(contract_path.read_bytes()).hexdigest(),
        "compiler": "h3-contract-compiler",
        "compiler_version": "test",
        "prompt_template_version": "intent-prompt-v1",
        "target_model": "minimax_h3_ref2va_pruned",
        "locked": copy.deepcopy(contract["locked"]),
        "creative_choices": {"lens_family": "normal"},
    }
    ir_path = tmp_path / "compiler-ir.json"
    write_json(ir_path, compiler_ir)
    prompt = tmp_path / "prompt.txt"
    prompt.write_text(render_runtime_prompt(contract, compiler_ir), encoding="utf-8")
    return contract_path, ir_path, storyboard, prompt


def test_matching_contract_passes(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    result = check(contract, ir, storyboard, prompt)
    assert result["status"] == "pass"
    assert result["hard_failures"] == []


def test_changed_locked_order_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(ir.read_text(encoding="utf-8"))
    value["locked"]["ordered_events"] = list(reversed(value["locked"]["ordered_events"]))
    write_json(ir, value)
    result = check(contract, ir, storyboard, prompt)
    assert {item["code"] for item in result["hard_failures"]} == {"locked_meaning_changed"}


def test_delayed_gaze_change_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(ir.read_text(encoding="utf-8"))
    value["locked"]["gaze"]["before_final_moment"] = "occasionally_toward_lens"
    write_json(ir, value)
    result = check(contract, ir, storyboard, prompt)
    assert "locked_meaning_changed" in {item["code"] for item in result["hard_failures"]}


def test_intentional_omission_restoration_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(ir.read_text(encoding="utf-8"))
    value["locked"]["omitted_events"] = []
    write_json(ir, value)
    result = check(contract, ir, storyboard, prompt)
    assert "locked_meaning_changed" in {item["code"] for item in result["hard_failures"]}


def test_screen_direction_change_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(ir.read_text(encoding="utf-8"))
    value["locked"]["screen_direction"] = "away_from_exit"
    write_json(ir, value)
    result = check(contract, ir, storyboard, prompt)
    assert "locked_meaning_changed" in {item["code"] for item in result["hard_failures"]}


def test_non_allow_list_creative_choice_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(ir.read_text(encoding="utf-8"))
    value["creative_choices"]["camera_movement"] = "push_in"
    write_json(ir, value)
    result = check(contract, ir, storyboard, prompt)
    assert "creative_choice_not_allowed" in {item["code"] for item in result["hard_failures"]}


def test_stale_contract_hash_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(ir.read_text(encoding="utf-8"))
    value["source_contract_sha256"] = "0" * 64
    write_json(ir, value)
    result = check(contract, ir, storyboard, prompt)
    assert "contract_hash_mismatch" in {item["code"] for item in result["hard_failures"]}


def test_forbidden_prompt_phrase_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    prompt.write_text("The camera performs a slow push-in while she exits.\n", encoding="utf-8")
    result = check(contract, ir, storyboard, prompt)
    assert "prompt_template_mismatch" in {item["code"] for item in result["hard_failures"]}


def test_claude_reproduction_prose_drift_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    prompt.write_text(
        "She elegantly walks to the door, occasionally glancing at the camera, picks up her bag, "
        "then walks down the corridor as the camera slowly pushes in.\n",
        encoding="utf-8",
    )
    result = check(contract, ir, storyboard, prompt)
    assert "prompt_template_mismatch" in {item["code"] for item in result["hard_failures"]}


def test_negated_camera_constraints_in_template_pass(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    result = check(contract, ir, storyboard, prompt)
    assert result["status"] == "pass"


def test_claude_reproduction_unapproved_creative_value_fails(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(ir.read_text(encoding="utf-8"))
    value["creative_choices"]["lens_family"] = "85mm with a slow dolly toward her face"
    write_json(ir, value)
    prompt.write_text(render_runtime_prompt(json.loads(contract.read_text(encoding="utf-8")), value), encoding="utf-8")
    result = check(contract, ir, storyboard, prompt)
    assert "creative_choice_value_not_allowed" in {item["code"] for item in result["hard_failures"]}


def test_approved_contract_rejects_redirect_level_and_removed_feasibility_term(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    value = json.loads(contract.read_text(encoding="utf-8"))
    value["creative_envelope"]["level"] = "L3"
    value["feasibility"]["decision"] = "HIDE_TRANSITION"
    write_json(contract, value)
    result = check(contract, ir, storyboard, prompt)
    assert {item["code"] for item in result["hard_failures"]} == {"contract_schema"}


def test_event_prompt_lines_must_cover_ordered_events_exactly(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    contract_value = json.loads(contract.read_text(encoding="utf-8"))
    contract_value["locked"]["prompt_segments"]["event_lines"].pop("pause")
    write_json(contract, contract_value)
    ir_value = json.loads(ir.read_text(encoding="utf-8"))
    ir_value["source_contract_sha256"] = hashlib.sha256(contract.read_bytes()).hexdigest()
    ir_value["locked"] = copy.deepcopy(contract_value["locked"])
    write_json(ir, ir_value)
    prompt.write_text("incomplete deterministic prompt\n", encoding="utf-8")
    result = check(contract, ir, storyboard, prompt)
    assert "event_prompt_coverage_mismatch" in {item["code"] for item in result["hard_failures"]}


def test_legacy_v1_contract_remains_readable(tmp_path: Path) -> None:
    contract, ir, storyboard, prompt = artifacts(tmp_path)
    contract_value = json.loads(contract.read_text(encoding="utf-8"))
    contract_value["schema_version"] = 1
    contract_value["locked"].pop("prompt_segments")
    contract_value["creative_envelope"].pop("allowed_values")
    write_json(contract, contract_value)
    ir_value = json.loads(ir.read_text(encoding="utf-8"))
    ir_value["schema_version"] = 1
    ir_value.pop("prompt_template_version")
    ir_value["locked"] = copy.deepcopy(contract_value["locked"])
    ir_value["source_contract_sha256"] = hashlib.sha256(contract.read_bytes()).hexdigest()
    write_json(ir, ir_value)
    prompt.write_text("Static camera. She reaches the door, pauses, looks briefly at the end, and exits.\n", encoding="utf-8")
    result = check(contract, ir, storyboard, prompt)
    assert result["status"] == "pass"
