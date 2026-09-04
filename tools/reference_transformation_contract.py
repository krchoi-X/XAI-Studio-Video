"""Pure v1/v2 normalization for reference-bound image transformations."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


OPERATION_KINDS = (
    "face_geometry", "facial_feature", "expression", "pose", "hand_gesture",
    "hair", "wardrobe", "background", "lighting", "camera", "framing",
)
STRENGTHS = ("subtle", "moderate", "exploratory")
STRATEGIES = ("auto", "identity_edit", "recompose_with_reference", "staged")
DEFAULT_PRESERVE = (
    "identity", "unmentioned_face_geometry", "hairstyle", "expression", "pose",
    "lighting", "camera", "framing", "wardrobe", "background", "accessories",
    "body_proportions",
)

CONFLICTS: dict[str, tuple[str, ...]] = {
    "face_geometry": ("unmentioned_face_geometry",),
    "facial_feature": ("unmentioned_face_geometry",),
    "expression": ("expression",),
    "pose": ("pose",),
    "hand_gesture": ("pose",),
    "hair": ("hairstyle",),
    "wardrobe": ("wardrobe", "accessories"),
    "background": ("background",),
    "lighting": ("lighting",),
    "camera": ("camera", "framing"),
    "framing": ("framing", "camera"),
}

LEGACY_KIND_MAP = {
    "face_detail": "facial_feature",
    "eyebrows": "facial_feature",
    "eyebrow_density": "facial_feature",
    "face_geometry": "face_geometry",
    "hair": "hair",
    "expression": "expression",
    "pose": "pose",
    "hand_gesture": "hand_gesture",
    "wardrobe": "wardrobe",
    "background": "background",
    "lighting": "lighting",
    "camera": "camera",
    "framing": "framing",
}

LOCAL_KINDS = {"face_geometry", "facial_feature", "expression", "hair", "lighting"}
RECOMPOSE_KINDS = {"pose", "hand_gesture", "camera", "framing"}
IDENTITY_SENSITIVE_KINDS = {"face_geometry", "facial_feature"}


class ContractError(ValueError):
    """Raised when a request cannot be represented safely."""


def _unique_strings(values: list[str] | tuple[str, ...]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if isinstance(value, str) and value.strip()))


def resolve_conflicts(operations: list[dict[str, Any]], requested_preserve: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    effective = _unique_strings(requested_preserve)
    released: list[dict[str, str]] = []
    for operation in operations:
        for lock in CONFLICTS.get(operation["kind"], ()):
            if lock in effective:
                effective.remove(lock)
                released.append({"operation_id": operation["id"], "released_lock": lock})
    return released, effective


def resolve_strategy(operations: list[dict[str, Any]], requested: str = "auto") -> tuple[str, str]:
    if requested not in STRATEGIES:
        raise ContractError(f"unsupported strategy: {requested}")
    kinds = {operation["kind"] for operation in operations}
    if requested != "auto":
        return requested, "operator_requested"
    if kinds & RECOMPOSE_KINDS and kinds & IDENTITY_SENSITIVE_KINDS:
        return "staged", "recomposition_and_identity_sensitive_operations"
    if kinds & RECOMPOSE_KINDS:
        return "recompose_with_reference", "recomposition_operation_present"
    return "identity_edit", "local_operations_only"


def _validate_operations(operations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not operations:
        raise ContractError("at least one operation is required")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in operations:
        operation_id = str(raw.get("id", "")).strip()
        kind = str(raw.get("kind", "")).strip()
        instruction = str(raw.get("instruction", "")).strip()
        strength = str(raw.get("strength", "subtle")).strip()
        if not operation_id or operation_id in seen:
            raise ContractError("operation IDs must be non-empty and unique")
        if kind not in OPERATION_KINDS:
            raise ContractError(f"unsupported operation kind: {kind}")
        if not instruction:
            raise ContractError(f"operation {operation_id} has no instruction")
        if strength not in STRENGTHS:
            raise ContractError(f"unsupported strength: {strength}")
        seen.add(operation_id)
        result.append({"id": operation_id, "kind": kind, "instruction": instruction, "strength": strength})
    return result


def normalize_request(raw: dict[str, Any]) -> dict[str, Any]:
    """Return a v2 execution plan without modifying the source dictionary."""
    source = deepcopy(raw)
    version = source.get("schema_version", 1)
    if version not in (1, 2):
        raise ContractError(f"unsupported schema version: {version}")

    if version == 1:
        changes = source.get("changes") or {}
        if not isinstance(changes, dict) or not changes:
            raise ContractError("v1 request has no changes")
        operations = []
        for index, (legacy_key, instruction) in enumerate(changes.items(), 1):
            kind = LEGACY_KIND_MAP.get(str(legacy_key))
            if kind is None:
                raise ContractError(f"ambiguous legacy change kind cannot execute: {legacy_key}")
            operations.append({
                "id": f"legacy-op-{index}", "kind": kind,
                "instruction": str(instruction).strip(), "strength": source.get("strength", "subtle"),
            })
        requested_preserve = _unique_strings(source.get("preserve") or DEFAULT_PRESERVE)
        requested_strategy = "auto"
        reference = {
            "asset_id": source.get("reference_asset_id"),
            "path": source.get("reference_path"),
            "sha256": source.get("reference_sha256"),
            "byte_count": source.get("reference_byte_count"),
        }
    else:
        operations = source.get("operations") or []
        requested_preserve = _unique_strings(source.get("requested_preserve") or DEFAULT_PRESERVE)
        requested_strategy = source.get("requested_strategy", "auto")
        reference = deepcopy(source.get("reference") or {})

    operations = _validate_operations(operations)
    resolved_conflicts, effective_preserve = resolve_conflicts(operations, requested_preserve)
    resolved_strategy, strategy_reason = resolve_strategy(operations, requested_strategy)
    return {
        "schema_version": 2,
        "kind": "reference_transformation",
        "source_schema_version": version,
        "variation_id": source.get("variation_id"),
        "character_id": source.get("character_id"),
        "reference": reference,
        "operator_request": str(source.get("operator_request", "")).strip(),
        "operations": operations,
        "requested_preserve": requested_preserve,
        "resolved_conflicts": resolved_conflicts,
        "effective_preserve": effective_preserve,
        "requested_strategy": requested_strategy,
        "resolved_strategy": resolved_strategy,
        "strategy_reason": strategy_reason,
        "engine_policy": deepcopy(source.get("engine_policy") or {
            "required_capability": "reference_image_edit",
            "preferred_engine": "krea2_identity_edit",
            "allow_text_fallback": False,
        }),
        "count": int(source.get("count", 4)),
        "effective_strength": {"mode": "prompt_only_unvalidated", "profile_version": None},
    }
