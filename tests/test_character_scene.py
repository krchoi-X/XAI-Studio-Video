import importlib.util
import sys
import unittest
import json
import tempfile
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
