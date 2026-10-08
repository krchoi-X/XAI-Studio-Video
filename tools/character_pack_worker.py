#!/usr/bin/env python3
"""Execute one queued Character Pack regeneration request.

The worker uses the existing reference-bound Character Scene CLI and the
append-only :mod:`character_pack` runtime.  It never chooses a fallback engine
and never approves a candidate or pack.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any, Callable

from character_pack import CharacterPackError, CharacterPackJob


SLOT_SCENES: dict[str, dict[str, str]] = {
    "face_front": {"camera": "straight-on front view, zero yaw", "pose": "head upright, shoulders square to camera"},
    "face_left30": {"camera": "camera sees the face turned 30 degrees to the subject's left", "pose": "head upright, controlled left three-quarter turn"},
    "face_right30": {"camera": "camera sees the face turned 30 degrees to the subject's right", "pose": "head upright, controlled right three-quarter turn"},
    "face_left90": {"camera": "exact left profile, 90-degree yaw", "pose": "head upright in a strict left profile"},
    "face_right90": {"camera": "exact right profile, 90-degree yaw", "pose": "head upright in a strict right profile"},
    "body_front": {"camera": "straight-on full-body front view", "pose": "neutral anatomical stance facing camera"},
    "body_three_quarter": {"camera": "full-body three-quarter view", "pose": "neutral anatomical stance at a controlled three-quarter angle"},
    "body_side": {"camera": "strict full-body side view", "pose": "neutral anatomical stance in profile"},
    "body_back": {"camera": "straight-on full-body back view", "pose": "neutral anatomical stance facing away from camera"},
}


def scene_spec(slot_id: str) -> dict[str, str]:
    try:
        view = SLOT_SCENES[slot_id]
    except KeyError as exc:
        raise CharacterPackError(f"unsupported character-pack slot: {slot_id}") from exc
    body = slot_id.startswith("body_")
    return {
        **view,
        "expression": "neutral relaxed expression, closed mouth",
        "lighting": "soft even neutral studio lighting with no dramatic shadows",
        "location": "plain seamless neutral studio background",
        "scene_style": "clinical character reference photography; no beauty retouching",
        "wardrobe": "plain fitted neutral reference outfit with clear silhouette" if body else "neutral neckline with no distracting accessories",
        "negative_constraints": "no identity change, no anatomy distortion, no cropped head or limbs, no text, no collage",
    }


class SceneRenderer:
    def __init__(self, repo_root: Path, *, runner: Callable[..., Any] = subprocess.run):
        self.repo_root = Path(repo_root).resolve()
        self.runner = runner

    def render(self, request: dict[str, Any]) -> dict[str, Any]:
        command = [
            sys.executable,
            str(self.repo_root / "tools" / "character_scene.py"),
            "produce",
            "--character", request["character_id"],
            "--request", request["prompt"],
            "--count", "1",
            "--engines", request["engine"],
            "--strategy", "strict_translation",
            "--identity-reference", request["master_face"]["path"],
            "--reference-asset-id", request["master_face"]["asset_id"],
            "--scene-spec-json", json.dumps(scene_spec(request["slot_id"]), ensure_ascii=False),
            "--actor", "web",
        ]
        completed = self.runner(
            command,
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=7500,
        )
        if completed.returncode != 0:
            raise CharacterPackError((completed.stderr or completed.stdout or "character scene failed").strip())
        try:
            result = json.loads(completed.stdout)
            session_dir = Path(result["session_dir"]).resolve()
            run_dir = Path(result["runs"][0]["run_dir"]).resolve()
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            artifacts = run.get("artifacts") or []
            artifact = artifacts[0]
            output_path = Path(artifact["path"]).resolve()
        except (KeyError, IndexError, TypeError, json.JSONDecodeError, OSError) as exc:
            raise CharacterPackError("character scene returned no durable output artifact") from exc
        if not output_path.is_file():
            raise CharacterPackError("character scene output artifact is missing")
        settings = (run.get("settings") or {}).get("value") or {}
        return {
            "output_path": str(output_path),
            "model_type": request["model_type"],
            "seed": settings.get("seed"),
            "executor": "web",
            "run_id": str(run.get("run_id") or run_dir.name),
            "session_id": session_dir.name,
            "automatic_qa": {
                "prompt_exact_match": artifact.get("prompt_exact_match"),
                "prompt_normalized_match": artifact.get("prompt_normalized_match"),
                "identity_score_is_advisory": True,
                "gallery_sync_pending": True,
            },
        }


def request_gallery_sync(url: str, *, opener: Callable[..., Any] = urllib.request.urlopen) -> None:
    opener(urllib.request.Request(url, method="POST"), timeout=120).read()


def run_initial_build(job: CharacterPackJob, renderer: SceneRenderer) -> tuple[list[dict[str, Any]], list[str]]:
    """Render every candidate-less required slot once, preserving partial success."""
    candidates: list[dict[str, Any]] = []
    errors: list[str] = []
    for slot_id, engine in job.default_engine_map().items():
        try:
            candidates.append(
                job.generate(slot_id, engine=engine, renderer=renderer, importer=lambda _request, _result: None)
            )
        except Exception as exc:
            errors.append(f"{slot_id}: {exc}")
    return candidates, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-dir", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--request-id")
    mode.add_argument("--initial", action="store_true")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--sync-url", default="http://127.0.0.1:8787/api/sync")
    args = parser.parse_args()
    job = CharacterPackJob(args.job_dir)
    try:
        renderer = SceneRenderer(args.repo_root)
        if args.initial:
            candidates, errors = run_initial_build(job, renderer)
            result: Any = {"candidates": candidates, "errors": errors}
        else:
            result = job.run_regeneration_request(
                args.request_id,
                renderer=renderer,
                importer=lambda _request, _result: None,
            )
            errors = []
        try:
            request_gallery_sync(args.sync_url)
        except Exception as exc:
            sync_name = "initial.sync-error.txt" if args.initial else f"{args.request_id}.sync-error.txt"
            (args.job_dir / "regeneration-requests").mkdir(parents=True, exist_ok=True)
            (args.job_dir / "regeneration-requests" / sync_name).write_text(str(exc), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if errors else 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

