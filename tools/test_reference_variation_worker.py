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
        })
        plan = worker.normalize_request(request)
        prompt = worker.compile_edit_instruction(request, plan)
        self.assertNotIn("{", prompt)
        self.assertNotIn("}", prompt)
        self.assertIn("- facial_feature [subtle]: 미간을 넓게", prompt)

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


if __name__ == "__main__":
    unittest.main()
