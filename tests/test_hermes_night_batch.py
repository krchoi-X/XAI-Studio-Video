import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("hermes_night_batch", TOOLS / "hermes_night_batch.py")
night = importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(night)


class HermesNightBatchTests(unittest.TestCase):
    def setUp(self):
        self.original_characters = night.cm.CHARACTERS
        self.original_shared_authority_root = night.cm.shared_authority_root
        self.temp = tempfile.TemporaryDirectory()
        night.cm.CHARACTERS = Path(self.temp.name) / "characters"
        night.cm.shared_authority_root = lambda: None
        target = night.cm.CHARACTERS / "ch-test"
        target.mkdir(parents=True)
        (target / "character.json").write_text("{}", encoding="utf-8")

    def tearDown(self):
        night.cm.CHARACTERS = self.original_characters
        night.cm.shared_authority_root = self.original_shared_authority_root
        self.temp.cleanup()

    def test_plan_is_normalized_and_budgeted(self):
        plan = night.validate_plan({"title": "test", "items": [{"character_id": "ch-test", "prompt": "창가의 상반신", "engines": ["z-image", "krea2"], "count": 3}]})
        self.assertEqual(6, plan["generated_image_budget"])
        self.assertEqual("strict_translation", plan["items"][0]["prompt_strategy"])

    def test_plan_rejects_excessive_morning_review_load(self):
        with self.assertRaises(night.cm.CharacterError):
            night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "서로 다른 장면", "engines": ["z-image", "krea2"], "count": 10} for _ in range(13)]})

    def test_nested_scenes_gets_structural_error_instead_of_prompt_length_advice(self):
        with self.assertRaisesRegex(night.cm.CharacterError, r"nested scenes.*own items\[\]"):
            night.validate_plan({"items": [{"character_id": "ch-test", "scenes": [
                {"prompt": "this prompt is already detailed and long enough"}
            ]}]})

    def test_variation_axes_are_preserved_for_tablet_comparison(self):
        plan = night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "해변 카페", "count": 1,
            "variation_axes": {"hair": "bob", "scene": "beach-cafe", "lighting": "sunset"}}]})
        self.assertEqual("sunset", plan["items"][0]["variation_axes"]["lighting"])

    def test_identity_reference_is_preserved_and_restricted_to_krea2(self):
        plan = night.validate_plan({"items": [{
            "character_id": "ch-test", "prompt": "reference-bound portrait",
            "engines": ["krea2"], "count": 1, "identity_reference": "character-default",
            "reference_asset_id": "asset-identity",
        }]})
        item = plan["items"][0]
        self.assertEqual("character-default", item["identity_reference"])
        self.assertEqual("asset-identity", item["reference_asset_id"])
        with self.assertRaisesRegex(night.cm.CharacterError, "identity_reference requires"):
            night.validate_plan({"items": [{
                "character_id": "ch-test", "prompt": "invalid mixed engines",
                "engines": ["z-image", "krea2"], "identity_reference": "character-default",
            }]})

    def test_prepare_item_forwards_identity_reference_to_shared_scene_cli(self):
        root = Path(self.temp.name) / "batch"
        root.mkdir()
        session = Path(self.temp.name) / "prepared-session"
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            return CompletedProcess(command, 0, json.dumps({"session_dir": str(session)}), "")

        item = {
            "id": "item-01", "character_id": "ch-test", "prompt": "reference-bound portrait",
            "engines": ["krea2"], "count": 1, "prompt_strategy": "strict_translation",
            "immutable_constraints": {}, "scene_spec": {},
            "identity_reference": "character-default", "reference_asset_id": "asset-identity",
        }
        prepared = night._prepare_item(item, root, fake_run)
        self.assertEqual(session.resolve(), prepared)
        self.assertEqual("character-default", calls[0][calls[0].index("--identity-reference") + 1])
        self.assertEqual("asset-identity", calls[0][calls[0].index("--reference-asset-id") + 1])

    def test_create_without_start_writes_durable_queue(self):
        root = Path(self.temp.name); plan_path = root / "input.json"
        plan_path.write_text(json.dumps({"source_request": "오늘 밤 테스트", "items": [{"character_id": "ch-test", "prompt": "흰 스튜디오 사진", "count": 1}]}), encoding="utf-8")
        batch = night.create(plan_path, root / "queue", False)
        self.assertTrue((batch / "plan.json").is_file())
        self.assertEqual("queued", json.loads((batch / "status.json").read_text(encoding="utf-8"))["status"])

    def test_gpu_lock_failure_retries_same_session_and_preserves_failed_run(self):
        root = Path(self.temp.name) / "batch"
        session = Path(self.temp.name) / "session"
        failed_run = session / "runs" / "run-failed"
        failed_run.mkdir(parents=True)
        (failed_run / "run.json").write_text(json.dumps({
            "status": "failed", "error": {"message": "RuntimeError: another XAI local WanGP worker already holds the GPU lock"}
        }), encoding="utf-8")
        session.mkdir(exist_ok=True)
        (session / "batch.yaml").write_text(json.dumps({
            "jobs": [{"output_dir": "outputs/krea2", "run_dir": str(failed_run), "status": "failed"}]
        }), encoding="utf-8")
        root.mkdir()
        item = {"id": "item-01", "attempts": []}
        (root / "plan.json").write_text(json.dumps({"items": [item]}), encoding="utf-8")
        calls = []
        results = iter([CompletedProcess([], 2, "", "render failed"), CompletedProcess([], 0, "{}", "")])

        def fake_run(command, **kwargs):
            calls.append(command)
            return next(results)

        delays = []
        result = night._render_item(item, session, root, fake_run, delays.append, (10, 20, 40))
        self.assertEqual(0, result.returncode)
        self.assertEqual([10], delays)
        self.assertEqual(2, len(calls))
        self.assertEqual(str(session.resolve()), calls[0][-1])
        self.assertEqual(calls[0], calls[1])
        self.assertTrue((failed_run / "run.json").is_file())
        self.assertTrue(item["attempts"][0]["gpu_lock_failure"])

    def test_non_lock_failure_is_not_retried(self):
        root = Path(self.temp.name) / "batch"
        session = Path(self.temp.name) / "session"
        root.mkdir(); session.mkdir()
        (root / "plan.json").write_text(json.dumps({"items": [{"id": "item-01"}]}), encoding="utf-8")
        (session / "batch.yaml").write_text(json.dumps({"jobs": []}), encoding="utf-8")
        item = {"id": "item-01"}
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            return CompletedProcess(command, 2, "", "invalid settings")

        result = night._render_item(item, session, root, fake_run, lambda _: self.fail("must not sleep"), (10, 20, 40))
        self.assertEqual(2, result.returncode)
        self.assertEqual(1, len(calls))

    def test_verify_krea2_session_does_not_require_ref2va_basis(self):
        session = Path(self.temp.name) / "session"
        output = Path(self.temp.name) / "library" / "outputs" / "krea2"
        run_dir = session / "runs" / "run-ok"
        output.mkdir(parents=True); run_dir.mkdir(parents=True)
        artifact = output / "run-ok.jpg"; artifact.write_bytes(b"image")
        (session / "prompt.txt").write_text("adult character in a new outfit\n", encoding="utf-8")
        (session / "krea2.settings.json").write_text(json.dumps({"model_type": "krea2_turbo_moody_krea"}), encoding="utf-8")
        (run_dir / "run.json").write_text(json.dumps({
            "run_id": "run-ok", "status": "needs_review", "artifacts": [{"path": str(artifact)}]
        }), encoding="utf-8")
        (session / "batch.yaml").write_text(json.dumps({
            "session": {"asset_root": str(output.parent)},
            "jobs": [{"output_dir": "outputs/krea2", "settings_file": "krea2.settings.json", "count": 1,
                      "status": "completed", "run_dir": str(run_dir)}]
        }), encoding="utf-8")
        verified = night.verify_session(session, ["krea2"])
        self.assertEqual("krea2_turbo_moody_krea", verified["runs"][0]["model_type"])
        self.assertEqual([], verified["runs"][0]["reference_bases"])


if __name__ == "__main__": unittest.main()
