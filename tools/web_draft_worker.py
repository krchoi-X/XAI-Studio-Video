"""Compile one Studio draft request in the background.

The scene compiler's `interpret` is cheap for the template strategies and slow for the ones
that consult the local model: measured at 2m08 warm and 4m19 cold against the 26B. Holding an
HTTP request open for that long makes reading a compilation feel like paying for it, which is
the opposite of the point, so the Studio spawns this and polls `status.json` instead.

This writes only inside its own job directory. It reserves no generation session, renders
nothing, and never touches the GPU.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def status(job_dir: Path, state: str, **extra: object) -> None:
    write_json(job_dir / "status.json", {"status": state, "updated_at": stamp(), **extra})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    job_dir = args.job_dir.resolve()
    request = json.loads((job_dir / "request.json").read_text(encoding="utf-8"))
    command = [
        sys.executable, str(args.repo_root / "tools" / "character_scene.py"), "interpret",
        "--character", request["character_id"], "--request", request["prompt"],
        "--model", request["prompt_model"], "--strategy", request["prompt_strategy"],
        "--constraints-json", json.dumps(request.get("immutable_constraints") or {}, ensure_ascii=False),
        "--scene-spec-json", json.dumps(request.get("scene_spec") or {}, ensure_ascii=False),
    ]
    status(job_dir, "running", progress="요청을 해석하는 중")
    try:
        completed = subprocess.run(
            command, cwd=str(args.repo_root), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=900,
        )
        (job_dir / "worker.log").write_text(
            (completed.stdout or "") + "\n--- stderr ---\n" + (completed.stderr or ""), encoding="utf-8",
        )
        if completed.returncode != 0:
            raise RuntimeError((completed.stderr or completed.stdout or f"exit {completed.returncode}").strip())
        draft = json.loads(completed.stdout)
    except Exception as error:  # a failed draft must still end, and say why
        status(job_dir, "failed", error=f"{type(error).__name__}: {error}")
        return 1
    write_json(job_dir / "draft.json", draft)
    status(job_dir, "completed", progress="해석이 끝났습니다")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
