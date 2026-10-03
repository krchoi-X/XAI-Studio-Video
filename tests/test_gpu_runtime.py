from __future__ import annotations

import json
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

import sys

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import gpu_runtime
import local_wangp


class _Response:
    def __init__(self, value):
        self.body = json.dumps(value).encode("utf-8") if value is not None else b""

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None

    def read(self):
        return self.body


class GPURuntimeTests(unittest.TestCase):
    def test_unload_hermes_uses_runtime_key_without_returning_it(self):
        with tempfile.TemporaryDirectory() as directory:
            descriptor = Path(directory) / "server.json"
            descriptor.write_text(json.dumps({
                "base_url": "http://127.0.0.1:18434/v1", "api_key": "secret-key",
            }), encoding="utf-8")
            requests = []

            def fake_urlopen(request, **_):
                requests.append(request)
                if request.full_url.endswith("/models"):
                    return _Response({"data": [
                        {"id": "huihui", "status": {"value": "loaded"}},
                        {"id": "minimax", "status": {"value": "unloaded"}},
                    ]})
                self.assertEqual({"model": "huihui"}, json.loads(request.data))
                return _Response(None)

            with patch.object(urllib.request, "urlopen", side_effect=fake_urlopen):
                result = gpu_runtime.unload_hermes_models(descriptor)
            self.assertEqual(["huihui"], result)
            self.assertEqual("Bearer secret-key", requests[0].headers["Authorization"])
            self.assertTrue(requests[1].full_url.endswith("/models/unload"))
            self.assertNotIn("secret-key", json.dumps(result))

    def test_prepare_renderer_retries_until_models_are_gone_and_vram_is_free(self):
        telemetry = iter([
            {"total_mb": 8188, "used_mb": 7000, "free_mb": 1188, "utilization_percent": 90},
            {"total_mb": 8188, "used_mb": 300, "free_mb": 7888, "utilization_percent": 1},
        ])
        releases = iter([
            {"hermes_unloaded": ["huihui"], "ollama_unloaded": ["meromero"], "errors": []},
            {"hermes_unloaded": [], "ollama_unloaded": [], "errors": []},
        ])
        with patch.object(gpu_runtime, "release_local_llms", side_effect=lambda: next(releases)), \
             patch.object(gpu_runtime, "hermes_loaded_models", return_value=[]), \
             patch.object(gpu_runtime, "ollama_loaded_models", return_value=[]):
            report = gpu_runtime.prepare_renderer_gpu(
                timeout_seconds=10, poll_seconds=0, sleep=lambda _: None,
                telemetry=lambda: next(telemetry),
            )
        self.assertEqual("ready", report["status"])
        self.assertEqual(["huihui"], report["hermes_unloaded"])
        self.assertEqual(["meromero"], report["ollama_unloaded"])
        self.assertGreaterEqual(report["telemetry"]["free_mb"], 6144)

    def test_prepare_renderer_fails_closed_when_vram_does_not_clear(self):
        with patch.object(gpu_runtime, "release_local_llms", return_value={
                 "hermes_unloaded": [], "ollama_unloaded": [], "errors": []}), \
             patch.object(gpu_runtime, "hermes_loaded_models", return_value=[]), \
             patch.object(gpu_runtime, "ollama_loaded_models", return_value=[]), \
             patch.object(gpu_runtime.time, "monotonic", side_effect=[0, 2]):
            with self.assertRaisesRegex(RuntimeError, "GPU handoff failed"):
                gpu_runtime.prepare_renderer_gpu(
                    timeout_seconds=1, poll_seconds=0, sleep=lambda _: None,
                    telemetry=lambda: {"total_mb": 8188, "used_mb": 5000, "free_mb": 3188, "utilization_percent": 2},
                )

    def test_wait_for_terminal_keeps_caller_blocked(self):
        records = iter([{"status": "starting"}, {"status": "running"}, {"status": "needs_review"}])
        sleeps = []
        with patch.object(local_wangp.wangp_recorder, "load_run", side_effect=lambda _: next(records)):
            result = local_wangp.wait_for_terminal(Path("run"), poll_seconds=0, sleep=sleeps.append)
        self.assertEqual("needs_review", result["status"])
        self.assertEqual([0, 0], sleeps)

    def test_submit_parser_exposes_blocking_hermes_option(self):
        args = local_wangp.build_parser().parse_args([
            "submit", "--runs-root", "runs", "--prompt-file", "prompt.txt",
            "--settings-file", "settings.json", "--project-id", "p", "--prompt-id", "s",
            "--requested-by", "hermes", "--wait",
        ])
        self.assertTrue(args.wait)
        self.assertEqual("hermes", args.requested_by)


if __name__ == "__main__":
    unittest.main()
