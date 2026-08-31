#!/usr/bin/env python3
"""Run one durable tablet-submitted character image job."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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
    parser.add_argument("--sync-url", default="http://127.0.0.1:8787/api/sync")
    args = parser.parse_args()
    job_dir = args.job_dir.resolve()
    request = json.loads((job_dir / "request.json").read_text(encoding="utf-8"))
    log_path = job_dir / "render.log"
    if request.get("mode") == "face-discovery":
        command = [sys.executable, str(args.repo_root / "tools" / "face_discovery.py"), "produce",
            "--character", request["character_id"], "--direction", request["direction"],
            "--count", str(request["count"]), "--engines", ",".join(request["engines"])]
    else:
        command = [sys.executable, str(args.repo_root / "tools" / "character_scene.py"), "produce",
            "--character", request["character_id"], "--request", request["prompt"],
            "--count", str(request["count"]), "--engines", ",".join(request["engines"]),
            "--model", request["prompt_model"], "--strategy", request.get("prompt_strategy", "identity-merge"),
            "--actor", "web",
            "--constraints-json", json.dumps(request.get("immutable_constraints") or {}, ensure_ascii=False),
            "--scene-spec-json", json.dumps(request.get("scene_spec") or {}, ensure_ascii=False)]
    status(job_dir, "running", progress="프롬프트를 정리하고 로컬 생성기를 시작하는 중")
    try:
        completed = subprocess.run(command, cwd=args.repo_root, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=7500)
        log_path.write_text((completed.stdout or "") + "\n--- stderr ---\n" + (completed.stderr or ""), encoding="utf-8")
        if completed.returncode != 0:
            raise RuntimeError((completed.stderr or completed.stdout or f"exit {completed.returncode}").strip())
        result = json.loads(completed.stdout)
        try:
            urllib.request.urlopen(urllib.request.Request(args.sync_url, method="POST"), timeout=120).read()
            synced = True
        except Exception as sync_error:  # render remains successful; a later app refresh can sync again
            synced = False
            (job_dir / "sync-error.txt").write_text(str(sync_error), encoding="utf-8")
        status(job_dir, "completed", progress="완료", session_dir=result.get("session_dir"), runs=result.get("runs", []), synced=synced)
        return 0
    except Exception as error:
        status(job_dir, "failed", progress="실패", error=str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
