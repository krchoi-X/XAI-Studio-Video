from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from tools.video_intent_contract import check


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def artifacts(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    storyboard = tmp_path / "storyboard.md"
    storyboard.write_text("Approved storyboard revision 3\n", encoding="utf-8")
    contract = {
        "schema_version": 1,
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
        },
        "creative_envelope": {
            "level": "L1",
            "allowed": ["lens_family", "light_softness"],
            "forbidden": ["push_in", "orbit"],
        },
        "feasibility": {"decision": "SHOW", "rationale": "One actor and one action chain."},
        "unresolved": [],
        "approval": {"approved_by": "user", "approved_at": "2026-10-03T22:00:00+09:00"},
    }
    contract_path = tmp_path / "intent-contract.json"
    write_json(contract_path, contract)
    compiler_ir = {
        "schema_version": 1,
        "source_contract_id": contract["contract_id"],
        "source_contract_sha256": hashlib.sha256(contract_path.read_bytes()).hexdigest(),
        "compiler": "h3-contract-compiler",
        "compiler_version": "test",
        "target_model": "minimax_h3_ref2va_pruned",
        "locked": copy.deepcopy(contract["locked"]),
        "creative_choices": {"lens_family": "normal"},
    }
    ir_path = tmp_path / "compiler-ir.json"
    write_json(ir_path, compiler_ir)
    prompt = tmp_path / "prompt.txt"
    prompt.write_text("Static camera. She reaches the door, pauses, looks briefly at the end, and exits.\n", encoding="utf-8")
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
    assert "forbidden_phrase_in_prompt" in {item["code"] for item in result["hard_failures"]}
