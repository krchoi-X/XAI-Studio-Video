import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "character_manager.py"
SPEC = importlib.util.spec_from_file_location("character_manager", MODULE_PATH)
cm = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(cm)


def record(character_id="ch-test-adult"):
    return {
        "schema_version": 1,
        "id": character_id,
        "name": "테스트",
        "status": "draft",
        "version": 1,
        "stable_dna": {
            "adult_age_range": "adult in their 20s",
            "visual_background": "Korean adult",
            "face": {key: "defined" for key in cm.FACE_FIELDS},
            "body": {key: "natural" for key in cm.BODY_FIELDS},
            "hair": "dark hair",
            "skin": "realistic skin",
            "distinctive_marks": [],
            "recognition_anchors": ["dark hair"],
        },
        "scene_defaults": {},
        "provenance": {"created_at": "x", "updated_at": "x", "created_by": "test", "sources": []},
    }


class CharacterManagerTests(unittest.TestCase):
    def test_valid_record_and_stable_hash(self):
        item = record()
        self.assertEqual([], cm.validate(item))
        self.assertEqual(cm.stable_hash(item), cm.stable_hash(json.loads(json.dumps(item))))

    def test_scene_change_does_not_change_stable_hash(self):
        item = record()
        before = cm.stable_hash(item)
        item["scene_defaults"]["expression"] = "smile"
        self.assertEqual(before, cm.stable_hash(item))

    def test_stable_change_changes_hash(self):
        item = record()
        before = cm.stable_hash(item)
        item["stable_dna"]["hair"] = "silver hair"
        self.assertNotEqual(before, cm.stable_hash(item))

    def test_missing_body_field_is_rejected(self):
        item = record()
        del item["stable_dna"]["body"]["pelvis_hips"]
        self.assertIn("stable_dna.body missing: pelvis_hips", cm.validate(item))

    def test_promotion_rejects_source_outside_drafts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "character.json"
            path.write_text(json.dumps(record(), ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(cm.CharacterError, "promotion source must be under"):
                cm.promote(path, False, "")


if __name__ == "__main__":
    unittest.main()
