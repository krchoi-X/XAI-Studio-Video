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

    def test_qwen21_is_a_single_reference_engine_and_keeps_the_budget(self):
        plan = night.validate_plan({"items": [{
            "character_id": "ch-test", "prompt": "profile view", "engines": ["qwen21"], "count": 2,
            "identity_reference": "character-default",
        }]})
        self.assertEqual(["qwen21"], plan["items"][0]["engines"])
        self.assertEqual(2, plan["generated_image_budget"])
        for engines in (["qwen21", "krea2"], ["z-image", "qwen21"], ["z-image"]):
            with self.assertRaisesRegex(night.cm.CharacterError, "identity_reference requires"):
                night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "mixed", "engines": engines,
                                                "identity_reference": "character-default"}]})
        self.assertEqual((48, 240), (night.MAX_ITEMS, night.MAX_GENERATED_IMAGES))
        with self.assertRaisesRegex(night.cm.CharacterError, "budget exceeded"):
            night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "서로 다른 장면",
                                            "engines": ["z-image", "krea2", "qwen21"], "count": 10} for _ in range(9)]})

    def _qwen_session(self, reference_inputs, settings_extra):
        session = Path(self.temp.name) / "qwen-session"
        output = Path(self.temp.name) / "library" / "outputs" / "qwen21"
        run_dir = session / "runs" / "run-q"
        output.mkdir(parents=True); run_dir.mkdir(parents=True)
        artifact = output / "run-q.jpg"; artifact.write_bytes(b"image")
        (session / "prompt.txt").write_text("same person, profile\n", encoding="utf-8")
        (session / "qwen21.settings.json").write_text(json.dumps({
            "model_type": "qwen_image_21_uncensored_q4_k_m", **settings_extra}), encoding="utf-8")
        (run_dir / "run.json").write_text(json.dumps({
            "run_id": "run-q", "status": "needs_review", "artifacts": [{"path": str(artifact)}],
            "reference_inputs": reference_inputs,
        }), encoding="utf-8")
        (session / "batch.yaml").write_text(json.dumps({
            "session": {"asset_root": str(output.parent)},
            "jobs": [{"engine": "qwen21", "model": "qwen_image_21_uncensored_q4_k_m", "output_dir": "outputs/qwen21",
                      "settings_file": "qwen21.settings.json", "count": 1, "status": "completed", "run_dir": str(run_dir)}]
        }), encoding="utf-8")
        return session

    def test_verify_qwen21_reference_session_checks_model_and_reference(self):
        bound = {"image_refs": ["face.png"], "_xai": {"allow_text_fallback": False}}
        session = self._qwen_session([{"basis": "explicit-reference", "sha256": "abc"}], bound)
        verified = night.verify_session(session, ["qwen21"], reference_bound=True)
        self.assertEqual("qwen_image_21_uncensored_q4_k_m", verified["runs"][0]["model_type"])
        self.assertTrue(verified["runs"][0]["output_dir"].endswith("qwen21"))

    def test_verify_rejects_a_reference_item_that_rendered_from_text(self):
        session = self._qwen_session([], {})
        with self.assertRaisesRegex(night.cm.CharacterError, "not bound to an identity reference"):
            night.verify_session(session, ["qwen21"], reference_bound=True)



class HermesNightBatchMultiReferenceTests(unittest.TestCase):
    setUp = HermesNightBatchTests.setUp
    tearDown = HermesNightBatchTests.tearDown

    def test_additional_references_and_seed_are_normalized_and_forwarded(self):
        plan = night.validate_plan({"items": [{
            "character_id": "ch-test", "prompt": "outfit swap", "engines": ["qwen21"], "count": 1, "seed": 99,
            "identity_reference": "character-default",
            "additional_references": ["wardrobe=D:/refs/outfit.jpg", {"role": "object", "path": "D:/refs/bag.png"}],
        }]})
        item = plan["items"][0]
        self.assertEqual(["wardrobe=D:/refs/outfit.jpg", "object=D:/refs/bag.png"], item["additional_references"])
        root = Path(self.temp.name) / "batch"; root.mkdir()
        calls = []

        def fake_run(command, **kwargs):
            calls.append(command)
            return CompletedProcess(command, 0, json.dumps({"session_dir": str(root / "s")}), "")

        night._prepare_item({**item, "prompt_strategy": "strict_translation"}, root, fake_run)
        refs = [calls[0][i + 1] for i, value in enumerate(calls[0]) if value == "--reference"]
        self.assertEqual(item["additional_references"], refs)
        self.assertEqual("99", calls[0][calls[0].index("--seed") + 1])

    def test_additional_references_require_identity_and_qwen21(self):
        for extra in ({"engines": ["krea2"], "identity_reference": "character-default"}, {"engines": ["qwen21"]}):
            with self.assertRaisesRegex(night.cm.CharacterError, "additional_references require"):
                night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "outfit", "count": 1,
                                                "additional_references": ["wardrobe=x.jpg"], **extra}]})
        with self.assertRaisesRegex(night.cm.CharacterError, "seed must be"):
            night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "outfit", "seed": -2}]})


if __name__ == "__main__": unittest.main()
