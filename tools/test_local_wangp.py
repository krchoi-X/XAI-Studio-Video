from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import local_wangp


class LocalWanGPTests(unittest.TestCase):
    def test_effective_settings_replace_prompt_and_name_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"prompt": "old", "seed": 7}), encoding="utf-8")
            settings = local_wangp.load_settings(path, "exact", "run-123")
            self.assertEqual(settings["prompt"], "exact")
            self.assertEqual(settings["output_filename"], "run-123")
            self.assertEqual(settings["seed"], 7)

    def test_json_safe_serializes_event_dataclass(self) -> None:
        from dataclasses import dataclass

        @dataclass
        class Progress:
            current_step: int
            total_steps: int

        self.assertEqual(local_wangp.json_safe(Progress(2, 20)), {"current_step": 2, "total_steps": 20})


if __name__ == "__main__":
    unittest.main()
