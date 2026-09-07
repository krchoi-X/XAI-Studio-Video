"""Explicit requester provenance on the WanGP submit path.

Includes a real end-to-end `local_wangp.py submit` against a fake WanGP root: a detached worker process is
started exactly as in production, but the fake `shared.api` writes a tiny WAV instead of touching the GPU.
"""
from __future__ import annotations

import argparse
import json
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import local_wangp
import wangp_recorder

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent

FAKE_WANGP_API = '''
"""Fake WanGP API for tests: no GPU, no model, writes one small WAV artifact."""
import struct, time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Event:
    kind: str
    data: object


class Events:
    def __init__(self, events):
        self._events = list(events)

    def iter(self, timeout=0.5):
        for event in self._events:
            yield event


@dataclass
class Result:
    success: bool
    generated_files: list
    errors: list = field(default_factory=list)
    artifacts: list = field(default_factory=list)


class Job:
    def __init__(self, path):
        self.path = path
        self.events = Events([
            Event("preview", {"phase": "inference", "current_step": 1, "total_steps": 2, "progress": 40}),
            Event("preview", {"phase": "inference", "current_step": 2, "total_steps": 2, "progress": 80}),
            Event("completed", {"success": True}),
        ])

    def result(self, timeout=0):
        return Result(success=True, generated_files=[str(self.path)])


class Session:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)

    def submit(self, settings):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / f"{settings.get('output_filename', 'out')}.wav"
        frames = b"".join(struct.pack("<h", 0) for _ in range(400))
        header = b"RIFF" + struct.pack("<I", 36 + len(frames)) + b"WAVEfmt " + struct.pack(
            "<IHHIIHH", 16, 1, 1, 8000, 16000, 2, 16) + b"data" + struct.pack("<I", len(frames))
        path.write_bytes(header + frames)
        return Job(path)


def init(root=None, config_path=None, output_dir=None, cli_args=(), console_output=False, console_isatty=False):
    return Session(output_dir)
'''


def make_fake_wangp(root: Path) -> Path:
    wangp = root / "FakeWanGP"
    (wangp / "shared").mkdir(parents=True)
    (wangp / "shared" / "__init__.py").write_text("", encoding="utf-8")
    (wangp / "shared" / "api.py").write_text(FAKE_WANGP_API, encoding="utf-8")
    (wangp / "wgp.py").write_text("", encoding="utf-8")
    (wangp / "wgp_config.json").write_text("{}", encoding="utf-8")
    (wangp / "outputs").mkdir()
    return wangp


class ActorNormalizationTests(unittest.TestCase):
    def test_accepts_known_and_new_actors(self):
        self.assertEqual(wangp_recorder.normalize_actor("Grok"), "grok")
        self.assertEqual(wangp_recorder.normalize_actor(" HERMES "), "hermes")
        self.assertEqual(wangp_recorder.normalize_actor("Grok Bot"), "grok-bot")
        self.assertEqual(wangp_recorder.normalize_actor("claude"), "claude")

    def test_missing_stays_null_and_is_never_guessed(self):
        self.assertIsNone(wangp_recorder.normalize_actor(None))
        self.assertIsNone(wangp_recorder.normalize_actor(""))
        self.assertIsNone(wangp_recorder.normalize_actor("   "))

    def test_rejects_junk(self):
        for value in ("a b/c", "../etc", "x" * 40, "-leading"):
            with self.assertRaises(ValueError):
                wangp_recorder.normalize_actor(value)


class RecorderProvenanceTests(unittest.TestCase):
    def prepare(self, root: Path, **extra):
        prompt = root / "prompt.txt"
        prompt.write_text("exact prompt\n", encoding="utf-8")
        namespace = argparse.Namespace(
            runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p1", prompt_id="pr1",
            target="local", settings_file=None, run_id=None, **extra)
        return wangp_recorder.prepare_run(namespace)

    def test_prepare_records_requester_and_executor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.prepare(root, requested_by="Grok", executor="local-wangp-worker")
            record = json.loads((Path(result["run_dir"]) / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(record["requested_by"], "grok")
            self.assertEqual(record["executor"], "local-wangp-worker")
            self.assertEqual(record["renderer"], "WanGP", "engine stays separate from requester and executor")
            event = json.loads((Path(result["run_dir"]) / "events.jsonl").read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(event["requested_by"], "grok")

    def test_prepare_without_requester_writes_null(self):
        with tempfile.TemporaryDirectory() as directory:
            record = json.loads((Path(self.prepare(Path(directory))["run_dir"]) / "run.json").read_text(encoding="utf-8"))
            self.assertIsNone(record["requested_by"])
            self.assertIsNone(record["executor"])

    def test_legacy_namespace_without_the_new_fields_still_works(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            prompt.write_text("p", encoding="utf-8")
            result = wangp_recorder.prepare_run(argparse.Namespace(
                runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p", prompt_id="q",
                target="vast", settings_file=None, run_id="run-legacy"))
            self.assertIsNone(result["requested_by"])


class SubmitEndToEndTests(unittest.TestCase):
    """Real submit -> detached worker -> run record, with a fake WanGP (no GPU)."""

    def submit(self, root: Path, extra_args: list[str], env: dict | None = None) -> dict:
        wangp = make_fake_wangp(root)
        prompt = root / "prompt.txt"
        prompt.write_text("a quiet sea\n", encoding="utf-8")
        settings = root / "settings.json"
        settings.write_text(json.dumps({"model_type": "fake_model", "resolution": "64x64", "num_inference_steps": 2}), encoding="utf-8")
        command = [sys.executable, str(TOOLS / "local_wangp.py"), "submit",
                   "--runs-root", str(root / "runs"), "--prompt-file", str(prompt), "--settings-file", str(settings),
                   "--project-id", "test-project", "--prompt-id", "shot-01",
                   "--wangp-root", str(wangp), "--wangp-python", sys.executable,
                   "--output-dir", str(root / "outputs")] + extra_args
        completed = subprocess.run(command, cwd=str(REPO), capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", timeout=120, env=env)
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        return json.loads(completed.stdout)

    def wait_terminal(self, run_dir: Path, timeout: float = 90.0) -> dict:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            record = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            if record["status"] in wangp_recorder.TERMINAL_STATES or record["status"] == "needs_review":
                return record
            time.sleep(0.5)
        raise AssertionError(f"run did not finish: {record}")

    def test_requester_survives_detached_worker_and_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            submitted = self.submit(root, ["--requested-by", "grok"])
            self.assertEqual(submitted["requested_by"], "grok")
            self.assertEqual(submitted["executor"], "local-wangp-worker")
            run_dir = Path(submitted["run_dir"])
            queued = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(queued["requested_by"], "grok")
            record = self.wait_terminal(run_dir)
            # the detached worker rewrote run.json several times; provenance must still be there
            self.assertEqual(record["requested_by"], "grok")
            self.assertEqual(record["executor"], "local-wangp-worker")
            self.assertEqual(record["status"], "needs_review")
            self.assertEqual(len(record["artifacts"]), 1)
            self.assertEqual(record["renderer"], "WanGP")
            self.assertEqual(record["settings"]["value"]["model_type"], "fake_model")
            self.assertIn("--requested-by", record["local_worker"]["command"])
            status = json.loads(subprocess.run(
                [sys.executable, str(TOOLS / "local_wangp.py"), "status", "--run-dir", str(run_dir)],
                cwd=str(REPO), capture_output=True, text=True, encoding="utf-8", check=True).stdout)
            self.assertEqual(status["run"]["requested_by"], "grok")

    def test_environment_default_and_omission(self):
        import os

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "env"
            root.mkdir()
            env = dict(os.environ, XAI_REQUESTED_BY="claude")
            submitted = self.submit(root, [], env=env)
            self.assertEqual(submitted["requested_by"], "claude")
            self.wait_terminal(Path(submitted["run_dir"]))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "none"
            root.mkdir()
            env = {k: v for k, v in os.environ.items() if k != "XAI_REQUESTED_BY"}
            submitted = self.submit(root, [], env=env)
            self.assertIsNone(submitted["requested_by"], "no flag and no env means null, never a guess")
            record = self.wait_terminal(Path(submitted["run_dir"]))
            self.assertIsNone(record["requested_by"])
            self.assertNotIn("--requested-by", record["local_worker"]["command"])

    def test_invalid_requester_is_rejected_before_any_record_is_written(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wangp = make_fake_wangp(root)
            prompt = root / "prompt.txt"
            prompt.write_text("p", encoding="utf-8")
            settings = root / "settings.json"
            settings.write_text("{}", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(TOOLS / "local_wangp.py"), "submit", "--runs-root", str(root / "runs"),
                 "--prompt-file", str(prompt), "--settings-file", str(settings), "--project-id", "p",
                 "--prompt-id", "q", "--wangp-root", str(wangp), "--wangp-python", sys.executable,
                 "--output-dir", str(root / "outputs"), "--requested-by", "not a valid actor/name"],
                cwd=str(REPO), capture_output=True, text=True, encoding="utf-8", timeout=60)
            self.assertEqual(completed.returncode, 2)
            self.assertIn("invalid requester token", completed.stderr)
            self.assertFalse((root / "runs").exists(), "no run directory is created for a rejected submission")


if __name__ == "__main__":
    unittest.main()
