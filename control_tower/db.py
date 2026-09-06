"""SQLite persistence (WAL). The filesystem run records remain the source of truth; this database keeps
job snapshots for history, per-workstation step-timing history for ETA, and a short host-sample ring."""
from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    status TEXT NOT NULL,
    title TEXT,
    requested_by TEXT,
    executor TEXT,
    created_at TEXT,
    finished_at TEXT,
    updated_at TEXT,
    payload TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS jobs_updated ON jobs(updated_at);
CREATE TABLE IF NOT EXISTS step_timings (
    timing_key TEXT PRIMARY KEY,
    mean_step_seconds REAL NOT NULL,
    samples INTEGER NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS host_samples (
    sampled_at TEXT NOT NULL,
    utilization REAL,
    memory_used_mib REAL,
    memory_total_mib REAL,
    temperature_c REAL,
    power_w REAL
);
CREATE INDEX IF NOT EXISTS host_samples_at ON host_samples(sampled_at);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


class Database:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(str(self.path), check_same_thread=False, isolation_level=None)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        self._conn.executescript(SCHEMA)
        self._conn.execute("INSERT OR REPLACE INTO meta(key, value) VALUES('schema_version', '1')")

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    # ------------------------------------------------------------------ jobs
    def upsert_job(self, job: dict[str, Any]) -> None:
        with self._lock:
            self._conn.execute(
                """INSERT INTO jobs(job_id, source, status, title, requested_by, executor, created_at, finished_at, updated_at, payload)
                   VALUES(?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(job_id) DO UPDATE SET source=excluded.source, status=excluded.status, title=excluded.title,
                   requested_by=excluded.requested_by, executor=excluded.executor, created_at=excluded.created_at,
                   finished_at=excluded.finished_at, updated_at=excluded.updated_at, payload=excluded.payload""",
                (
                    job["job_id"], job["source"], job["status"], job.get("title"), job.get("requested_by"), job.get("executor"),
                    job.get("created_at"), job.get("finished_at"), job.get("updated_at"), json.dumps(job, ensure_ascii=False),
                ),
            )

    def upsert_jobs(self, jobs: list[dict[str, Any]]) -> None:
        with self._lock:
            self._conn.execute("BEGIN")
            try:
                for job in jobs:
                    self.upsert_job(job)
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute("SELECT payload FROM jobs WHERE job_id=?", (job_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def list_jobs(self, limit: int = 100, status: str | None = None, source: str | None = None) -> list[dict[str, Any]]:
        clauses, params = [], []
        if status:
            clauses.append("status=?")
            params.append(status)
        if source:
            clauses.append("source=?")
            params.append(source)
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        with self._lock:
            rows = self._conn.execute(
                f"SELECT payload FROM jobs {where} ORDER BY COALESCE(finished_at, updated_at, created_at) DESC LIMIT ?",
                (*params, limit),
            ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def job_count(self) -> int:
        with self._lock:
            return int(self._conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0])

    # ------------------------------------------------------------------ step timings
    def get_step_timing(self, key: str) -> float | None:
        with self._lock:
            row = self._conn.execute("SELECT mean_step_seconds FROM step_timings WHERE timing_key=?", (key,)).fetchone()
        return float(row[0]) if row else None

    def record_step_timing(self, key: str, mean_step_seconds: float, weight: int = 1) -> None:
        if mean_step_seconds <= 0:
            return
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self._lock:
            row = self._conn.execute("SELECT mean_step_seconds, samples FROM step_timings WHERE timing_key=?", (key,)).fetchone()
            if row:
                old_mean, samples = float(row[0]), int(row[1])
                total = samples + weight
                new_mean = (old_mean * samples + mean_step_seconds * weight) / total
                self._conn.execute(
                    "UPDATE step_timings SET mean_step_seconds=?, samples=?, updated_at=? WHERE timing_key=?",
                    (new_mean, total, now, key),
                )
            else:
                self._conn.execute(
                    "INSERT INTO step_timings(timing_key, mean_step_seconds, samples, updated_at) VALUES(?,?,?,?)",
                    (key, mean_step_seconds, weight, now),
                )

    def list_step_timings(self) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute("SELECT timing_key, mean_step_seconds, samples, updated_at FROM step_timings ORDER BY updated_at DESC").fetchall()
        return [{"key": r[0], "mean_step_seconds": r[1], "samples": r[2], "updated_at": r[3]} for r in rows]

    # ------------------------------------------------------------------ host samples
    def record_host_sample(self, sampled_at: str, utilization: float | None, memory_used: float | None,
                           memory_total: float | None, temperature: float | None, power: float | None) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO host_samples(sampled_at, utilization, memory_used_mib, memory_total_mib, temperature_c, power_w) VALUES(?,?,?,?,?,?)",
                (sampled_at, utilization, memory_used, memory_total, temperature, power),
            )

    def prune_host_samples(self, keep_hours: float = 6.0) -> None:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=keep_hours)).isoformat(timespec="seconds")
        with self._lock:
            self._conn.execute("DELETE FROM host_samples WHERE sampled_at < ?", (cutoff,))

    def recent_host_samples(self, minutes: float = 30.0, limit: int = 900) -> list[dict[str, Any]]:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat(timespec="seconds")
        with self._lock:
            rows = self._conn.execute(
                "SELECT sampled_at, utilization, memory_used_mib, temperature_c, power_w FROM host_samples WHERE sampled_at >= ? ORDER BY sampled_at DESC LIMIT ?",
                (cutoff, limit),
            ).fetchall()
        return [{"at": r[0], "util": r[1], "mem": r[2], "temp": r[3], "power": r[4]} for r in reversed(rows)]
