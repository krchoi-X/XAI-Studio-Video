"""Data models for external media import planning and apply."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ItemStatus(str, Enum):
    PLANNED = "planned"
    MISSING = "missing"
    INVALID = "invalid"
    DUPLICATE = "duplicate"  # same dest + same hash (no-op)
    CONFLICT = "conflict"  # same dest name, different content
    PATH_REJECTED = "path_rejected"
    COPIED = "copied"
    SKIPPED_NOOP = "skipped_noop"
    FAILED = "failed"


@dataclass
class MediaProbe:
    kind: str  # image | video | unknown
    mime: str | None = None
    width: int | None = None
    height: int | None = None
    duration_seconds: float | None = None
    codec: str | None = None
    frame_rate: float | None = None
    has_audio: bool | None = None
    container: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ImportItem:
    """One media file to import."""

    source_path: str
    dest_name: str
    engine: str
    provider: str | None = None
    model: str | None = None
    prompt: str | None = None
    references: list[str] = field(default_factory=list)
    user_request: str | None = None
    created_at: str | None = None
    # Optional per-item session override (item-level sessions)
    session_id: str | None = None
    title: str | None = None

    # Filled by planner
    resolved_source: str | None = None
    sha256: str | None = None
    dest_path: str | None = None
    status: ItemStatus = ItemStatus.PLANNED
    message: str | None = None
    probe: MediaProbe | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, ItemStatus) else self.status
        if self.probe is not None:
            d["probe"] = self.probe.to_dict()
        return d


@dataclass
class PlanReport:
    character_id: str
    session_id: str
    title: str
    engine: str
    library_root: str
    record_root: str
    visibility: str
    provider: str | None
    model: str | None
    record_dir: str
    outputs_dir: str  # .../outputs/<engine>
    asset_root: str  # .../outputs (parent of engine dirs)
    items: list[ImportItem] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    # When prompts differ: "provenance" (default) or "split" into item sessions
    prompt_strategy: str = "provenance"

    def counts(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for item in self.items:
            key = item.status.value if isinstance(item.status, ItemStatus) else str(item.status)
            out[key] = out.get(key, 0) + 1
        return out

    def has_blocking_errors(self) -> bool:
        blocking = {
            ItemStatus.MISSING,
            ItemStatus.INVALID,
            ItemStatus.CONFLICT,
            ItemStatus.PATH_REJECTED,
            ItemStatus.FAILED,
        }
        return any(i.status in blocking for i in self.items) or bool(self.errors)

    def to_dict(self) -> dict[str, Any]:
        return {
            "character_id": self.character_id,
            "session_id": self.session_id,
            "title": self.title,
            "engine": self.engine,
            "library_root": self.library_root,
            "record_root": self.record_root,
            "visibility": self.visibility,
            "provider": self.provider,
            "model": self.model,
            "record_dir": self.record_dir,
            "outputs_dir": self.outputs_dir,
            "asset_root": self.asset_root,
            "prompt_strategy": self.prompt_strategy,
            "counts": self.counts(),
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "items": [i.to_dict() for i in self.items],
        }


@dataclass
class ApplyResult:
    plan: PlanReport
    copied: int = 0
    noop: int = 0
    failed: int = 0
    records_written: bool = False
    batch_published: bool = False
    sync_attempted: bool = False
    sync_ok: bool | None = None
    sync_message: str | None = None
    exit_code: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "copied": self.copied,
            "noop": self.noop,
            "failed": self.failed,
            "records_written": self.records_written,
            "batch_published": self.batch_published,
            "sync_attempted": self.sync_attempted,
            "sync_ok": self.sync_ok,
            "sync_message": self.sync_message,
            "exit_code": self.exit_code,
            "counts": self.plan.counts(),
            "plan": self.plan.to_dict(),
        }
