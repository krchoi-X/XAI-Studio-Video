import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location("hermes_night_batch", TOOLS / "hermes_night_batch.py")
night = importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(night)


class HermesNightBatchTests(unittest.TestCase):
    def setUp(self):
        self.original_characters = night.cm.CHARACTERS
        self.temp = tempfile.TemporaryDirectory()
        night.cm.CHARACTERS = Path(self.temp.name) / "characters"
        target = night.cm.CHARACTERS / "ch-test"
        target.mkdir(parents=True)
        (target / "character.json").write_text("{}", encoding="utf-8")

    def tearDown(self):
        night.cm.CHARACTERS = self.original_characters
        self.temp.cleanup()

    def test_plan_is_normalized_and_budgeted(self):
        plan = night.validate_plan({"title": "test", "items": [{"character_id": "ch-test", "prompt": "창가의 상반신", "engines": ["z-image", "krea2"], "count": 3}]})
        self.assertEqual(6, plan["generated_image_budget"])
        self.assertEqual("strict_translation", plan["items"][0]["prompt_strategy"])

    def test_plan_rejects_excessive_morning_review_load(self):
        with self.assertRaises(night.cm.CharacterError):
            night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "서로 다른 장면", "engines": ["z-image", "krea2"], "count": 10} for _ in range(13)]})

    def test_variation_axes_are_preserved_for_tablet_comparison(self):
        plan = night.validate_plan({"items": [{"character_id": "ch-test", "prompt": "해변 카페", "count": 1,
            "variation_axes": {"hair": "bob", "scene": "beach-cafe", "lighting": "sunset"}}]})
        self.assertEqual("sunset", plan["items"][0]["variation_axes"]["lighting"])

    def test_create_without_start_writes_durable_queue(self):
        root = Path(self.temp.name); plan_path = root / "input.json"
        plan_path.write_text(json.dumps({"source_request": "오늘 밤 테스트", "items": [{"character_id": "ch-test", "prompt": "흰 스튜디오 사진", "count": 1}]}), encoding="utf-8")
        batch = night.create(plan_path, root / "queue", False)
        self.assertTrue((batch / "plan.json").is_file())
        self.assertEqual("queued", json.loads((batch / "status.json").read_text(encoding="utf-8"))["status"])


if __name__ == "__main__": unittest.main()
