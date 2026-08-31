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
TEMPLATES = ROOT / "examples" / "character-lab" / "experiments" / "BATCH-002-harim-white-studio"
ENGINES = {
    "z-image": ("z-image.settings.json", "z_image"),
    "krea2": ("krea2.settings.json", "krea2_turbo_moody_krea"),
}

HAIR_VARIATIONS = {
    "긴 생머리 센터 파트": "long straight hair with a clearly defined center part, worn fully down",
    "낮게 묶은 포니테일": "a clearly visible low ponytail tied at the nape, with the hair pulled away from the shoulders",
    "느슨한 로우 번": "a clearly visible loose low bun secured at the nape, with only a few natural face-framing strands",
    "어깨 길이 단정한 단발": "a sleek, clearly defined shoulder-length bob; no hair extending below the shoulders, no ponytail, no bun, no extensions",
    "어깨 길이 단정한 보브": "a sleek, clearly defined shoulder-length bob; no hair extending below the shoulders, no ponytail, no bun, no extensions",
    "자연스러운 긴 웨이브": "long hair worn fully down in clearly visible natural waves from mid-length to the ends; not straight, not tied up",
}
HAIR_MARKERS = (
    "헤어", "머리", "생머리", "포니테일", "로우 번", "번 헤어", "보브", "웨이브",
    "hair", "ponytail", "bun", "bob", "braid", "pixie", "bangs", "hairstyle",
)
SCENE_FIELDS = {
    "hair_state", "hair", "wardrobe", "coverage", "activity", "pose", "expression",
    "props", "camera", "lens", "lighting", "location", "scene_style", "negative_constraints",
}
STRATEGY_ALIASES = {
    "identity-merge": "strict_translation",
    "strict_translation": "strict_translation",
    "enriched": "creative_expansion",
    "creative_expansion": "creative_expansion",
    "exact": "exact",
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
        lowered = request.lower()
        matched = next((value for phrase, value in HAIR_VARIATIONS.items() if phrase in request), None)
        if matched:
            scene_spec["hair"] = matched
        elif any(marker in lowered for marker in HAIR_MARKERS):
            scene_spec["hair"] = request.strip()
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
    if scene_spec.get("mode") not in {"strict_translation", "creative_expansion", "exact"}:
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
    payload = json.dumps({"model": model, "stream": False, "format": "json", "messages": [{"role": "user", "content": prompt}], "options": {"temperature": 0.25}}).encode()
    req = urllib.request.Request(cm.OLLAMA_CHAT, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as response:
        result = json.load(response)
    delta = json.loads(result["message"]["content"])
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


def prepare(character_id: str, request: str, model: str, count: int, engines: list[str], strategy: str = "strict_translation", immutable: dict[str, str] | None = None, supplied_scene_spec: dict[str, Any] | None = None, actor: str = "codex") -> Path:
    character_path = cm.CHARACTERS / character_id / "character.json"
    if not character_path.is_file():
        raise cm.CharacterError(f"unknown character: {character_id}")
    character = cm.load(character_path)
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
    created = datetime.now()
    title = delta["title"] if delta else request
    session_id = f"SCENE-{created.strftime('%Y%m%d-%H%M%S')}-{character_id[3:]}-{slug_text(title)}"
    root = cm.CHARACTERS / character_id / "02_generations" / session_id
    asset_root = ASSET_LIBRARY / "characters" / character_id / "generations" / session_id / "outputs"
    merged_prompt = identity_merge_prompt(character, request, immutable, scene_spec)
    enriched_prompt = compile_prompt(character, delta, request, immutable, scene_spec) if delta else merged_prompt
    prompt = request if operating_mode == "exact" else enriched_prompt
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
        "created_at": stamp(), "created_by": actor, "local_model": model if operating_mode == "creative_expansion" else None,
        "source_request": request, "runtime_prompt_sha256": prompt_hash, "scene_delta": delta,
        "prompt_strategy": operating_mode, "immutable_constraints": immutable, "scene_spec": scene_spec,
        "suppressed_stable_dna_fields": suppressed_dna_fields,
    })
    trace = {
        "schema_version": 3, "precedence": ["explicit_user_constraints", "immutable_scene_fields", "stable_character_dna", "bounded_identity_variables", "scene_requirements", "style_enrichment", "optional_creative_detail"],
        "strategy": operating_mode, "immutable_constraints": immutable, "scene_spec": scene_spec,
        "suppressed_stable_dna_fields": suppressed_dna_fields, "raw_user_prompt": request,
        "structured_scene_spec": scene_spec,
        "after_character_dna_merge": merged_prompt,
        "after_constraint_validation": validation,
        "after_scene_enrichment": enriched_prompt if operating_mode == "creative_expansion" else None,
        "after_scene_style_expansion": enriched_prompt if operating_mode == "creative_expansion" else None,
        "final_prompt_sent_to_hermes": None,
        "final_prompt_sent_to_image_engine": prompt,
        "invoked_by": actor, "hermes_agent_used": actor == "hermes", "local_llm_used": operating_mode == "creative_expansion", "created_at": stamp(),
    }
    write_json(root / "prompt-trace.json", trace)
    write_json(root / "trace.json", trace)
    jobs = []
    seed_base = int(created.strftime("%m%d%H%M%S"))
    for offset, engine in enumerate(engines, 1):
        if engine not in ENGINES:
            raise cm.CharacterError(f"unsupported engine: {engine}")
        template_name, model_name = ENGINES[engine]
        settings = json.loads((TEMPLATES / template_name).read_text(encoding="utf-8"))
        settings["batch_size"] = count
        settings["repeat_generation"] = 1
        settings["seed"] = seed_base + offset
        write_json(root / template_name, settings)
        jobs.append({"backend": "local-wangp", "model": model_name, "count": count, "seed": settings["seed"], "resolution": settings["resolution"], "steps": settings["num_inference_steps"], "settings_file": template_name, "output_dir": f"outputs/{engine}", "status": "prepared"})
    batch = {
        "schema_version": 1,
        "session": {"id": session_id, "character_id": character_id, "character_name": character["name"], "romanized_name": character.get("romanized_name", ""), "title": title, "status": "prepared", "visibility": "restricted", "asset_root": str(asset_root), "created_at": stamp(), "prompt_file": "prompt.txt", "scene_spec_file": "scene_spec.json", "scene_delta_file": "scene-delta.json", "prompt_trace_file": "prompt-trace.json", "prompt_strategy": operating_mode, "stable_dna_sha256": cm.stable_hash(character)},
        "jobs": jobs,
        "review": {"surface": "personal-prompt-studio", "initial_state": "needs_review"},
    }
    # JSON is valid YAML and keeps this tool dependency-free.
    write_json(root / "batch.yaml", batch)
    return root


def submit(root: Path, wait: bool) -> list[dict[str, Any]]:
    batch = yaml.safe_load((root / "batch.yaml").read_text(encoding="utf-8"))
    asset_root = Path(batch["session"]["asset_root"]).resolve() if batch["session"].get("asset_root") else root / "outputs"
    results = []
    for job in batch["jobs"]:
        if job.get("status") == "completed":
            continue
        if job.get("status") == "running":
            raise RuntimeError(f"{Path(job['output_dir']).name} is already running")
        engine = Path(job["output_dir"]).name
        command = [sys.executable, str(RUNNER), "submit", "--runs-root", str(root / "runs"), "--prompt-file", str(root / "prompt.txt"), "--settings-file", str(root / job["settings_file"]), "--project-id", root.name, "--prompt-id", f"{root.name}-{engine}", "--output-dir", str(asset_root / engine)]
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
    draft.add_argument("--actor", choices=("codex", "hermes", "web"), default="codex")
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
    produce.add_argument("--actor", choices=("codex", "hermes", "web"), default="codex")
    args = parser.parse_args()
    try:
        if args.command == "produce" and args.session_dir:
            root = args.session_dir.resolve()
            if not root.is_relative_to(cm.CHARACTERS.resolve()) or root.parent.name != "02_generations":
                raise cm.CharacterError("session-dir must be a character 02_generations session")
            if not (root / "batch.yaml").is_file() or not (root / "prompt.txt").is_file():
                raise cm.CharacterError("session-dir is missing batch.yaml or prompt.txt")
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
            root = prepare(args.character, args.request, args.model, args.count, engines, args.strategy, {str(key): str(value) for key, value in immutable.items()}, {str(key): value for key, value in scene_spec.items()}, args.actor)
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
