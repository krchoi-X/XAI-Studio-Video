#!/usr/bin/env python3
"""Validate Creative Treatment and production role-attribution sidecars."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
TREATMENT_SCHEMA = ROOT / "schemas" / "creative-treatment-v1.schema.json"
ROLES_SCHEMA = ROOT / "schemas" / "production-role-attribution-v1.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate(value: dict[str, Any], schema_path: Path) -> list[dict[str, str]]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        {
            "path": "/".join(map(str, error.path)) or "<root>",
            "message": error.message,
        }
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path))
    ]


def validate_treatment(value: dict[str, Any]) -> list[dict[str, str]]:
    return validate(value, TREATMENT_SCHEMA)


def validate_roles(value: dict[str, Any]) -> list[dict[str, str]]:
    return validate(value, ROLES_SCHEMA)


def approved_artifact(
    roles: dict[str, Any],
    kind: str,
    path: Path,
    *,
    base_dir: Path | None = None,
) -> bool:
    expected_path = str(path.resolve()).casefold()
    expected_hash = sha256_file(path)
    artifacts = roles.get("production_approval", {}).get("approved_artifacts", [])

    def resolve_recorded_path(value: str) -> Path:
        recorded = Path(value)
        if not recorded.is_absolute() and base_dir is not None:
            recorded = base_dir / recorded
        return recorded.resolve()

    return any(
        item.get("kind") == kind
        and str(resolve_recorded_path(item.get("path", ""))).casefold() == expected_path
        and item.get("sha256") == expected_hash
        for item in artifacts
        if isinstance(item, dict)
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--treatment", type=Path)
    parser.add_argument("--roles", type=Path)
    args = parser.parse_args(argv)
    if not args.treatment and not args.roles:
        parser.error("provide --treatment and/or --roles")
    result: dict[str, Any] = {"ok": True, "documents": {}}
    for name, path, schema in (
        ("treatment", args.treatment, TREATMENT_SCHEMA),
        ("roles", args.roles, ROLES_SCHEMA),
    ):
        if not path:
            continue
        resolved = path.resolve()
        try:
            value = load_json(resolved)
            issues = validate(value, schema)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            issues = [{"path": "<root>", "message": str(error)}]
        result["documents"][name] = {
            "path": str(resolved),
            "sha256": sha256_file(resolved) if resolved.is_file() else None,
            "issues": issues,
        }
        result["ok"] = result["ok"] and not issues
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
