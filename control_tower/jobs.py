"""Canonical Job model shared by every adapter.

`requested_by` (who asked), `executor` (what ran it), `engine` (runtime) and `model` are separate fields on
purpose. Progress carries an explicit `type`; only `step`, `items` and `exact` are measured. Everything else is
inferred and the UI must label it that way.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

ACTIVE_STATUSES = {"queued", "starting", "running", "provisioning", "uploading"}
COMPLETED_STATUSES = {"succeeded", "needs_review", "completed"}
FAILED_STATUSES = {"failed", "cancelled", "interrupted", "timed_out", "error"}
TERMINAL_STATUSES = COMPLETED_STATUSES | FAILED_STATUSES

MEASURED_PROGRESS_TYPES = {"exact", "step", "items"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_SUFFIXES = {".mp4", ".mov", ".webm", ".mkv"}


@dataclass
class Progress:
    type: str = "unknown"  # exact | step | items | phase | activity | unknown
    current: int | None = None
    total: int | None = None
    percent: float | None = None
    label: str = ""
    runtime_percent: float | None = None  # the runtime's own reported percent, if any (secondary)
    item_current: int | None = None
    item_total: int | None = None

    @property
    def measured(self) -> bool:
        return self.type in MEASURED_PROGRESS_TYPES and self.percent is not None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["measured"] = self.measured
        return data

    @classmethod
    def step(cls, current: int, total: int, label: str | None = None, **extra: Any) -> "Progress":
        total = max(total, 1)
        pct = round(100.0 * min(current, total) / total, 1)
        return cls(type="step", current=current, total=total, percent=pct, label=label or f"step {current}/{total}", **extra)

    @classmethod
    def items(cls, current: int, total: int, label: str | None = None, **extra: Any) -> "Progress":
        total = max(total, 1)
        pct = round(100.0 * min(current, total) / total, 1)
        return cls(type="items", current=current, total=total, percent=pct, label=label or f"{current}/{total} items", **extra)

    @classmethod
    def phase(cls, label: str, **extra: Any) -> "Progress":
        return cls(type="phase", label=label, **extra)

    @classmethod
    def activity(cls, label: str, **extra: Any) -> "Progress":
        return cls(type="activity", label=label, **extra)

    @classmethod
    def unknown(cls, label: str = "progress unavailable") -> "Progress":
        return cls(type="unknown", label=label)


@dataclass
class Output:
    path: str
    kind: str  # image | video | file
    byte_count: int | None = None
    sha256: str | None = None
    exists: bool = True
    index: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def output_kind(path: str) -> str:
    lower = path.lower()
    dot = lower.rfind(".")
    suffix = lower[dot:] if dot >= 0 else ""
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix in VIDEO_SUFFIXES:
        return "video"
    return "file"


@dataclass
class Job:
    job_id: str
    source: str  # wangp-run | night-batch | web-job
    title: str
    requested_by: str  # hermes | codex | web | claude | grok | unknown
    executor: str
    requested_by_basis: str | None = None  # record | parent | process-env | process-lineage | manual | None
    engine: str | None = None
    model: str | None = None
    status: str = "unknown"
    phase: str | None = None
    created_at: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    updated_at: str | None = None
    elapsed_seconds: float | None = None
    progress: Progress = field(default_factory=Progress.unknown)
    eta_seconds: float | None = None
    eta_basis: str | None = None  # recent_steps | history | None
    outputs: list[Output] = field(default_factory=list)
    parent_job_id: str | None = None
    character_id: str | None = None
    session_id: str | None = None
    session_dir: str | None = None
    run_dir: str | None = None
    worker_pid: int | None = None
    worker_alive: bool | None = None
    error: str | None = None
    note: str | None = None
    last_event_at: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.status in ACTIVE_STATUSES

    @property
    def is_terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["progress"] = self.progress.to_dict()
        data["outputs"] = [o.to_dict() for o in self.outputs]
        data["is_active"] = self.is_active
        data["is_terminal"] = self.is_terminal
        data["outcome"] = "completed" if self.status in COMPLETED_STATUSES else "failed" if self.status in FAILED_STATUSES else "active" if self.is_active else "unknown"
        return data
