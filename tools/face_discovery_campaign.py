#!/usr/bin/env python3
"""Run several face-discovery directions sequentially on one local GPU."""

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


def write(path: Path, data: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--items", required=True, help="comma-separated character:direction pairs")
    parser.add_argument("--engines", default="z-image,krea2")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--sync-url", default="http://127.0.0.1:8787/api/sync")
    args = parser.parse_args()
    job_dir = args.job_dir.resolve()
    job_dir.mkdir(parents=True, exist_ok=True)
    items = [tuple(item.split(":", 1)) for item in args.items.split(",")]
    state = {"status": "running", "created_at": stamp(), "updated_at": stamp(), "items": [{"character_id": character, "direction": direction, "status": "queued"} for character, direction in items]}
    write(job_dir / "status.json", state)
    try:
        for index, (character, direction) in enumerate(items):
            state["items"][index]["status"] = "running"
            state["updated_at"] = stamp()
            write(job_dir / "status.json", state)
            command = [sys.executable, str(args.repo_root / "tools" / "face_discovery.py"), "produce", "--character", character, "--direction", direction, "--engines", args.engines, "--count", str(args.count)]
            completed = subprocess.run(command, cwd=args.repo_root, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=7500)
            (job_dir / f"{index + 1:02d}-{direction}.log").write_text((completed.stdout or "") + "\n--- stderr ---\n" + (completed.stderr or ""), encoding="utf-8")
            if completed.returncode != 0:
                raise RuntimeError(f"{direction}: {(completed.stderr or completed.stdout).strip()}")
            result = json.loads(completed.stdout)
            state["items"][index].update({"status": "completed", "session_dir": result.get("session_dir")})
            state["updated_at"] = stamp()
            write(job_dir / "status.json", state)
            try:
                urllib.request.urlopen(urllib.request.Request(args.sync_url, method="POST"), timeout=120).read()
            except Exception as sync_error:
                state["items"][index]["sync_error"] = str(sync_error)
        state.update({"status": "completed", "updated_at": stamp()})
        write(job_dir / "status.json", state)
        return 0
    except Exception as error:
        state.update({"status": "failed", "updated_at": stamp(), "error": str(error)})
        write(job_dir / "status.json", state)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
