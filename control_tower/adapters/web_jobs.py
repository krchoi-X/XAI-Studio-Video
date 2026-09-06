"""Gallery (Personal Prompt Studio) tablet job adapter: `<workspace>/generation-jobs/<gen_id>/{status,request}.json`.

The web worker only reports coarse textual progress, so these jobs carry `activity`/`phase` progress; the
linked WanGP runs (via `session_dir` / `runs`) provide the measured steps.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from ..jobs import Job, Progress
from ..util import parse_iso, read_json_safe, seconds_between, utc_now

STATUS_MAP = {"queued": "queued", "running": "running", "completed": "succeeded", "failed": "failed"}


class WebJobAdapter:
    def __init__(self, roots: list[Path]) -> None:
        self.roots = [Path(r) for r in roots]

    def discover(self, now: datetime | None = None) -> list[Job]:
        now = now or utc_now()
        jobs: list[Job] = []
        seen: set[str] = set()
        for root in self.roots:
            if not root.is_dir():
                continue
            for job_dir in sorted(root.iterdir()):
                if job_dir.name in seen or not job_dir.is_dir():
                    continue
                status = read_json_safe(job_dir / "status.json")
                request = read_json_safe(job_dir / "request.json")
                if not isinstance(status, dict):
                    continue
                request = request if isinstance(request, dict) else {}
                seen.add(job_dir.name)
                jobs.append(self._build(job_dir, status, request, now))
        return jobs

    def _build(self, job_dir: Path, status: dict[str, Any], request: dict[str, Any], now: datetime) -> Job:
        raw = str(status.get("status") or "unknown")
        norm = STATUS_MAP.get(raw, raw)
        created = parse_iso(request.get("created_at") or status.get("created_at"))
        updated = parse_iso(status.get("updated_at"))
        finished = updated if norm in {"succeeded", "failed"} else None
        text = str(status.get("progress") or raw)
        if norm == "running":
            progress = Progress.activity(text)
        elif norm == "queued":
            progress = Progress.phase("queued")
        elif norm == "succeeded":
            progress = Progress(type="exact", percent=100.0, label="completed")
        else:
            progress = Progress.unknown(text)
        engines = request.get("engines") or []
        mode = request.get("mode") or "scene"
        prompt = str(request.get("prompt") or request.get("direction") or "")
        title = f"{request.get('character_id') or 'character'} · {mode} · {prompt[:60]}" if prompt else f"{request.get('character_id') or 'web job'} · {mode}"
        elapsed = seconds_between(created, finished or now) if norm != "queued" else None
        runs = status.get("runs") if isinstance(status.get("runs"), list) else []
        return Job(
            job_id=f"web:{job_dir.name}",
            source="web-job",
            title=title,
            requested_by="web",
            executor="web-generation-worker",
            engine="WanGP",
            model=", ".join(str(e) for e in engines) if engines else None,
            status=norm,
            created_at=created.isoformat(timespec="seconds") if created else None,
            started_at=created.isoformat(timespec="seconds") if created and norm != "queued" else None,
            finished_at=finished.isoformat(timespec="seconds") if finished else None,
            updated_at=status.get("updated_at"),
            elapsed_seconds=round(elapsed, 1) if elapsed is not None else None,
            progress=progress,
            character_id=request.get("character_id"),
            session_dir=str(status["session_dir"]) if status.get("session_dir") else None,
            run_dir=str(job_dir),
            error=str(status.get("error"))[:300] if status.get("error") else None,
            details={
                "mode": mode,
                "count": request.get("count"),
                "engines": engines,
                "prompt_model": request.get("prompt_model"),
                "prompt": prompt[:400],
                "synced": status.get("synced"),
                "run_dirs": [r.get("run_dir") for r in runs if isinstance(r, dict) and r.get("run_dir")],
            },
        )
