from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import wangp_recorder


class RecorderTests(unittest.TestCase):
    def test_prepare_writes_run_before_submission(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            prompt.write_text("exact prompt\n", encoding="utf-8")
            result = wangp_recorder.prepare_run(
                argparse.Namespace(
                    runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p1",
                    prompt_id="pr1", target="vast", settings_file=None, run_id="run-test",
                )
            )
            run_dir = Path(result["run_dir"])
            self.assertTrue((run_dir / "run.json").is_file())
            self.assertTrue((run_dir / "events.jsonl").is_file())
            self.assertEqual(result["status"], "queued")
            self.assertEqual(result["prompt"]["sha256"], wangp_recorder.sha256_file(prompt))

    def test_attach_marks_exact_embedded_prompt_as_succeeded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            prompt.write_text("same prompt", encoding="utf-8")
            prepared = wangp_recorder.prepare_run(
                argparse.Namespace(
                    runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p1",
                    prompt_id="pr1", target="local", settings_file=None, run_id="run-test",
                )
            )
            artifact = root / "result.mp4"
            artifact.write_bytes(b"fake-video")
            with patch.object(wangp_recorder, "ffprobe_metadata", return_value={"prompt": "same prompt"}):
                record = wangp_recorder.attach_artifact(
                    argparse.Namespace(run_dir=prepared["run_dir"], artifact=str(artifact), ffprobe="ffprobe")
                )
            self.assertEqual(record["status"], "succeeded")
            self.assertTrue(record["artifacts"][0]["prompt_exact_match"])

    def test_attach_does_not_silently_accept_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            prompt.write_text("expected", encoding="utf-8")
            prepared = wangp_recorder.prepare_run(
                argparse.Namespace(
                    runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p1",
                    prompt_id="pr1", target="runpod", settings_file=None, run_id="run-test",
                )
            )
            artifact = root / "result.mp4"
            artifact.write_bytes(b"fake-video")
            with patch.object(wangp_recorder, "ffprobe_metadata", return_value={"prompt": "different"}):
                record = wangp_recorder.attach_artifact(
                    argparse.Namespace(run_dir=prepared["run_dir"], artifact=str(artifact), ffprobe="ffprobe")
                )
            self.assertEqual(record["status"], "needs_review")
            self.assertFalse(record["artifacts"][0]["prompt_exact_match"])


if __name__ == "__main__":
    unittest.main()
