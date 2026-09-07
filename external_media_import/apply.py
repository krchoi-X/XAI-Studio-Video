"""Apply / resume: copy media, write provenance, publish batch.yaml last."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .hashutil import sha256_file
from .models import ApplyResult, ImportItem, ItemStatus, PlanReport
from .planner import build_plan


def _atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except OSError:
            pass
        raise


def _build_prompt_txt(plan: PlanReport, actionable: list[ImportItem]) -> str:
    """Write prompt.txt without inventing a single fake shared prompt."""
    prompts = [(i.dest_name, (i.prompt or "").strip()) for i in actionable]
    nonempty = [p for _, p in prompts if p]
    unique = list(dict.fromkeys(nonempty))
    if plan.prompt_strategy == "shared" and len(unique) <= 1:
        return unique[0] if unique else ""
    # File-tagged sections (matches register-reika-gpt-gallery.py pattern)
    blocks: list[str] = []
    for name, prompt in prompts:
        if prompt:
            blocks.append(f"{name}\n{prompt}")
        else:
            blocks.append(f"{name}\n")
    return "\n\n".join(blocks).rstrip() + ("\n" if blocks else "")


def _build_batch_manifest(plan: PlanReport, actionable: list[ImportItem]) -> dict[str, Any]:
    engines: dict[str, list[ImportItem]] = {}
    for item in actionable:
        engines.setdefault(item.engine, []).append(item)

    jobs = []
    for eng, eng_items in engines.items():
        sample = eng_items[0]
        jobs.append(
            {
                "backend": (sample.provider or eng or "").lower().replace(" ", "-") if sample.provider else eng,
                "provider": sample.provider or eng,
                "model": sample.model,
                "count": len(eng_items),
                "output_dir": f"outputs/{eng}",
                "status": "completed",
            }
        )

    return {
        "schema_version": 1,
        "session": {
            "id": plan.session_id,
            "character_id": plan.character_id,
            "title": plan.title,
            "status": "completed",
            "visibility": plan.visibility,
            "asset_root": plan.asset_root,
            "prompt_file": "prompt.txt",
        },
        "jobs": jobs,
        "review": {
            "initial_state": "needs_review",
        },
        "import": {
            "tool": "external_media_import",
            "prompt_strategy": plan.prompt_strategy,
        },
    }


def _build_provenance(plan: PlanReport, actionable: list[ImportItem]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in actionable:
        row: dict[str, Any] = {
            "file": item.dest_name,
            "original_path": item.resolved_source or item.source_path,
            "sha256": item.sha256,
            "engine": item.engine,
            "provider": item.provider,
            "model": item.model,
            "prompt": item.prompt,
            "references": list(item.references),
            "user_request": item.user_request,
            "created_at": item.created_at,
            "dest_path": item.dest_path,
        }
        if item.probe is not None:
            row["media"] = item.probe.to_dict()
        # Drop nulls for cleaner JSON
        rows.append({k: v for k, v in row.items() if v is not None and v != []})
    return rows


def _copy_one(item: ImportItem) -> ItemStatus:
    assert item.resolved_source and item.dest_path and item.sha256
    src = Path(item.resolved_source)
    dest = Path(item.dest_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        existing = sha256_file(dest)
        if existing == item.sha256:
            item.status = ItemStatus.SKIPPED_NOOP
            item.message = "same batch+file+hash — no-op"
            return item.status
        item.status = ItemStatus.CONFLICT
        item.message = "destination exists with different hash"
        return item.status

    # Copy to temp beside dest, then replace — never mutate source; never overwrite silently
    fd, tmp_name = tempfile.mkstemp(prefix=dest.name + ".", suffix=".partial", dir=str(dest.parent))
    os.close(fd)
    tmp_path = Path(tmp_name)
    try:
        shutil.copy2(src, tmp_path)
        copied_hash = sha256_file(tmp_path)
        if copied_hash != item.sha256:
            tmp_path.unlink(missing_ok=True)
            item.status = ItemStatus.FAILED
            item.message = "copied bytes hash mismatch"
            return item.status
        os.replace(tmp_path, dest)
        item.status = ItemStatus.COPIED
        item.message = "copied"
        return item.status
    except Exception as exc:  # noqa: BLE001
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        item.status = ItemStatus.FAILED
        item.message = f"copy failed: {exc}"
        return item.status


def apply_plan(
    plan: PlanReport,
    *,
    allow_partial: bool = False,
    write_records: bool = True,
    publish_batch: bool = True,
) -> ApplyResult:
    """Copy planned items; publish batch.yaml only after all copies succeed (unless allow_partial)."""
    result = ApplyResult(plan=plan)

    if plan.errors and not allow_partial:
        result.failed = len(plan.errors)
        result.exit_code = 2
        return result

    blocking = {ItemStatus.MISSING, ItemStatus.INVALID, ItemStatus.CONFLICT, ItemStatus.PATH_REJECTED}
    blockers = [i for i in plan.items if i.status in blocking]
    if blockers and not allow_partial:
        result.failed = len(blockers)
        result.exit_code = 2
        return result

    actionable = [
        i
        for i in plan.items
        if i.status in {ItemStatus.PLANNED, ItemStatus.DUPLICATE}
    ]
    # DUPLICATE is already on disk with same hash — count as noop without re-copy
    for item in plan.items:
        if item.status == ItemStatus.DUPLICATE:
            item.status = ItemStatus.SKIPPED_NOOP
            result.noop += 1

    to_copy = [i for i in plan.items if i.status == ItemStatus.PLANNED]
    for item in to_copy:
        status = _copy_one(item)
        if status == ItemStatus.COPIED:
            result.copied += 1
        elif status == ItemStatus.SKIPPED_NOOP:
            result.noop += 1
        else:
            result.failed += 1

    if result.failed and not allow_partial:
        result.exit_code = 3
        # Do NOT publish batch.yaml on copy failure
        return result

    success_items = [
        i
        for i in plan.items
        if i.status in {ItemStatus.COPIED, ItemStatus.SKIPPED_NOOP, ItemStatus.DUPLICATE}
    ]

    if write_records and success_items:
        record_dir = Path(plan.record_dir)
        record_dir.mkdir(parents=True, exist_ok=True)

        prompt_text = _build_prompt_txt(plan, success_items)
        _atomic_write_text(record_dir / "prompt.txt", prompt_text)

        provenance = _build_provenance(plan, success_items)
        _atomic_write_text(
            record_dir / "import-provenance.json",
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        )
        result.records_written = True

        if publish_batch:
            # Atomic LAST after copies + other records
            manifest = _build_batch_manifest(plan, success_items)
            _atomic_write_text(
                record_dir / "batch.yaml",
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            )
            result.batch_published = True

    result.exit_code = 0 if result.failed == 0 else 3
    return result


def run_apply(**plan_kwargs: Any) -> ApplyResult:
    plan = build_plan(**plan_kwargs)
    return apply_plan(plan)


def run_resume(**plan_kwargs: Any) -> ApplyResult:
    """Resume after interrupt: identical to apply (hash-equal destinations are no-ops)."""
    return run_apply(**plan_kwargs)


def sync_only_marker_ok(plan: PlanReport) -> bool:
    """True when all library files already match and batch.yaml exists (sync retry safe)."""
    batch = Path(plan.record_dir) / "batch.yaml"
    if not batch.is_file():
        return False
    for item in plan.items:
        if item.status not in {ItemStatus.DUPLICATE, ItemStatus.SKIPPED_NOOP, ItemStatus.PLANNED}:
            # PLANNED means missing on disk — not sync-only ready
            if item.status == ItemStatus.PLANNED:
                return False
            if item.status in {ItemStatus.MISSING, ItemStatus.INVALID, ItemStatus.CONFLICT, ItemStatus.PATH_REJECTED}:
                return False
    # After re-plan, duplicates mean files present; planned means not present
    return all(
        i.status == ItemStatus.DUPLICATE
        or (i.dest_path and Path(i.dest_path).is_file())
        for i in plan.items
        if i.status not in {ItemStatus.PATH_REJECTED, ItemStatus.MISSING, ItemStatus.INVALID}
    )
