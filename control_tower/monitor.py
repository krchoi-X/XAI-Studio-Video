"""Background monitor: samples host + processes + jobs on their own cadences and publishes one snapshot.

The snapshot is what the API and SSE stream hand to the UI. Everything here is observation; nothing
starts, stops or edits any job.
"""
from __future__ import annotations

import json
import logging
import threading
import time
from datetime import datetime
from typing import Any, Callable

from .adapters.night_batch import NightBatchAdapter
from .adapters.wangp_runs import WangpRunAdapter
from .adapters.web_jobs import WebJobAdapter
from .config import Config
from .db import Database
from .gpu import HostSample, NvidiaSmiCollector
from .jobs import COMPLETED_STATUSES, Job
from .processes import AI_RUNTIME_KINDS, ProcessObserver, ProcessSnapshot
from .util import iso_now, read_json_safe, utc_now

log = logging.getLogger("control_tower.monitor")


class MonitorService:
    def __init__(
        self,
        config: Config,
        db: Database | None = None,
        gpu_collector: Any | None = None,
        process_observer: ProcessObserver | None = None,
        adapters: list[Any] | None = None,
    ) -> None:
        self.config = config
        self.db = db or Database(config.db_path)
        self.gpu = gpu_collector or NvidiaSmiCollector(config.nvidia_smi)
        self.processes = process_observer or ProcessObserver(str(config.wangp_root))
        self.adapters = adapters if adapters is not None else [
            WangpRunAdapter(config.scan_roots, history_lookup=self.db.get_step_timing),
            NightBatchAdapter(config.night_batch_root),
            WebJobAdapter(config.web_job_roots),
        ]
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.version = 0
        self.full_version = 0  # bumps only when processes or jobs changed (host-only ticks are cheap)
        self.started_at = iso_now()
        self.host: HostSample | None = None
        self.host_error_since: str | None = None
        self.procs: ProcessSnapshot | None = None
        self.jobs: list[Job] = []
        self.job_errors: dict[str, str] = {}
        self._last_host = 0.0
        self._last_procs = 0.0
        self._last_jobs = 0.0
        self._timing_recorded: set[str] = set()
        self._proc_signature: Any = None
        self._attribution_cache: dict[str, dict[str, Any]] | None = None
        self._manual_cache: tuple[float, dict[str, Any]] = (0.0, {})
        self._job_signature: dict[str, str] = {}
        self._last_prune = 0.0
        # Seed the timing-recorded set with terminal jobs already persisted so restarts don't double count.
        for row in self.db.list_jobs(limit=5000):
            if row.get("status") in COMPLETED_STATUSES:
                self._timing_recorded.add(row["job_id"])

    # ------------------------------------------------------------------ lifecycle
    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self.tick(force=True)
        self._thread = threading.Thread(target=self._loop, name="control-tower-monitor", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        with self._cond:
            self._cond.notify_all()
        if self._thread:
            self._thread.join(timeout=5)
        try:
            self.db.close()
        except Exception:
            log.exception("db close failed")

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self.tick()
            except Exception:  # keep the monitor alive no matter what
                log.exception("monitor tick failed")
            self._stop.wait(0.5)

    # ------------------------------------------------------------------ sampling
    def tick(self, force: bool = False) -> None:
        now = time.time()
        changed = full = False
        if force or now - self._last_host >= self.config.host_interval:
            self._sample_host()
            self._last_host = now
            changed = True
        if force or now - self._last_procs >= self.config.process_interval:
            full = self._sample_processes() or full
            self._last_procs = now
            changed = True
        if force or now - self._last_jobs >= self.config.job_interval:
            full = self._sample_jobs() or full
            self._last_jobs = now
            changed = True
        if changed:
            with self._cond:
                self.version += 1
                if full:
                    self.full_version += 1
                self._cond.notify_all()

    def _sample_host(self) -> None:
        sample = self.gpu.sample()
        self.host = sample
        if sample.ok:
            self.host_error_since = None
            g = sample.gpus[0] if sample.gpus else None
            if g is not None:
                try:
                    self.db.record_host_sample(sample.sampled_at, g.utilization_percent, g.memory_used_mib,
                                               g.memory_total_mib, g.temperature_c, g.power_draw_w)
                except Exception:
                    log.exception("host sample persistence failed")
        else:
            self.host_error_since = self.host_error_since or sample.sampled_at
        if time.time() - self._last_prune > 600:
            try:
                self.db.prune_host_samples()
            except Exception:
                log.exception("prune failed")
            self._last_prune = time.time()

    def _gpu_pids(self) -> dict[int, float | None]:
        if not self.host or not self.host.ok:
            return {}
        return {p.pid: p.used_memory_mib for g in self.host.gpus for p in g.processes}

    def _sample_processes(self) -> bool:
        """Scan processes; return True when the snapshot changed in a way the UI must re-render."""
        self.procs = self.processes.scan(gpu_pids=self._gpu_pids())
        # transient helper/child processes and per-process CPU flicker do not justify a 60 KB re-render
        signature = (
            tuple(sorted((p.pid, p.kind, p.agent, p.on_gpu) for p in self.procs.processes if p.kind not in {"other", "node"} and not p.kind.endswith("-helper"))),
            tuple((a.agent, a.state, a.on_gpu) for a in self.procs.agents),
        )
        changed = signature != self._proc_signature
        self._proc_signature = signature
        return changed

    def _sample_jobs(self) -> bool:
        """Discover jobs; return True when any job changed (active jobs change every scan by design)."""
        now = utc_now()
        jobs: list[Job] = []
        for adapter in self.adapters:
            name = type(adapter).__name__
            try:
                jobs.extend(adapter.discover(now))
                self.job_errors.pop(name, None)
            except Exception as exc:
                log.exception("adapter %s failed", name)
                self.job_errors[name] = str(exc)
        link_parents(jobs)
        self._attribute_jobs(jobs)
        self.jobs = jobs
        self._mark_agents_with_running_jobs()
        return self._persist_jobs(jobs)

    # ------------------------------------------------------------------ requester attribution
    def _manual_attributions(self) -> dict[str, Any]:
        path = self.config.db_path.parent / "attributions.json"
        try:
            stamp = path.stat().st_mtime
        except OSError:
            self._manual_cache = (0.0, {})
            return {}
        if self._manual_cache[0] != stamp:
            data = read_json_safe(path)
            self._manual_cache = (stamp, data if isinstance(data, dict) else {})
        return self._manual_cache[1]

    def _attribute_jobs(self, jobs: list[Job]) -> None:
        """Fill `requested_by` for runs whose records say nothing, from (1) a persisted observation,
        (2) the live worker process (env marker or parent lineage), (3) the manual attributions file."""
        if self._attribution_cache is None:
            try:
                self._attribution_cache = self.db.get_attributions()
            except Exception:
                log.exception("attribution load failed")
                self._attribution_cache = {}
        manual = self._manual_attributions()
        manual_sessions = manual.get("sessions") if isinstance(manual.get("sessions"), dict) else {}
        manual_runs = manual.get("runs") if isinstance(manual.get("runs"), dict) else {}
        by_pid = {p.pid: p for p in (self.procs.processes if self.procs else [])}
        for job in jobs:
            if job.source != "wangp-run":
                continue
            if job.requested_by != "unknown":
                if job.requested_by_basis is None:
                    job.requested_by_basis = "parent" if job.parent_job_id else "record"
                continue
            stored = self._attribution_cache.get(job.job_id)
            if stored:
                job.requested_by, job.requested_by_basis = stored["requested_by"], stored["basis"]
                job.details["attribution_evidence"] = stored.get("evidence")
                continue
            if job.is_active and job.worker_pid:
                proc = by_pid.get(job.worker_pid)
                if proc and proc.launched_by:
                    basis = "process-env" if proc.launched_by_basis == "env" else "process-lineage"
                    evidence = f"worker PID {proc.pid} carries a {proc.launched_by} {proc.launched_by_basis} marker"
                    job.requested_by, job.requested_by_basis = proc.launched_by, basis
                    job.details["attribution_evidence"] = evidence
                    self._attribution_cache[job.job_id] = {"requested_by": proc.launched_by, "basis": basis, "evidence": evidence}
                    try:
                        self.db.record_attribution(job.job_id, proc.launched_by, basis, evidence)
                    except Exception:
                        log.exception("attribution persistence failed")
                    continue
            run_id = str(job.details.get("run_id") or "")
            entry = manual_runs.get(run_id) or (manual_sessions.get(job.session_id) if job.session_id else None)
            if isinstance(entry, dict) and entry.get("requested_by"):
                job.requested_by, job.requested_by_basis = str(entry["requested_by"]).lower(), "manual"
                job.details["attribution_evidence"] = entry.get("note")

    def _mark_agents_with_running_jobs(self) -> None:
        """An agent whose requested job is running is working even if its own process looks idle."""
        if not self.procs:
            return
        running_by = {j.requested_by for j in self.jobs if j.status == "running" and j.requested_by != "unknown"}
        for agent in self.procs.agents:
            if agent.agent in running_by and agent.state != "working":
                agent.state = "working"
                agent.note = "a job it requested is running (activity inferred from the job, not its own CPU)"

    def _persist_jobs(self, jobs: list[Job]) -> bool:
        payloads = [j.to_dict() for j in jobs]
        dirty: list[dict[str, Any]] = []
        seen: set[str] = set()
        for payload in payloads:
            seen.add(payload["job_id"])
            encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True)
            if self._job_signature.get(payload["job_id"]) != encoded:
                self._job_signature[payload["job_id"]] = encoded
                dirty.append(payload)
        removed = [k for k in self._job_signature if k not in seen]
        for key in removed:
            del self._job_signature[key]
        if dirty:
            try:
                self.db.upsert_jobs(dirty)
            except Exception:
                log.exception("job persistence failed")
        for job in jobs:
            if job.status in COMPLETED_STATUSES and job.job_id not in self._timing_recorded:
                key = job.details.get("timing_key")
                mean = job.details.get("mean_step_seconds")
                samples = int(job.details.get("step_samples") or 0)
                self._timing_recorded.add(job.job_id)
                if key and mean and samples >= 2:
                    try:
                        self.db.record_step_timing(str(key), float(mean), weight=samples)
                    except Exception:
                        log.exception("timing history failed")
        return bool(dirty or removed)

    # ------------------------------------------------------------------ views
    def wait_for_change(self, version: int, timeout: float) -> int:
        with self._cond:
            if self.version == version:
                self._cond.wait(timeout)
            return self.version

    def active_jobs(self) -> list[Job]:
        return [j for j in self.jobs if j.is_active]

    def untracked(self) -> list[dict[str, Any]]:
        """GPU work that no adapter accounts for. Heuristic identification only."""
        host = self.host
        procs = self.procs
        if not host or not host.ok or not host.gpus:
            return []
        gpu = host.gpus[0]
        util = gpu.utilization_percent or 0.0
        tracked_pids = {j.worker_pid for j in self.active_jobs() if j.worker_pid}
        tracked_family = set(tracked_pids)
        by_pid = {p.pid: p for p in (procs.processes if procs else [])}
        for p in by_pid.values():
            if p.ppid in tracked_pids:
                tracked_family.add(p.pid)
        results: list[dict[str, Any]] = []
        any_tracked_running = bool(tracked_pids)
        for gp in gpu.processes:
            info = by_pid.get(gp.pid)
            kind = info.kind if info else "unknown"
            if gp.pid in tracked_family:
                continue
            ai_runtime = kind in AI_RUNTIME_KINDS
            significant = ai_runtime or util >= self.config.untracked_gpu_util_threshold
            if not significant:
                continue
            if info is None:
                # psutil could not see the process (permissions or it exited between samples)
                exe = gp.name
                label = "unknown GPU process"
            else:
                exe = info.exe or info.name
                label = info.label
            results.append({
                "pid": gp.pid,
                "executable": exe,
                "kind": kind,
                "likely": label,
                "confidence": "heuristic",
                "cwd": info.cwd if info else None,
                "elapsed_seconds": info.elapsed_seconds if info else None,
                "cpu_percent": info.cpu_percent if info else None,
                "gpu_memory_mib": gp.used_memory_mib,
                "gpu_utilization_percent": util,
                "reason": "AI runtime holding the GPU" if ai_runtime else f"GPU utilization {util:.0f}% with no tracked job",
            })
        if not results and util >= self.config.untracked_gpu_util_threshold and not any_tracked_running:
            results.append({
                "pid": None, "executable": None, "kind": "unknown", "likely": "unidentified GPU load",
                "confidence": "none", "cwd": None, "elapsed_seconds": None, "cpu_percent": None,
                "gpu_memory_mib": None, "gpu_utilization_percent": util,
                "reason": f"GPU utilization {util:.0f}% but nvidia-smi lists no compute process",
            })
        return results

    def host_view(self) -> dict[str, Any]:
        """Small payload for host-only SSE ticks."""
        return {
            "host": self.host.to_dict() if self.host else {"ok": False, "error": "not sampled yet", "gpus": []},
            "untracked": self.untracked(),
            "now": iso_now(),
            "snapshot_version": self.version,
        }

    def overview(self) -> dict[str, Any]:
        host = self.host.to_dict() if self.host else {"ok": False, "error": "not sampled yet", "gpus": []}
        procs = self.procs.to_dict() if self.procs else {"processes": [], "agents": [], "scanned_at": None, "total_processes": 0, "error": None}
        active = sorted(self.active_jobs(), key=lambda j: (0 if j.status == "running" else 1, j.started_at or j.created_at or ""))
        queue = [j for j in active if j.status in {"queued", "starting"} or j.source in {"night-batch", "web-job"}]
        # night-batch queued items expand into queue rows
        queue_rows: list[dict[str, Any]] = []
        for job in active:
            if job.source == "night-batch":
                for item in job.details.get("queued_items", []):
                    queue_rows.append({"kind": "night-batch-item", "parent_job_id": job.job_id, "title": f"{item.get('character_id')} · {(item.get('prompt') or '')[:80]}",
                                       "engines": item.get("engines"), "count": item.get("count"), "requested_by": job.requested_by})
            elif job.status in {"queued", "starting"}:
                queue_rows.append({"kind": job.source, "parent_job_id": job.parent_job_id, "job_id": job.job_id, "title": job.title,
                                   "engines": [job.model] if job.model else [], "count": None, "requested_by": job.requested_by})
        recent = sorted((j for j in self.jobs if j.is_terminal), key=lambda j: j.finished_at or j.updated_at or "", reverse=True)
        recent = [j for j in recent if j.source == "wangp-run"][: self.config.recent_limit]
        running = [j for j in active if j.status == "running"]
        return {
            "service": {"name": "XAI Control Tower", "version": "0.1.0", "started_at": self.started_at, "now": iso_now(),
                        "machine": self.config.machine_label, "snapshot_version": self.version, "gallery_url": self.config.gallery_url,
                        "adapter_errors": self.job_errors, "host_error_since": self.host_error_since},
            "host": host,
            "processes": procs,
            "running": [j.to_dict() for j in running],
            "active": [j.to_dict() for j in active],
            "queue": queue_rows,
            "recent": [j.to_dict() for j in recent],
            "untracked": self.untracked(),
            "counts": {"jobs_total": len(self.jobs), "active": len(active), "running": len(running), "queue": len(queue_rows),
                       "history_rows": self.db.job_count()},
        }


def link_parents(jobs: list[Job]) -> None:
    """Attach WanGP runs to the night batch or web job whose session they belong to."""
    by_session: dict[str, str] = {}
    by_run_dir: dict[str, str] = {}
    for job in jobs:
        if job.source == "night-batch":
            for sd in job.details.get("item_session_dirs", []):
                by_session[_norm(sd)] = job.job_id
        elif job.source == "web-job":
            if job.session_dir:
                by_session[_norm(job.session_dir)] = job.job_id
            for rd in job.details.get("run_dirs", []):
                by_run_dir[_norm(rd)] = job.job_id
    for job in jobs:
        if job.source != "wangp-run" or job.parent_job_id:
            continue
        parent = by_run_dir.get(_norm(job.run_dir)) if job.run_dir else None
        if parent is None and job.session_dir:
            parent = by_session.get(_norm(job.session_dir))
        if parent:
            job.parent_job_id = parent
            if job.requested_by == "unknown":
                job.requested_by = "web" if parent.startswith("web:") else "hermes"
                job.requested_by_basis = "parent"


def _norm(path: str | None) -> str:
    return (path or "").replace("/", "\\").rstrip("\\").lower()
