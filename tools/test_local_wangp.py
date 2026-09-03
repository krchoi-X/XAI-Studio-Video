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

    def test_reference_variation_records_hash_and_rejects_text_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "source.png"
            image.write_bytes(b"image-bytes")
            settings = {
                "model_type": "krea2_turbo_edit",
                "base_model_type": "krea2_turbo_edit",
                "image_refs": [str(image)],
                "_xai": {"kind": "reference_variation", "reference_asset_ids": ["ast-1"]},
            }
            records = local_wangp.validate_reference_settings(settings)
            self.assertEqual(records[0]["asset_id"], "ast-1")
            self.assertEqual(records[0]["sha256"], local_wangp.wangp_recorder.sha256_file(image))
            settings["base_model_type"] = "krea2_turbo"
            with self.assertRaisesRegex(ValueError, "fallback is disabled"):
                local_wangp.validate_reference_settings(settings)

    def test_reference_variation_requires_existing_image(self) -> None:
        settings = {
            "model_type": "krea2_turbo_edit",
            "image_refs": ["missing.png"],
            "_xai": {"kind": "reference_variation"},
        }
        with self.assertRaisesRegex(ValueError, "not found"):
            local_wangp.validate_reference_settings(settings)


if __name__ == "__main__":
    unittest.main()
