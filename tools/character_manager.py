#!/usr/bin/env python3
"""Repository control plane for Hermes/local-LLM character management."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / "characters"
DRAFTS = CHARACTERS / ".drafts"
INDEX = CHARACTERS / "index.json"
DEFAULT_MODEL = "meromero26b-a4b-hermes:latest"
OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"
ID_RE = re.compile(r"^ch-[a-z0-9]+(?:-[a-z0-9]+)*$")

FACE_FIELDS = ("shape", "eyes", "eyebrows", "nose", "lips", "jaw")
BODY_FIELDS = (
    "height_impression", "limb_proportions", "shoulders", "torso", "bust",
    "waist", "pelvis_hips", "lower_body", "body_hair",
)


class CharacterError(ValueError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_hash(record: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(record["stable_dna"]).encode("utf-8")).hexdigest()


def validate(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "id", "name", "status", "version", "stable_dna", "scene_defaults", "provenance"):
        if key not in record:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors
    if record["schema_version"] != 1:
        errors.append("schema_version must be 1")
    if not ID_RE.fullmatch(str(record["id"])):
        errors.append("id must match ch-lowercase-slug")
    if record["status"] not in {"draft", "candidate", "approved", "deprecated"}:
        errors.append("invalid status")
    if not isinstance(record["version"], int) or record["version"] < 1:
        errors.append("version must be a positive integer")
    dna = record.get("stable_dna", {})
    for key in ("adult_age_range", "visual_background", "face", "body", "hair", "skin", "distinctive_marks"):
        if key not in dna:
            errors.append(f"stable_dna missing: {key}")
    for key in FACE_FIELDS:
        if not str(dna.get("face", {}).get(key, "")).strip():
            errors.append(f"stable_dna.face missing: {key}")
    for key in BODY_FIELDS:
        if not str(dna.get("body", {}).get(key, "")).strip():
            errors.append(f"stable_dna.body missing: {key}")
    return errors


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, newline="\n") as handle:
        handle.write(text)
        temp = Path(handle.name)
    os.replace(temp, path)


def render_core(record: dict[str, Any]) -> str:
    dna = record["stable_dna"]
    face = dna["face"]
    body = dna["body"]
    anchors = "\n".join(f"- {x}" for x in dna.get("recognition_anchors", [])) or "- 미정"
    marks = "\n".join(f"- {x}" for x in dna.get("distinctive_marks", [])) or "- 없음/미정"
    return f"""# {record['name']} — Character Core

- ID: `{record['id']}`
- version: `{record['version']}`
- status: `{record['status']}`
- Stable DNA SHA-256: `{stable_hash(record)}`

## Stable identity

- adult age range: {dna['adult_age_range']}
- visual background: {dna['visual_background']}
- face shape: {face['shape']}
- eyes: {face['eyes']}
- eyebrows: {face['eyebrows']}
- nose: {face['nose']}
- lips: {face['lips']}
- jaw: {face['jaw']}
- hair: {dna['hair']}
- skin: {dna['skin']}
- height impression: {body['height_impression']}
- limb proportions: {body['limb_proportions']}
- shoulders: {body['shoulders']}
- torso: {body['torso']}
- bust: {body['bust']}
- waist: {body['waist']}
- pelvis / hips: {body['pelvis_hips']}
- lower body: {body['lower_body']}
- body hair: {body['body_hair']}

## Recognition anchors

{anchors}

## Distinctive marks

{marks}

## Scene defaults (mutable)

{chr(10).join(f'- {k}: {v}' for k, v in record.get('scene_defaults', {}).items())}

Scene-specific pose, expression, outfit, camera, lens, lighting, location, and action belong in a Scene Delta. They must not be added to Stable DNA.
"""


def render_base_prompt(record: dict[str, Any], exclude_fields: set[str] | None = None) -> str:
    """Render Stable DNA while omitting fields explicitly replaced by a Scene Spec."""
    exclude_fields = exclude_fields or set()
    dna = record["stable_dna"]
    f = dna["face"]
    b = dna["body"]
    hair = "" if "hair" in exclude_fields else f"Hair: {dna['hair']}. "
    return (
        f"An adult {dna['visual_background']} character named {record.get('romanized_name') or record['name']}. "
        f"Face: {f['shape']}; {f['eyes']}; {f['eyebrows']}; {f['nose']}; {f['lips']}; {f['jaw']}. "
        f"{hair}Skin: {dna['skin']}. "
        f"Body: {b['height_impression']}; {b['limb_proportions']}; shoulders {b['shoulders']}; "
        f"torso {b['torso']}; bust {b['bust']}; waist {b['waist']}; pelvis and hips {b['pelvis_hips']}; "
        f"lower body {b['lower_body']}; body hair {b['body_hair']}. "
        "Preserve one coherent adult identity and anatomically consistent body. Keep pose, expression, outfit, camera, lens, lighting, location, and action as scene variables."
    )


def rebuild_index() -> list[dict[str, Any]]:
    items = []
    if CHARACTERS.exists():
        for path in sorted(CHARACTERS.glob("ch-*/character.json")):
            record = load(path)
            items.append({
                "id": record["id"], "name": record["name"], "romanized_name": record.get("romanized_name", ""),
                "status": record["status"], "version": record["version"],
                "stable_dna_sha256": stable_hash(record), "path": path.relative_to(ROOT).as_posix(),
            })
    atomic_write(INDEX, json.dumps({"schema_version": 1, "updated_at": now(), "characters": items}, ensure_ascii=False, indent=2) + "\n")
    return items


def ollama_draft(request: str, model: str) -> dict[str, Any]:
    prompt = f"""Create one character record from the user's Korean or English request.
Return JSON only. Do not invent biography. All people must be adults.
Stable DNA contains identity only; scene_defaults may contain mutable default expression/makeup/gaze.
Required structure:
{{"schema_version":1,"id":"ch-slug","name":"...","romanized_name":"...","status":"draft","version":1,
"stable_dna":{{"adult_age_range":"...","visual_background":"...","face":{{"shape":"...","eyes":"...","eyebrows":"...","nose":"...","lips":"...","jaw":"..."}},"body":{{"height_impression":"...","limb_proportions":"...","shoulders":"...","torso":"...","bust":"...","waist":"...","pelvis_hips":"...","lower_body":"...","body_hair":"..."}},"hair":"...","skin":"...","distinctive_marks":[],"recognition_anchors":[]}},
"scene_defaults":{{"expression":"...","makeup":"...","gaze":"..."}},"approved_references":[],"prompt_sources":[],"lora_associations":[],"video_test_associations":[],"provenance":{{"created_at":"","updated_at":"","created_by":"hermes-local-llm","sources":[]}}}}
User request: {request}"""
    payload = json.dumps({"model": model, "stream": False, "format": "json", "messages": [{"role": "user", "content": prompt}], "options": {"temperature": 0.2}}).encode()
    req = urllib.request.Request(OLLAMA_CHAT, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as response:
        result = json.load(response)
    record = json.loads(result["message"]["content"])
    stamp = now()
    record.setdefault("provenance", {})
    record["provenance"].update({"created_at": stamp, "updated_at": stamp, "created_by": "hermes-local-llm"})
    if not record["provenance"].get("sources"):
        record["provenance"]["sources"] = ["natural-language-request"]
    record["status"] = "draft"
    record["schema_version"] = 1
    record["version"] = 1
    record["provenance"]["stable_dna_sha256"] = stable_hash(record)
    return record


def save_draft(record: dict[str, Any], request: str = "") -> Path:
    errors = validate(record)
    if errors:
        raise CharacterError("invalid draft:\n- " + "\n- ".join(errors))
    target = DRAFTS / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{record['id']}" / "character.json"
    atomic_write(target, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    atomic_write(target.with_name("request-summary.md"), render_core(record))
    if request:
        atomic_write(target.with_name("request.txt"), request.rstrip() + "\n")
    return target


def promote(path: Path, allow_stable_change: bool, reason: str) -> Path:
    path = path.resolve()
    if not path.is_relative_to(DRAFTS.resolve()):
        raise CharacterError(f"promotion source must be under {DRAFTS}")
    record = load(path)
    errors = validate(record)
    if errors:
        raise CharacterError("validation failed:\n- " + "\n- ".join(errors))
    target_dir = CHARACTERS / record["id"]
    target = target_dir / "character.json"
    if target.exists():
        current = load(target)
        if stable_hash(current) != stable_hash(record) and not allow_stable_change:
            raise CharacterError("Stable DNA drift blocked. Re-run with --allow-stable-change and --reason.")
        record["version"] = current["version"] + 1
        record["provenance"]["created_at"] = current["provenance"]["created_at"]
    record["status"] = "candidate" if record["status"] == "draft" else record["status"]
    record["provenance"]["updated_at"] = now()
    record["provenance"]["stable_dna_sha256"] = stable_hash(record)
    if reason:
        record["provenance"]["change_reason"] = reason
    atomic_write(target, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    atomic_write(target_dir / "00_character-core" / "character_core.md", render_core(record))
    atomic_write(target_dir / "01_prompts" / "base_appearance.txt", render_base_prompt(record) + "\n")
    rebuild_index()
    return target


def cmd_validate(character: str | None) -> int:
    paths = [CHARACTERS / character / "character.json"] if character else sorted(CHARACTERS.glob("ch-*/character.json"))
    failures = 0
    for path in paths:
        if not path.exists():
            print(f"MISSING {path}")
            failures += 1
            continue
        record = load(path)
        errors = validate(record)
        stored = record.get("provenance", {}).get("stable_dna_sha256")
        if stored and stored != stable_hash(record):
            errors.append("stored stable_dna_sha256 does not match content")
        if errors:
            failures += 1
            print(f"FAIL {record.get('id', path.parent.name)}: {'; '.join(errors)}")
        else:
            print(f"OK   {record['id']} v{record['version']} {stable_hash(record)[:12]}")
    return 1 if failures else 0


def refresh(character: str) -> Path:
    target = CHARACTERS / character / "character.json"
    if not target.is_file():
        raise CharacterError(f"unknown character: {character}")
    record = load(target)
    errors = validate(record)
    if errors:
        raise CharacterError("validation failed:\n- " + "\n- ".join(errors))
    record["provenance"]["stable_dna_sha256"] = stable_hash(record)
    atomic_write(target, json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    atomic_write(target.parent / "00_character-core" / "character_core.md", render_core(record))
    atomic_write(target.parent / "01_prompts" / "base_appearance.txt", render_base_prompt(record) + "\n")
    rebuild_index()
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("list")
    check = sub.add_parser("validate")
    check.add_argument("--character")
    draft = sub.add_parser("draft")
    draft.add_argument("--request", required=True)
    draft.add_argument("--model", default=DEFAULT_MODEL)
    promote_parser = sub.add_parser("promote")
    promote_parser.add_argument("draft", type=Path)
    promote_parser.add_argument("--allow-stable-change", action="store_true")
    promote_parser.add_argument("--reason", default="")
    refresh_parser = sub.add_parser("refresh")
    refresh_parser.add_argument("--character", required=True)
    args = parser.parse_args()

    try:
        if args.command == "doctor":
            print(f"root={ROOT}")
            print(f"characters={CHARACTERS}")
            print(f"ollama={OLLAMA_CHAT}")
            return cmd_validate(None)
        if args.command == "list":
            for item in rebuild_index():
                print(f"{item['id']}\t{item['status']}\tv{item['version']}\t{item['name']}")
            return 0
        if args.command == "validate":
            return cmd_validate(args.character)
        if args.command == "draft":
            path = save_draft(ollama_draft(args.request, args.model), args.request)
            print(path)
            return 0
        if args.command == "promote":
            print(promote(args.draft.resolve(), args.allow_stable_change, args.reason))
            return 0
        if args.command == "refresh":
            print(refresh(args.character))
            return 0
    except (CharacterError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
