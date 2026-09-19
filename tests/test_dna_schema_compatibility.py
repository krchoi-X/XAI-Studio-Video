"""Two Stable DNA body schemas are in use. Both are read; neither is rewritten."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("character_manager", TOOLS / "character_manager.py")
cm = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(cm)

ANATOMICAL_BODY = {key: f"{key} wording" for key in cm.BODY_FIELDS}
COMPACT_BODY = {
    "overall": "slender balanced graceful adult build",
    "neck": "long graceful neck",
    "shoulders": "soft relaxed shoulders",
    "athleticism": "light athletic tone from yoga and tennis",
    "proportions": "natural adult body proportions",
}


def record(body: dict, **dna_overrides) -> dict:
    dna = {
        "adult_age_range": "adult",
        "visual_background": "Korean adult",
        "face": {key: f"{key} wording" for key in cm.FACE_FIELDS},
        "body": body,
        "hair": "dark hair",
        "skin": "realistic",
        "distinctive_marks": ["a specific mark"],
        "recognition_anchors": ["an anchor"],
    }
    dna.update(dna_overrides)
    return {
        "schema_version": 1, "id": "ch-test", "name": "Test", "romanized_name": "Test",
        "status": "candidate", "version": 1, "stable_dna": dna,
        "scene_defaults": {}, "provenance": {},
    }


class BodyShapeTests(unittest.TestCase):
    def test_each_shape_is_recognised(self):
        self.assertEqual(cm.body_shape(ANATOMICAL_BODY), "anatomical")
        self.assertEqual(cm.body_shape(COMPACT_BODY), "compact")

    def test_a_body_that_is_neither_is_not_quietly_accepted(self):
        self.assertEqual(cm.body_shape({"overall": "a build"}), "unknown")


class ValidationTests(unittest.TestCase):
    def test_both_shapes_validate(self):
        self.assertEqual(cm.validate(record(ANATOMICAL_BODY)), [])
        self.assertEqual(cm.validate(record(COMPACT_BODY)), [])

    def test_a_compact_record_need_not_carry_distinctive_marks(self):
        compact = record(COMPACT_BODY)
        del compact["stable_dna"]["distinctive_marks"]
        self.assertEqual(cm.validate(compact), [])

    def test_an_anatomical_record_still_must(self):
        """It is required where it has always been required; nothing is relaxed backwards."""
        anatomical = record(ANATOMICAL_BODY)
        del anatomical["stable_dna"]["distinctive_marks"]
        self.assertIn("stable_dna missing: distinctive_marks", cm.validate(anatomical))

    def test_a_half_written_body_says_what_is_missing_from_each_shape(self):
        errors = cm.validate(record({"overall": "a build", "bust": "something"}))
        self.assertEqual(len(errors), 1)
        self.assertIn("anatomical is missing", errors[0])
        self.assertIn("compact is missing", errors[0])

    def test_face_requirements_are_unchanged_for_both(self):
        broken = record(COMPACT_BODY)
        del broken["stable_dna"]["face"]["jaw"]
        self.assertIn("stable_dna.face missing: jaw", cm.validate(broken))

    def test_an_extra_face_field_is_allowed_rather_than_rejected(self):
        extra = record(COMPACT_BODY)
        extra["stable_dna"]["face"]["profile"] = "balanced delicate profile"
        self.assertEqual(cm.validate(extra), [])


class WarningTests(unittest.TestCase):
    def test_a_compact_record_is_valid_but_says_what_it_gives_up(self):
        compact = record(COMPACT_BODY)
        del compact["stable_dna"]["distinctive_marks"]
        del compact["stable_dna"]["recognition_anchors"]
        notes = cm.warnings_for(compact)
        self.assertEqual(cm.validate(compact), [])
        self.assertTrue(any("distinctive_marks" in note for note in notes))
        self.assertTrue(any("recognition_anchors" in note for note in notes))
        self.assertTrue(any("compact body shape" in note for note in notes))

    def test_a_complete_anatomical_record_has_nothing_to_warn_about(self):
        self.assertEqual(cm.warnings_for(record(ANATOMICAL_BODY)), [])


class RenderingTests(unittest.TestCase):
    def test_an_anatomical_body_renders_with_its_original_phrasing(self):
        sentence = cm.body_sentence(ANATOMICAL_BODY)
        self.assertTrue(sentence.startswith("height_impression wording; limb_proportions wording; shoulders "))
        self.assertIn("pelvis and hips", sentence)
        self.assertIn("body hair", sentence)

    def test_a_compact_body_renders_every_field_it_carries(self):
        sentence = cm.body_sentence(COMPACT_BODY)
        for value in COMPACT_BODY.values():
            self.assertIn(value, sentence)

    def test_a_field_nobody_hardcoded_still_reaches_the_prompt(self):
        """Validating and then never appearing is the bug this shape prevents."""
        body = dict(COMPACT_BODY, posture="upright and unhurried")
        self.assertIn("upright and unhurried", cm.body_sentence(body))

    def test_both_shapes_render_a_whole_prompt_without_raising(self):
        for body in (ANATOMICAL_BODY, COMPACT_BODY):
            prompt = cm.render_base_prompt(record(body))
            self.assertIn("Body:", prompt)
            self.assertIn("Preserve one coherent adult identity", prompt)

    def test_both_shapes_render_a_core_document(self):
        for body in (ANATOMICAL_BODY, COMPACT_BODY):
            self.assertIn("## Stable identity", cm.render_core(record(body)))


class LiveRecordTests(unittest.TestCase):
    """The records on disk are the thing this must not disturb."""

    def records(self):
        for path in sorted((ROOT / "characters").glob("ch-*/character.json")):
            yield path, json.loads(path.read_text(encoding="utf-8"))

    def test_every_checked_in_character_validates(self):
        for path, record_ in self.records():
            self.assertEqual(cm.validate(record_), [], path.parent.name)

    def test_the_checked_in_characters_are_all_anatomical(self):
        """If one turns compact later, its prompt changes shape, and that should be noticed."""
        for path, record_ in self.records():
            self.assertEqual(cm.body_shape(record_["stable_dna"]["body"]), "anatomical", path.parent.name)


if __name__ == "__main__":
    unittest.main()
