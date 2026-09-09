import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from control_tower import eta  # noqa: E402
from control_tower.adapters.night_batch import NightBatchAdapter  # noqa: E402
from control_tower.adapters.wangp_runs import WangpRunAdapter  # noqa: E402
from control_tower.adapters.web_jobs import WebJobAdapter  # noqa: E402
from control_tower.db import Database  # noqa: E402
from control_tower.monitor import link_parents  # noqa: E402

T0 = datetime(2026, 9, 6, 1, 0, 0, tzinfo=timezone(timedelta(hours=9)))


def iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def make_session(root: Path, character: str, session_id: str, title: str, invoked_by: str | None, visibility="restricted") -> Path:
    session = root / character / "02_generations" / session_id
    session.mkdir(parents=True)
    (session / "batch.yaml").write_text(json.dumps({"schema_version": 1, "session": {
        "id": session_id, "character_id": character, "title": title, "status": "running", "visibility": visibility}}), encoding="utf-8")
    if invoked_by:
        (session / "prompt-trace.json").write_text(json.dumps({"invoked_by": invoked_by, "created_at": iso(T0)}), encoding="utf-8")
    return session


def make_run(session: Path, run_id: str, status: str, events: list[dict], pid: int | None = 4242, settings=None, artifacts=None, created=T0) -> Path:
    run_dir = session / "runs" / run_id
    run_dir.mkdir(parents=True)
    record = {
        "schema_version": 1, "run_id": run_id, "project_id": "p", "prompt_id": "shot-01", "status": status,
        "created_at": iso(created), "updated_at": iso(created), "target": "local", "renderer": "WanGP",
        "provider_job_id": None, "prompt": {"path": "x", "sha256": "abc", "normalized_sha256": "abc", "byte_count": 1},
        "settings": {"path": None, "value": settings or {"model_type": "z_image", "resolution": "768x1024", "num_inference_steps": 8, "batch_size": 3}},
        "artifacts": artifacts or [], "error": None,
    }
    if pid:
        record["local_worker"] = {"pid": pid, "command": []}
    (run_dir / "run.json").write_text(json.dumps(record), encoding="utf-8")
    with (run_dir / "events.jsonl").open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return run_dir


def step_events(start: datetime, steps: int, total: int, seconds_per_step: float, phase="inference") -> list[dict]:
    events = [{"at": iso(start), "state": "queued"}, {"at": iso(start), "state": "starting", "local_worker_pid": 4242},
              {"at": iso(start + timedelta(seconds=5)), "state": "running", "provider_job_id": "local-pid-1"}]
    for i in range(1, steps + 1):
        at = start + timedelta(seconds=5 + i * seconds_per_step)
        events.append({"at": iso(at), "state": "running", "progress": f"{phase} {i}/{total}",
                       "preview": {"image": "<PIL>", "phase": phase, "status": "Denoising", "progress": 20 + i * 8, "current_step": i, "total_steps": total}})
    return events


class WangpAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.now = T0 + timedelta(minutes=2)

    def tearDown(self):
        self.tmp.cleanup()

    def adapter(self, alive=True, history=None):
        return WangpRunAdapter([self.root], history_lookup=lambda key: (history or {}).get(key), pid_alive=lambda pid: alive)

    def test_running_job_with_measured_step_progress_and_eta(self):
        session = make_session(self.root, "ch-test", "SCENE-20260906-010000-test-scene", "테스트 장면", "hermes")
        make_run(session, "run-a", "running", step_events(T0, 4, 8, 6.0))
        jobs = self.adapter().discover(now=T0 + timedelta(seconds=40))
        self.assertEqual(len(jobs), 1)
        job = jobs[0]
        self.assertEqual(job.job_id, "wangp:run-a")
        self.assertEqual(job.status, "running")
        self.assertEqual(job.requested_by, "hermes")
        self.assertEqual(job.executor, "local-wangp-worker")
        self.assertEqual(job.engine, "WanGP")
        self.assertEqual(job.model, "z_image")
        self.assertEqual(job.character_id, "ch-test")
        self.assertEqual(job.title, "테스트 장면 · z_image")
        self.assertTrue(job.progress.measured)
        self.assertEqual((job.progress.type, job.progress.current, job.progress.total, job.progress.percent), ("step", 4, 8, 50.0))
        self.assertEqual(job.progress.runtime_percent, 52)
        self.assertEqual(job.eta_basis, "recent_steps")
        self.assertAlmostEqual(job.eta_seconds, 24.0, delta=0.5)  # 4 remaining × 6 s
        self.assertTrue(job.worker_alive)
        self.assertEqual(job.details["visibility"], "restricted")
        self.assertEqual(job.details["timing_key"], "z_image|768x1024|8||b3")

    def test_eta_unavailable_with_one_step_and_no_history(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "codex")
        make_run(session, "run-b", "running", step_events(T0, 1, 8, 6.0))
        job = self.adapter().discover(now=T0 + timedelta(seconds=15))[0]
        self.assertIsNone(job.eta_seconds)
        self.assertIsNone(job.eta_basis)
        self.assertTrue(job.progress.measured)

    def test_eta_from_history_when_steps_insufficient(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "codex")
        make_run(session, "run-c", "running", step_events(T0, 1, 8, 6.0))
        job = self.adapter(history={"z_image|768x1024|8||b3": 10.0}).discover(now=T0 + timedelta(seconds=15))[0]
        self.assertEqual(job.eta_basis, "history")
        self.assertAlmostEqual(job.eta_seconds, 70.0)

    def test_running_without_steps_is_inferred_activity(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "web")
        make_run(session, "run-d", "running", step_events(T0, 0, 8, 6.0))
        job = self.adapter().discover(now=T0 + timedelta(seconds=15))[0]
        self.assertEqual(job.progress.type, "activity")
        self.assertFalse(job.progress.measured)
        self.assertIsNone(job.progress.percent)
        self.assertIsNone(job.eta_seconds)

    def test_decoding_phase_after_denoise(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "hermes")
        events = step_events(T0, 8, 8, 6.0)
        events.append({"at": iso(T0 + timedelta(seconds=60)), "state": "running", "progress": "decoding None/None",
                       "preview": {"phase": "decoding", "progress": 90, "current_step": None, "total_steps": None}})
        make_run(session, "run-e", "running", events)
        job = self.adapter().discover(now=T0 + timedelta(seconds=65))[0]
        self.assertEqual(job.progress.type, "phase")
        self.assertIn("decoding", job.progress.label)
        self.assertFalse(job.progress.measured)
        self.assertIsNone(job.eta_seconds, "decode time is not step based; no ETA")

    def test_dead_worker_marks_run_interrupted(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "hermes")
        make_run(session, "run-f", "running", step_events(T0, 3, 8, 6.0), pid=99999)
        job = self.adapter(alive=False).discover(now=self.now)[0]
        self.assertEqual(job.status, "interrupted")
        self.assertFalse(job.worker_alive)
        self.assertIn("99999", job.note)
        self.assertTrue(job.is_terminal)
        self.assertEqual(job.progress.type, "step")  # last measured step is kept, labelled stopped
        self.assertIn("stopped", job.progress.label)

    def test_stale_but_alive_worker_gets_note(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "hermes")
        make_run(session, "run-g", "running", step_events(T0, 3, 8, 6.0))
        job = self.adapter(alive=True).discover(now=T0 + timedelta(minutes=45))[0]
        self.assertEqual(job.status, "running")
        self.assertIn("no events for", job.note)

    def test_completed_run_outputs_and_mean_step(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "hermes")
        img = self.root / "out.jpg"
        img.write_bytes(b"x")
        events = step_events(T0, 8, 8, 7.0)
        done_at = T0 + timedelta(seconds=70)
        events.append({"at": iso(done_at), "state": "completed", "data": {"success": True}})
        events.append({"at": iso(done_at), "state": "needs_review", "artifact_path": str(img)})
        make_run(session, "run-h", "needs_review", events, artifacts=[{"path": str(img), "sha256": "s", "byte_count": 1},
                                                                        {"path": str(self.root / "missing.mp4"), "sha256": "t", "byte_count": 2}])
        job = self.adapter().discover(now=self.now)[0]
        self.assertEqual(job.status, "needs_review")
        self.assertTrue(job.is_terminal)
        self.assertEqual(job.progress.percent, 100.0)
        self.assertEqual([o.kind for o in job.outputs], ["image", "video"])
        self.assertEqual([o.exists for o in job.outputs], [True, False])
        self.assertAlmostEqual(job.details["mean_step_seconds"], 7.0)
        self.assertEqual(job.details["step_samples"], 7)
        self.assertEqual(job.finished_at, iso(done_at))
        self.assertAlmostEqual(job.elapsed_seconds, 70.0)

    def test_failed_run_keeps_error(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", None)
        run_dir = make_run(session, "run-i", "failed", step_events(T0, 0, 8, 6.0) + [{"at": iso(T0 + timedelta(seconds=9)), "state": "failed", "message": "CUDA out of memory"}])
        record = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        record["error"] = {"message": "CUDA out of memory", "last_progress": None}
        (run_dir / "run.json").write_text(json.dumps(record), encoding="utf-8")
        job = self.adapter().discover(now=self.now)[0]
        self.assertEqual(job.status, "failed")
        self.assertEqual(job.error, "CUDA out of memory")
        self.assertEqual(job.requested_by, "unknown", "no prompt-trace means the requester is not invented")
        self.assertEqual(job.progress.type, "unknown")

    def test_multi_item_repeat_generation(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "hermes")
        events = step_events(T0, 4, 4, 5.0)
        second = step_events(T0 + timedelta(seconds=40), 2, 4, 5.0)[3:]
        make_run(session, "run-j", "running", events + second, settings={"model_type": "z_image", "resolution": "768x1024", "num_inference_steps": 4, "repeat_generation": 3})
        job = self.adapter().discover(now=T0 + timedelta(seconds=60))[0]
        self.assertEqual((job.progress.item_current, job.progress.item_total), (2, 3))
        self.assertEqual(job.progress.current, 2)
        self.assertIn("item 2/3", job.progress.label)
        # remaining = 2 steps in this item + 4 steps in item 3 = 6 × 5 s
        self.assertAlmostEqual(job.eta_seconds, 30.0, delta=1.0)

    def test_cache_reuses_terminal_jobs(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "hermes")
        make_run(session, "run-k", "failed", step_events(T0, 0, 8, 6.0))
        adapter = self.adapter()
        first = adapter.discover(now=self.now)[0]
        second = adapter.discover(now=self.now)[0]
        self.assertIs(first, second)

    def test_run_outside_a_session_is_named_from_the_record(self):
        """Hermes passes --runs-root <repo root>, so the run's parent is not a session directory."""
        (self.root / "README.md").write_text("# XAI-Studio-Video\n", encoding="utf-8")
        run_dir = self.root / "runs" / "run-loose"
        run_dir.mkdir(parents=True)
        (run_dir / "run.json").write_text(json.dumps({
            "run_id": "run-loose", "project_id": "jun-cafe-scene", "prompt_id": "shot-01", "status": "failed",
            "created_at": iso(T0), "updated_at": iso(T0), "target": "local", "renderer": "WanGP",
            "requested_by": "hermes", "executor": "local-wangp-worker",
            "settings": {"value": {"model_type": "minimax_h3"}}, "artifacts": [],
            "error": {"message": "Unknown model type minimax_h3"},
        }), encoding="utf-8")
        (run_dir / "events.jsonl").write_text("", encoding="utf-8")
        job = self.adapter().discover(now=self.now)[0]
        self.assertEqual(job.title, "jun-cafe-scene · shot-01", "must not inherit the repository README heading")
        self.assertIsNone(job.session_id)
        self.assertIsNone(job.character_id)
        self.assertEqual((job.requested_by, job.requested_by_basis), ("hermes", "record"))
        self.assertEqual(job.executor, "local-wangp-worker")
        self.assertEqual(job.error, "Unknown model type minimax_h3")

    def test_loose_run_falls_back_to_the_run_id_when_nothing_was_recorded(self):
        run_dir = self.root / "runs" / "run-bare"
        run_dir.mkdir(parents=True)
        (run_dir / "run.json").write_text(json.dumps({
            "run_id": "run-bare", "status": "failed", "created_at": iso(T0), "updated_at": iso(T0),
            "target": "local", "renderer": "WanGP", "settings": {"value": {}}, "artifacts": [],
        }), encoding="utf-8")
        (run_dir / "events.jsonl").write_text("", encoding="utf-8")
        job = self.adapter().discover(now=self.now)[0]
        self.assertEqual(job.title, "run-bare")
        self.assertEqual(job.requested_by, "unknown")

    def test_a_real_session_still_uses_its_own_title(self):
        session = make_session(self.root, "ch-test", "SCENE-20260909-120000-test", "카페 장면", "hermes")
        make_run(session, "run-in-session", "needs_review", [])
        job = self.adapter().discover(now=self.now)[0]
        self.assertEqual(job.title, "카페 장면 · z_image")
        self.assertEqual(job.session_id, "SCENE-20260909-120000-test")
        self.assertEqual(job.character_id, "ch-test")

    def test_scan_skips_outputs_dirs(self):
        session = make_session(self.root, "ch-test", "SCENE-1", "s", "hermes")
        (session / "outputs" / "runs" / "junk").mkdir(parents=True)
        (session / "outputs" / "runs" / "junk" / "run.json").write_text("{}", encoding="utf-8")
        make_run(session, "run-l", "failed", [])
        self.assertEqual([j.job_id for j in self.adapter().discover(now=self.now)], ["wangp:run-l"])


class NightBatchAndWebTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_night_batch_running_with_queue(self):
        batch = self.root / "night" / "NIGHT-1"
        batch.mkdir(parents=True)
        (batch / "plan.json").write_text(json.dumps({"batch_id": "NIGHT-1", "title": "Lia 야간", "created_by": "hermes", "created_at": iso(T0), "items": [
            {"id": "item-01", "status": "completed", "character_id": "ch-lia", "prompt": "a", "engines": ["z-image"], "count": 3, "session_dir": "D:/s1", "started_at": iso(T0)},
            {"id": "item-02", "status": "running", "character_id": "ch-lia", "prompt": "b", "engines": ["krea2"], "count": 3, "session_dir": "D:/s2"},
            {"id": "item-03", "status": "queued", "character_id": "ch-aoi", "prompt": "c", "engines": ["z-image", "krea2"], "count": 2},
        ]}), encoding="utf-8")
        (batch / "status.json").write_text(json.dumps({"status": "running", "updated_at": iso(T0), "total_items": 3, "completed_items": 1, "failed_items": 0}), encoding="utf-8")
        jobs = NightBatchAdapter(self.root / "night").discover(now=T0 + timedelta(minutes=5))
        self.assertEqual(len(jobs), 1)
        job = jobs[0]
        self.assertEqual(job.job_id, "night:NIGHT-1")
        self.assertEqual(job.status, "running")
        self.assertEqual(job.requested_by, "hermes")
        self.assertEqual(job.executor, "hermes-night-batch-runner")
        self.assertEqual((job.progress.type, job.progress.current, job.progress.total), ("items", 1, 3))
        self.assertTrue(job.progress.measured)
        self.assertEqual(job.session_dir, "D:/s2")
        self.assertEqual([i["id"] for i in job.details["queued_items"]], ["item-03"])

    def test_web_job(self):
        job_dir = self.root / "web" / "gen_1"
        job_dir.mkdir(parents=True)
        (job_dir / "request.json").write_text(json.dumps({"character_id": "ch-lia", "engines": ["z-image"], "count": 2, "mode": "scene", "prompt": "hello", "created_at": iso(T0)}), encoding="utf-8")
        (job_dir / "status.json").write_text(json.dumps({"status": "running", "updated_at": iso(T0), "progress": "프롬프트 정리 중", "session_dir": "D:/s9",
                                                          "runs": [{"run_dir": "D:/s9/runs/run-x"}]}), encoding="utf-8")
        job = WebJobAdapter([self.root / "web", self.root / "missing"]).discover(now=T0 + timedelta(seconds=30))[0]
        self.assertEqual(job.job_id, "web:gen_1")
        self.assertEqual(job.requested_by, "web")
        self.assertEqual(job.progress.type, "activity")
        self.assertFalse(job.progress.measured)
        self.assertEqual(job.progress.label, "프롬프트 정리 중")
        self.assertEqual(job.details["run_dirs"], ["D:/s9/runs/run-x"])

    def test_link_parents(self):
        from control_tower.jobs import Job

        night = Job(job_id="night:N", source="night-batch", title="n", requested_by="hermes", executor="x", details={"item_session_dirs": ["D:\\S2"]})
        web = Job(job_id="web:W", source="web-job", title="w", requested_by="web", executor="x", session_dir="D:/S9", details={"run_dirs": ["D:/S9/runs/run-x"]})
        run1 = Job(job_id="wangp:1", source="wangp-run", title="r", requested_by="unknown", executor="x", session_dir="D:/s2/", run_dir="D:/s2/runs/run-1")
        run2 = Job(job_id="wangp:2", source="wangp-run", title="r", requested_by="unknown", executor="x", session_dir="D:/s9", run_dir="D:\\s9\\runs\\run-x")
        run3 = Job(job_id="wangp:3", source="wangp-run", title="r", requested_by="codex", executor="x", session_dir="D:/other", run_dir="D:/other/runs/r")
        link_parents([night, web, run1, run2, run3])
        self.assertEqual((run1.parent_job_id, run1.requested_by), ("night:N", "hermes"))
        self.assertEqual((run2.parent_job_id, run2.requested_by), ("web:W", "web"))
        self.assertIsNone(run3.parent_job_id)


class EtaAndDbTests(unittest.TestCase):
    def test_estimate_rules(self):
        self.assertEqual(eta.estimate([], 5, None), (None, None))
        self.assertEqual(eta.estimate([6.0], 5, None), (None, None))
        self.assertEqual(eta.estimate([6.0], 5, 4.0), (20.0, "history"))
        value, basis = eta.estimate([6.0, 6.0, 6.0], 5, 4.0)
        self.assertEqual(basis, "recent_steps")
        self.assertAlmostEqual(value, 30.0)
        self.assertEqual(eta.estimate([6.0, 6.0], 0, None)[0], 0.0)

    def test_step_durations_ignore_resets(self):
        obs = [eta.StepObservation(1, T0), eta.StepObservation(2, T0 + timedelta(seconds=6)), eta.StepObservation(4, T0 + timedelta(seconds=18)),
               eta.StepObservation(1, T0 + timedelta(seconds=30))]
        self.assertEqual(eta.step_durations(obs), [6.0, 6.0])

    def test_db_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Database(Path(tmp) / "ct.sqlite3")
            db.upsert_jobs([{"job_id": "wangp:1", "source": "wangp-run", "status": "running", "title": "t", "updated_at": "2026-09-06T00:00:00+00:00"}])
            db.upsert_job({"job_id": "wangp:1", "source": "wangp-run", "status": "needs_review", "title": "t", "finished_at": "2026-09-06T00:10:00+00:00"})
            self.assertEqual(db.get_job("wangp:1")["status"], "needs_review")
            self.assertEqual(db.job_count(), 1)
            db.record_step_timing("k", 6.0, weight=2)
            db.record_step_timing("k", 12.0, weight=2)
            self.assertAlmostEqual(db.get_step_timing("k"), 9.0)
            self.assertIsNone(db.get_step_timing("nope"))
            db.record_host_sample("2026-09-06T00:00:00+00:00", 50.0, 1000.0, 8188.0, 60.0, 40.0)
            self.assertEqual(db.recent_host_samples(minutes=10 ** 6)[0]["util"], 50.0)
            db.close()


if __name__ == "__main__":
    unittest.main()
