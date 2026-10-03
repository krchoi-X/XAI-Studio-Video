#!/usr/bin/env python3
"""Validate a video Intent Contract and compare it with a compiler intermediate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_SCHEMAS = {
    1: ROOT / "schemas" / "video-intent-contract-v1.schema.json",
    2: ROOT / "schemas" / "video-intent-contract-v2.schema.json",
}
IR_SCHEMAS = {
    1: ROOT / "schemas" / "video-compiler-ir-v1.schema.json",
    2: ROOT / "schemas" / "video-compiler-ir-v2.schema.json",
}
CHECKER_VERSION = "video-intent-contract-v1.1"
PROMPT_TEMPLATE_VERSION = "intent-prompt-v1"


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


def schema_issues(value: dict[str, Any], schema_path: Path, prefix: str) -> list[dict[str, str]]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues = []
    for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
        path = "/".join(map(str, error.path)) or "<root>"
        issues.append({"code": f"{prefix}_schema", "path": path, "message": error.message})
    return issues


def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def normalized_phrase(value: str) -> str:
    return " ".join(value.casefold().replace("_", " ").replace("-", " ").split())


def render_runtime_prompt(contract: dict[str, Any], compiler_ir: dict[str, Any]) -> str:
    """Render the complete runtime prompt without generative rewriting.

    Human-approved prose lives in ``locked.prompt_segments``. The compiler may
    select only pre-approved creative values, so no free-form prose remains for
    an LLM to reinterpret after contract approval.
    """
    if contract.get("schema_version") != 2 or compiler_ir.get("schema_version") != 2:
        raise ValueError("deterministic prompt rendering requires contract and compiler IR schema_version 2")
    locked = contract["locked"]
    segments = locked["prompt_segments"]
    lines = [
        f"intent_template: {PROMPT_TEMPLATE_VERSION}",
        f"target_model: {compiler_ir['target_model']}",
        "subject_definitions:",
        segments["subject_definition"],
        "scene_description:",
        segments["scene_definition"],
        "ordered_action:",
    ]
    for event_id in locked["ordered_events"]:
        lines.append(f"- {event_id}: {segments['event_lines'][event_id]}")
    lines.extend([
        "gaze_and_direction:",
        segments["gaze_line"],
        segments["direction_line"],
        "camera_instructions:",
        segments["camera_line"],
        "final_state:",
        segments["final_state_line"],
        "omissions_and_constraints:",
        segments["omission_line"],
        "approved_creative_choices:",
    ])
    for key in sorted(compiler_ir.get("creative_choices", {})):
        lines.append(f"- {key}: {compiler_ir['creative_choices'][key]}")
    return "\n".join(lines) + "\n"


def compare(
    contract: dict[str, Any],
    contract_sha256: str,
    compiler_ir: dict[str, Any],
    *,
    storyboard_sha256: str | None = None,
    prompt_text: str | None = None,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if contract.get("status") != "approved":
        issues.append(issue("contract_not_approved", "status", "storyboard-derived compilation requires an approved contract"))
    if contract.get("unresolved"):
        issues.append(issue("contract_unresolved", "unresolved", "approved execution contract must not contain unresolved decisions"))
    if storyboard_sha256 is not None and storyboard_sha256 != contract.get("source", {}).get("sha256"):
        issues.append(issue("storyboard_hash_mismatch", "source/sha256", "storyboard file hash does not match the approved contract"))
    if compiler_ir.get("source_contract_id") != contract.get("contract_id"):
        issues.append(issue("contract_id_mismatch", "source_contract_id", "compiler intermediate names a different contract"))
    if compiler_ir.get("source_contract_sha256") != contract_sha256:
        issues.append(issue("contract_hash_mismatch", "source_contract_sha256", "compiler intermediate contract hash is stale or incorrect"))
    if compiler_ir.get("locked") != contract.get("locked"):
        issues.append(issue("locked_meaning_changed", "locked", "compiler intermediate must preserve the locked object exactly"))

    allowed = set(contract.get("creative_envelope", {}).get("allowed", []))
    choices = set(compiler_ir.get("creative_choices", {}))
    extra = sorted(choices - allowed)
    if extra:
        issues.append(issue("creative_choice_not_allowed", "creative_choices", f"creative keys are outside the allow-list: {extra}"))

    if contract.get("schema_version") == 1:
        if prompt_text is not None:
            prompt = normalized_phrase(prompt_text)
            forbidden = list(contract.get("creative_envelope", {}).get("forbidden", []))
            forbidden += list(contract.get("locked", {}).get("forbidden_additions", []))
            found = sorted({value for value in forbidden if normalized_phrase(value) in prompt})
            if found:
                issues.append(issue("forbidden_phrase_in_prompt", "prompt", f"runtime prompt contains forbidden contract terms: {found}"))
        return issues

    segments = contract.get("locked", {}).get("prompt_segments", {})
    event_lines = segments.get("event_lines", {}) if isinstance(segments, dict) else {}
    events = contract.get("locked", {}).get("ordered_events", [])
    event_prompt_coverage_ok = set(event_lines) == set(events)
    if not event_prompt_coverage_ok:
        issues.append(issue("event_prompt_coverage_mismatch", "locked/prompt_segments/event_lines", "event prompt lines must match ordered_events exactly"))

    if compiler_ir.get("prompt_template_version") != PROMPT_TEMPLATE_VERSION:
        issues.append(issue("prompt_template_version_mismatch", "prompt_template_version", f"compiler must use {PROMPT_TEMPLATE_VERSION}"))

    allowed_values = contract.get("creative_envelope", {}).get("allowed_values", {})
    if set(allowed_values) != allowed:
        issues.append(issue("creative_value_policy_mismatch", "creative_envelope/allowed_values", "allowed_values keys must match the allow-list exactly"))
    for key, value in compiler_ir.get("creative_choices", {}).items():
        if key in allowed and value not in allowed_values.get(key, []):
            issues.append(issue("creative_choice_value_not_allowed", f"creative_choices/{key}", f"creative value is not approved for {key}"))

    if prompt_text is not None and event_prompt_coverage_ok:
        expected_prompt = render_runtime_prompt(contract, compiler_ir)
        normalized_prompt = prompt_text.replace("\r\n", "\n")
        if normalized_prompt != expected_prompt:
            issues.append(issue("prompt_template_mismatch", "prompt", "runtime prompt must equal the deterministic rendering of the approved contract and creative choices"))
    return issues


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        handle.write(value)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def check(contract_path: Path, ir_path: Path, storyboard_path: Path | None, prompt_path: Path | None) -> dict[str, Any]:
    contract = load_json(contract_path)
    compiler_ir = load_json(ir_path)
    contract_version = contract.get("schema_version")
    ir_version = compiler_ir.get("schema_version")
    failures: list[dict[str, str]] = []
    if contract_version not in CONTRACT_SCHEMAS:
        failures.append(issue("unsupported_contract_version", "schema_version", "unsupported Intent Contract schema version"))
    else:
        failures.extend(schema_issues(contract, CONTRACT_SCHEMAS[contract_version], "contract"))
    if ir_version not in IR_SCHEMAS:
        failures.append(issue("unsupported_compiler_ir_version", "schema_version", "unsupported compiler IR schema version"))
    else:
        failures.extend(schema_issues(compiler_ir, IR_SCHEMAS[ir_version], "compiler_ir"))
    if contract_version != ir_version:
        failures.append(issue("schema_version_mismatch", "schema_version", "contract and compiler IR schema versions must match"))
    contract_hash = sha256_file(contract_path)
    storyboard_hash = sha256_file(storyboard_path) if storyboard_path else None
    prompt_text = prompt_path.read_text(encoding="utf-8-sig") if prompt_path else None
    if not failures:
        failures.extend(compare(
            contract,
            contract_hash,
            compiler_ir,
            storyboard_sha256=storyboard_hash,
            prompt_text=prompt_text,
        ))
    return {
        "schema_version": 1,
        "checker_version": CHECKER_VERSION,
        "checked_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "contract_id": contract.get("contract_id"),
        "contract_sha256": contract_hash,
        "storyboard_sha256": storyboard_hash,
        "compiler_intermediate_sha256": sha256_file(ir_path),
        "runtime_prompt_sha256": sha256_file(prompt_path) if prompt_path else None,
        "status": "pass" if not failures else "fail",
        "hard_failures": failures,
        "warnings": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--compiler-ir", type=Path, required=True)
    parser.add_argument("--storyboard", type=Path)
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument("--prompt", type=Path, help="check an existing deterministic runtime prompt")
    prompt_group.add_argument("--render-prompt", type=Path, help="write the deterministic runtime prompt, then check it")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    prompt_path = args.prompt.resolve() if args.prompt else None
    if args.render_prompt:
        prompt_path = args.render_prompt.resolve()
        try:
            atomic_text(prompt_path, render_runtime_prompt(load_json(args.contract.resolve()), load_json(args.compiler_ir.resolve())))
        except (KeyError, TypeError, ValueError) as error:
            parser.error(f"cannot render prompt from invalid contract/compiler IR: {error}")
    result = check(
        args.contract.resolve(),
        args.compiler_ir.resolve(),
        args.storyboard.resolve() if args.storyboard else None,
        prompt_path,
    )
    if args.out:
        atomic_json(args.out.resolve(), result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
