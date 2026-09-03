import json
import tempfile
import unittest
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

    def test_status_updates_are_atomic_and_keep_prior_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            job = Path(directory)
            (job / "status.json").write_text('{"status":"queued","created_at":"then"}', encoding="utf-8")
            worker.update_status(job, "running", progress="one")
            state = json.loads((job / "status.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "running")
            self.assertEqual(state["created_at"], "then")
            self.assertEqual(state["progress"], "one")


if __name__ == "__main__":
    unittest.main()
