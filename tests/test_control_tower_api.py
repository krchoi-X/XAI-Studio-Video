import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from control_tower.app import create_app  # noqa: E402
from control_tower.config import Config  # noqa: E402
from control_tower.db import Database  # noqa: E402
from control_tower.gpu import GpuProcess, GpuSample, HostSample  # noqa: E402
from control_tower.jobs import Job, Output, Progress  # noqa: E402
from control_tower.monitor import MonitorService  # noqa: E402
from control_tower.processes import ProcessObserver  # noqa: E402

T0 = datetime(2026, 9, 6, 1, 0, 0, tzinfo=timezone.utc)


class FakeGpu:
    def __init__(self, util=97.0, pids=(28141,)):
        self.util = util
        self.pids = pids

    def sample(self):
        gpu = GpuSample(index=0, name="NVIDIA GeForce RTX 4070 Laptop GPU", driver_version="610.88", utilization_percent=self.util,
                        memory_utilization_percent=40.0, memory_used_mib=7400.0, memory_total_mib=8188.0, temperature_c=72.0,
                        power_draw_w=78.0, power_limit_w=None, sm_clock_mhz=2400.0, pstate="P0",
                        processes=[GpuProcess(pid=p, name=r"D:\AI\WanGP\env_uv\Scripts\python.exe") for p in self.pids])
        return HostSample(ok=True, gpus=[gpu])


class FakeProcesses(ProcessObserver):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def scan(self, gpu_pids=None, rows=None, now=None):
        return super().scan(gpu_pids=gpu_pids, rows=list(self.rows), now=now)


class FakeAdapter:
    def __init__(self, jobs):
        self.jobs = jobs

    def discover(self, now=None):
        return list(self.jobs)


def wangp_worker_row(pid, cpu=300.0):
    return {"pid": pid, "ppid": 1, "name": "python.exe", "exe": None, "create_time": T0.timestamp(), "rss": 2 * 1024 ** 3, "cpu": cpu,
            "cmdline": rf'"D:\AI\WanGP\env_uv\Scripts\python.exe" D:\codex\XAI-studio\tools\local_wangp.py worker --run-dir D:\x'}


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.image = root / "out.jpg"
        self.image.write_bytes(b"\xff\xd8\xff\xdbfakejpeg")
        self.cfg = Config(db_path=root / "ct.sqlite3", scan_roots=[root / "none"], night_batch_root=root / "none", web_job_roots=[])
        self.running = Job(job_id="wangp:run-live", source="wangp-run", title="Lia beach #14", requested_by="hermes", executor="local-wangp-worker",
                           engine="WanGP", model="minimax_h3", status="running", progress=Progress.step(31, 42, label="inference 31/42"),
                           eta_seconds=423.0, eta_basis="recent_steps", worker_pid=28141, worker_alive=True, started_at=T0.isoformat())
        self.done = Job(job_id="wangp:run-done", source="wangp-run", title="done", requested_by="codex", executor="local-wangp-worker", status="needs_review",
                        finished_at=(T0 + timedelta(minutes=5)).isoformat(), outputs=[Output(path=str(self.image), kind="image", exists=True, index=0)],
                        details={"timing_key": "k", "mean_step_seconds": 6.0, "step_samples": 7})

    def tearDown(self):
        self.tmp.cleanup()

    def make_client(self, jobs, gpu=None, rows=None):
        service = MonitorService(self.cfg, db=Database(self.cfg.db_path), gpu_collector=gpu or FakeGpu(),
                                 process_observer=FakeProcesses(rows if rows is not None else [wangp_worker_row(28141)]),
                                 adapters=[FakeAdapter(jobs)])
        app = create_app(self.cfg, monitor=service)
        return TestClient(app), service

    def test_overview_tracks_running_job_and_no_untracked(self):
        client, service = self.make_client([self.running, self.done])
        with client:
            health = client.get("/api/health").json()
            self.assertTrue(health["ok"] and health["gpu_ok"])
            view = client.get("/api/overview").json()
            self.assertEqual(view["counts"]["running"], 1)
            job = view["running"][0]
            self.assertEqual(job["requested_by"], "hermes")
            self.assertEqual(job["executor"], "local-wangp-worker")
            self.assertTrue(job["progress"]["measured"])
            self.assertEqual(job["progress"]["percent"], 73.8)
            self.assertEqual(job["eta_basis"], "recent_steps")
            self.assertEqual(view["untracked"], [], "the GPU process is the tracked worker")
            self.assertEqual(view["host"]["gpus"][0]["utilization_percent"], 97.0)
            agents = {a["agent"]: a for a in view["processes"]["agents"]}
            self.assertEqual(agents["wangp"]["state"], "working")
            self.assertTrue(agents["wangp"]["on_gpu"])
            self.assertEqual([r["job_id"] for r in view["recent"]], ["wangp:run-done"])
            # timing history recorded once for the completed job
            self.assertEqual(service.db.get_step_timing("k"), 6.0)
            service.tick(force=True)
            self.assertEqual(service.db.get_step_timing("k"), 6.0)

    def test_untracked_workload_when_no_job_claims_gpu(self):
        client, _ = self.make_client([self.done], gpu=FakeGpu(util=98.0, pids=(17421,)), rows=[wangp_worker_row(17421)])
        with client:
            view = client.get("/api/overview").json()
            self.assertEqual(view["counts"]["running"], 0)
            self.assertEqual(len(view["untracked"]), 1)
            item = view["untracked"][0]
            self.assertEqual(item["pid"], 17421)
            self.assertEqual(item["confidence"], "heuristic")
            self.assertIn("WanGP", item["likely"])
            self.assertEqual(item["gpu_utilization_percent"], 98.0)

    def test_untracked_ignores_idle_desktop_helper(self):
        helper = {"pid": 27584, "ppid": 1, "name": "ChatGPT.exe", "exe": r"C:\Program Files\WindowsApps\OpenAI.Codex_26\app\ChatGPT.exe",
                  "cmdline": r'"C:\Program Files\WindowsApps\OpenAI.Codex_26\app\ChatGPT.exe" --type=utility', "create_time": T0.timestamp(), "rss": 1, "cpu": 0.0}
        client, _ = self.make_client([], gpu=FakeGpu(util=0.0, pids=(27584,)), rows=[helper])
        with client:
            view = client.get("/api/overview").json()
            self.assertEqual(view["untracked"], [])
            self.assertEqual({a["agent"]: a["state"] for a in view["processes"]["agents"]}["codex"], "idle")

    def test_running_job_explains_high_util_so_helper_is_not_untracked(self):
        """A desktop app on the GPU must not be reported while a tracked job explains the utilization."""
        helper = {"pid": 27584, "ppid": 1, "name": "ChatGPT.exe", "exe": r"C:\Program Files\WindowsApps\OpenAI.Codex_26\app\ChatGPT.exe",
                  "cmdline": r'"C:\Program Files\WindowsApps\OpenAI.Codex_26\app\ChatGPT.exe" --type=utility', "create_time": T0.timestamp(), "rss": 1, "cpu": 0.0}
        client, _ = self.make_client([self.running], gpu=FakeGpu(util=100.0, pids=(28141, 27584)),
                                     rows=[wangp_worker_row(28141), helper])
        with client:
            view = client.get("/api/overview").json()
            self.assertEqual(view["counts"]["running"], 1)
            self.assertEqual(view["untracked"], [])

    def test_ai_runtime_on_gpu_is_reported_even_while_another_job_runs(self):
        """A second WanGP process that no job accounts for is still surfaced."""
        client, _ = self.make_client([self.running], gpu=FakeGpu(util=100.0, pids=(28141, 17421)),
                                     rows=[wangp_worker_row(28141), wangp_worker_row(17421)])
        with client:
            view = client.get("/api/overview").json()
            untracked = view["untracked"]
            self.assertEqual([u["pid"] for u in untracked], [17421])
            self.assertEqual(untracked[0]["reason"], "AI runtime holding the GPU")

    def test_high_util_without_process_reports_unidentified(self):
        client, _ = self.make_client([], gpu=FakeGpu(util=90.0, pids=()), rows=[])
        with client:
            view = client.get("/api/overview").json()
            self.assertEqual(view["untracked"][0]["confidence"], "none")

    def test_job_detail_outputs_and_404s(self):
        client, _ = self.make_client([self.running, self.done])
        with client:
            detail = client.get("/api/jobs/wangp:run-done").json()
            self.assertEqual(detail["outcome"], "completed")
            self.assertEqual(client.get("/api/jobs/wangp:run-done/outputs/0").content, self.image.read_bytes())
            self.assertEqual(client.get("/api/jobs/wangp:run-done/outputs/1").status_code, 404)
            self.assertEqual(client.get("/api/jobs/nope").status_code, 404)
            listing = client.get("/api/jobs").json()
            self.assertEqual([j["job_id"] for j in listing["jobs"]], ["wangp:run-live", "wangp:run-done"])
            self.assertEqual(client.get("/api/jobs?status=running").json()["total"], 1)
            history = client.get("/api/jobs/history").json()["jobs"]
            self.assertEqual({j["job_id"] for j in history}, {"wangp:run-live", "wangp:run-done"})
            self.assertEqual(client.get("/api/timings").json()["step_timings"][0]["key"], "k")
            page = client.get("/").text
            self.assertIn("XAI CONTROL TOWER", page)

    def test_gpu_failure_is_reported_not_zeroed(self):
        class BrokenGpu:
            def sample(self):
                return HostSample(ok=False, gpus=[], error="nvidia-smi not found on PATH")

        client, _ = self.make_client([], gpu=BrokenGpu(), rows=[])
        with client:
            host = client.get("/api/host").json()
            self.assertFalse(host["ok"])
            self.assertIn("not found", host["error"])
            self.assertEqual(host["gpus"], [])
            self.assertFalse(client.get("/api/health").json()["gpu_ok"])

    def test_sse_frames_overview_then_host_then_keepalive(self):
        from control_tower.app import sse_frame

        service = MonitorService(self.cfg, db=Database(self.cfg.db_path), gpu_collector=FakeGpu(),
                                 process_observer=FakeProcesses([wangp_worker_row(28141)]), adapters=[FakeAdapter([self.running])])
        try:
            service.tick(force=True)
            frame, version, full = sse_frame(service, -1, -1, 0.1)
            self.assertTrue(frame.startswith("event: overview"))
            payload = json.loads(frame.split("data: ", 1)[1])
            self.assertEqual(payload["counts"]["running"], 1)
            # host-only change -> small host event
            service._sample_host()
            with service._cond:
                service.version += 1
                service._cond.notify_all()
            frame, version, full = sse_frame(service, version, full, 0.1)
            self.assertTrue(frame.startswith("event: host"))
            host_payload = json.loads(frame.split("data: ", 1)[1])
            self.assertIn("untracked", host_payload)
            self.assertNotIn("recent", host_payload)
            # nothing changed -> keepalive comment
            frame, version2, full2 = sse_frame(service, version, full, 0.05)
            self.assertEqual((frame, version2, full2), (": keepalive\n\n", version, full))
        finally:
            service.db.close()

    # NOTE: the live /api/events endpoint is verified with curl (see docs/control-tower-v0.1.md); Starlette's
    # TestClient cannot close an infinite streaming response without deadlocking, so it is not exercised here.


if __name__ == "__main__":
    unittest.main()
