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
