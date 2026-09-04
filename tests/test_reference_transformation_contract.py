import copy
import json
from pathlib import Path

import pytest

from tools.reference_transformation_contract import ContractError, normalize_request, resolve_strategy


FIXTURE = Path(__file__).parent / "fixtures" / "reference-transformation" / "v1-lighting-request.json"
SCHEMA = Path(__file__).parents[1] / "schemas" / "reference-transformation-request-v2.schema.json"


def test_v2_schema_and_example_share_the_contract_vocabulary():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    request = {
        "schema_version": 2, "kind": "reference_transformation", "character_id": "ch-lia",
        "reference": {"asset_id": "ast-source"},
        "operator_request": "얼굴을 조금 갸름하게 하고 손을 볼에",
        "operations": [
            {"id": "face", "kind": "face_geometry", "instruction": "얼굴을 조금 갸름하게", "strength": "subtle"},
            {"id": "hand", "kind": "hand_gesture", "instruction": "손을 볼에 대기", "strength": "moderate"},
        ],
        "requested_preserve": ["identity", "unmentioned_face_geometry", "pose", "wardrobe"],
        "requested_strategy": "auto",
        "engine_policy": {"required_capability": "reference_image_edit", "preferred_engine": "krea2_identity_edit", "allow_text_fallback": False},
        "count": 4,
    }
    assert schema["properties"]["schema_version"]["const"] == 2
    assert set(schema["required"]).issubset(request)
    allowed = set(schema["properties"]["operations"]["items"]["properties"]["kind"]["enum"])
    assert {operation["kind"] for operation in request["operations"]}.issubset(allowed)
    assert normalize_request(request)["resolved_strategy"] == "staged"


def test_v1_fixture_normalizes_without_mutation():
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    before = copy.deepcopy(raw)
    plan = normalize_request(raw)
    assert raw == before
    assert plan["source_schema_version"] == 1
    assert plan["operations"] == [{"id": "legacy-op-1", "kind": "lighting", "instruction": "강한 자연광으로 변경", "strength": "subtle"}]
    assert plan["resolved_conflicts"] == [{"operation_id": "legacy-op-1", "released_lock": "lighting"}]
    assert "identity" in plan["effective_preserve"]
    assert "lighting" not in plan["effective_preserve"]
    assert plan["resolved_strategy"] == "identity_edit"
    assert plan["engine_policy"]["allow_text_fallback"] is False


def test_face_and_hand_request_becomes_staged_and_releases_only_matching_locks():
    raw = {
        "schema_version": 2, "kind": "reference_transformation",
        "character_id": "ch-lia", "reference": {"asset_id": "ast-source"},
        "operator_request": "얼굴을 갸름하게 하고 손을 볼에",
        "operations": [
            {"id": "face", "kind": "face_geometry", "instruction": "얼굴을 조금 갸름하게", "strength": "subtle"},
            {"id": "hand", "kind": "hand_gesture", "instruction": "손을 볼에 대기", "strength": "moderate"},
        ],
        "requested_preserve": ["identity", "unmentioned_face_geometry", "pose", "wardrobe", "background"],
        "requested_strategy": "auto", "count": 4,
        "engine_policy": {"required_capability": "reference_image_edit", "preferred_engine": "krea2_identity_edit", "allow_text_fallback": False},
    }
    plan = normalize_request(raw)
    assert plan["resolved_strategy"] == "staged"
    assert plan["strategy_reason"] == "recomposition_and_identity_sensitive_operations"
    assert plan["effective_preserve"] == ["identity", "wardrobe", "background"]
    assert plan["resolved_conflicts"] == [
        {"operation_id": "face", "released_lock": "unmentioned_face_geometry"},
        {"operation_id": "hand", "released_lock": "pose"},
    ]


@pytest.mark.parametrize(("kind", "expected"), [("pose", "recompose_with_reference"), ("lighting", "identity_edit")])
def test_auto_strategy_is_deterministic(kind, expected):
    strategy, _ = resolve_strategy([{"id": "op", "kind": kind, "instruction": "x", "strength": "subtle"}])
    assert strategy == expected


def test_ambiguous_v1_change_is_inspectable_but_not_executable():
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    raw["changes"] = {"mystery": "change something"}
    with pytest.raises(ContractError, match="ambiguous legacy"):
        normalize_request(raw)


def test_duplicate_operation_ids_are_rejected():
    raw = {
        "schema_version": 2, "operator_request": "test request", "operations": [
            {"id": "same", "kind": "lighting", "instruction": "morning", "strength": "subtle"},
            {"id": "same", "kind": "hair", "instruction": "short", "strength": "subtle"},
        ],
    }
    with pytest.raises(ContractError, match="unique"):
        normalize_request(raw)
