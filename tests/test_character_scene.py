import importlib.util
import sys
import unittest
import json
import tempfile
import hashlib
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("character_scene", TOOLS / "character_scene.py")
scene = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(scene)


class CharacterScenePromptTests(unittest.TestCase):
    def setUp(self):
        self.character = {
            "id": "ch-test", "name": "Test", "version": 1,
            "stable_dna": {
                "adult_age_range": "adult", "visual_background": "Korean adult",
                "face": {key: "defined" for key in scene.cm.FACE_FIELDS},
                "body": {key: "natural" for key in scene.cm.BODY_FIELDS},
                "hair": "dark hair", "skin": "realistic", "distinctive_marks": [], "recognition_anchors": [],
            },
            "bounded_identity": {"hair_states": {"A": "high ponytail near the crown"}},
        }

    def test_identity_merge_keeps_user_scene_ahead_of_dna(self):
        prompt = scene.identity_merge_prompt(self.character, "explicit scene, no towel", {"coverage": "user-specified"})
        self.assertLess(prompt.index("explicit scene, no towel"), prompt.index("STABLE CHARACTER IDENTITY"))
        self.assertNotIn("complete plausible outfit", prompt)
        self.assertNotIn("covering every visible body region", prompt)

    def test_hair_scene_spec_replaces_conflicting_stable_hair(self):
        prompt = scene.identity_merge_prompt(self.character, "어깨 길이 단정한 보브", {})
        self.assertIn("shoulder-length bob", prompt)
        self.assertNotIn("Hair: dark hair", prompt)
        self.assertIn("- hair:", prompt)

    def test_non_hair_scene_preserves_stable_hair(self):
        prompt = scene.identity_merge_prompt(self.character, "창가에 앉은 상반신 사진", {})
        self.assertIn("Hair: dark hair", prompt)

    def test_generic_hair_mention_does_not_turn_entire_request_into_override(self):
        request = "Portrait with long dark hair, full bangs, and natural skin"
        spec = scene.build_scene_spec(request, {})
        self.assertNotIn("hair", spec)
        prompt = scene.identity_merge_prompt(self.character, request, {}, spec)
        self.assertIn("Hair: dark hair", prompt)
        self.assertNotIn(f"- hair: {request}", prompt)

    def test_explicit_scene_spec_is_recorded_and_suppresses_hair(self):
        spec = scene.build_scene_spec("새로운 모습", {}, {"hair": "short silver pixie cut"})
        prompt = scene.identity_merge_prompt(self.character, "새로운 모습", {}, spec)
        self.assertIn("short silver pixie cut", prompt)
        self.assertNotIn("Hair: dark hair", prompt)

    def test_hair_state_resolves_from_bounded_identity(self):
        spec = {"hair_state": "A"}
        scene.resolve_hair_state(self.character, spec)
        self.assertEqual("high ponytail near the crown", spec["hair"])

    def test_unknown_hair_state_is_rejected(self):
        with self.assertRaises(scene.cm.CharacterError):
            scene.resolve_hair_state(self.character, {"hair_state": "Z"})

    def test_scene_spec_rejects_coverage_wardrobe_conflict(self):
        spec = {"schema_version": 1, "character": "ch-test", "character_version": 1,
                "mode": "strict_translation", "coverage": "none", "wardrobe": "a towel"}
        result = scene.validate_scene_spec(self.character, spec)
        self.assertEqual("failed", result["status"])
        self.assertTrue(any("conflicts" in error for error in result["errors"]))

    def test_legacy_strategy_names_map_to_operating_modes(self):
        self.assertEqual("strict_translation", scene.normalize_strategy("identity-merge"))
        self.assertEqual("creative_expansion", scene.normalize_strategy("enriched"))

    def test_immutable_none_overrides_enriched_outfit(self):
        delta = {key: "value" for key in ("title", "pose", "expression", "outfit", "camera", "lens", "lighting", "location", "action", "styling", "negative_constraints")}
        delta["outfit"] = "a towel"
        prompt = scene.compile_prompt(self.character, {**delta, "outfit": "none"}, "explicit adult scene", {"coverage": "none"})
        self.assertIn("Coverage is none", prompt)
        self.assertIn("Outfit: none", prompt)
        self.assertNotIn("complete plausible outfit", prompt)

    def test_session_requester_prefers_batch_created_by(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            batch = {"session": {"created_by": "grok"}, "jobs": []}
            (root / "prompt-trace.json").write_text(json.dumps({"invoked_by": "codex"}), encoding="utf-8")
            self.assertEqual("grok", scene.session_requester(root, batch))

    def test_session_requester_falls_back_to_prompt_trace_and_stays_none(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertIsNone(scene.session_requester(root, {"session": {}}), "no record means no guess")
            # BOM-prefixed trace files are written by some orchestrators
            (root / "prompt-trace.json").write_bytes(b"\xef\xbb\xbf" + json.dumps({"invoked_by": "hermes"}).encode("utf-8"))
            self.assertEqual("hermes", scene.session_requester(root, {"session": {}}))

    def test_submit_forwards_requester_to_the_runner(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset_root = root / "assets"
            asset_root.mkdir()
            (root / "prompt.txt").write_text("p", encoding="utf-8")
            (root / "z-image.settings.json").write_text("{}", encoding="utf-8")
            (root / "batch.yaml").write_text(json.dumps({
                "session": {"asset_root": str(asset_root), "status": "prepared", "created_by": "grok"},
                "jobs": [{"output_dir": "outputs/z-image", "status": "prepared", "count": 1, "settings_file": "z-image.settings.json"}],
            }), encoding="utf-8")
            calls = []

            class Completed:
                stdout = json.dumps({"run_dir": str(root / "runs" / "run-1"), "run_id": "run-1"})

            def fake_run(command, **kwargs):
                calls.append(command)
                (root / "runs" / "run-1").mkdir(parents=True, exist_ok=True)
                (root / "runs" / "run-1" / "run.json").write_text(json.dumps({"status": "needs_review", "artifacts": [{"path": "a"}]}), encoding="utf-8")
                return Completed()

            original = scene.subprocess.run
            scene.subprocess.run = fake_run
            try:
                scene.submit(root, wait=True)
            finally:
                scene.subprocess.run = original
            self.assertIn("--requested-by", calls[0])
            self.assertEqual("grok", calls[0][calls[0].index("--requested-by") + 1])

    def test_submit_omits_requester_for_legacy_sessions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset_root = root / "assets"
            asset_root.mkdir()
            (root / "prompt.txt").write_text("p", encoding="utf-8")
            (root / "z-image.settings.json").write_text("{}", encoding="utf-8")
            (root / "batch.yaml").write_text(json.dumps({
                "session": {"asset_root": str(asset_root), "status": "prepared"},
                "jobs": [{"output_dir": "outputs/z-image", "status": "prepared", "count": 1, "settings_file": "z-image.settings.json"}],
            }), encoding="utf-8")
            calls = []

            class Completed:
                stdout = json.dumps({"run_dir": str(root / "runs" / "run-1"), "run_id": "run-1"})

            def fake_run(command, **kwargs):
                calls.append(command)
                (root / "runs" / "run-1").mkdir(parents=True, exist_ok=True)
                (root / "runs" / "run-1" / "run.json").write_text(json.dumps({"status": "needs_review", "artifacts": [{"path": "a"}]}), encoding="utf-8")
                return Completed()

            original = scene.subprocess.run
            scene.subprocess.run = fake_run
            try:
                scene.submit(root, wait=True)
            finally:
                scene.subprocess.run = original
            self.assertNotIn("--requested-by", calls[0])

    def test_face_discovery_records_the_actor(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("face_discovery", TOOLS / "face_discovery.py")
        face = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(face)
        parser_actions = {}

        # the CLI must offer the same actors as the scene pipeline, so grok/claude can identify themselves
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--actor", choices=face.scene.ACTORS, default="codex")
        self.assertEqual("grok", parser.parse_args(["--actor", "grok"]).actor)
        self.assertIn("grok", face.scene.ACTORS)
        # prepare() takes the actor and defaults to today's behaviour
        import inspect

        signature = inspect.signature(face.prepare)
        self.assertIn("actor", signature.parameters)
        self.assertEqual("codex", signature.parameters["actor"].default)

    def test_actor_choices_include_grok_and_claude(self):
        self.assertEqual(("codex", "hermes", "web", "grok", "claude", "user"), scene.ACTORS)

    def test_character_default_identity_reference_is_hash_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "identity.png"
            reference.write_bytes(b"identity reference bytes")
            character = {**self.character, "reference_defaults": {"identity": {
                "path": str(reference), "state": "user-selected", "source": "operator chose this face",
            }}}
            resolved = scene.resolve_identity_reference(character, "character-default")
            self.assertEqual("identity", resolved["role"])
            self.assertEqual("character-default", resolved["basis"])
            self.assertEqual(hashlib.sha256(reference.read_bytes()).hexdigest(), resolved["sha256"])
            self.assertEqual("user-selected", resolved["state"])

    def test_identity_reference_requires_a_real_supported_image(self):
        with tempfile.TemporaryDirectory() as directory:
            unsupported = Path(directory) / "identity.txt"
            unsupported.write_text("not an image", encoding="utf-8")
            with self.assertRaisesRegex(scene.cm.CharacterError, "unsupported identity reference"):
                scene.resolve_identity_reference(self.character, str(unsupported))
            with self.assertRaisesRegex(scene.cm.CharacterError, "no reference_defaults.identity"):
                scene.resolve_identity_reference(self.character, "character-default")

    def test_identity_reference_compiles_krea2_edit_settings_without_fallback(self):
        reference = {
            "path": r"D:\library\reika.png", "sha256": "abc123", "byte_count": 42,
            "asset_id": "asset-reika", "role": "identity", "basis": "character-default",
        }
        settings = scene.apply_identity_reference(
            {"model_type": "krea2_turbo_moody_krea", "NAG_scale": 1, "seed": 7},
            reference, "ch-mizuki-reika", "new scene", "grok",
        )
        self.assertEqual("krea2_turbo_edit", settings["model_type"])
        self.assertEqual([reference["path"]], settings["image_refs"])
        self.assertEqual(["abc123"], settings["_xai"]["reference_sha256s"])
        self.assertEqual(["asset-reika"], settings["_xai"]["reference_asset_ids"])
        self.assertFalse(settings["_xai"]["allow_text_fallback"])
        self.assertNotIn("NAG_scale", settings)

    def test_existing_session_submit_skips_completed_engines(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            asset_root = root / "assets"
            asset_root.mkdir()
            (root / "batch.yaml").write_text(json.dumps({
                "session": {"asset_root": str(asset_root), "status": "prepared"},
                "jobs": [{"output_dir": "outputs/z-image", "status": "completed", "count": 1}],
            }), encoding="utf-8")
            self.assertEqual([], scene.submit(root, wait=True))
            batch = json.loads((root / "batch.yaml").read_text(encoding="utf-8"))
            self.assertEqual("completed", batch["session"]["status"])


if __name__ == "__main__":
    unittest.main()


class CraftExpansionTests(unittest.TestCase):
    """Craft enrichment must be unable to restage the scene it decorates."""

    def setUp(self):
        self.character = {
            "id": "ch-test", "name": "Test", "version": 1,
            "stable_dna": {
                "adult_age_range": "adult", "visual_background": "Korean adult",
                "face": {key: "defined" for key in scene.cm.FACE_FIELDS},
                "body": {key: "natural" for key in scene.cm.BODY_FIELDS},
                "hair": "dark hair", "skin": "realistic", "distinctive_marks": [], "recognition_anchors": [],
            },
            "bounded_identity": {"hair_states": {"A": "high ponytail near the crown"}},
        }
        self.craft = {
            "camera": "waist-up, slight high angle", "lens": "50mm, shallow depth of field",
            "lighting": "late afternoon window light", "styling": "muted film grade",
            "negative_constraints": "no lens flare, no motion blur",
        }

    def test_the_meaning_half_is_the_strict_prompt_character_for_character(self):
        request = "크림색 니트를 입고 창가에 기대 앉은 상반신"
        immutable = {"coverage": "user-specified"}
        strict = scene.identity_merge_prompt(self.character, request, immutable)
        craft = scene.compile_craft_prompt(self.character, self.craft, request, immutable)
        self.assertTrue(craft.startswith(strict))

    def test_only_photography_is_appended(self):
        prompt = scene.compile_craft_prompt(self.character, self.craft, "창가에 앉은 상반신", {})
        appended = prompt[len(scene.identity_merge_prompt(self.character, "창가에 앉은 상반신", {})):]
        self.assertIn("waist-up, slight high angle", appended)
        self.assertIn("late afternoon window light", appended)
        for meaning in ("Outfit:", "Pose:", "Action:", "Location:", "Expression:"):
            self.assertNotIn(meaning, appended)

    def test_the_mode_is_a_recognised_strategy(self):
        self.assertEqual(scene.normalize_strategy("craft_expansion"), "craft_expansion")

    def test_scene_spec_validation_accepts_the_mode(self):
        spec = {"schema_version": 1, "character": "ch-test", "character_version": 1, "mode": "craft_expansion"}
        self.assertEqual(scene.validate_scene_spec(self.character, spec)["status"], "passed")

    def test_a_locked_craft_field_survives_the_model(self):
        captured = {}

        def fake_urlopen(request, timeout=0):
            captured["body"] = json.loads(request.data.decode())
            return _Response({"message": {"content": json.dumps({
                "camera": "model framing", "lens": "model lens",
                "lighting": "model lighting", "styling": "model styling",
                "negative_constraints": "model negatives",
            })}})

        original = scene.urllib.request.urlopen
        scene.urllib.request.urlopen = fake_urlopen
        try:
            craft = scene.local_craft_delta(
                "창가에 앉은 상반신", self.character, "test-model", {},
                {"lighting": "정오의 직사광"},
            )
        finally:
            scene.urllib.request.urlopen = original
        self.assertEqual(craft["lighting"], "정오의 직사광")
        self.assertEqual(craft["camera"], "model framing")

    def test_the_model_is_never_asked_for_a_meaning_field(self):
        def fake_urlopen(request, timeout=0):
            body = json.loads(request.data.decode())
            asked = body["messages"][0]["content"]
            for field in scene.MEANING_FIELDS:
                assert f"string fields: " not in asked or field not in asked.split("string fields: ")[1].split("\n")[0], field
            return _Response({"message": {"content": json.dumps({
                "camera": "c", "lens": "l", "lighting": "li", "styling": "s", "negative_constraints": "n",
            })}})

        original = scene.urllib.request.urlopen
        scene.urllib.request.urlopen = fake_urlopen
        try:
            scene.local_craft_delta("장면", self.character, "test-model", {}, {})
        finally:
            scene.urllib.request.urlopen = original

    def test_a_short_model_answer_is_refused_rather_than_padded(self):
        def fake_urlopen(request, timeout=0):
            return _Response({"message": {"content": json.dumps({"camera": "c", "lens": "l"})}})

        original = scene.urllib.request.urlopen
        scene.urllib.request.urlopen = fake_urlopen
        try:
            with self.assertRaises(scene.cm.CharacterError):
                scene.local_craft_delta("장면", self.character, "test-model", {}, {})
        finally:
            scene.urllib.request.urlopen = original


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


class InterpretTests(unittest.TestCase):
    """Reading the compilation must cost nothing but the compilation."""

    def setUp(self):
        self.character = {
            "id": "ch-test", "name": "Test", "version": 1,
            "stable_dna": {
                "adult_age_range": "adult", "visual_background": "Korean adult",
                "face": {key: "defined" for key in scene.cm.FACE_FIELDS},
                "body": {key: "natural" for key in scene.cm.BODY_FIELDS},
                "hair": "dark hair", "skin": "realistic", "distinctive_marks": [], "recognition_anchors": [],
            },
            "bounded_identity": {"hair_states": {"A": "high ponytail near the crown"}},
        }
        self._record_path = scene.cm.character_record_path
        self._load = scene.cm.load
        self._reserve = scene.cm.reserve_generation_session
        scene.cm.character_record_path = lambda character_id: _AlwaysAFile()
        scene.cm.load = lambda path: self.character
        scene.cm.reserve_generation_session = self._forbidden

    def tearDown(self):
        scene.cm.character_record_path = self._record_path
        scene.cm.load = self._load
        scene.cm.reserve_generation_session = self._reserve

    @staticmethod
    def _forbidden(*_args, **_kwargs):
        raise AssertionError("interpret must not reserve a generation session")

    def test_a_template_mode_compiles_without_a_model_or_a_session(self):
        result = scene.interpret("ch-test", "\ucc3d\uac00\uc5d0 \uc549\uc740 \uc0c1\ubc18\uc2e0", "test-model", "strict_translation")
        self.assertFalse(result["local_llm_used"])
        self.assertIsNone(result["local_model"])
        self.assertEqual(result["fields"], [])
        self.assertIn("STABLE CHARACTER IDENTITY", result["prompt"])

    def test_exact_returns_the_request_itself(self):
        result = scene.interpret("ch-test", "\uadf8\ub300\ub85c \ubcf4\ub0bc \ubb38\uc7a5", "test-model", "exact")
        self.assertEqual(result["prompt"], "\uadf8\ub300\ub85c \ubcf4\ub0bc \ubb38\uc7a5")

    def test_craft_fields_come_back_with_the_key_that_locks_them(self):
        original = scene.urllib.request.urlopen
        scene.urllib.request.urlopen = _craft_response
        try:
            result = scene.interpret("ch-test", "\ucc3d\uac00\uc5d0 \uc549\uc740 \uc0c1\ubc18\uc2e0", "test-model", "craft_expansion")
        finally:
            scene.urllib.request.urlopen = original
        keys = {item["key"]: item for item in result["fields"]}
        self.assertEqual(keys["styling"]["scene_field"], "scene_style")
        self.assertEqual(keys["camera"]["scene_field"], "camera")
        self.assertTrue(result["local_llm_used"])
        self.assertFalse(any(item["locked"] for item in result["fields"]))

    def test_a_locked_field_reports_itself_locked_and_keeps_the_operator_value(self):
        original = scene.urllib.request.urlopen
        scene.urllib.request.urlopen = _craft_response
        try:
            result = scene.interpret(
                "ch-test", "\ucc3d\uac00\uc5d0 \uc549\uc740 \uc0c1\ubc18\uc2e0", "test-model", "craft_expansion",
                supplied_scene_spec={"scene_style": "\uc0c1\uc5c5 \uad11\uace0 \ub9c8\uac10"},
            )
        finally:
            scene.urllib.request.urlopen = original
        styling = next(item for item in result["fields"] if item["key"] == "styling")
        self.assertTrue(styling["locked"])
        self.assertEqual(styling["value"], "\uc0c1\uc5c5 \uad11\uace0 \ub9c8\uac10")
        self.assertIn("\uc0c1\uc5c5 \uad11\uace0 \ub9c8\uac10", result["prompt"])

    def test_every_offered_scene_field_is_one_the_validator_accepts(self):
        for delta_key, scene_field in scene.DELTA_TO_SCENE_FIELD.items():
            self.assertIn(scene_field, scene.SCENE_FIELDS, delta_key)

    def test_an_invalid_lock_is_refused_rather_than_silently_dropped(self):
        with self.assertRaises(scene.cm.CharacterError):
            scene.interpret("ch-test", "\uc7a5\uba74", "test-model", "strict_translation",
                            supplied_scene_spec={"face": "different face"})


def _craft_response(request, timeout=0):
    return _Response({"message": {"content": json.dumps({
        "camera": "model framing", "lens": "model lens", "lighting": "model lighting",
        "styling": "model styling", "negative_constraints": "model negatives",
    })}})


class _AlwaysAFile:
    def is_file(self):
        return True
