"""WanGP adapter: builds canonical Jobs from `tools/wangp_recorder.py` run records.

Sources (all read-only):
  <session>/runs/<run_id>/run.json          status, prompt, settings, artifacts, local_worker.pid
  <session>/runs/<run_id>/events.jsonl      queued/starting/running(+preview step events)/completed/failed
  <session>/session-provenance.json         requested_by / title / character (written by wangp_recorder session)
  <session>/batch.yaml                      scene session title, character, id, created_by
  <session>/prompt-trace.json               invoked_by (hermes | codex | web | grok | claude)
  <session>/handoff.json                    an agent's own session record, read for its requester only
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

from .. import eta as eta_mod
from ..jobs import ACTIVE_STATUSES, COMPLETED_STATUSES, FAILED_STATUSES, Job, Output, Progress, output_kind
from ..util import parse_iso, read_json_safe, read_jsonl, seconds_between, utc_now

EXECUTOR_LOCAL_WORKER = "local-wangp-worker"
STALE_EVENT_MINUTES = 20
QUEUED_ABANDON_HOURS = 24


def default_pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        import psutil

        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except Exception:
        return False


# Files that make a directory a real production session rather than just the parent of a runs/ folder.
SESSION_MARKERS = ("batch.yaml", "session-provenance.json", "prompt-trace.json", "handoff.json", "sequence-status.json")


class SessionContext:
    __slots__ = ("title", "character_id", "session_id", "requested_by", "requested_by_basis", "kind", "session_dir",
                 "visibility", "is_session")

    def __init__(self, session_dir: Path) -> None:
        self.session_dir = str(session_dir)
        # A producer may pass any --runs-root, including the repository root. Only treat the parent as a session
        # when it actually looks like one; otherwise the run would inherit the repository's own name and README.
        self.is_session = any((session_dir / marker).is_file() for marker in SESSION_MARKERS)
        self.session_id = session_dir.name if self.is_session else None
        self.title = session_dir.name if self.is_session else ""
        self.character_id = None
        self.requested_by = "unknown"
        self.requested_by_basis = None
        self.kind = "unknown"
        self.visibility = None
        parent = session_dir.parent
        if parent.name == "02_generations" and parent.parent.name.startswith("ch-"):
            self.character_id = parent.parent.name
        prefix = session_dir.name.split("-", 1)[0].upper()
        if prefix in {"SCENE", "FACE", "VARIATION", "VIDEO", "NIGHT"}:
            self.kind = prefix.lower()

    def to_dict(self) -> dict[str, Any]:
        return {k: getattr(self, k) for k in self.__slots__}


PROVENANCE_KEYS = ("requested_by", "invoked_by", "actor", "created_by", "requester")


def explicit_requester(record: dict[str, Any] | None) -> str | None:
    """Return an explicitly recorded requester from a provenance record, or None."""
    if not isinstance(record, dict):
        return None
    for key in PROVENANCE_KEYS:
        value = record.get(key)
        if isinstance(value, str) and value.strip() and value.strip().lower() not in {"unknown", "none", "null"}:
            return value.strip().lower()
    return None


def load_session_context(session_dir: Path) -> SessionContext:
    ctx = SessionContext(session_dir)
    batch_path = session_dir / "batch.yaml"
    if yaml is not None and batch_path.is_file():
        try:
            batch = yaml.safe_load(batch_path.read_text(encoding="utf-8")) or {}
            session = batch.get("session") or {}
            ctx.title = str(session.get("title") or ctx.title)
            ctx.character_id = session.get("character_id") or ctx.character_id
            ctx.session_id = str(session.get("id") or ctx.session_id)
            ctx.visibility = session.get("visibility") or None
        except Exception:
            pass
    # Explicit provenance, first hit wins: prompt-trace.json (scene pipeline), then optional keys another
    # producer may write into batch.yaml / handoff.json / sequence-status.json. Nothing is guessed here.
    candidates: list[dict[str, Any]] = []
    # session-provenance.json is written by `tools/wangp_recorder.py session` and is the most authoritative
    provenance = read_json_safe(session_dir / "session-provenance.json")
    if isinstance(provenance, dict):
        candidates.append(provenance)
    trace = read_json_safe(session_dir / "prompt-trace.json")
    if isinstance(trace, dict):
        candidates.append(trace)
    if yaml is not None and batch_path.is_file():
        try:
            candidates.append((yaml.safe_load(batch_path.read_text(encoding="utf-8")) or {}).get("session") or {})
        except Exception:
            pass
    for name in ("handoff.json", "sequence-status.json"):
        extra = read_json_safe(session_dir / name)
        if isinstance(extra, dict):
            candidates.append(extra)
    for record in candidates:
        actor = explicit_requester(record)
        if actor:
            ctx.requested_by = actor
            ctx.requested_by_basis = "record"
            break
    if isinstance(provenance, dict):
        ctx.title = str(provenance.get("title") or ctx.title)
        ctx.character_id = provenance.get("character_id") or ctx.character_id
    if ctx.is_session and ctx.title == session_dir.name:
        readme = session_dir / "README.md"
        if readme.is_file():
            try:
                for line in readme.read_text(encoding="utf-8", errors="replace").splitlines()[:10]:
                    if line.startswith("# "):
                        ctx.title = line[2:].strip()
                        break
            except OSError:
                pass
    return ctx


class WangpRunAdapter:
    def __init__(
        self,
        scan_roots: list[Path],
        history_lookup: Callable[[str], float | None] | None = None,
        pid_alive: Callable[[int | None], bool] = default_pid_alive,
    ) -> None:
        self.scan_roots = [Path(p) for p in scan_roots]
        self.history_lookup = history_lookup or (lambda key: None)
        self.pid_alive = pid_alive
        self._run_cache: dict[str, tuple[tuple[float, float, int], Job]] = {}
        self._session_cache: dict[str, tuple[tuple[float, ...], SessionContext]] = {}

    # ------------------------------------------------------------------ discovery
    def run_dirs(self) -> list[Path]:
        found: list[Path] = []
        for root in self.scan_roots:
            if not root.is_dir():
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                base = os.path.basename(dirpath)
                if base == "runs":
                    for name in dirnames:
                        candidate = Path(dirpath) / name
                        if (candidate / "run.json").is_file():
                            found.append(candidate)
                    dirnames[:] = []
                    continue
                # never descend into media output trees or VCS metadata
                dirnames[:] = [d for d in dirnames if d not in {"outputs", ".git", "__pycache__", "node_modules"}]
        return found

    def session_context(self, session_dir: Path) -> SessionContext:
        key = str(session_dir)
        stamp = tuple(_mtime(session_dir / name) for name in
                      ("batch.yaml", "prompt-trace.json", "handoff.json", "sequence-status.json", "session-provenance.json"))
        cached = self._session_cache.get(key)
        if cached and cached[0] == stamp:
            return cached[1]
        ctx = load_session_context(session_dir)
        self._session_cache[key] = (stamp, ctx)
        return ctx

    def discover(self, now: datetime | None = None) -> list[Job]:
        now = now or utc_now()
        jobs: list[Job] = []
        seen: set[str] = set()
        for run_dir in self.run_dirs():
            key = str(run_dir)
            seen.add(key)
            run_path = run_dir / "run.json"
            events_path = run_dir / "events.jsonl"
            stamp = (_mtime(run_path), _mtime(events_path), _size(events_path))
            cached = self._run_cache.get(key)
            if cached and cached[0] == stamp and cached[1].is_terminal:
                jobs.append(cached[1])
                continue
            job = self.parse_run(run_dir, now)
            if job is None:
                continue
            self._run_cache[key] = (stamp, job)
            jobs.append(job)
        for key in list(self._run_cache):
            if key not in seen:
                del self._run_cache[key]
        return jobs

    # ------------------------------------------------------------------ parsing
    def parse_run(self, run_dir: Path, now: datetime | None = None) -> Job | None:
        now = now or utc_now()
        run = read_json_safe(run_dir / "run.json")
        if not isinstance(run, dict) or not run.get("run_id"):
            return None
        events = read_jsonl(run_dir / "events.jsonl")
        session_dir = run_dir.parent.parent if run_dir.parent.name == "runs" else run_dir.parent
        ctx = self.session_context(session_dir)
        settings = (run.get("settings") or {}).get("value") or {}
        if not isinstance(settings, dict):
            settings = {}
        model = settings.get("model_type") or settings.get("base_model_type")
        resolution = settings.get("resolution")
        steps_cfg = _int(settings.get("num_inference_steps"))
        frames = _int(settings.get("video_length"))
        batch_size = _int(settings.get("batch_size")) or 1
        items_total = _int(settings.get("repeat_generation")) or 1

        status = str(run.get("status") or "unknown")
        created = parse_iso(run.get("created_at"))
        started = None
        finished = None
        last_event_at = None
        item_idx = 0
        last_step: int | None = None
        total_steps: int | None = None
        phase: str | None = None
        runtime_pct: float | None = None
        observations: list[eta_mod.StepObservation] = []
        all_durations: list[float] = []
        last_preview_had_steps = False
        for event in events:
            at = parse_iso(event.get("at"))
            state = event.get("state")
            if at is not None:
                last_event_at = at
            if state == "running" and started is None:
                started = at
            if state == "starting" and started is None and at is not None:
                started = at
            preview = event.get("preview")
            if state == "running" and isinstance(preview, dict):
                cs = _int(preview.get("current_step"))
                ts = _int(preview.get("total_steps"))
                phase = preview.get("phase") or phase
                rp = preview.get("progress")
                runtime_pct = float(rp) if isinstance(rp, (int, float)) else runtime_pct
                if cs is not None and ts:
                    if last_step is not None and cs < last_step:
                        all_durations.extend(eta_mod.step_durations(observations))
                        observations = []
                        item_idx += 1
                    if at is not None:
                        observations.append(eta_mod.StepObservation(cs, at))
                    last_step, total_steps = cs, ts
                    last_preview_had_steps = True
                else:
                    last_preview_had_steps = False
        if status in COMPLETED_STATUSES or status in FAILED_STATUSES:
            finished = last_event_at or parse_iso(run.get("updated_at"))
        started = started or created
        if total_steps is None and steps_cfg:
            total_steps = steps_cfg

        worker = run.get("local_worker") or {}
        worker_pid = _int(worker.get("pid"))
        worker_alive: bool | None = None
        note: str | None = None
        if status in ACTIVE_STATUSES:
            if worker_pid:
                worker_alive = bool(self.pid_alive(worker_pid))
                if not worker_alive:
                    status = "interrupted"
                    note = f"worker PID {worker_pid} is not running; the run record was never finalized"
                    finished = last_event_at or parse_iso(run.get("updated_at"))
            elif status == "queued" and created and now - created > timedelta(hours=QUEUED_ABANDON_HOURS):
                status = "interrupted"
                note = "queued record without a worker for more than 24h"
                finished = parse_iso(run.get("updated_at")) or created
            if status in ACTIVE_STATUSES and last_event_at and now - last_event_at > timedelta(minutes=STALE_EVENT_MINUTES):
                idle_min = int((now - last_event_at).total_seconds() // 60)
                note = f"worker alive but no events for {idle_min} min"

        # ---------------------------------------------------------- progress + ETA
        progress: Progress
        eta_seconds: float | None = None
        eta_basis: str | None = None
        extra = {"runtime_percent": runtime_pct, "item_current": item_idx + 1, "item_total": items_total}
        if status in ACTIVE_STATUSES:
            if last_step is not None and total_steps and last_preview_had_steps:
                label = f"{phase or 'step'} {last_step}/{total_steps}"
                if items_total > 1:
                    label += f" · item {item_idx + 1}/{items_total}"
                progress = Progress.step(last_step, total_steps, label=label, **extra)
            elif last_step is not None and total_steps:
                progress = Progress.phase(f"{phase or 'post-processing'} · denoise {last_step}/{total_steps} done", current=last_step, total=total_steps, **extra)
            elif status == "running":
                progress = Progress.activity(f"{phase or 'preparing'} · no step events yet", **extra)
            else:
                progress = Progress.phase(status, **extra)
            if total_steps and last_step is not None:
                remaining = max(total_steps - last_step, 0) + max(items_total - item_idx - 1, 0) * total_steps
                # earlier items of the same run share model/resolution/steps, so their step times count too
                durations = all_durations + eta_mod.step_durations(observations)
                history_mean = self.history_lookup(eta_mod.timing_key(model, resolution, total_steps, frames, batch_size))
                eta_seconds, eta_basis = eta_mod.estimate(durations, remaining, history_mean)
                if eta_basis == "recent_steps" and not last_preview_had_steps:
                    eta_seconds, eta_basis = None, None  # denoising finished; decode time is not step-based
        elif status in COMPLETED_STATUSES:
            progress = Progress(type="exact", current=total_steps, total=total_steps, percent=100.0, label="completed", **extra)
        else:
            if last_step is not None and total_steps:
                progress = Progress.step(last_step, total_steps, label=f"stopped at {phase or 'step'} {last_step}/{total_steps}", **extra)
            else:
                progress = Progress.unknown(f"{status} before any step event")

        all_durations.extend(eta_mod.step_durations(observations))
        mean_step = (sum(all_durations) / len(all_durations)) if all_durations else None

        outputs: list[Output] = []
        for index, artifact in enumerate(run.get("artifacts") or []):
            path = str(artifact.get("path") or "")
            if not path:
                continue
            outputs.append(Output(
                path=path, kind=output_kind(path), byte_count=_int(artifact.get("byte_count")),
                sha256=artifact.get("sha256"), exists=os.path.isfile(path), index=index,
            ))

        error = None
        if isinstance(run.get("error"), dict):
            error = str(run["error"].get("message") or "")
        elif run.get("error"):
            error = str(run["error"])

        requested_by = ctx.requested_by
        requested_by_basis = ctx.requested_by_basis
        run_actor = explicit_requester(run)
        if run_actor:
            requested_by, requested_by_basis = run_actor, "record"

        prompt_id = run.get("prompt_id")
        if not ctx.is_session:
            # No session directory: name the job from what the producer did record.
            parts = [str(run.get("project_id") or "").strip(), str(prompt_id or "").strip()]
            title = " · ".join(part for part in parts if part) or str(run["run_id"])
        elif ctx.kind == "video" and prompt_id:
            title = f"{ctx.title} · {prompt_id}"
        elif model and ctx.kind in {"scene", "face", "variation"}:
            title = f"{ctx.title} · {model}"
        else:
            title = ctx.title

        elapsed = seconds_between(started, finished if finished else now) if status not in {"queued"} else None
        job = Job(
            job_id=f"wangp:{run['run_id']}",
            source="wangp-run",
            title=title,
            requested_by=requested_by,
            requested_by_basis=requested_by_basis,
            # an executor recorded at submit time wins over the inference from the run shape
            executor=str(run.get("executor")) if run.get("executor") else (
                EXECUTOR_LOCAL_WORKER if worker_pid else "wangp" if run.get("target") == "local" else str(run.get("target") or "unknown")),
            engine=str(run.get("renderer") or "WanGP"),
            model=str(model) if model else None,
            status=status,
            phase=phase,
            created_at=_iso(created),
            started_at=_iso(started),
            finished_at=_iso(finished),
            updated_at=run.get("updated_at"),
            elapsed_seconds=round(elapsed, 1) if elapsed is not None else None,
            progress=progress,
            eta_seconds=eta_seconds,
            eta_basis=eta_basis,
            outputs=outputs,
            character_id=ctx.character_id,
            session_id=ctx.session_id,
            session_dir=ctx.session_dir,
            run_dir=str(run_dir),
            worker_pid=worker_pid,
            worker_alive=worker_alive,
            error=error or None,
            note=note,
            last_event_at=_iso(last_event_at),
            details={
                "run_id": run.get("run_id"),
                "project_id": run.get("project_id"),
                "prompt_id": prompt_id,
                "target": run.get("target"),
                "provider_job_id": run.get("provider_job_id"),
                "resolution": resolution,
                "steps": total_steps,
                "frames": frames,
                "batch_size": batch_size,
                "repeat_generation": items_total,
                "prompt_sha256": (run.get("prompt") or {}).get("sha256"),
                "prompt_path": (run.get("prompt") or {}).get("path"),
                "event_count": len(events),
                "session_kind": ctx.kind,
                "visibility": ctx.visibility,
                "timing_key": eta_mod.timing_key(model, resolution, total_steps, frames, batch_size),
                "mean_step_seconds": round(mean_step, 2) if mean_step else None,
                "step_samples": len(all_durations),
            },
        )
        return job


def _mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def _size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def _int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _iso(value: datetime | None) -> str | None:
    return value.isoformat(timespec="seconds") if value else None
