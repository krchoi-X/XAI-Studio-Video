from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import local_wangp
import character_manager as cm


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

    def test_reference_transformation_v2_also_requires_bound_image(self) -> None:
        settings = {
            "model_type": "krea2_turbo_edit",
            "image_refs": ["missing.png"],
            "_xai": {"kind": "reference_transformation", "reference_asset_ids": ["ast-2"]},
        }
        with self.assertRaisesRegex(ValueError, "not found"):
            local_wangp.validate_reference_settings(settings)

    def test_ref2va_uses_the_durable_character_default_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            characters = root / "characters"
            image = root / "jun.png"
            image.write_bytes(b"identity image")
            character_path = characters / "ch-jun" / "character.json"
            character_path.parent.mkdir(parents=True)
            character_path.write_text(json.dumps({"reference_defaults": {"identity": {
                "path": str(image), "source": "human-selected base portrait",
            }}}), encoding="utf-8")
            session = characters / "ch-jun" / "02_generations" / "VIDEO-test"
            session.mkdir(parents=True)
            original = cm.CHARACTERS
            cm.CHARACTERS = characters
            try:
                settings = {"model_type": "minimax_h3_ref2va_pruned", "image_refs": []}
                records = local_wangp.resolve_character_default_reference(settings, session)
            finally:
                cm.CHARACTERS = original
            self.assertEqual(settings["image_refs"], [str(image.resolve())])
            self.assertEqual(records[0]["basis"], "character-default")
            self.assertEqual(records[0]["character_id"], "ch-jun")

    def test_explicit_ref2va_reference_is_never_replaced(self) -> None:
        settings = {"model_type": "minimax_h3_ref2va_pruned", "image_refs": ["chosen.png"]}
        self.assertEqual(local_wangp.resolve_character_default_reference(settings, Path("missing-session")), [])
        self.assertEqual(settings["image_refs"], ["chosen.png"])

    def test_ref2va_without_a_default_fails_before_starting_worker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            characters = Path(directory) / "characters"
            session = characters / "ch-none" / "02_generations" / "VIDEO-test"
            session.mkdir(parents=True)
            (characters / "ch-none" / "character.json").write_text("{}", encoding="utf-8")
            original = cm.CHARACTERS
            cm.CHARACTERS = characters
            try:
                with self.assertRaisesRegex(ValueError, "no reference_defaults.identity"):
                    local_wangp.resolve_character_default_reference(
                        {"model_type": "minimax_h3_ref2va_pruned", "image_refs": []}, session,
                    )
            finally:
                cm.CHARACTERS = original


if __name__ == "__main__":
    unittest.main()
