"""Build dry-run / plan reports from manifest or source folder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .hashutil import sha256_file
from .models import ImportItem, ItemStatus, PlanReport
from .paths import PathSafetyError, ensure_under_allowed_roots, normalize_user_path, safe_dest_name
from .probe import SUPPORTED_SUFFIXES, probe_media


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def parse_manifest_items(
    manifest: dict[str, Any],
    *,
    default_engine: str,
    default_provider: str | None,
    default_model: str | None,
) -> list[ImportItem]:
    """Accept several manifest shapes used in this repo."""
    items_raw = (
        manifest.get("items")
        or manifest.get("images")
        or manifest.get("files")
        or manifest.get("media")
        or []
    )
    if not isinstance(items_raw, list):
        raise ValueError("manifest items must be a list")

    top_engine = str(manifest.get("engine") or default_engine)
    top_provider = manifest.get("provider", default_provider)
    top_model = manifest.get("model", default_model)

    out: list[ImportItem] = []
    for idx, raw in enumerate(items_raw):
        if isinstance(raw, str):
            source = raw
            dest_name = Path(raw).name
            engine = top_engine
            provider = top_provider
            model = top_model
            prompt = None
            refs: list[str] = []
            user_request = None
            created_at = None
            session_id = None
            title = None
        elif isinstance(raw, dict):
            source = (
                raw.get("source")
                or raw.get("source_path")
                or raw.get("path")
                or raw.get("original_path")
            )
            if not source and raw.get("file"):
                # relative file name only — caller must supply source-dir
                source = raw.get("file")
            if not source:
                raise ValueError(f"manifest item[{idx}] missing source path")
            dest_name = str(raw.get("dest_name") or raw.get("file") or Path(str(source)).name)
            engine = str(raw.get("engine") or top_engine)
            provider = raw.get("provider", top_provider)
            model = raw.get("model", top_model)
            prompt = raw.get("prompt") or raw.get("prompt_text")
            refs = [str(x) for x in _as_list(raw.get("references") or raw.get("reference") or raw.get("reference_image"))]
            user_request = raw.get("user_request") or raw.get("request")
            created_at = raw.get("created_at") or raw.get("timestamp")
            session_id = raw.get("session_id")
            title = raw.get("title")
        else:
            raise ValueError(f"manifest item[{idx}] must be str or object")

        out.append(
            ImportItem(
                source_path=str(source),
                dest_name=safe_dest_name(dest_name),
                engine=engine,
                provider=str(provider) if provider is not None else None,
                model=str(model) if model is not None else None,
                prompt=str(prompt) if prompt is not None else None,
                references=refs,
                user_request=str(user_request) if user_request is not None else None,
                created_at=str(created_at) if created_at is not None else None,
                session_id=str(session_id) if session_id else None,
                title=str(title) if title else None,
            )
        )
    return out


def items_from_source_dir(
    source_dir: Path,
    *,
    engine: str,
    provider: str | None,
    model: str | None,
    prompt: str | None = None,
) -> list[ImportItem]:
    files = sorted(
        p for p in source_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES
    )
    return [
        ImportItem(
            source_path=str(p),
            dest_name=p.name,
            engine=engine,
            provider=provider,
            model=model,
            prompt=prompt,
        )
        for p in files
    ]


def _unique_prompts(items: Iterable[ImportItem]) -> list[str]:
    seen: list[str] = []
    for item in items:
        p = (item.prompt or "").strip()
        if p and p not in seen:
            seen.append(p)
    return seen


def build_plan(
    *,
    character_id: str,
    session_id: str,
    title: str,
    engine: str,
    library_root: Path,
    record_root: Path,
    visibility: str = "standard",
    provider: str | None = None,
    model: str | None = None,
    manifest_path: Path | None = None,
    source_dir: Path | None = None,
    allowed_source_roots: list[Path] | None = None,
    shared_prompt: str | None = None,
    prompt_strategy: str = "auto",
    probe: bool = True,
    ffprobe_bin: str | None = None,
) -> PlanReport:
    library_root = normalize_user_path(library_root)
    record_root = normalize_user_path(record_root)

    if not character_id:
        raise ValueError("character-id is required")
    if not session_id:
        raise ValueError("session-id is required")
    if not engine:
        raise ValueError("engine is required (first path element under outputs/)")

    items: list[ImportItem] = []
    errors: list[str] = []
    warnings: list[str] = []

    roots: list[Path] = []
    if allowed_source_roots:
        roots.extend(normalize_user_path(r) for r in allowed_source_roots)
    if source_dir is not None:
        roots.append(normalize_user_path(source_dir))
    if manifest_path is not None:
        roots.append(normalize_user_path(manifest_path).parent)

    # Deduplicate roots while preserving order
    seen_roots: set[str] = set()
    uniq_roots: list[Path] = []
    for r in roots:
        key = str(r.resolve()) if r.exists() else str(r.absolute())
        if key not in seen_roots:
            seen_roots.add(key)
            uniq_roots.append(r)

    if manifest_path is not None:
        manifest = _load_json(normalize_user_path(manifest_path))
        if not isinstance(manifest, dict):
            raise ValueError("manifest root must be a JSON object")
        items.extend(
            parse_manifest_items(
                manifest,
                default_engine=engine,
                default_provider=provider,
                default_model=model,
            )
        )
        # Resolve relative "file" entries against source_dir if provided
        if source_dir is not None:
            src = normalize_user_path(source_dir)
            for item in items:
                p = Path(item.source_path)
                if not p.is_absolute():
                    candidate = src / p
                    if candidate.exists():
                        item.source_path = str(candidate)

    if source_dir is not None and manifest_path is None:
        items.extend(
            items_from_source_dir(
                normalize_user_path(source_dir),
                engine=engine,
                provider=provider,
                model=model,
                prompt=shared_prompt,
            )
        )

    if shared_prompt:
        for item in items:
            if not item.prompt:
                item.prompt = shared_prompt

    if not items:
        errors.append("no media items found (provide --manifest and/or --source-dir with supported files)")

    if not uniq_roots:
        # Fall back: allow each item's parent once resolved — but without roots we reject abs escapes loosely
        # Require at least one root for safety.
        errors.append("no allowed source roots; pass --allowed-source-root and/or --source-dir / --manifest")

    asset_root = library_root / character_id / "generations" / session_id / "outputs"
    outputs_dir = asset_root / engine
    record_dir = record_root / session_id

    # Resolve prompt strategy
    prompts = _unique_prompts(items)
    strategy = prompt_strategy
    if strategy == "auto":
        strategy = "provenance" if len(prompts) > 1 else "shared"
    if len(prompts) > 1 and strategy == "shared":
        warnings.append(
            "multiple distinct prompts in one session; refusing to mash into one fake shared prompt — "
            "using provenance/file-tagged prompt.txt instead"
        )
        strategy = "provenance"

    # Dest name uniqueness within plan
    dest_index: dict[str, list[int]] = {}
    for i, item in enumerate(items):
        dest_index.setdefault(item.dest_name.lower(), []).append(i)
    for name, idxs in dest_index.items():
        if len(idxs) > 1:
            for i in idxs:
                items[i].status = ItemStatus.CONFLICT
                items[i].message = f"duplicate destination name within plan: {items[i].dest_name}"

    for item in items:
        if item.status == ItemStatus.CONFLICT and item.message and "within plan" in item.message:
            continue

        item.engine = item.engine or engine
        item.provider = item.provider or provider
        item.model = item.model or model

        dest_path = outputs_dir / item.dest_name
        item.dest_path = str(dest_path)

        if not uniq_roots:
            item.status = ItemStatus.PATH_REJECTED
            item.message = "no allowed source roots"
            continue

        try:
            resolved = ensure_under_allowed_roots(
                Path(item.source_path),
                uniq_roots,
                label=item.dest_name,
            )
        except PathSafetyError as exc:
            item.status = ItemStatus.PATH_REJECTED
            item.message = str(exc)
            continue

        item.resolved_source = str(resolved)
        if not resolved.is_file():
            item.status = ItemStatus.MISSING
            item.message = f"source file not found: {resolved}"
            continue

        try:
            item.sha256 = sha256_file(resolved)
        except OSError as exc:
            item.status = ItemStatus.INVALID
            item.message = f"cannot hash source: {exc}"
            continue

        if probe:
            media = probe_media(resolved, ffprobe_bin=ffprobe_bin)
            item.probe = media
            if media.kind not in {"image", "video"}:
                item.status = ItemStatus.INVALID
                item.message = media.error or "unsupported media"
                continue
            # Supported kinds only for v1
            if media.kind == "image" and media.mime not in {
                "image/png",
                "image/jpeg",
                "image/webp",
            }:
                item.status = ItemStatus.INVALID
                item.message = f"unsupported image mime: {media.mime}"
                continue
            if media.kind == "video" and media.mime not in {"video/mp4", "video/webm"}:
                item.status = ItemStatus.INVALID
                item.message = f"unsupported video mime/container: {media.mime or media.container}"
                continue

        if dest_path.exists():
            try:
                existing_hash = sha256_file(dest_path)
            except OSError as exc:
                item.status = ItemStatus.FAILED
                item.message = f"cannot hash existing dest: {exc}"
                continue
            if existing_hash == item.sha256:
                item.status = ItemStatus.DUPLICATE
                item.message = "same batch+file+hash — no-op"
            else:
                item.status = ItemStatus.CONFLICT
                item.message = (
                    f"destination exists with different content "
                    f"(dest={existing_hash[:12]}… src={item.sha256[:12]}…)"
                )
            continue

        item.status = ItemStatus.PLANNED
        item.message = "will copy"

    return PlanReport(
        character_id=character_id,
        session_id=session_id,
        title=title,
        engine=engine,
        library_root=str(library_root),
        record_root=str(record_root),
        visibility=visibility,
        provider=provider,
        model=model,
        record_dir=str(record_dir),
        outputs_dir=str(outputs_dir),
        asset_root=str(asset_root),
        items=items,
        errors=errors,
        warnings=warnings,
        prompt_strategy=strategy,
    )
