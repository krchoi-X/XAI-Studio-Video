#!/usr/bin/env python3
"""Prepare and render face-first discovery batches for Hae-won and Harim."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import character_manager as cm
import character_scene as scene

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "docs" / "character-face-discovery-workflow.md"
CHARACTER_PREFIX = {"ch-jung-haewon": "HAEWON", "ch-harim": "HARIM"}


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def discovery_prompt(character_id: str, direction: str) -> str:
    prefix = CHARACTER_PREFIX.get(character_id)
    direction = direction.upper()
    if not prefix or not re.fullmatch(rf"{prefix}-[A-D]", direction):
        raise cm.CharacterError(f"invalid face direction {direction} for {character_id}")
    document = WORKFLOW.read_text(encoding="utf-8")
    match = re.search(rf"^#### {re.escape(direction)}\s+—.*?^```text\s*$\n(.*?)^```\s*$", document, re.MULTILINE | re.DOTALL)
    if not match:
        raise cm.CharacterError(f"prompt not found in workflow: {direction}")
    return match.group(1).strip()


def prepare(character_id: str, direction: str, count: int, engines: list[str]) -> Path:
    character_path = cm.CHARACTERS / character_id / "character.json"
    if not character_path.is_file():
        raise cm.CharacterError(f"unknown character: {character_id}")
    character = cm.load(character_path)
    prompt = discovery_prompt(character_id, direction)
    created = datetime.now()
    session_id = f"FACE-{created.strftime('%Y%m%d-%H%M%S')}-{character_id[3:]}-{direction.lower()}"
    root = character_path.parent / "02_generations" / session_id
    asset_root = scene.ASSET_LIBRARY / "characters" / character_id / "generations" / session_id / "outputs"
    prompt_text = prompt + "\n"
    prompt_hash = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    cm.atomic_write(root / "request.txt", f"Face discovery {direction}\n")
    cm.atomic_write(root / "prompt.txt", prompt_text)
    scene.write_json(root / "metadata.json", {
        "schema_version": 1, "session_id": session_id, "character": character_id,
        "character_version": character["version"], "stable_dna_sha256": cm.stable_hash(character),
        "phase": "face-discovery", "direction": direction, "created_at": stamp(),
        "prompt_source": "docs/character-face-discovery-workflow.md", "runtime_prompt_sha256": prompt_hash,
        "constraints": {"body_dna_applied": False, "signature_hair_minimized": True, "scene_variables_locked": True},
    })
    jobs = []
    seed_base = int(created.strftime("%m%d%H%M%S"))
    for offset, engine in enumerate(engines, 1):
        if engine not in scene.ENGINES:
            raise cm.CharacterError(f"unsupported engine: {engine}")
        template_name, model_name = scene.ENGINES[engine]
        settings = json.loads((scene.TEMPLATES / template_name).read_text(encoding="utf-8"))
        settings.update({"batch_size": count, "repeat_generation": 1, "seed": seed_base + offset})
        scene.write_json(root / template_name, settings)
        jobs.append({"backend": "local-wangp", "model": model_name, "count": count, "seed": settings["seed"], "resolution": settings["resolution"], "steps": settings["num_inference_steps"], "settings_file": template_name, "output_dir": f"outputs/{engine}", "status": "prepared"})
    scene.write_json(root / "batch.yaml", {
        "schema_version": 1,
        "session": {"id": session_id, "character_id": character_id, "character_name": character["name"], "romanized_name": character.get("romanized_name", ""), "title": f"{direction} face discovery", "phase": "face-discovery", "direction": direction, "status": "prepared", "visibility": "restricted", "asset_root": str(asset_root), "created_at": stamp(), "prompt_file": "prompt.txt", "metadata_file": "metadata.json", "stable_dna_sha256": cm.stable_hash(character)},
        "jobs": jobs, "review": {"surface": "personal-prompt-studio", "taxonomy": "face-discovery", "initial_state": "face-exploration"},
    })
    return root


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "produce"):
        command = sub.add_parser(name)
        command.add_argument("--character", required=True, choices=sorted(CHARACTER_PREFIX))
        command.add_argument("--direction", required=True)
        command.add_argument("--count", type=int, default=8)
        command.add_argument("--engines", default="z-image,krea2")
    args = parser.parse_args()
    try:
        if not 1 <= args.count <= 12:
            raise cm.CharacterError("count must be between 1 and 12 per engine")
        engines = list(dict.fromkeys(item.strip() for item in args.engines.split(",") if item.strip()))
        root = prepare(args.character, args.direction.upper(), args.count, engines)
        result = {"session_dir": str(root), "status": "prepared", "direction": args.direction.upper()}
        if args.command == "produce":
            result.update({"status": "completed", "runs": scene.submit(root, wait=True)})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (cm.CharacterError, OSError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
