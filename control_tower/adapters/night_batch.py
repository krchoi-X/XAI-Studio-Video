"""Hermes night-batch adapter: `D:\\AI_Studio\\workspace\\hermes-night-batches\\<batch>/{status,plan}.json`.

One Job per batch (items progress is measured: completed+failed / total). Queued items become queue
entries; the running item's `session_dir` lets WanGP runs be linked back as children of the batch.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from ..jobs import Job, Progress
from ..util import parse_iso, read_json_safe, seconds_between, utc_now

STATUS_MAP = {"queued": "queued", "running": "running", "completed": "succeeded", "failed": "failed",
              "completed_with_failures": "needs_review", "partial": "needs_review"}


class NightBatchAdapter:
    def __init__(self, queue_root: Path) -> None:
        self.queue_root = Path(queue_root)

    def discover(self, now: datetime | None = None) -> list[Job]:
        now = now or utc_now()
        jobs: list[Job] = []
        if not self.queue_root.is_dir():
            return jobs
        for batch_dir in sorted(self.queue_root.iterdir()):
            status = read_json_safe(batch_dir / "status.json")
            plan = read_json_safe(batch_dir / "plan.json")
            if not isinstance(status, dict) or not isinstance(plan, dict):
                continue
            job = self._build(batch_dir, status, plan, now)
            if job:
                jobs.append(job)
        return jobs

    def _build(self, batch_dir: Path, status: dict[str, Any], plan: dict[str, Any], now: datetime) -> Job | None:
        batch_id = str(plan.get("batch_id") or batch_dir.name)
        raw_status = str(status.get("status") or "unknown")
        norm = STATUS_MAP.get(raw_status, raw_status)
        items = [i for i in (plan.get("items") or []) if isinstance(i, dict)]
        total = int(status.get("total_items") or len(items) or 0)
        completed = int(status.get("completed_items") or 0)
        failed = int(status.get("failed_items") or 0)
        if norm == "succeeded" and failed:
            norm = "needs_review"
        created = parse_iso(plan.get("created_at") or status.get("created_at"))
        updated = parse_iso(status.get("updated_at"))
        started = None
        finished = updated if norm in {"succeeded", "failed", "needs_review"} else None
        for item in items:
            st = parse_iso(item.get("started_at"))
            if st and (started is None or st < started):
                started = st
        running_item = next((i for i in items if i.get("status") == "running"), None)
        queued_items = [i for i in items if i.get("status") == "queued"]
        done = completed + failed
        if norm in {"queued"}:
            progress = Progress.items(0, total, label=f"0/{total} items · waiting")
        else:
            label = f"{done}/{total} items"
            if running_item:
                label += f" · running {running_item.get('id')}"
            progress = Progress.items(done, total, label=label)
        engines = sorted({e for i in items for e in (i.get("engines") or [])})
        elapsed = seconds_between(started or created, finished or now) if norm != "queued" else None
        return Job(
            job_id=f"night:{batch_id}",
            source="night-batch",
            title=str(plan.get("title") or batch_id),
            requested_by=str(plan.get("created_by") or "hermes"),
            requested_by_basis="record" if plan.get("created_by") else None,
            executor="hermes-night-batch-runner",
            engine="WanGP",
            model=", ".join(engines) if engines else None,
            status=norm,
            phase="item " + str(running_item.get("id")) if running_item else None,
            created_at=created.isoformat(timespec="seconds") if created else None,
            started_at=(started or created).isoformat(timespec="seconds") if (started or created) and norm != "queued" else None,
            finished_at=finished.isoformat(timespec="seconds") if finished else None,
            updated_at=status.get("updated_at"),
            elapsed_seconds=round(elapsed, 1) if elapsed is not None else None,
            progress=progress,
            eta_seconds=None,
            eta_basis=None,
            session_dir=str(running_item.get("session_dir")) if running_item and running_item.get("session_dir") else None,
            run_dir=str(batch_dir),
            details={
                "batch_id": batch_id,
                "source_request": plan.get("source_request"),
                "generated_image_budget": plan.get("generated_image_budget"),
                "completed_items": completed,
                "failed_items": failed,
                "total_items": total,
                "queued_items": [{"id": i.get("id"), "character_id": i.get("character_id"), "prompt": i.get("prompt"),
                                  "engines": i.get("engines"), "count": i.get("count")} for i in queued_items],
                "items": [{"id": i.get("id"), "status": i.get("status"), "character_id": i.get("character_id"),
                           "prompt": (i.get("prompt") or "")[:160], "session_dir": i.get("session_dir"),
                           "error": (i.get("error") or "")[:300] or None} for i in items],
                "item_session_dirs": [i.get("session_dir") for i in items if i.get("session_dir")],
            },
        )
