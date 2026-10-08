#!/usr/bin/env python3
"""Durable orchestration for schema-v1 character-pack candidate jobs.

This module deliberately stops at the renderer/importer boundary.  Callers supply
those adapters, which keeps contract tests deterministic and prevents this layer
from acquiring GPU, Gallery-database, or provider side effects.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
JOB_SCHEMA = ROOT / "schemas" / "character-pack-job-v1.schema.json"
MANIFEST_SCHEMA = ROOT / "schemas" / "character-pack-candidate-manifest-v1.schema.json"

FACE_SLOTS = (
    "face_front",
    "face_left30",
    "face_right30",
    "face_left90",
    "face_right90",
)
BODY_SLOTS = (
    "body_front",
    "body_three_quarter",
    "body_side",
    "body_back",
)
ALLOWED_ENGINES = ("qwen21", "krea2")
DEFAULT_ENGINES = {"face": "qwen21", "body": "krea2"}
MODEL_TYPES = {
    "qwen21": "qwen_image_21_uncensored_q4_k_m",
    "krea2": "krea2_turbo_edit",
}
ADAPTER_VERSION = 1
REQUEST_ID_RE = re.compile(r"^cpr-[A-Za-z0-9._-]+$")


class CharacterPackError(ValueError):
    """A durable job or adapter result violates the frozen contract."""


class Renderer(Protocol):
    def render(self, request: dict[str, Any]) -> Mapping[str, Any]: ...


class Importer(Protocol):
    def import_output(self, request: dict[str, Any], result: Mapping[str, Any]) -> str | None: ...


Clock = Callable[[], str]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CharacterPackError(f"invalid character-pack document: {path}") from exc
    if not isinstance(value, dict):
        raise CharacterPackError(f"character-pack document is not an object: {path}")
    return value


def _validator(path: Path) -> Draft202012Validator:
    return Draft202012Validator(_load(path))


def _validate_job(value: dict[str, Any]) -> None:
    errors = sorted(_validator(JOB_SCHEMA).iter_errors(value), key=lambda error: list(error.path))
    if errors:
        raise CharacterPackError(f"invalid character-pack job: {errors[0].message}")


def _validate_manifest(value: dict[str, Any]) -> None:
    errors = sorted(_validator(MANIFEST_SCHEMA).iter_errors(value), key=lambda error: list(error.path))
    if errors:
        raise CharacterPackError(f"invalid character-pack manifest: {errors[0].message}")


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _stable_hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_bytes(encoded)


def _build_review_sheet(target: Path, members: list[tuple[dict[str, Any], Path]], *, title: str, columns: int) -> dict[str, Any]:
    """Build a human-review aid without turning the sheet into a source reference."""
    from PIL import Image, ImageDraw, ImageFont, ImageOps

    tile_width, tile_height, caption_height = 256, 320, 28
    gap, header = 12, 48
    rows = (len(members) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (gap + columns * (tile_width + gap), header + gap + rows * (tile_height + caption_height + gap)),
        "#eee9df",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((gap, 16), title, fill="#2b2926", font=font)
    for index, (member, source) in enumerate(members):
        row, column = divmod(index, columns)
        x = gap + column * (tile_width + gap)
        y = header + gap + row * (tile_height + caption_height + gap)
        try:
            with Image.open(source) as opened:
                image = ImageOps.contain(opened.convert("RGB"), (tile_width, tile_height))
        except Exception as exc:
            raise CharacterPackError(f"could not render review sheet member: {member['slot_id']}") from exc
        tile = Image.new("RGB", (tile_width, tile_height), "#d8d1c6")
        tile.paste(image, ((tile_width - image.width) // 2, (tile_height - image.height) // 2))
        sheet.paste(tile, (x, y))
        draw.text((x + 4, y + tile_height + 8), member["slot_id"], fill="#2b2926", font=font)
    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target, format="PNG")
    content = target.read_bytes()
    return {
        "file": target.parent.name + "/" + target.name,
        "sha256": _sha256_bytes(content),
        "byte_count": len(content),
        "source_slots": [member["slot_id"] for member, _ in members],
        "review_aid_only": True,
    }


def _verify_master(binding: Mapping[str, Any]) -> Path:
    path = Path(str(binding.get("path", ""))).resolve()
    if not path.is_file():
        raise CharacterPackError("frozen Master Face is missing")
    content = path.read_bytes()
    if len(content) != binding.get("byte_count"):
        raise CharacterPackError("frozen Master Face byte count changed")
    if _sha256_bytes(content) != binding.get("sha256"):
        raise CharacterPackError("frozen Master Face SHA-256 changed")
    return path


def _slot(slot_id: str) -> dict[str, Any]:
    return {
        "slot_id": slot_id,
        "stage": "face" if slot_id.startswith("face_") else "body",
        "required": True,
        "status": "pending",
        "attempts": 0,
        "last_error": None,
    }


def create_job(
    directory: Path,
    *,
    character_id: str,
    requested_by: str,
    dna: Mapping[str, Any],
    master_face: Mapping[str, Any],
    include_body: bool = False,
    job_id: str | None = None,
    clock: Clock = utc_now,
) -> "CharacterPackJob":
    """Create a new job while freezing the supplied DNA and Master Face bindings."""
    directory = Path(directory).resolve()
    if directory.exists():
        raise CharacterPackError(f"character-pack job directory already exists: {directory}")
    _verify_master(master_face)
    now = clock()
    identifier = job_id or f"cpj-{uuid.uuid4().hex}"
    slot_ids = FACE_SLOTS + (BODY_SLOTS if include_body else ())
    job = {
        "schema_version": 1,
        "kind": "character_pack_job",
        "job_id": identifier,
        "character_id": character_id,
        "status": "ready",
        "requested_by": requested_by,
        "created_at": now,
        "updated_at": now,
        "dna": deepcopy(dict(dna)),
        "master_face": deepcopy(dict(master_face)),
        "engine_policy": {
            "face_default": "qwen21",
            "body_default": "krea2",
            "allowed": list(ALLOWED_ENGINES),
            "fallback": "none",
        },
        "slots": [_slot(slot_id) for slot_id in slot_ids],
    }
    suffix = identifier.removeprefix("cpj-")
    manifest = {
        "schema_version": 1,
        "kind": "character_pack_candidate_manifest",
        "manifest_id": f"cpm-{suffix}",
        "job_id": identifier,
        "character_id": character_id,
        "dna": deepcopy(dict(dna)),
        "master_face": deepcopy(dict(master_face)),
        "published_at": now,
        "slots": [
            {
                "slot_id": slot["slot_id"],
                "stage": slot["stage"],
                "selected_candidate_id": None,
                "candidates": [],
            }
            for slot in job["slots"]
        ],
    }
    _validate_job(job)
    _validate_manifest(manifest)
    directory.mkdir(parents=True, exist_ok=False)
    _atomic_json(directory / "candidate-manifest.json", manifest)
    _atomic_json(directory / "job.json", job)
    return CharacterPackJob(directory, clock=clock)


class CharacterPackJob:
    """A resumable schema-v1 job with append-only candidate lists."""

    def __init__(self, directory: Path, *, clock: Clock = utc_now):
        self.directory = Path(directory).resolve()
        self.job_path = self.directory / "job.json"
        self.manifest_path = self.directory / "candidate-manifest.json"
        self.clock = clock
        self.job = _load(self.job_path)
        self.manifest = _load(self.manifest_path)
        _validate_job(self.job)
        _validate_manifest(self.manifest)
        self._validate_pair()

    def _validate_pair(self) -> None:
        for field in ("job_id", "character_id", "dna", "master_face"):
            if self.job[field] != self.manifest[field]:
                raise CharacterPackError(f"job and candidate manifest disagree on {field}")
        job_slots = [(item["slot_id"], item["stage"]) for item in self.job["slots"]]
        manifest_slots = [(item["slot_id"], item["stage"]) for item in self.manifest["slots"]]
        if job_slots != manifest_slots or len({slot_id for slot_id, _ in job_slots}) != len(job_slots):
            raise CharacterPackError("job and candidate manifest slot sets disagree")

    def _job_slot(self, slot_id: str) -> dict[str, Any]:
        for slot in self.job["slots"]:
            if slot["slot_id"] == slot_id:
                return slot
        raise CharacterPackError(f"slot is not part of this job: {slot_id}")

    def _manifest_slot(self, slot_id: str) -> dict[str, Any]:
        for slot in self.manifest["slots"]:
            if slot["slot_id"] == slot_id:
                return slot
        raise CharacterPackError(f"slot is not part of this manifest: {slot_id}")

    def default_engine_map(self, slot_ids: tuple[str, ...] | list[str] | None = None) -> dict[str, str]:
        targets = slot_ids or [slot["slot_id"] for slot in self.job["slots"]]
        return {
            slot_id: self.job["engine_policy"][f"{self._job_slot(slot_id)['stage']}_default"]
            for slot_id in targets
        }

    def _persist_job(self) -> None:
        self.job["updated_at"] = self.clock()
        _validate_job(self.job)
        _atomic_json(self.job_path, self.job)

    def _persist_manifest(self) -> None:
        self.manifest["published_at"] = self.clock()
        _validate_manifest(self.manifest)
        _atomic_json(self.manifest_path, self.manifest)

    def _candidate_attempt(self, candidate_id: str) -> int:
        marker = candidate_id.rsplit(".a", 1)
        if len(marker) == 2 and marker[1].isdigit():
            return int(marker[1])
        return 0

    def _reconcile_slot(self, slot_id: str) -> None:
        job_slot = self._job_slot(slot_id)
        candidates = self._manifest_slot(slot_id)["candidates"]
        completed_attempt = max((self._candidate_attempt(item["candidate_id"]) for item in candidates), default=0)
        job_slot["attempts"] = max(job_slot["attempts"], completed_attempt)
        if candidates and job_slot["status"] in {"pending", "queued", "running", "failed"}:
            job_slot["status"] = "needs_review"
            job_slot["last_error"] = None

    def _update_overall_status(self) -> None:
        required = [slot for slot in self.job["slots"] if slot["required"]]
        statuses = {slot["status"] for slot in required}
        if "running" in statuses or "queued" in statuses:
            self.job["status"] = "generating"
        elif "failed" in statuses:
            self.job["status"] = "failed"
        elif required and all(slot["status"] == "selected" for slot in required):
            self.job["status"] = "ready_for_pack_approval"
        elif "selected" in statuses:
            self.job["status"] = "partially_reviewed"
        elif required and all(self._manifest_slot(slot["slot_id"])["candidates"] for slot in required):
            self.job["status"] = "needs_review"
        else:
            self.job["status"] = "ready"

    def _invoke_renderer(self, renderer: Renderer | Callable[[dict[str, Any]], Mapping[str, Any]], request: dict[str, Any]) -> Mapping[str, Any]:
        call = getattr(renderer, "render", renderer)
        result = call(deepcopy(request))
        if not isinstance(result, Mapping):
            raise CharacterPackError("renderer returned no result object")
        return result

    def _invoke_importer(
        self,
        importer: Importer | Callable[[dict[str, Any], Mapping[str, Any]], str | None],
        request: dict[str, Any],
        result: Mapping[str, Any],
    ) -> str | None:
        call = getattr(importer, "import_output", importer)
        asset_id = call(deepcopy(request), deepcopy(dict(result)))
        if asset_id is not None and (not isinstance(asset_id, str) or not asset_id.strip()):
            raise CharacterPackError("importer returned an invalid Gallery asset id")
        return asset_id

    def generate(
        self,
        slot_id: str,
        *,
        engine: str,
        renderer: Renderer | Callable[[dict[str, Any]], Mapping[str, Any]],
        importer: Importer | Callable[[dict[str, Any], Mapping[str, Any]], str | None],
    ) -> dict[str, Any]:
        """Append one candidate attempt for a logical slot using exactly ``engine``."""
        slot = self._job_slot(slot_id)
        if engine not in self.job["engine_policy"]["allowed"]:
            raise CharacterPackError(f"engine is not allowed for this job: {engine}")
        _verify_master(self.job["master_face"])
        self._reconcile_slot(slot_id)
        attempt = slot["attempts"] + 1
        candidate_id = f"{self.job['job_id']}.{slot_id}.a{attempt:03d}"
        prompt = (
            f"Character pack {slot_id}; preserve the frozen Master Face identity exactly; "
            f"DNA binding {self.job['dna']['stable_dna_sha256']}."
        )
        settings = {
            "slot_id": slot_id,
            "stage": slot["stage"],
            "engine": engine,
            "model_type": MODEL_TYPES[engine],
            "fallback": "none",
        }
        request = {
            "request_id": candidate_id,
            "job_id": self.job["job_id"],
            "character_id": self.job["character_id"],
            "slot_id": slot_id,
            "stage": slot["stage"],
            "attempt": attempt,
            "engine": engine,
            "model_type": MODEL_TYPES[engine],
            "adapter_version": ADAPTER_VERSION,
            "prompt": prompt,
            "settings": settings,
            "dna": deepcopy(self.job["dna"]),
            "master_face": deepcopy(self.job["master_face"]),
            "requested_by": self.job["requested_by"],
        }
        slot.update({"status": "running", "attempts": attempt, "last_error": None})
        self._update_overall_status()
        self._persist_job()
        try:
            result = self._invoke_renderer(renderer, request)
            if result.get("model_type", MODEL_TYPES[engine]) != MODEL_TYPES[engine]:
                raise CharacterPackError("renderer changed the selected engine model; fallback is forbidden")
            output_path = Path(str(result.get("output_path", ""))).resolve()
            if not output_path.is_file():
                raise CharacterPackError("renderer output is missing")
            content = output_path.read_bytes()
            if not content:
                raise CharacterPackError("renderer output is empty")
            for required in ("run_id", "session_id", "executor"):
                if not isinstance(result.get(required), str) or not str(result[required]).strip():
                    raise CharacterPackError(f"renderer result is missing {required}")
            asset_id = self._invoke_importer(importer, request, result)
            candidate = {
                "candidate_id": candidate_id,
                "engine": engine,
                "model_type": MODEL_TYPES[engine],
                "adapter_version": ADAPTER_VERSION,
                "prompt_sha256": _sha256_bytes(prompt.encode("utf-8")),
                "settings_sha256": _stable_hash(settings),
                "seed": result.get("seed"),
                "requested_by": self.job["requested_by"],
                "executor": result["executor"],
                "run_id": result["run_id"],
                "session_id": result["session_id"],
                "output": {
                    "path": str(output_path),
                    "sha256": _sha256_bytes(content),
                    "byte_count": len(content),
                    "asset_id": asset_id,
                },
                "review_state": "needs_review",
                "automatic_qa": deepcopy(dict(result.get("automatic_qa", {}))),
                "created_at": self.clock(),
            }
            manifest_slot = self._manifest_slot(slot_id)
            if any(item["candidate_id"] == candidate_id for item in manifest_slot["candidates"]):
                raise CharacterPackError(f"candidate attempt already exists: {candidate_id}")
            manifest_slot["candidates"].append(candidate)
            self._persist_manifest()
            slot.update({
                "status": "selected" if manifest_slot["selected_candidate_id"] is not None else "needs_review",
                "last_error": None,
            })
            self._update_overall_status()
            self._persist_job()
            return deepcopy(candidate)
        except Exception as exc:
            slot.update({"status": "failed", "last_error": str(exc)})
            self._update_overall_status()
            self._persist_job()
            if isinstance(exc, CharacterPackError):
                raise
            raise CharacterPackError(f"candidate attempt failed: {exc}") from exc

    def run_pending(
        self,
        *,
        engine_by_slot: Mapping[str, str],
        renderer: Renderer | Callable[[dict[str, Any]], Mapping[str, Any]],
        importer: Importer | Callable[[dict[str, Any], Mapping[str, Any]], str | None],
    ) -> list[dict[str, Any]]:
        """Generate each candidate-less required slot once.

        The caller must pass an engine for every slot that still needs work.  This
        makes the per-slot choice explicit even when it came from
        :meth:`default_engine_map` and prevents an adapter-level fallback.
        """
        pending: list[str] = []
        reconciled = False
        for slot in self.job["slots"]:
            self._reconcile_slot(slot["slot_id"])
            if slot["required"] and not self._manifest_slot(slot["slot_id"])["candidates"]:
                pending.append(slot["slot_id"])
            else:
                reconciled = True
        missing = [slot_id for slot_id in pending if slot_id not in engine_by_slot]
        extras = [slot_id for slot_id in engine_by_slot if slot_id not in pending]
        if missing:
            raise CharacterPackError(f"explicit engine selection missing for slots: {', '.join(missing)}")
        if extras:
            raise CharacterPackError(f"engine selection includes completed or unknown slots: {', '.join(extras)}")
        if reconciled:
            self._update_overall_status()
            self._persist_job()
        candidates = []
        for slot_id in pending:
            candidates.append(
                self.generate(slot_id, engine=engine_by_slot[slot_id], renderer=renderer, importer=importer)
            )
        return candidates

    def regenerate(
        self,
        slot_id: str,
        *,
        engine: str,
        renderer: Renderer | Callable[[dict[str, Any]], Mapping[str, Any]],
        importer: Importer | Callable[[dict[str, Any], Mapping[str, Any]], str | None],
    ) -> dict[str, Any]:
        """Append a new candidate without changing or deleting earlier candidates."""
        return self.generate(slot_id, engine=engine, renderer=renderer, importer=importer)

    def _request_path(self, request_id: str) -> Path:
        if not REQUEST_ID_RE.fullmatch(request_id):
            raise CharacterPackError("invalid character-pack regeneration request id")
        return self.directory / "regeneration-requests" / f"{request_id}.json"

    def queue_regeneration(self, slot_id: str, *, engine: str, request_id: str) -> dict[str, Any]:
        """Durably queue one explicit slot/engine request without starting a renderer."""
        slot = self._job_slot(slot_id)
        if engine not in self.job["engine_policy"]["allowed"]:
            raise CharacterPackError(f"engine is not allowed for this job: {engine}")
        if slot["status"] in {"queued", "running"}:
            raise CharacterPackError(f"slot already has generation in flight: {slot_id}")
        _verify_master(self.job["master_face"])
        path = self._request_path(request_id)
        if path.exists():
            raise CharacterPackError(f"regeneration request already exists: {request_id}")
        now = self.clock()
        request = {
            "schema_version": 1,
            "kind": "character_pack_regeneration_request",
            "request_id": request_id,
            "job_id": self.job["job_id"],
            "character_id": self.job["character_id"],
            "slot_id": slot_id,
            "engine": engine,
            "status": "queued",
            "created_at": now,
            "updated_at": now,
            "candidate_id": None,
            "error": None,
        }
        _atomic_json(path, request)
        slot.update({"status": "queued", "last_error": None})
        self._update_overall_status()
        self._persist_job()
        return deepcopy(request)

    def run_regeneration_request(
        self,
        request_id: str,
        *,
        renderer: Renderer | Callable[[dict[str, Any]], Mapping[str, Any]],
        importer: Importer | Callable[[dict[str, Any], Mapping[str, Any]], str | None],
    ) -> dict[str, Any]:
        """Execute one queued request exactly once through the normal append-only path."""
        path = self._request_path(request_id)
        request = _load(path)
        if request.get("job_id") != self.job["job_id"] or request.get("character_id") != self.job["character_id"]:
            raise CharacterPackError("regeneration request does not belong to this job")
        if request.get("status") != "queued":
            raise CharacterPackError(f"regeneration request is not queued: {request_id}")
        slot_id = str(request.get("slot_id") or "")
        engine = str(request.get("engine") or "")
        self._job_slot(slot_id)
        if engine not in self.job["engine_policy"]["allowed"]:
            raise CharacterPackError(f"engine is not allowed for this job: {engine}")
        request.update({"status": "running", "updated_at": self.clock()})
        _atomic_json(path, request)
        try:
            candidate = self.regenerate(slot_id, engine=engine, renderer=renderer, importer=importer)
            request.update({
                "status": "completed",
                "updated_at": self.clock(),
                "candidate_id": candidate["candidate_id"],
                "error": None,
            })
            _atomic_json(path, request)
            return deepcopy(candidate)
        except Exception as exc:
            request.update({"status": "failed", "updated_at": self.clock(), "error": str(exc)})
            _atomic_json(path, request)
            slot = self._job_slot(slot_id)
            slot.update({"status": "failed", "last_error": str(exc)})
            self._update_overall_status()
            self._persist_job()
            raise

    def fail_regeneration_request(self, request_id: str, error: str) -> dict[str, Any]:
        """Fail a queued request when its worker cannot be launched."""
        path = self._request_path(request_id)
        request = _load(path)
        if request.get("job_id") != self.job["job_id"] or request.get("status") not in {"queued", "running"}:
            raise CharacterPackError(f"regeneration request cannot be failed: {request_id}")
        message = str(error).strip() or "worker launch failed"
        request.update({"status": "failed", "updated_at": self.clock(), "error": message})
        _atomic_json(path, request)
        slot = self._job_slot(str(request.get("slot_id") or ""))
        slot.update({"status": "failed", "last_error": message})
        self._update_overall_status()
        self._persist_job()
        return deepcopy(request)

    def _candidate(self, slot_id: str, candidate_id: str) -> dict[str, Any]:
        for candidate in self._manifest_slot(slot_id)["candidates"]:
            if candidate["candidate_id"] == candidate_id:
                return candidate
        raise CharacterPackError(f"candidate is not part of slot {slot_id}: {candidate_id}")

    def select(self, slot_id: str, candidate_id: str) -> dict[str, Any]:
        """Select exactly one candidate for a slot, preserving every candidate entry."""
        manifest_slot = self._manifest_slot(slot_id)
        selected = self._candidate(slot_id, candidate_id)
        for candidate in manifest_slot["candidates"]:
            if candidate["review_state"] == "selected":
                candidate["review_state"] = "needs_review"
        selected["review_state"] = "selected"
        manifest_slot["selected_candidate_id"] = candidate_id
        self._persist_manifest()
        job_slot = self._job_slot(slot_id)
        job_slot.update({"status": "selected", "last_error": None})
        self._update_overall_status()
        self._persist_job()
        return deepcopy(selected)

    def select_candidate(self, slot_id: str, candidate_id: str) -> dict[str, Any]:
        """Integration-facing alias matching the Studio presentation action."""
        return self.select(slot_id, candidate_id)

    def reject(self, slot_id: str, candidate_id: str) -> dict[str, Any]:
        """Mark a candidate rejected without deleting its output or provenance."""
        manifest_slot = self._manifest_slot(slot_id)
        rejected = self._candidate(slot_id, candidate_id)
        rejected["review_state"] = "rejected"
        if manifest_slot["selected_candidate_id"] == candidate_id:
            manifest_slot["selected_candidate_id"] = None
        self._persist_manifest()
        job_slot = self._job_slot(slot_id)
        remaining = [
            candidate
            for candidate in manifest_slot["candidates"]
            if candidate["review_state"] != "rejected"
        ]
        if manifest_slot["selected_candidate_id"] is not None:
            status = "selected"
        else:
            status = "needs_review" if remaining else "rejected"
        job_slot.update({"status": status, "last_error": None})
        self._update_overall_status()
        self._persist_job()
        return deepcopy(rejected)

    def reject_candidate(self, slot_id: str, candidate_id: str) -> dict[str, Any]:
        """Integration-facing alias matching the Studio presentation action."""
        return self.reject(slot_id, candidate_id)

    def attach_gallery_asset(self, slot_id: str, candidate_id: str, asset_id: str) -> dict[str, Any]:
        """Bind an imported Gallery asset after verifying the candidate bytes again."""
        if not isinstance(asset_id, str) or not asset_id.strip():
            raise CharacterPackError("Gallery asset id is invalid")
        candidate = self._candidate(slot_id, candidate_id)
        current = candidate["output"].get("asset_id")
        if current not in (None, asset_id):
            raise CharacterPackError(f"candidate already names a different Gallery asset: {candidate_id}")
        path = Path(candidate["output"]["path"]).resolve()
        if not path.is_file():
            raise CharacterPackError(f"candidate output is missing: {candidate_id}")
        content = path.read_bytes()
        if len(content) != candidate["output"]["byte_count"] or _sha256_bytes(content) != candidate["output"]["sha256"]:
            raise CharacterPackError(f"candidate output changed before Gallery binding: {candidate_id}")
        candidate["output"]["asset_id"] = asset_id
        self._persist_manifest()
        return deepcopy(candidate)

    def _selected_required(self) -> list[tuple[dict[str, Any], dict[str, Any]]]:
        selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for job_slot in self.job["slots"]:
            if not job_slot["required"]:
                continue
            manifest_slot = self._manifest_slot(job_slot["slot_id"])
            selected_id = manifest_slot["selected_candidate_id"]
            matches = [
                candidate
                for candidate in manifest_slot["candidates"]
                if candidate["review_state"] == "selected"
            ]
            if not isinstance(selected_id, str) or len(matches) != 1 or matches[0]["candidate_id"] != selected_id:
                raise CharacterPackError(
                    f"required slot must have exactly one selected candidate: {job_slot['slot_id']}"
                )
            candidate = matches[0]
            asset_id = candidate["output"].get("asset_id")
            if not isinstance(asset_id, str) or not asset_id.strip():
                raise CharacterPackError(
                    f"selected candidate lacks a durable Gallery asset id: {candidate['candidate_id']}"
                )
            path = Path(candidate["output"]["path"]).resolve()
            if not path.is_file():
                raise CharacterPackError(f"selected candidate output is missing: {candidate['candidate_id']}")
            content = path.read_bytes()
            if len(content) != candidate["output"]["byte_count"]:
                raise CharacterPackError(f"selected candidate byte count changed: {candidate['candidate_id']}")
            if _sha256_bytes(content) != candidate["output"]["sha256"]:
                raise CharacterPackError(f"selected candidate SHA-256 changed: {candidate['candidate_id']}")
            selected.append((job_slot, candidate))
        return selected

    def prepare_identity_set(self, *, approved_by: str, approved_at: str | None = None) -> dict[str, Any]:
        """Prepare a deterministic approved-set document after all publish checks."""
        if approved_by != "user":
            raise CharacterPackError("final character-pack approval requires an explicit user decision")
        source_bytes = self.manifest_path.read_bytes()
        source = json.loads(source_bytes)
        _validate_manifest(source)
        if source != self.manifest:
            raise CharacterPackError("candidate manifest changed after this job was loaded")
        selected = self._selected_required()
        approved_at = approved_at or self.clock()
        members = []
        for slot, candidate in selected:
            suffix = Path(candidate["output"]["path"]).suffix.lower() or ".bin"
            members.append({
                "slot_id": slot["slot_id"],
                "stage": slot["stage"],
                "file": f"members/{slot['slot_id']}{suffix}",
                "sha256": candidate["output"]["sha256"],
                "byte_count": candidate["output"]["byte_count"],
                "asset_id": candidate["output"]["asset_id"],
                "candidate_id": candidate["candidate_id"],
                "engine": candidate["engine"],
                "model_type": candidate["model_type"],
            })
        return {
            "schema_version": 1,
            "character_id": self.job["character_id"],
            "review_state": "approved",
            "approved_by": approved_by,
            "approved_at": approved_at,
            "source": {
                "kind": self.manifest["kind"],
                "job_id": self.job["job_id"],
                "manifest_id": self.manifest["manifest_id"],
                "manifest_path": str(self.manifest_path),
                "manifest_sha256": _sha256_bytes(source_bytes),
                "snapshot": "inputs/candidate-manifest.json",
                "dna": deepcopy(self.job["dna"]),
                "master_face": deepcopy(self.job["master_face"]),
            },
            "members": members,
        }

    def publish_identity_set(
        self,
        destination: Path,
        *,
        approved_by: str,
        approved_at: str | None = None,
    ) -> Path:
        """Copy selected bytes and atomically publish one immutable set manifest."""
        destination = Path(destination).resolve()
        if destination.exists():
            raise FileExistsError(f"immutable identity-set destination already exists: {destination}")
        prepared = self.prepare_identity_set(approved_by=approved_by, approved_at=approved_at)
        source_manifest_bytes = self.manifest_path.read_bytes()
        if _sha256_bytes(source_manifest_bytes) != prepared["source"]["manifest_sha256"]:
            raise CharacterPackError("candidate manifest changed during identity-set preparation")
        selected = self._selected_required()
        destination.mkdir(parents=True, exist_ok=False)
        members_dir = destination / "members"
        inputs_dir = destination / "inputs"
        sheets_dir = destination / "sheets"
        members_dir.mkdir()
        inputs_dir.mkdir()
        for (_, candidate), member in zip(selected, prepared["members"], strict=True):
            source = Path(candidate["output"]["path"]).resolve()
            target = destination / member["file"]
            shutil.copyfile(source, target)
            copied = target.read_bytes()
            if len(copied) != member["byte_count"] or _sha256_bytes(copied) != member["sha256"]:
                raise CharacterPackError(f"identity-set member copy changed: {member['slot_id']}")
        member_sources = [(member, destination / member["file"]) for member in prepared["members"]]
        face_sources = [item for item in member_sources if item[0]["stage"] == "face"]
        body_sources = [item for item in member_sources if item[0]["stage"] == "body"]
        sheets = []
        if face_sources:
            sheets.append(_build_review_sheet(
                sheets_dir / "face-sheet.png", face_sources,
                title=f"{self.job['character_id']} - approved face views", columns=len(face_sources),
            ))
        if body_sources:
            sheets.append(_build_review_sheet(
                sheets_dir / "body-sheet.png", body_sources,
                title=f"{self.job['character_id']} - approved body views", columns=len(body_sources),
            ))
        sheets.append(_build_review_sheet(
            sheets_dir / "master-sheet.png", member_sources,
            title=f"{self.job['character_id']} - approved Character Pack",
            columns=min(5, len(member_sources)),
        ))
        prepared["sheets"] = sheets
        (inputs_dir / "candidate-manifest.json").write_bytes(source_manifest_bytes)
        manifest_path = destination / "identity-set.json"
        pending = destination / ".identity-set.json.pending"
        with pending.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(prepared, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.link(pending, manifest_path)
        pending.unlink()
        self.job["status"] = "approved"
        self._persist_job()
        return manifest_path
