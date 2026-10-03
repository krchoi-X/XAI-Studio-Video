import hashlib
import json
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path

import reference_variation_worker as worker


class ReferenceVariationWorkerTests(unittest.TestCase):
    def request(self) -> dict:
        return {
            "variation_id": "var-test",
            "character_id": "ch-test",
            "reference_asset_id": "ast-test",
            "reference_path": "D:/library/source.jpg",
            "operator_request": "눈썹만 진하게",
            "preserve": ["identity", "lighting"],
            "changes": {"eyebrows": "darker"},
            "strength": "subtle",
            "source_resolution": "768x1024",
        }

    def test_edit_settings_use_exact_reference_and_do_not_double_load_identity_lora(self) -> None:
        settings = worker.settings_for(self.request(), 42, Path("D:/WanGP"))
        self.assertEqual(settings["model_type"], "krea2_turbo_edit")
        self.assertEqual(settings["video_prompt_type"], "KI")
        self.assertEqual(settings["image_refs"], ["D:/library/source.jpg"])
        self.assertEqual(settings["activated_loras"], [])
        self.assertEqual(settings["_xai"]["reference_asset_ids"], ["ast-test"])

    def test_compiled_instruction_uses_template_safe_prose_instead_of_json(self) -> None:
        request = self.request()
        request.update({
            "schema_version": 2,
            "kind": "reference_transformation",
            "operations": [{"id": "op-1", "kind": "facial_feature", "instruction": "미간을 넓게", "strength": "subtle"}],
            "requested_preserve": ["identity", "wardrobe"],
            "character_contract": {
                "character_id": "ch-test", "record_path": "D:/records/ch-test/character.json",
                "character_version": 3, "stable_dna_sha256": "a" * 64,
                "stable_dna": {"recognition_anchors": ["amber eyes"]},
                "stable_dna_prompt": "- recognition anchors: amber eyes",
            },
        })
        plan = worker.normalize_request(request)
        prompt = worker.compile_edit_instruction(request, plan)
        self.assertNotIn("{", prompt)
        self.assertNotIn("}", prompt)
        self.assertIn("- facial_feature [subtle]", prompt)
        self.assertIn("Released source field: named facial features", prompt)
        self.assertIn("Target state: 미간을 넓게", prompt)
        self.assertIn("Canonical Stable DNA is mandatory identity authority", prompt)
        self.assertIn("- recognition anchors: amber eyes", prompt)
        self.assertLess(prompt.index("recognition anchors"), prompt.index("Requested change"))

    def test_compiler_releases_selected_source_fields_without_knowing_their_current_state(self) -> None:
        request = self.request()
        request.update({
            "schema_version": 2,
            "operations": [
                {"id": "pose", "kind": "pose", "instruction": "sit at the bath edge", "strength": "moderate"},
                {"id": "wardrobe", "kind": "wardrobe", "instruction": "Coverage is none.", "strength": "moderate"},
                {"id": "background", "kind": "background", "instruction": "quiet hot spring", "strength": "exploratory"},
            ],
            "requested_preserve": ["identity", "pose", "wardrobe", "background", "body_proportions"],
        })
        plan = worker.normalize_request(request)
        prompt = worker.compile_edit_instruction(request, plan)
        self.assertIn("every typed operation below replaces its named mutable field", prompt)
        self.assertIn("Released source field: body pose and contacts", prompt)
        self.assertIn("Released source field: body coverage, garments, footwear, and accessories", prompt)
        self.assertIn("Positive target interpretation: The adult subject's final wardrobe state is unclothed.", prompt)
        self.assertNotIn("source swimsuit", prompt.lower())
        self.assertNotIn("pixel identity and composition", prompt)
        self.assertIn("Preserve exactly: identity, body_proportions.", prompt)

    def test_character_contract_rechecks_current_canonical_dna(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_path = Path(directory) / "character.json"
            dna = {"recognition_anchors": ["amber eyes"], "hair": "long black hair"}
            digest = hashlib.sha256(json.dumps(dna, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            record = {"id": "ch-test", "version": 3, "stable_dna": dna}
            record_path.write_text(json.dumps(record), encoding="utf-8")
            request = self.request()
            request["character_contract"] = {
                "character_id": "ch-test", "record_path": str(record_path), "character_version": 3,
                "stable_dna_sha256": digest, "stable_dna": dna,
                "stable_dna_prompt": "- recognition anchors: amber eyes\n- hair: long black hair",
            }
            manager = SimpleNamespace(
                character_record_path=lambda _: record_path,
                load=lambda _: record,
                stable_hash=lambda value: hashlib.sha256(json.dumps(
                    value["stable_dna"], ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ).encode()).hexdigest(),
            )
            self.assertEqual(request["character_contract"], worker.validate_character_contract(request, manager))
            manager.load = lambda _: {**record, "version": 4}
            with self.assertRaisesRegex(ValueError, "version changed"):
                worker.validate_character_contract(request, manager)

    def test_status_updates_are_atomic_and_keep_prior_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            job = Path(directory)
            (job / "status.json").write_text('{"status":"queued","created_at":"then"}', encoding="utf-8")
            worker.update_status(job, "running", progress="one")
            state = json.loads((job / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "running")
            self.assertEqual(state["created_at"], "then")
            self.assertEqual(state["progress"], "one")

    def test_unverified_recomposition_blocks_before_reference_or_gpu_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            job = Path(directory)
            request = self.request()
            request.update({
                "schema_version": 2,
                "kind": "reference_transformation",
                "operations": [{"id": "hand", "kind": "hand_gesture", "instruction": "손을 볼에 대기", "strength": "moderate"}],
                "requested_preserve": ["identity", "pose", "wardrobe"],
                "requested_strategy": "auto",
            })
            (job / "request.json").write_text(json.dumps(request), encoding="utf-8")
            (job / "status.json").write_text('{"status":"queued"}', encoding="utf-8")
            result = worker.run(SimpleNamespace(job_dir=str(job), repo_root=directory))
            state = json.loads((job / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(result, 3)
            self.assertEqual(state["status"], "blocked_capability")
            self.assertEqual(state["resolved_strategy"], "recompose_with_reference")
            self.assertIn("no text-to-image fallback", state["error"])

    def test_only_qwen_pose_recomposition_passes_the_bounded_gate(self) -> None:
        pose_plan = worker.normalize_request({
            "schema_version": 2,
            "operations": [
                {"id": "pose", "kind": "pose", "instruction": "kneel beside the table", "strength": "moderate"},
                {"id": "outfit", "kind": "wardrobe", "instruction": "cream camisole", "strength": "moderate"},
            ],
            "requested_preserve": ["identity", "pose", "wardrobe"],
        })
        self.assertTrue(worker.supports_plan("qwen21", pose_plan))
        self.assertFalse(worker.supports_plan("krea2", pose_plan))
        self.assertEqual(
            {"mode": "prompt_only_limited_validation", "profile_version": worker.QWEN21_POSE_PROFILE},
            worker.effective_strength("qwen21", pose_plan),
        )

        hand_plan = worker.normalize_request({
            "schema_version": 2,
            "operations": [{"id": "hand", "kind": "hand_gesture", "instruction": "hand on cheek", "strength": "moderate"}],
        })
        self.assertFalse(worker.supports_plan("qwen21", hand_plan))

        staged_plan = worker.normalize_request({
            "schema_version": 2,
            "operations": [
                {"id": "pose", "kind": "pose", "instruction": "kneel", "strength": "moderate"},
                {"id": "face", "kind": "face_geometry", "instruction": "slimmer face", "strength": "subtle"},
            ],
        })
        self.assertFalse(worker.supports_plan("qwen21", staged_plan))

    def test_qwen_pose_recomposition_reaches_dependency_check_not_capability_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            job = Path(directory) / "job"
            job.mkdir()
            source = Path(directory) / "source.jpg"
            source.write_bytes(b"source")
            request = {
                **self.request(), "schema_version": 2, "kind": "reference_transformation",
                "engine_id": "qwen21", "reference_path": str(source),
                "reference_sha256": worker.sha256_file(source), "reference_byte_count": source.stat().st_size,
                "reference": {"asset_id": "ast-test", "path": str(source), "sha256": worker.sha256_file(source), "byte_count": source.stat().st_size},
                "operations": [{"id": "pose", "kind": "pose", "instruction": "kneel beside the table", "strength": "moderate"}],
                "requested_preserve": ["identity", "pose", "wardrobe"], "requested_strategy": "auto",
            }
            (job / "request.json").write_text(json.dumps(request), encoding="utf-8")
            (job / "status.json").write_text('{"status":"queued"}', encoding="utf-8")
            empty_wangp = Path(directory) / "wangp"
            empty_wangp.mkdir()
            result = worker.run(SimpleNamespace(job_dir=str(job), repo_root=directory, wangp_root=str(empty_wangp)))
            state = json.loads((job / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(2, result)
            self.assertEqual("blocked_dependency", state["status"])

    def test_records_without_an_engine_stay_krea2(self) -> None:
        self.assertEqual("krea2", worker.engine_of(self.request()))
        settings = worker.settings_for(self.request(), 7, Path("D:/WanGP"))
        self.assertEqual("krea2_turbo_edit", settings["model_type"])
        self.assertNotIn("engine", settings["_xai"])
        with self.assertRaisesRegex(ValueError, "unsupported reference variation engine"):
            worker.engine_of({**self.request(), "engine_id": "z-image"})

    def test_qwen21_settings_are_hash_bound_and_pass_the_submit_gate(self) -> None:
        import local_wangp

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.jpg"
            source.write_bytes(b"source image bytes")
            request = {**self.request(), "engine_id": "qwen21", "reference_path": str(source),
                       "reference_sha256": worker.sha256_file(source), "reference_byte_count": source.stat().st_size}
            settings = worker.settings_for(request, 42, Path("D:/WanGP"))
            self.assertEqual("qwen_image_21_uncensored_q4_k_m", settings["model_type"])
            self.assertEqual("I", settings["video_prompt_type"])
            self.assertEqual("608x832", settings["resolution"])
            self.assertEqual([str(source)], settings["image_refs"])
            self.assertFalse(settings["_xai"]["allow_text_fallback"])
            self.assertNotIn("model_filename", settings)
            records = local_wangp.validate_reference_settings(settings)
            self.assertEqual(("ast-test", "source"), (records[0]["asset_id"], records[0]["role"]))
            source.write_bytes(b"changed after queueing")
            with self.assertRaisesRegex(ValueError, "changed after preparation"):
                local_wangp.validate_reference_settings(settings)
            self.assertEqual("832x608", worker.settings_for({**request, "source_resolution": "1402x1122"}, 1, Path("D:/WanGP"))["resolution"])

    def test_missing_qwen21_components_block_before_any_session_or_gpu_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            job = Path(directory) / "job"
            job.mkdir()
            source = Path(directory) / "source.jpg"
            source.write_bytes(b"source")
            request = {**self.request(), "engine_id": "qwen21", "reference_path": str(source),
                       "reference_sha256": worker.sha256_file(source), "reference_byte_count": source.stat().st_size}
            (job / "request.json").write_text(json.dumps(request), encoding="utf-8")
            (job / "status.json").write_text('{"status":"queued"}', encoding="utf-8")
            empty_wangp = Path(directory) / "wangp"
            empty_wangp.mkdir()
            result = worker.run(SimpleNamespace(job_dir=str(job), repo_root=directory, wangp_root=str(empty_wangp)))
            state = json.loads((job / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(2, result)
            self.assertEqual("blocked_dependency", state["status"])
            self.assertIn("Qwen Image 2.1", state["progress"])
            self.assertIn("qwen_image_21_uncensored_q4_k_m.json", state["error"])

    def test_installed_qwen21_components_resolve_from_the_finetune_definition(self) -> None:
        root = Path(r"D:\AI\WanGP")
        if not (root / "finetunes" / "qwen_image_21_uncensored_q4_k_m.json").is_file():
            self.skipTest("WanGP Qwen finetune is not installed on this machine")
        missing = [str(path) for path in worker.ENGINES["qwen21"]["required"](root) if not path.is_file()]
        self.assertEqual([], missing)
        self.assertTrue(str(worker._qwen21_checkpoint(root)).lower().endswith(".gguf"))


if __name__ == "__main__":
    unittest.main()
