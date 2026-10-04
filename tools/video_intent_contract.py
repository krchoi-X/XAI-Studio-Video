#!/usr/bin/env python3
"""Validate a video Intent Contract and compare it with a compiler intermediate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
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
CHECKER_VERSION = "video-intent-contract-v1.2"
GENERIC_PROMPT_TEMPLATE_VERSION = "intent-prompt-v1"
H3_REF2VA_TEMPLATE_VERSION = "h3-ref2va-v1"
H3_FL2VA_TEMPLATE_VERSION = "h3-fl2va-v1"
PROMPT_TEMPLATE_VERSION = GENERIC_PROMPT_TEMPLATE_VERSION  # backward-compatible import
SUPPORTED_PROMPT_TEMPLATES = {
    GENERIC_PROMPT_TEMPLATE_VERSION,
    H3_REF2VA_TEMPLATE_VERSION,
    H3_FL2VA_TEMPLATE_VERSION,
}
H3_PROFILE_KEYS = {
    H3_REF2VA_TEMPLATE_VERSION: "h3_ref2va_v1",
    H3_FL2VA_TEMPLATE_VERSION: "h3_fl2va_v1",
}
CREATIVE_PLACEHOLDER = re.compile(r"\{\{([a-z][a-z0-9_]*)\}\}")


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


def required_template_for_target(target_model: str) -> str | None:
    target = target_model.casefold()
    if target.startswith("minimax_h3_ref2va"):
        return H3_REF2VA_TEMPLATE_VERSION
    if target.startswith("minimax_h3_fl2va"):
        return H3_FL2VA_TEMPLATE_VERSION
    return None


def substitute_creative_choices(value: str, choices: dict[str, Any]) -> str:
    placeholders = CREATIVE_PLACEHOLDER.findall(value)
    if set(placeholders) != set(choices):
        raise ValueError("H3 profile placeholders must match compiler creative_choices exactly")
    rendered = value
    for key in placeholders:
        choice = choices[key]
        if not isinstance(choice, str) or not choice:
            raise ValueError(f"creative choice must be a non-empty string: {key}")
        rendered = rendered.replace("{{" + key + "}}", choice)
    if "{{" in rendered or "}}" in rendered:
        raise ValueError("unresolved H3 profile placeholder")
    return rendered


def render_h3_profile(profile: dict[str, Any], fields: tuple[str, ...], choices: dict[str, Any]) -> str:
    body = "\n".join(f"{field}:\n{profile[field]}" for field in fields)
    return substitute_creative_choices(body, choices) + "\n"


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
    template = compiler_ir["prompt_template_version"]
    required_template = required_template_for_target(compiler_ir["target_model"])
    if required_template is not None and template != required_template:
        raise ValueError(f"{compiler_ir['target_model']} requires {required_template}")
    if template == H3_REF2VA_TEMPLATE_VERSION:
        profile = locked.get("engine_prompt_profiles", {}).get(H3_PROFILE_KEYS[template])
        if not isinstance(profile, dict):
            raise ValueError("approved H3 Ref2VA prompt profile is missing")
        return render_h3_profile(
            profile,
            (
                "subject_definitions",
                "summary",
                "retention_analysis",
                "detailed_description",
                "overall_soundscape",
                "non_diegetic_music",
            ),
            compiler_ir.get("creative_choices", {}),
        )
    if template == H3_FL2VA_TEMPLATE_VERSION:
        profile = locked.get("engine_prompt_profiles", {}).get(H3_PROFILE_KEYS[template])
        if not isinstance(profile, dict):
            raise ValueError("approved H3 FL2VA prompt profile is missing")
        return render_h3_profile(
            profile,
            ("integrated_multimodal_description", "overall_soundscape", "non_diegetic_music"),
            compiler_ir.get("creative_choices", {}),
        )
    if template != GENERIC_PROMPT_TEMPLATE_VERSION:
        raise ValueError(f"unsupported prompt template: {template}")
    lines = [
        f"intent_template: {GENERIC_PROMPT_TEMPLATE_VERSION}",
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

    template = compiler_ir.get("prompt_template_version")
    if template not in SUPPORTED_PROMPT_TEMPLATES:
        issues.append(issue("prompt_template_version_mismatch", "prompt_template_version", "compiler names an unsupported prompt template"))
    required_template = required_template_for_target(str(compiler_ir.get("target_model", "")))
    if required_template is not None and template != required_template:
        issues.append(issue(
            "prompt_template_target_mismatch",
            "prompt_template_version",
            f"{compiler_ir.get('target_model')} requires {required_template}",
        ))

    profile_key = H3_PROFILE_KEYS.get(template)
    profile = contract.get("locked", {}).get("engine_prompt_profiles", {}).get(profile_key) if profile_key else None
    if profile_key and not isinstance(profile, dict):
        issues.append(issue("engine_prompt_profile_missing", f"locked/engine_prompt_profiles/{profile_key}", "approved engine-specific prompt profile is required"))
    if isinstance(profile, dict):
        narrative_field = "detailed_description" if template == H3_REF2VA_TEMPLATE_VERSION else "integrated_multimodal_description"
        narrative = profile.get(narrative_field, "")
        event_positions = []
        for event_id in events:
            event_line = event_lines.get(event_id, "")
            if not event_line or narrative.count(event_line) != 1:
                issues.append(issue(
                    "engine_profile_event_mismatch",
                    f"locked/engine_prompt_profiles/{profile_key}/{narrative_field}",
                    f"approved event line for {event_id} must occur exactly once in the H3 narrative section",
                ))
                continue
            event_positions.append(narrative.index(event_line))
        if len(event_positions) == len(events) and event_positions != sorted(event_positions):
            issues.append(issue(
                "engine_profile_event_order_mismatch",
                f"locked/engine_prompt_profiles/{profile_key}/{narrative_field}",
                "H3 narrative section must preserve approved event order",
            ))

    allowed_values = contract.get("creative_envelope", {}).get("allowed_values", {})
    if set(allowed_values) != allowed:
        issues.append(issue("creative_value_policy_mismatch", "creative_envelope/allowed_values", "allowed_values keys must match the allow-list exactly"))
    for key, value in compiler_ir.get("creative_choices", {}).items():
        if key in allowed and value not in allowed_values.get(key, []):
            issues.append(issue("creative_choice_value_not_allowed", f"creative_choices/{key}", f"creative value is not approved for {key}"))

    if prompt_text is not None and event_prompt_coverage_ok and not any(
        item["code"] in {"prompt_template_version_mismatch", "prompt_template_target_mismatch", "engine_prompt_profile_missing"}
        for item in issues
    ):
        try:
            expected_prompt = render_runtime_prompt(contract, compiler_ir)
        except (KeyError, TypeError, ValueError) as error:
            issues.append(issue("prompt_render_failed", "prompt", str(error)))
        else:
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
