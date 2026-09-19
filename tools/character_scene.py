#!/usr/bin/env python3
"""Draft and render Stable-DNA-safe character scene variations with local LLM + WanGP."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import character_manager as cm
import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSET_LIBRARY = Path(r"D:\AI_Studio\library")
RUNNER = ROOT / "tools" / "local_wangp.py"
# Who may ask for a scene session. The value is provenance only (invoked_by / created_by / requested_by);
# it never changes prompts, seeds, or which engine runs.
ACTORS = ("codex", "hermes", "web", "grok", "claude", "user")
TEMPLATES = ROOT / "examples" / "character-lab" / "experiments" / "BATCH-002-harim-white-studio"
ENGINES = {
    "z-image": ("z-image.settings.json", "z_image"),
    "krea2": ("krea2.settings.json", "krea2_turbo_moody_krea"),
}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
KREA2_IDENTITY_EDIT_MODEL = "krea2_turbo_edit"
KREA2_IDENTITY_EDIT_CHECKPOINT = Path(r"D:\AI\WanGP\ckpts\Krea2Turbo_quanto_bf16_int8.safetensors")

HAIR_VARIATIONS = {
    "긴 생머리 센터 파트": "long straight hair with a clearly defined center part, worn fully down",
    "낮게 묶은 포니테일": "a clearly visible low ponytail tied at the nape, with the hair pulled away from the shoulders",
    "느슨한 로우 번": "a clearly visible loose low bun secured at the nape, with only a few natural face-framing strands",
    "어깨 길이 단정한 단발": "a sleek, clearly defined shoulder-length bob; no hair extending below the shoulders, no ponytail, no bun, no extensions",
    "어깨 길이 단정한 보브": "a sleek, clearly defined shoulder-length bob; no hair extending below the shoulders, no ponytail, no bun, no extensions",
    "자연스러운 긴 웨이브": "long hair worn fully down in clearly visible natural waves from mid-length to the ends; not straight, not tied up",
}
SCENE_FIELDS = {
    "hair_state", "hair", "wardrobe", "coverage", "activity", "pose", "expression",
    "props", "camera", "lens", "lighting", "location", "scene_style", "negative_constraints",
}
STRATEGY_ALIASES = {
    "identity-merge": "strict_translation",
    "strict_translation": "strict_translation",
    "enriched": "creative_expansion",
    "creative_expansion": "creative_expansion",
    "craft_expansion": "craft_expansion",
    "exact": "exact",
}
# What the request already decided, and what it usually leaves unsaid. `craft_expansion`
# asks the local model for the second list only, so enrichment cannot restage the scene.
MEANING_FIELDS = ("pose", "expression", "outfit", "location", "action")
CRAFT_FIELDS = ("camera", "lens", "lighting", "styling")
# Modes that consult the local model at all; the rest compile from templates only.
LLM_MODES = {"creative_expansion", "craft_expansion"}
# This box is an 8GB laptop 4070 that has been holding two 27B-class models at once, so a
# scene or craft answer has been measured between two and five minutes, and has timed out at
# five. The worker that calls this allows 900s; stay inside that so the inner call reports a
# timeout, naming the step that ran long.
LOCAL_MODEL_TIMEOUT_SECONDS = 840
# A delta field and the Scene Spec key that overrides it are not always the same word.
# Only the values here are accepted by `validate_scene_spec`, so a caller that locks a
# field has to send the key on the right, not the label it saw.
DELTA_TO_SCENE_FIELD = {
    "pose": "pose", "expression": "expression", "camera": "camera", "lens": "lens",
    "lighting": "lighting", "location": "location", "negative_constraints": "negative_constraints",
    "outfit": "wardrobe", "action": "activity", "styling": "scene_style",
}


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slug_text(text: str) -> str:
    words = [part.lower() for part in "".join(ch if ch.isalnum() else " " for ch in text).split() if part.isascii()]
    return "-".join(words[:5]) or "scene-variation"


def immutable_lines(immutable: dict[str, str]) -> list[str]:
    lines = []
    coverage = immutable.get("coverage", "user-specified")
    if coverage == "none":
        lines.append("Coverage is none. Do not add clothing, towels, robes, sheets, censor bars, or strategic covering objects.")
    elif coverage == "clothed":
        lines.append("The subject is clothed; preserve the user's explicitly requested wardrobe.")
    wardrobe = immutable.get("wardrobe", "").strip()
    if wardrobe:
        lines.append(f"Wardrobe is immutable: {wardrobe}")
    hair_state = immutable.get("hair_state", "").strip()
    if hair_state:
        lines.append(f"Hair state is immutable: {hair_state}")
    return lines


def build_scene_spec(request: str, immutable: dict[str, str], supplied: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build explicit mutable fields without asking an LLM to reinterpret them."""
    scene_spec = {str(key): value.strip() if isinstance(value, str) else value for key, value in (supplied or {}).items() if not isinstance(value, str) or value.strip()}
    hair_state = immutable.get("hair_state", "").strip()
    if hair_state:
        scene_spec["hair_state"] = hair_state
    elif "hair" not in scene_spec:
        matched = next((value for phrase, value in HAIR_VARIATIONS.items() if phrase in request), None)
        if matched:
            scene_spec["hair"] = matched
        # Do not treat an entire free-form prompt as a hair override merely
        # because it mentions hair or bangs. Doing so suppresses canonical
        # hair DNA and duplicates the whole prompt under Scene Spec. Callers
        # must pass an explicit scene_spec.hair for non-standard overrides.
    wardrobe = immutable.get("wardrobe", "").strip()
    if wardrobe:
        scene_spec["wardrobe"] = wardrobe
    coverage = immutable.get("coverage", "user-specified").strip()
    if coverage != "user-specified":
        scene_spec["coverage"] = coverage
    return scene_spec


def scene_spec_lines(scene_spec: dict[str, Any]) -> str:
    visible = {key: value for key, value in scene_spec.items() if key in SCENE_FIELDS}
    if not visible:
        return "- No structured field overrides."
    return "\n".join(f"- {key}: {value}" for key, value in visible.items())


def normalize_strategy(strategy: str) -> str:
    try:
        return STRATEGY_ALIASES[strategy]
    except KeyError as exc:
        raise cm.CharacterError(f"unsupported prompt strategy: {strategy}") from exc


def resolve_hair_state(character: dict[str, Any], scene_spec: dict[str, Any]) -> None:
    state = str(scene_spec.get("hair_state", "")).strip()
    if not state:
        return
    states = character.get("bounded_identity", {}).get("hair_states", {})
    if state not in states:
        available = ", ".join(sorted(states)) or "none"
        raise cm.CharacterError(f"undefined hair_state {state!r} for {character['id']}; available: {available}")
    scene_spec["hair"] = states[state]


def validate_scene_spec(character: dict[str, Any], scene_spec: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    allowed = {"schema_version", "character", "character_version", "mode"} | SCENE_FIELDS
    unknown = sorted(set(scene_spec) - allowed)
    if unknown:
        errors.append("unsupported Scene Spec fields: " + ", ".join(unknown))
    if scene_spec.get("schema_version") != 1:
        errors.append("scene_spec.schema_version must be 1")
    if scene_spec.get("character") != character["id"]:
        errors.append("scene_spec.character does not match the selected character")
    if scene_spec.get("character_version") != character["version"]:
        errors.append("scene_spec.character_version does not match current Character DNA")
    if scene_spec.get("mode") not in {"strict_translation", "creative_expansion", "craft_expansion", "exact"}:
        errors.append("scene_spec.mode is invalid")
    if scene_spec.get("coverage", "user-specified") not in {"user-specified", "none", "clothed"}:
        errors.append("scene_spec.coverage is invalid")
    for forbidden in ("face", "body", "skin"):
        if forbidden in scene_spec:
            errors.append(f"Stable DNA field cannot be overridden by Scene Spec: {forbidden}")
    if scene_spec.get("coverage") == "none" and str(scene_spec.get("wardrobe", "")).strip().lower() not in {"", "none"}:
        errors.append("coverage=none conflicts with a non-empty wardrobe")
    return {"status": "passed" if not errors else "failed", "errors": errors, "warnings": []}


def local_scene_delta(request: str, character: dict[str, Any], model: str, immutable: dict[str, str], scene_spec: dict[str, str]) -> dict[str, str]:
    dna = json.dumps(character["stable_dna"], ensure_ascii=False)
    prompt = f"""You compile a mutable scene variation for an existing adult character.
Return JSON only with exactly these string fields: title, pose, expression, outfit, camera, lens, lighting, location, action, styling, negative_constraints.
Priority 1 is the user's explicit constraints and immutable fields. Priority 2 is Stable DNA. Priority 3 is scene requirements. Priority 4 is style enrichment. Priority 5 is optional detail.
Do not contradict, soften, sanitize, or replace explicit user constraints. Do not introduce clothing, towels, robes, props, accessories, or coverage that the user did not request. Do not introduce another person. Keep anatomy coherent.
Immutable constraints: {json.dumps(immutable, ensure_ascii=False)}
Scene Spec fields are authoritative and must be copied without reinterpretation: {json.dumps(scene_spec, ensure_ascii=False)}
Character ID: {character['id']}
Stable DNA: {dna}
User scene request: {request}"""
    delta = cm.chat_json(prompt, model, temperature=0.25, timeout=LOCAL_MODEL_TIMEOUT_SECONDS)
    required = ("title", "pose", "expression", "outfit", "camera", "lens", "lighting", "location", "action", "styling", "negative_constraints")
    missing = [key for key in required if not str(delta.get(key, "")).strip()]
    if missing:
        raise cm.CharacterError("scene delta missing: " + ", ".join(missing))
    result = {key: str(delta[key]).strip() for key in required}
    if immutable.get("coverage") == "none":
        result["outfit"] = "none"
        result["negative_constraints"] = (result["negative_constraints"] + ", no clothing, no towel, no robe, no sheet, no censoring or covering object").strip(", ")
    if immutable.get("wardrobe", "").strip():
        result["outfit"] = immutable["wardrobe"].strip()
    for key in ("pose", "expression", "outfit", "camera", "lens", "lighting", "location", "action", "styling"):
        if scene_spec.get(key):
            result[key] = scene_spec[key]
    if scene_spec.get("wardrobe"):
        result["outfit"] = str(scene_spec["wardrobe"])
    if scene_spec.get("activity"):
        result["action"] = str(scene_spec["activity"])
    if scene_spec.get("scene_style"):
        result["styling"] = str(scene_spec["scene_style"])
    return result


def local_craft_delta(request: str, character: dict[str, Any], model: str, immutable: dict[str, str], scene_spec: dict[str, str]) -> dict[str, str]:
    """Ask the local model how to shoot the scene, never what the scene is.

    `local_scene_delta` asks for eleven fields and then has the Scene Spec take five of
    them back. Here the five are never requested: a model that is not asked for wardrobe
    cannot return wardrobe, so there is nothing to undo and nothing to leak through a
    field the operator left unlocked.
    """
    dna = json.dumps(character["stable_dna"], ensure_ascii=False)
    fields = ", ".join(CRAFT_FIELDS) + ", negative_constraints"
    prompt = f"""You choose how to photograph a scene that is already decided.
Return JSON only with exactly these string fields: {fields}.
The user's scene is fixed. Do not restate it, extend it, or describe what the subject wears, does, where they are, how they are posed, or what their expression is - those are decided and are not yours to set.
Describe only the photography: framing and shot scale, lens and perspective, light, and finishing style. Keep them consistent with the scene as written.
negative_constraints lists what the camera must avoid, never what the subject must avoid doing.
Immutable constraints: {json.dumps(immutable, ensure_ascii=False)}
Scene Spec fields are authoritative: {json.dumps(scene_spec, ensure_ascii=False)}
Character ID: {character['id']}
Stable DNA: {dna}
User scene request: {request}"""
    delta = cm.chat_json(prompt, model, temperature=0.25, timeout=LOCAL_MODEL_TIMEOUT_SECONDS)
    required = CRAFT_FIELDS + ("negative_constraints",)
    missing = [key for key in required if not str(delta.get(key, "")).strip()]
    if missing:
        raise cm.CharacterError("craft delta missing: " + ", ".join(missing))
    craft = {key: str(delta[key]).strip() for key in required}
    # A locked craft field is the operator's, exactly as it is for a meaning field.
    for key in CRAFT_FIELDS + ("negative_constraints",):
        locked = scene_spec.get(DELTA_TO_SCENE_FIELD[key])
        if locked:
            craft[key] = str(locked)
    return craft


def compile_craft_prompt(character: dict[str, Any], craft: dict[str, str], request: str, immutable: dict[str, str], scene_spec: dict[str, str] | None = None) -> str:
    """The strict prompt, unchanged, with photography appended.

    Built from `identity_merge_prompt` rather than beside it so the half that carries
    meaning is the same text `strict_translation` sends. That equality is asserted in the
    tests: it is what makes "craft cannot change the scene" checkable.
    """
    base = identity_merge_prompt(character, request, immutable, scene_spec)
    return base + f"""

PRIORITY 3 - PHOTOGRAPHY ONLY. These describe the shot, never the scene. If any line here implies a change to wardrobe, pose, action, expression or location, ignore that line and keep the scene above:
Camera and framing: {craft['camera']}
Lens and perspective: {craft['lens']}
Lighting: {craft['lighting']}
Finishing style: {craft['styling']}

Avoid: {craft['negative_constraints']}"""


def identity_merge_prompt(character: dict[str, Any], request: str, immutable: dict[str, str], scene_spec: dict[str, str] | None = None) -> str:
    scene_spec = scene_spec or build_scene_spec(request, immutable)
    suppressed = set(scene_spec) & set(character["stable_dna"])
    base = cm.render_base_prompt(character, suppressed)
    locks = "\n".join(f"- {line}" for line in immutable_lines(immutable)) or "- No additional immutable fields. Preserve the user's wording."
    return f"""Create one photorealistic image of exactly one adult character.

PRIORITY 1 — EXPLICIT USER SCENE. Preserve this meaning without adding or removing wardrobe, coverage, props, people, or actions:
{request}

IMMUTABLE CONSTRAINTS:
{locks}

AUTHORITATIVE SCENE SPEC. These values replace same-named Stable DNA fields rather than being appended to them:
{scene_spec_lines(scene_spec)}

PRIORITY 2 — STABLE CHARACTER IDENTITY. Apply identity only; it must not override the explicit scene:
{base}

Maintain one coherent adult subject, one anatomically continuous body, coordinated eyes sharing one target, realistic hands, and one active camera state. Do not add optional creative details that change the scene's meaning."""


def compile_prompt(character: dict[str, Any], delta: dict[str, str], request: str, immutable: dict[str, str], scene_spec: dict[str, str] | None = None) -> str:
    scene_spec = scene_spec or build_scene_spec(request, immutable)
    suppressed = set(scene_spec) & set(character["stable_dna"])
    base = cm.render_base_prompt(character, suppressed)
    locks = "\n".join(f"- {line}" for line in immutable_lines(immutable)) or "- Preserve all explicit user constraints."
    return f"""Create one photorealistic image of exactly one adult character.

PRIORITY 1 — EXPLICIT USER SCENE. Do not sanitize, soften, or contradict it:
{request}

IMMUTABLE CONSTRAINTS:
{locks}

AUTHORITATIVE SCENE SPEC. These values replace same-named Stable DNA fields rather than being appended to them:
{scene_spec_lines(scene_spec)}

PRIORITY 2 — STABLE CHARACTER IDENTITY. Identity only; never override the scene:
{base}

PRIORITY 3–5 — ENRICHED SCENE DELTA:
Pose: {delta['pose']}
Expression: {delta['expression']}
Outfit: {delta['outfit']}
Camera and framing: {delta['camera']}
Lens and perspective: {delta['lens']}
Lighting: {delta['lighting']}
Location: {delta['location']}
Action: {delta['action']}
Scene styling: {delta['styling']}

Maintain one coherent face, one anatomically continuous adult body, one active shot scale, coordinated eyes sharing one target, and realistic hands. Do not let scene variables alter Stable Character Identity or explicit user constraints.

Avoid: {delta['negative_constraints']}"""


def write_json(path: Path, data: Any) -> None:
    cm.atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_identity_reference(character: dict[str, Any], selection: str | None,
                               asset_id: str | None = None) -> dict[str, Any] | None:
    """Resolve one explicit identity reference without guessing from the filesystem."""
    selected = str(selection or "").strip()
    if not selected:
        if asset_id:
            raise cm.CharacterError("--reference-asset-id requires --identity-reference")
        return None
    basis = "explicit-path"
    source = None
    state = None
    recorded_asset_id = str(asset_id).strip() if asset_id else None
    if selected == "character-default":
        defaults = character.get("reference_defaults")
        identity = defaults.get("identity") if isinstance(defaults, dict) else None
        if not isinstance(identity, dict) or not str(identity.get("path") or "").strip():
            raise cm.CharacterError(
                f"{character['id']} has no reference_defaults.identity; an explicit image path is required"
            )
        selected = str(identity["path"]).strip()
        basis = "character-default"
        source = identity.get("source")
        state = identity.get("state")
        recorded_asset_id = recorded_asset_id or identity.get("asset_id")
    path = Path(selected).resolve()
    if not path.is_file():
        raise cm.CharacterError(f"identity reference image not found: {path}")
    if path.suffix.lower() not in IMAGE_SUFFIXES:
        raise cm.CharacterError(f"unsupported identity reference image: {path}")
    return {
        "role": "identity",
        "basis": basis,
        "asset_id": str(recorded_asset_id) if recorded_asset_id else None,
        "path": str(path),
        "sha256": sha256_file(path),
        "byte_count": path.stat().st_size,
        "source": source,
        "state": state,
    }


def apply_identity_reference(settings: dict[str, Any], reference: dict[str, Any],
                             character_id: str, request: str, actor: str) -> dict[str, Any]:
    """Compile a text-to-image Krea2 job into a hash-bound Identity Edit job."""
    result = dict(settings)
    for key in ("NAG_scale", "NAG_tau", "NAG_alpha", "type"):
        result.pop(key, None)
    result.update({
        "model_type": KREA2_IDENTITY_EDIT_MODEL,
        "base_model_type": KREA2_IDENTITY_EDIT_MODEL,
        "model_filename": str(KREA2_IDENTITY_EDIT_CHECKPOINT),
        "image_mode": 1,
        "video_prompt_type": "KI",
        "image_refs": [reference["path"]],
        "remove_background_images_ref": 0,
        "num_inference_steps": 8,
        "guidance_scale": 0,
        "activated_loras": [],
        "loras_multipliers": "",
        "_xai": {
            "kind": "reference_transformation",
            "schema_version": 2,
            "character_id": character_id,
            "reference_role": "identity",
            "reference_asset_ids": [reference["asset_id"]] if reference.get("asset_id") else [],
            "reference_sha256s": [reference["sha256"]],
            "reference_byte_counts": [reference["byte_count"]],
            "operator_request": request,
            "requested_by": actor,
            "allow_text_fallback": False,
        },
    })
    return result


def interpret(character_id: str, request: str, model: str, strategy: str = "strict_translation",
              immutable: dict[str, str] | None = None, supplied_scene_spec: dict[str, Any] | None = None) -> dict[str, Any]:
    """Compile one request and stop, so it can be read before anything is spent.

    Reserves no session, writes no file, and starts no GPU work. `prepare` does the same
    compilation and then commits to it; keeping the two in one function would mean a
    preview that reserves a session directory every time somebody looks.

    The returned `fields` are what the local model contributed, each carrying the Scene
    Spec key that overrides it. Send those keys back in `scene_spec` to make a field
    binding: the compiler already restores Scene Spec values after the model answers, so a
    locked field is not a request, it is the value that will be used.
    """
    immutable = immutable or {}
    character_path = cm.character_record_path(character_id)
    if not character_path.is_file():
        raise cm.CharacterError(f"unknown character: {character_id}")
    character = cm.load(character_path)
    operating_mode = normalize_strategy(strategy)
    scene_spec = build_scene_spec(request, immutable, supplied_scene_spec)
    scene_spec.update({"schema_version": 1, "character": character_id, "character_version": character["version"], "mode": operating_mode})
    resolve_hair_state(character, scene_spec)
    validation = validate_scene_spec(character, scene_spec)
    if validation["errors"]:
        raise cm.CharacterError("Scene Spec validation failed:\n- " + "\n- ".join(validation["errors"]))
    delta = local_scene_delta(request, character, model, immutable, scene_spec) if operating_mode == "creative_expansion" else None
    craft = local_craft_delta(request, character, model, immutable, scene_spec) if operating_mode == "craft_expansion" else None
    merged_prompt = identity_merge_prompt(character, request, immutable, scene_spec)
    if delta:
        prompt = compile_prompt(character, delta, request, immutable, scene_spec)
    elif craft:
        prompt = compile_craft_prompt(character, craft, request, immutable, scene_spec)
    else:
        prompt = merged_prompt
    if operating_mode == "exact":
        prompt = request
    produced = craft or delta or {}
    fields = [
        {
            "key": key,
            "value": value,
            "scene_field": DELTA_TO_SCENE_FIELD[key],
            # `locked` is what the operator already fixed, by a Scene Spec entry or an
            # immutable constraint; the model's wording for it was overwritten above.
            "locked": bool(scene_spec.get(DELTA_TO_SCENE_FIELD[key])),
        }
        for key, value in produced.items()
        if key in DELTA_TO_SCENE_FIELD
    ]
    return {
        "schema_version": 1,
        "character_id": character_id,
        "character_version": character["version"],
        "stable_dna_sha256": cm.stable_hash(character),
        "strategy": operating_mode,
        "request": request,
        "scene_spec": {key: value for key, value in scene_spec.items() if key in SCENE_FIELDS},
        "validation": validation,
        "suppressed_stable_dna_fields": sorted(set(scene_spec) & set(character["stable_dna"])),
        "fields": fields,
        "prompt": prompt,
        "local_llm_used": operating_mode in LLM_MODES,
        "local_model": model if operating_mode in LLM_MODES else None,
    }


def prepare(character_id: str, request: str, model: str, count: int, engines: list[str], strategy: str = "strict_translation", immutable: dict[str, str] | None = None, supplied_scene_spec: dict[str, Any] | None = None, actor: str = "codex", identity_reference: str | None = None, reference_asset_id: str | None = None) -> Path:
    character_path = cm.character_record_path(character_id)
    if not character_path.is_file():
        raise cm.CharacterError(f"unknown character: {character_id}")
    character = cm.load(character_path)
    unknown_engines = [engine for engine in engines if engine not in ENGINES]
    if unknown_engines:
        raise cm.CharacterError("unsupported engine: " + ", ".join(unknown_engines))
    reference = resolve_identity_reference(character, identity_reference, reference_asset_id)
    if reference and engines != ["krea2"]:
        raise cm.CharacterError("identity-reference generation requires --engines krea2; no text-only fallback is allowed")
    immutable = immutable or {}
    operating_mode = normalize_strategy(strategy)
    scene_spec = build_scene_spec(request, immutable, supplied_scene_spec)
    scene_spec.update({"schema_version": 1, "character": character_id, "character_version": character["version"], "mode": operating_mode})
    resolve_hair_state(character, scene_spec)
    validation = validate_scene_spec(character, scene_spec)
    if validation["errors"]:
        raise cm.CharacterError("Scene Spec validation failed:\n- " + "\n- ".join(validation["errors"]))
    suppressed_dna_fields = sorted(set(scene_spec) & set(character["stable_dna"]))
    delta = local_scene_delta(request, character, model, immutable, scene_spec) if operating_mode == "creative_expansion" else None
    craft = local_craft_delta(request, character, model, immutable, scene_spec) if operating_mode == "craft_expansion" else None
    created = datetime.now()
    title = delta["title"] if delta else request
    session_id = f"SCENE-{created.strftime('%Y%m%d-%H%M%S')}-{character_id[3:]}-{slug_text(title)}"
    root = cm.reserve_generation_session(character_id, session_id, ASSET_LIBRARY)
    asset_root = ASSET_LIBRARY / "characters" / character_id / "generations" / session_id / "outputs"
    merged_prompt = identity_merge_prompt(character, request, immutable, scene_spec)
    enriched_prompt = compile_prompt(character, delta, request, immutable, scene_spec) if delta else merged_prompt
    if craft:
        enriched_prompt = compile_craft_prompt(character, craft, request, immutable, scene_spec)
    prompt = request if operating_mode == "exact" else enriched_prompt
    if reference and operating_mode != "exact":
        prompt = (
            "IDENTITY REFERENCE LOCK — The provided identity-reference image is authoritative for this "
            "character's exact facial identity. Preserve its individual eye shape and spacing, nose, lips, "
            "jaw and facial proportions. Change only the scene variables requested below; do not substitute "
            "a generic face.\n\n" + prompt
        )
    runtime_prompt = prompt + "\n"
    prompt_hash = hashlib.sha256(runtime_prompt.encode("utf-8")).hexdigest()
    cm.atomic_write(root / "request.txt", request.rstrip() + "\n")
    cm.atomic_write(root / "prompt.raw.md", request.rstrip() + "\n")
    write_json(root / "scene_spec.json", scene_spec)
    cm.atomic_write(root / "prompt.txt", runtime_prompt)
    cm.atomic_write(root / "compiled_prompt.md", runtime_prompt)
    write_json(root / "scene-delta.json", {
        "schema_version": 1, "session_id": session_id, "character_id": character_id,
        "character_version": character["version"], "stable_dna_sha256": cm.stable_hash(character),
        "created_at": stamp(), "created_by": actor, "local_model": model if operating_mode in LLM_MODES else None,
        "source_request": request, "runtime_prompt_sha256": prompt_hash, "scene_delta": delta, "craft_delta": craft,
        "prompt_strategy": operating_mode, "immutable_constraints": immutable, "scene_spec": scene_spec,
        "suppressed_stable_dna_fields": suppressed_dna_fields,
        "reference_inputs": [reference] if reference else [],
    })
    trace = {
        "schema_version": 3, "precedence": ["explicit_user_constraints", "immutable_scene_fields", "stable_character_dna", "bounded_identity_variables", "scene_requirements", "style_enrichment", "optional_creative_detail"],
        "strategy": operating_mode, "immutable_constraints": immutable, "scene_spec": scene_spec,
        "suppressed_stable_dna_fields": suppressed_dna_fields, "raw_user_prompt": request,
        "structured_scene_spec": scene_spec,
        "after_character_dna_merge": merged_prompt,
        "after_constraint_validation": validation,
        "after_scene_enrichment": enriched_prompt if operating_mode in LLM_MODES else None,
        "after_scene_style_expansion": enriched_prompt if operating_mode in LLM_MODES else None,
        "craft_delta": craft,
        "final_prompt_sent_to_hermes": None,
        "final_prompt_sent_to_image_engine": prompt,
        "reference_inputs": [reference] if reference else [],
        "invoked_by": actor, "hermes_agent_used": actor == "hermes", "local_llm_used": operating_mode in LLM_MODES, "created_at": stamp(),
    }
    write_json(root / "prompt-trace.json", trace)
    write_json(root / "trace.json", trace)
    jobs = []
    seed_base = int(created.strftime("%m%d%H%M%S"))
    for offset, engine in enumerate(engines, 1):
        template_name, model_name = ENGINES[engine]
        settings = json.loads((TEMPLATES / template_name).read_text(encoding="utf-8"))
        settings["batch_size"] = count
        settings["repeat_generation"] = 1
        settings["seed"] = seed_base + offset
        if reference:
            settings = apply_identity_reference(settings, reference, character_id, request, actor)
            model_name = KREA2_IDENTITY_EDIT_MODEL
        write_json(root / template_name, settings)
        jobs.append({"backend": "local-wangp", "model": model_name, "count": count, "seed": settings["seed"], "resolution": settings["resolution"], "steps": settings["num_inference_steps"], "settings_file": template_name, "output_dir": f"outputs/{engine}", "status": "prepared", "reference_inputs": [reference] if reference else []})
    batch = {
        "schema_version": 1,
        "session": {"id": session_id, "character_id": character_id, "character_name": character["name"], "romanized_name": character.get("romanized_name", ""), "title": title, "status": "prepared", "created_by": actor, "visibility": "restricted", "asset_root": str(asset_root), "created_at": stamp(), "prompt_file": "prompt.txt", "scene_spec_file": "scene_spec.json", "scene_delta_file": "scene-delta.json", "prompt_trace_file": "prompt-trace.json", "prompt_strategy": operating_mode, "stable_dna_sha256": cm.stable_hash(character), "reference_inputs": [reference] if reference else []},
        "jobs": jobs,
        "review": {"surface": "personal-prompt-studio", "initial_state": "needs_review"},
    }
    # JSON is valid YAML and keeps this tool dependency-free.
    from creation_records import snapshot_inputs
    snapshot_inputs(root, character, Path(__file__))
    write_json(root / "batch.yaml", batch)
    return root


def session_requester(root: Path, batch: dict[str, Any]) -> str | None:
    """Requester recorded when the session was prepared: batch.yaml created_by, else prompt-trace invoked_by.
    Older sessions without either return None so the run record stays null (never guessed)."""
    value = (batch.get("session") or {}).get("created_by")
    if not value:
        trace_path = root / "prompt-trace.json"
        if trace_path.is_file():
            try:
                value = json.loads(trace_path.read_text(encoding="utf-8-sig")).get("invoked_by")
            except (OSError, ValueError):
                value = None
    return str(value) if value else None


def submit(root: Path, wait: bool) -> list[dict[str, Any]]:
    batch = yaml.safe_load((root / "batch.yaml").read_text(encoding="utf-8"))
    asset_root = Path(batch["session"]["asset_root"]).resolve() if batch["session"].get("asset_root") else root / "outputs"
    requester = session_requester(root, batch)
    results = []
    for job in batch["jobs"]:
        if job.get("status") == "completed":
            continue
        if job.get("status") == "running":
            raise RuntimeError(f"{Path(job['output_dir']).name} is already running")
        engine = Path(job["output_dir"]).name
        command = [sys.executable, str(RUNNER), "submit", "--runs-root", str(root / "runs"), "--prompt-file", str(root / "prompt.txt"), "--settings-file", str(root / job["settings_file"]), "--project-id", root.name, "--prompt-id", f"{root.name}-{engine}", "--output-dir", str(asset_root / engine)]
        if requester:
            command += ["--requested-by", requester]
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
        result = json.loads(completed.stdout)
        results.append(result)
        job["status"] = "running"
        job["run_dir"] = result["run_dir"]
        write_json(root / "batch.yaml", batch)
        if wait:
            deadline = time.monotonic() + 3600
            while True:
                record = json.loads((Path(result["run_dir"]) / "run.json").read_text(encoding="utf-8"))
                if record.get("status") == "failed":
                    job["status"] = "failed"
                    write_json(root / "batch.yaml", batch)
                    raise RuntimeError(f"{engine} failed: {record.get('error')}")
                if len(record.get("artifacts") or []) >= int(job["count"]):
                    job["status"] = "completed"
                    write_json(root / "batch.yaml", batch)
                    break
                if time.monotonic() >= deadline:
                    job["status"] = "timed_out"
                    write_json(root / "batch.yaml", batch)
                    raise RuntimeError(f"{engine} timed out after 60 minutes")
                time.sleep(10)
    if wait:
        batch["session"]["status"] = "completed"
        write_json(root / "batch.yaml", batch)
    return results


def main() -> int:
    # Compiled prompts carry em dashes and Korean; a Windows console defaults to cp949 and
    # would fail the whole command on the print, after the model has already been paid for.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    draft = sub.add_parser("prepare")
    draft.add_argument("--character", required=True)
    draft.add_argument("--request", required=True)
    draft.add_argument("--model", default=cm.DEFAULT_MODEL)
    draft.add_argument("--count", type=int, default=4)
    draft.add_argument("--engines", default="z-image,krea2")
    draft.add_argument("--strategy", choices=tuple(STRATEGY_ALIASES), default="strict_translation")
    draft.add_argument("--constraints-json", default="{}")
    draft.add_argument("--scene-spec-json", default="{}")
    draft.add_argument("--identity-reference", help="character-default or an explicit local image path; requires --engines krea2")
    draft.add_argument("--reference-asset-id", help="optional durable Gallery/adapter asset ID for the identity reference")
    draft.add_argument("--actor", choices=ACTORS, default="codex", help="who is asking: recorded as invoked_by / created_by and forwarded to the run record as requested_by")
    read = sub.add_parser("interpret", help="compile a request and print it without reserving a session or touching the GPU")
    read.add_argument("--character", required=True)
    read.add_argument("--request", required=True)
    read.add_argument("--model", default=cm.DEFAULT_MODEL)
    read.add_argument("--strategy", choices=tuple(STRATEGY_ALIASES), default="strict_translation")
    read.add_argument("--constraints-json", default="{}")
    read.add_argument("--scene-spec-json", default="{}")
    produce = sub.add_parser("produce")
    produce.add_argument("--character")
    produce.add_argument("--request")
    produce.add_argument("--session-dir", type=Path)
    produce.add_argument("--model", default=cm.DEFAULT_MODEL)
    produce.add_argument("--count", type=int, default=4)
    produce.add_argument("--engines", default="z-image,krea2")
    produce.add_argument("--strategy", choices=tuple(STRATEGY_ALIASES), default="strict_translation")
    produce.add_argument("--constraints-json", default="{}")
    produce.add_argument("--scene-spec-json", default="{}")
    produce.add_argument("--identity-reference", help="character-default or an explicit local image path; requires --engines krea2")
    produce.add_argument("--reference-asset-id", help="optional durable Gallery/adapter asset ID for the identity reference")
    produce.add_argument("--actor", choices=ACTORS, default="codex", help="who is asking: recorded as invoked_by / created_by and forwarded to the run record as requested_by")
    args = parser.parse_args()
    try:
        if args.command == "interpret":
            immutable = json.loads(args.constraints_json)
            scene_spec = json.loads(args.scene_spec_json)
            if not isinstance(immutable, dict) or not isinstance(scene_spec, dict):
                raise cm.CharacterError("constraints-json and scene-spec-json must be objects")
            print(json.dumps(interpret(
                args.character, args.request, args.model, args.strategy,
                {str(key): str(value) for key, value in immutable.items()},
                {str(key): value for key, value in scene_spec.items()},
            ), ensure_ascii=False, indent=2))
            return 0
        if args.command == "produce" and args.session_dir:
            if args.identity_reference or args.reference_asset_id:
                raise cm.CharacterError("reference options belong to preparation; reuse the existing session settings unchanged")
            root = cm.validate_generation_session(args.session_dir)
        else:
            if not args.character or not args.request:
                raise cm.CharacterError("--character and --request are required unless --session-dir is provided")
            if not 1 <= args.count <= 20:
                raise cm.CharacterError("count must be between 1 and 20 per engine")
            engines = [item.strip() for item in args.engines.split(",") if item.strip()]
            immutable = json.loads(args.constraints_json)
            if not isinstance(immutable, dict):
                raise cm.CharacterError("constraints-json must be an object")
            scene_spec = json.loads(args.scene_spec_json)
            if not isinstance(scene_spec, dict):
                raise cm.CharacterError("scene-spec-json must be an object")
            root = prepare(args.character, args.request, args.model, args.count, engines, args.strategy, {str(key): str(value) for key, value in immutable.items()}, {str(key): value for key, value in scene_spec.items()}, args.actor, args.identity_reference, args.reference_asset_id)
        result: dict[str, Any] = {"session_dir": str(root), "status": "prepared"}
        if args.command == "produce":
            result.update({"status": "completed", "runs": submit(root, wait=True)})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (cm.CharacterError, OSError, RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
