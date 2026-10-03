from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_prepared_reference_hash_must_still_match(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "identity.png"
            image.write_bytes(b"original identity")
            settings = {
                "model_type": "krea2_turbo_edit",
                "image_refs": [str(image)],
                "_xai": {
                    "kind": "reference_transformation",
                    "reference_role": "identity",
                    "reference_sha256s": [local_wangp.wangp_recorder.sha256_file(image)],
                    "reference_byte_counts": [image.stat().st_size],
                },
            }
            records = local_wangp.validate_reference_settings(settings)
            self.assertEqual("identity", records[0]["role"])
            image.write_bytes(b"changed identity")
            with self.assertRaisesRegex(ValueError, "changed after preparation"):
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
            original_shared_authority_root = cm.shared_authority_root
            cm.CHARACTERS = characters
            cm.shared_authority_root = lambda: None
            try:
                settings = {"model_type": "minimax_h3_ref2va_pruned", "image_refs": []}
                records = local_wangp.resolve_character_default_reference(settings, session)
            finally:
                cm.CHARACTERS = original
                cm.shared_authority_root = original_shared_authority_root
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
            original_shared_authority_root = cm.shared_authority_root
            cm.CHARACTERS = characters
            cm.shared_authority_root = lambda: None
            try:
                with self.assertRaisesRegex(ValueError, "no reference_defaults.identity"):
                    local_wangp.resolve_character_default_reference(
                        {"model_type": "minimax_h3_ref2va_pruned", "image_refs": []}, session,
                    )
            finally:
                cm.CHARACTERS = original
                cm.shared_authority_root = original_shared_authority_root

    def test_registered_production_plan_is_immutable_after_session_registration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = root / "session"
            session.mkdir()
            plan = root / "plan.json"
            plan.write_text('{"schema_version": 2}', encoding="utf-8")
            expected_hash = local_wangp.wangp_recorder.sha256_file(plan)
            (session / "session-provenance.json").write_text(json.dumps({
                "production_plan": {"path": str(plan), "sha256": expected_hash}
            }), encoding="utf-8")
            resolved = local_wangp._registered_production_plan(session, None)
            self.assertEqual(resolved, (plan.resolve(), expected_hash))
            plan.write_text('{"schema_version": 2, "changed": true}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed after session registration"):
                local_wangp._registered_production_plan(session, None)

    def test_invalid_v2_contract_stops_before_a_run_is_created(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = root / "session"
            session.mkdir()
            prompt = session / "pack-A.txt"
            prompt.write_text("Lia walks on the beach.", encoding="utf-8")
            settings = session / "pack-A.settings.json"
            settings.write_text(json.dumps({
                "model_type": "minimax_h3_ref2va_pruned",
                "image_refs": ["missing-identity.png", "missing-body.png"],
            }), encoding="utf-8")
            source = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "shot-production-plan" / "lia-pack-contract-v2.json"
            plan_path = session / "shot-production-plan-v2.json"
            plan_path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            (session / "session-provenance.json").write_text(json.dumps({
                "requested_by": "hermes",
                "production_plan": {
                    "path": str(plan_path),
                    "sha256": local_wangp.wangp_recorder.sha256_file(plan_path),
                },
            }), encoding="utf-8")
            fake_python = root / "python.exe"
            fake_python.write_bytes(b"")
            plan = local_wangp.shot_production_plan.load_json(plan_path)
            contract = plan["character_contracts"][0]
            current = {"ch-lia": {
                "record_path": contract["record_path"],
                "character_version": contract["character_version"],
                "stable_dna_sha256": contract["stable_dna_sha256"],
            }}
            args = type("Args", (), {
                "wangp_root": str(root), "wangp_python": str(fake_python),
                "prompt_file": str(prompt), "settings_file": str(settings),
                "runs_root": str(session / "runs"), "requested_by": None,
                "executor": None, "production_plan": None, "prompt_id": "pack-A",
            })()
            with patch.object(local_wangp, "_current_character_contracts", return_value=current):
                with self.assertRaisesRegex(ValueError, "mandatory prompt anchors are missing"):
                    local_wangp.submit(args)
            self.assertFalse((session / "runs").exists())


if __name__ == "__main__":
    unittest.main()
