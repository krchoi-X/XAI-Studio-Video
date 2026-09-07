import json
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from control_tower.adapters.wangp_runs import WangpRunAdapter, explicit_requester  # noqa: E402
from control_tower.config import Config  # noqa: E402
from control_tower.db import Database  # noqa: E402
from control_tower.gpu import HostSample  # noqa: E402
from control_tower.jobs import Job  # noqa: E402
from control_tower.monitor import MonitorService  # noqa: E402
from control_tower.processes import ProcessObserver  # noqa: E402

T0 = datetime(2026, 9, 7, 1, 0, 0, tzinfo=timezone(timedelta(hours=9)))
WANGP_WORKER = r'"D:\AI\WanGP\env_uv\Scripts\python.exe" D:\codex\XAI-studio\tools\local_wangp.py worker --run-dir D:\x'


def iso(dt):
    return dt.isoformat(timespec="seconds")


class NoGpu:
    def sample(self):
        return HostSample(ok=True, gpus=[])


class FakeProcesses(ProcessObserver):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def scan(self, gpu_pids=None, rows=None, now=None):
        return super().scan(gpu_pids=gpu_pids, rows=list(self.rows), now=now)


class ListAdapter:
    def __init__(self, jobs):
        self.jobs = jobs

    def discover(self, now=None):
        # return fresh copies so monitor mutations do not leak between ticks
        return [Job(**{**j.__dict__}) for j in self.jobs]


def worker_row(pid, env):
    return {"pid": pid, "ppid": 9999, "name": "python.exe", "exe": None, "cmdline": WANGP_WORKER,
            "create_time": time.time() - 60, "rss": 1, "cpu": 200.0, "env": env}


def make_job(job_id, status, session_id="VIDEO-S", worker_pid=None, requested_by="unknown"):
    return Job(job_id=job_id, source="wangp-run", title="t", requested_by=requested_by, executor="local-wangp-worker",
               status=status, session_id=session_id, worker_pid=worker_pid, details={"run_id": job_id.split(":", 1)[1]})


class AttributionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cfg = Config(db_path=self.root / "ct.sqlite3", scan_roots=[], night_batch_root=self.root / "none", web_job_roots=[])

    def tearDown(self):
        self.tmp.cleanup()

    def service(self, jobs, rows, db=None):
        return MonitorService(self.cfg, db=db or Database(self.cfg.db_path), gpu_collector=NoGpu(),
                              process_observer=FakeProcesses(rows), adapters=[ListAdapter(jobs)])

    def test_live_env_marker_attribution_persists_across_completion_and_restart(self):
        running = make_job("wangp:run-g1", "running", worker_pid=80)
        svc = self.service([running], [worker_row(80, {"SAND_LOCAL_EXEC_GENERATION": "1", "HERMES_HOME": "x"})])
        try:
            svc.tick(force=True)
            job = svc.jobs[0]
            self.assertEqual((job.requested_by, job.requested_by_basis), ("grok", "process-env"))
            self.assertIn("grok env marker", job.details["attribution_evidence"])
            agents = {a.agent: a for a in svc.procs.agents}
            self.assertEqual(agents["grok"].state, "working")
            self.assertEqual(svc.db.get_attributions()["wangp:run-g1"]["requested_by"], "grok")
            # worker gone, run finished: attribution must survive from the persisted observation
            svc.adapters = [ListAdapter([make_job("wangp:run-g1", "needs_review")])]
            svc.processes = FakeProcesses([])
            svc.tick(force=True)
            self.assertEqual((svc.jobs[0].requested_by, svc.jobs[0].requested_by_basis), ("grok", "process-env"))
        finally:
            svc.db.close()
        # restart with a fresh service on the same database
        svc2 = self.service([make_job("wangp:run-g1", "needs_review")], [])
        try:
            svc2.tick(force=True)
            self.assertEqual((svc2.jobs[0].requested_by, svc2.jobs[0].requested_by_basis), ("grok", "process-env"))
        finally:
            svc2.db.close()

    def test_lineage_attribution_and_agent_working_from_job(self):
        daemon = {"pid": 71, "ppid": 1, "name": "Grok Bot.exe", "exe": r"C:\Program Files\Grok Bot\Grok Bot.exe",
                  "cmdline": r'"C:\Program Files\Grok Bot\Grok Bot.exe" "C:\Program Files\Grok Bot\resources\app.asar\dist\local-exec-daemon\main.cjs"',
                  "create_time": time.time() - 600, "rss": 1, "cpu": 0.0}
        worker = worker_row(80, {"PATH": "x"})
        worker["ppid"] = 71
        svc = self.service([make_job("wangp:run-g2", "running", worker_pid=80)], [daemon, worker])
        try:
            svc.tick(force=True)
            job = svc.jobs[0]
            self.assertEqual((job.requested_by, job.requested_by_basis), ("grok", "process-lineage"))
            agents = {a.agent: a for a in svc.procs.agents}
            self.assertEqual(agents["grok"].state, "working")
            # an agent whose requested job runs is 'working' even without its own CPU/GPU activity
            svc.adapters = [ListAdapter([make_job("wangp:run-g3", "running", worker_pid=999, requested_by="hermes")])]
            svc.processes = FakeProcesses([])
            svc.tick(force=True)
            hermes = {a.agent: a for a in svc.procs.agents}["hermes"]
            self.assertEqual(hermes.state, "working")
            self.assertTrue(hermes.note.startswith("a job it requested is running"))
        finally:
            svc.db.close()

    def test_manual_attribution_file(self):
        (self.root / "attributions.json").write_text(json.dumps({
            "sessions": {"VIDEO-S": {"requested_by": "Grok", "note": "user said so"}},
            "runs": {"run-m2": {"requested_by": "claude", "note": "run-level"}},
        }), encoding="utf-8")
        jobs = [make_job("wangp:run-m1", "needs_review"), make_job("wangp:run-m2", "needs_review", session_id="OTHER"),
                make_job("wangp:run-m3", "needs_review", session_id="OTHER"), make_job("wangp:run-m4", "needs_review", requested_by="hermes")]
        svc = self.service(jobs, [])
        try:
            svc.tick(force=True)
            by_id = {j.job_id: j for j in svc.jobs}
            self.assertEqual((by_id["wangp:run-m1"].requested_by, by_id["wangp:run-m1"].requested_by_basis), ("grok", "manual"))
            self.assertEqual(by_id["wangp:run-m1"].details["attribution_evidence"], "user said so")
            self.assertEqual((by_id["wangp:run-m2"].requested_by, by_id["wangp:run-m2"].requested_by_basis), ("claude", "manual"))
            self.assertEqual((by_id["wangp:run-m3"].requested_by, by_id["wangp:run-m3"].requested_by_basis), ("unknown", None))
            self.assertEqual((by_id["wangp:run-m4"].requested_by, by_id["wangp:run-m4"].requested_by_basis), ("hermes", "record"))
        finally:
            svc.db.close()

    def test_submit_time_requested_by_and_executor_from_run_json(self):
        """A run recorded by `local_wangp.py submit --requested-by grok` reads as grok (record)."""
        session = self.root / "ch-x" / "02_generations" / "VIDEO-20260907-100000-x"
        run_dir = session / "runs" / "run-explicit"
        run_dir.mkdir(parents=True)
        (run_dir / "run.json").write_text(json.dumps({
            "schema_version": 1, "run_id": "run-explicit", "project_id": "p", "prompt_id": "shot-01",
            "status": "running", "created_at": iso(T0), "updated_at": iso(T0), "target": "local", "renderer": "WanGP",
            "requested_by": "grok", "executor": "local-wangp-worker",
            "settings": {"value": {"model_type": "minimax_h3_ref2va_pruned", "resolution": "576x768", "num_inference_steps": 20}},
            "artifacts": [], "error": None, "local_worker": {"pid": 4242},
        }), encoding="utf-8")
        (run_dir / "events.jsonl").write_text(
            json.dumps({"at": iso(T0), "state": "queued", "requested_by": "grok"}) + "\n", encoding="utf-8")
        job = WangpRunAdapter([self.root], pid_alive=lambda pid: True).discover(now=T0 + timedelta(minutes=1))[0]
        self.assertEqual((job.requested_by, job.requested_by_basis), ("grok", "record"))
        self.assertEqual(job.executor, "local-wangp-worker", "executor is recorded, not inferred")
        self.assertEqual(job.engine, "WanGP")
        self.assertEqual(job.model, "minimax_h3_ref2va_pruned")

    def test_null_requested_by_key_does_not_claim_a_requester(self):
        """New records always carry the key; a null value must not read as a requester."""
        session = self.root / "ch-x" / "02_generations" / "VIDEO-20260907-110000-x"
        run_dir = session / "runs" / "run-null"
        run_dir.mkdir(parents=True)
        (run_dir / "run.json").write_text(json.dumps({
            "run_id": "run-null", "status": "needs_review", "created_at": iso(T0), "updated_at": iso(T0),
            "target": "local", "renderer": "WanGP", "requested_by": None, "executor": None,
            "settings": {"value": {}}, "artifacts": [],
        }), encoding="utf-8")
        (run_dir / "events.jsonl").write_text("", encoding="utf-8")
        job = WangpRunAdapter([self.root], pid_alive=lambda pid: False).discover(now=T0 + timedelta(minutes=1))[0]
        self.assertEqual((job.requested_by, job.requested_by_basis), ("unknown", None))
        self.assertEqual(job.executor, "wangp", "no recorded executor falls back to the inferred one")

    def test_explicit_record_keys_including_bom(self):
        self.assertEqual(explicit_requester({"invoked_by": "hermes"}), "hermes")
        self.assertEqual(explicit_requester({"requested_by": "Grok Bot"}), "grok bot")
        self.assertIsNone(explicit_requester({"invoked_by": "unknown"}))
        self.assertIsNone(explicit_requester({"hermes_agent_used": False}))
        session = self.root / "ch-x" / "02_generations" / "VIDEO-20260907-000000-x"
        run_dir = session / "runs" / "run-bom"
        run_dir.mkdir(parents=True)
        # BOM-prefixed handoff.json written by a PowerShell orchestrator
        (session / "handoff.json").write_bytes(b"\xef\xbb\xbf" + json.dumps({"project_id": "x", "requested_by": "grok"}).encode("utf-8"))
        (run_dir / "run.json").write_text(json.dumps({"run_id": "run-bom", "status": "needs_review", "created_at": iso(T0), "updated_at": iso(T0),
                                                       "settings": {"value": {}}, "artifacts": []}), encoding="utf-8")
        (run_dir / "events.jsonl").write_text("", encoding="utf-8")
        job = WangpRunAdapter([self.root], pid_alive=lambda pid: False).discover(now=T0 + timedelta(minutes=1))[0]
        self.assertEqual((job.requested_by, job.requested_by_basis), ("grok", "record"))


if __name__ == "__main__":
    unittest.main()
