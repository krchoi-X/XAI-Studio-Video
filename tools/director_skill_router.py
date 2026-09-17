#!/usr/bin/env python3
"""Select a bounded Director Memory skill subset for each storyboard candidate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


MANIFEST_RELATIVE_PATH = Path("docs/director-memory/skill-router.json")


def load_manifest(repo_root: Path) -> tuple[dict[str, Any], str]:
    path = repo_root / MANIFEST_RELATIVE_PATH
    raw = path.read_bytes()
    manifest = json.loads(raw.decode("utf-8"))
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported director skill manifest version")
    skill_ids = [item["skill_id"] for item in manifest.get("skills", [])]
    if len(skill_ids) != len(set(skill_ids)):
        raise ValueError("director skill manifest contains duplicate skill_id values")
    known = set(skill_ids)
    for mode in manifest.get("modes", []):
        missing = set(mode.get("skill_ids", [])) - known
        if missing:
            raise ValueError(f"mode {mode.get('mode_id')} references unknown skills: {sorted(missing)}")
    return manifest, hashlib.sha256(raw).hexdigest()


def _request_text(request: dict[str, Any]) -> str:
    values = [request.get("idea", ""), request.get("output_intent", "")]
    values.extend(str(value) for value in request.get("constraints", {}).values() if value is not None)
    return " ".join(values).casefold()


def _mode_score(mode: dict[str, Any], text: str) -> tuple[int, int, str]:
    matches = sum(1 for signal in mode.get("signals", []) if signal.casefold() in text)
    return (-matches, int(mode.get("priority", 9999)), mode["mode_id"])


def _ordered_modes(manifest: dict[str, Any], request: dict[str, Any]) -> list[dict[str, Any]]:
    text = _request_text(request)
    ranked = sorted(manifest["modes"], key=lambda mode: _mode_score(mode, text))
    if len(ranked) < 2:
        return ranked

    # Keep the first route practical, then prefer a different lane for comparison.
    first = next((mode for mode in ranked if mode.get("lane") == "safe"), ranked[0])
    remaining = [mode for mode in ranked if mode["mode_id"] != first["mode_id"]]
    different_lane = [mode for mode in remaining if mode.get("lane") != first.get("lane")]
    return [first, *(different_lane or remaining), *[mode for mode in remaining if mode not in different_lane]]


def route_request(repo_root: Path, request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest, manifest_hash = load_manifest(repo_root)
    count = 1 if request.get("mode") == "exact" else int(request["candidate_count"])
    modes = _ordered_modes(manifest, request)[:count]
    if len(modes) != count:
        raise ValueError(f"director router needs {count} modes but found {len(modes)}")

    skills = {item["skill_id"]: item for item in manifest["skills"]}
    routes: list[dict[str, Any]] = []
    for index, mode in enumerate(modes):
        selected = list(dict.fromkeys(mode["skill_ids"]))
        minimum = int(manifest["selection"]["min_skills_per_candidate"])
        maximum = int(manifest["selection"]["max_skills_per_candidate"])
        if not minimum <= len(selected) <= maximum:
            raise ValueError(f"mode {mode['mode_id']} selects {len(selected)} skills; expected {minimum}-{maximum}")
        refs = list(dict.fromkeys(skills[skill_id]["source"] for skill_id in selected))
        routes.append({
            "candidate_index": index,
            "candidate_key": chr(ord("A") + index),
            "storyboard_id": None,
            "mode": mode["mode_id"],
            "lane": mode["lane"],
            "creative_intent": mode["creative_intent"],
            "selected_skills": selected,
            "source_refs": refs[: int(manifest["selection"]["max_references_per_candidate"])],
            "rationale": f"Selected {mode['mode_id']} from signals in the validated episode request; use only its listed skills.",
        })

    subsets = [tuple(sorted(route["selected_skills"])) for route in routes]
    warnings = []
    if len(subsets) != len(set(subsets)):
        warnings.append("Two candidate routes selected the same skill subset; require an explicit creative reason before generation.")
    routing = {
        "schema_version": 1,
        "request_id": request["request_id"],
        "manifest": {"path": MANIFEST_RELATIVE_PATH.as_posix(), "sha256": manifest_hash},
        "candidate_routes": routes,
        "warnings": warnings,
    }
    return routing, selected_context(manifest, routing)


def selected_context(manifest: dict[str, Any], routing: dict[str, Any]) -> dict[str, Any]:
    skill_map = {item["skill_id"]: item for item in manifest["skills"]}
    candidates = []
    for route in routing["candidate_routes"]:
        candidates.append({
            "candidate_key": route["candidate_key"],
            "mode": route["mode"],
            "creative_intent": route["creative_intent"],
            "skills": [
                {
                    key: skill_map[skill_id][key]
                    for key in ("skill_id", "guidance", "what_to_extract", "do_not_copy", "source")
                }
                for skill_id in route["selected_skills"]
            ],
        })
    return {"director_core": manifest["director_core"], "candidates": candidates}


def finalize_routing(routing: dict[str, Any], storyboards: list[dict[str, Any]]) -> dict[str, Any]:
    if len(storyboards) != len(routing["candidate_routes"]):
        raise ValueError(
            f"storyboard count {len(storyboards)} does not match routed candidate count {len(routing['candidate_routes'])}"
        )
    finalized = json.loads(json.dumps(routing))
    for route, storyboard in zip(finalized["candidate_routes"], storyboards):
        route["storyboard_id"] = storyboard["id"]
    return finalized
