from __future__ import annotations

import json
from pathlib import Path

from tools.storyboard_preflight import extract_source, validate_plan
from tools.storyboard_revision import sha256


SOURCE = """# Test

#### S01
- **예상 길이**: 10초
- **시간순 행동**:
  1. 남자가 방에 들어온다.
  2. 남자가 의자에 앉는다.
- **대사 및 소리**: 없음.
- **반드시 유지할 요소**: 의자, 닫힌 문
- **보이면 안 되는 요소**: 다른 사람

#### S02
- **예상 길이**: 10초
- **시간순 행동**:
  1. 사진에는 복도에서 본 방이 보인다.
  2. 여자가 오른쪽으로 사라진다.
- **대사 및 소리**: 여자 목소리 "여기 있어요."
- **반드시 유지할 요소**: 사진
- **보이면 안 되는 요소**: 자막
"""


def make_plan(tmp_path: Path) -> tuple[Path, dict]:
    source = tmp_path / "scenarios" / "TEST-001.md"
    source.parent.mkdir()
    source.write_text(SOURCE, encoding="utf-8")
    storyboard = tmp_path / "storyboards" / "TEST-001" / "storyboard-r001.md"
    storyboard.parent.mkdir(parents=True)
    storyboard.write_text("---\nrevision: 1\n---\n# board\n", encoding="utf-8")
    plan = {
        "schema_version": 1,
        "artifact_type": "storyboard_preflight_plan",
        "profile": "minimax-h3",
        "source": {"path": "scenarios/TEST-001.md", "sha256": sha256(source)},
        "storyboard": {"path": "storyboards/TEST-001/storyboard-r001.md", "sha256": sha256(storyboard)},
        "scope": {"mode": "full", "included_scenes": ["S01", "S02"], "intentionally_unproduced": []},
        "units": [
            {"id": "C01", "source_events": ["S01.A01"], "duration_seconds": 5, "visible_action_count": 1, "setup_id": "ROOM", "information_mode": "direct", "preview_purposes": ["setup"], "start_keyframe_id": "KF-ROOM", "blocking_anchor": None, "continuation_depth": 0, "dialogue_lines": []},
            {"id": "C02", "source_events": ["S01.A02"], "duration_seconds": 5, "visible_action_count": 1, "setup_id": "ROOM", "information_mode": "direct", "preview_purposes": ["continuity"], "start_keyframe_id": None, "blocking_anchor": None, "continuation_depth": 1, "dialogue_lines": []},
            {"id": "C03", "source_events": ["S02.A01"], "duration_seconds": 5, "visible_action_count": 1, "setup_id": "PHOTO", "information_mode": "separate_plate", "preview_purposes": ["reveal"], "start_keyframe_id": "KF-PHOTO", "blocking_anchor": None, "continuation_depth": 0, "dialogue_lines": [{"source_id": "S02.D01", "text": "여기 있어요."}]},
            {"id": "C04", "source_events": ["S02.A02"], "duration_seconds": 5, "visible_action_count": 1, "setup_id": "HALL", "information_mode": "direct", "preview_purposes": ["continuity"], "start_keyframe_id": "KF-HALL", "blocking_anchor": "doorframe", "continuation_depth": 0, "dialogue_lines": []}
        ],
        "acknowledged_constraints": ["S01.M01", "S01.M02", "S01.F01", "S02.M01", "S02.F01"],
        "unresolved": []
    }
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return plan_path, plan


def write_plan(path: Path, plan: dict) -> None:
    path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")


def test_extract_assigns_stable_event_dialogue_and_constraint_ids(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(SOURCE, encoding="utf-8")
    result = extract_source(source)

    assert [event["id"] for scene in result["scenes"] for event in scene["events"]] == ["S01.A01", "S01.A02", "S02.A01", "S02.A02"]
    assert result["scenes"][1]["dialogue"] == [{"id": "S02.D01", "text": "여기 있어요."}]
    assert [item["id"] for scene in result["scenes"] for item in scene["constraints"]] == ["S01.M01", "S01.M02", "S01.F01", "S02.M01", "S02.F01"]


def test_complete_plan_is_ready_without_llm_review(tmp_path: Path) -> None:
    plan_path, _ = make_plan(tmp_path)
    report = validate_plan(plan_path, root=tmp_path)

    assert report["ready"] is True
    assert report["source_event_count"] == 4


def test_missing_or_reordered_event_is_a_hard_failure(tmp_path: Path) -> None:
    plan_path, plan = make_plan(tmp_path)
    plan["units"][1]["source_events"] = ["S02.A01"]
    write_plan(plan_path, plan)
    report = validate_plan(plan_path, root=tmp_path)

    assert report["ready"] is False
    assert any("missing source events" in error for error in report["errors"])
    assert any("duplicate source events" in error for error in report["errors"])


def test_nested_information_and_direction_require_controls(tmp_path: Path) -> None:
    plan_path, plan = make_plan(tmp_path)
    plan["units"][2]["information_mode"] = "direct"
    plan["units"][2]["preview_purposes"] = []
    plan["units"][3]["start_keyframe_id"] = None
    plan["units"][3]["blocking_anchor"] = None
    write_plan(plan_path, plan)
    report = validate_plan(plan_path, root=tmp_path)

    assert report["ready"] is False
    assert any("nested screen/photo" in error for error in report["errors"])
    assert any("direction-sensitive" in error for error in report["errors"])


def test_unresolved_source_decision_blocks_ready_state(tmp_path: Path) -> None:
    plan_path, plan = make_plan(tmp_path)
    plan["unresolved"] = [{"source_locator": "S02", "reason": "door geometry conflicts"}]
    write_plan(plan_path, plan)
    report = validate_plan(plan_path, root=tmp_path)

    assert report["ok"] is True
    assert report["ready"] is False
    assert report["repair_items"] == ["blocked:S02: door geometry conflicts"]
