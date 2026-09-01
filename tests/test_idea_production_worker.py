from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.idea_production_worker import process


ROOT = Path(__file__).resolve().parents[1]


class IdeaProductionWorkerTests(unittest.TestCase):
    def request(self) -> dict:
        return {
            "schema_version": 1, "request_id": "req_test_1", "action": "create_storyboards",
            "idea": "하림이 바닷가를 걷는다.", "character_ids": ["ch-harim"],
            "candidate_count": 2, "mode": "creative_expansion", "constraints": {},
            "reference_asset_ids": [], "output_intent": "image",
        }

    def test_persists_schema_valid_storyboards_and_status(self) -> None:
        candidate = {
            "schema_version": 1, "request_id": "req_test_1", "status": "needs_user_choice",
            "storyboards": [{"id": "sb_one", "title": "산책", "summary": "조용한 산책", "shots": [{"id": "shot_01", "purpose": "도입", "description": "바닷가를 걷는다", "continuity": {}, "sample_request": {}}]}],
            "errors": [],
        }
        with tempfile.TemporaryDirectory() as temporary:
            job = Path(temporary)
            (job / "request.json").write_text(json.dumps(self.request(), ensure_ascii=False), encoding="utf-8")
            (job / "resolved-references.json").write_text(json.dumps({"characters": [{"id": "ch-harim", "status": "resolved"}], "assets": []}), encoding="utf-8")
            with patch("tools.idea_production_worker.generate", return_value=candidate):
                process(job, ROOT, "test-model")
            self.assertEqual(json.loads((job / "status.json").read_text(encoding="utf-8"))["status"], "needs_user_choice")
            self.assertEqual(json.loads((job / "storyboards.json").read_text(encoding="utf-8"))["storyboards"][0]["id"], "sb_one")

    def test_missing_reference_stops_before_llm(self) -> None:
        request = self.request()
        request["reference_asset_ids"] = ["asset_missing"]
        with tempfile.TemporaryDirectory() as temporary:
            job = Path(temporary)
            (job / "request.json").write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
            (job / "resolved-references.json").write_text(json.dumps({"characters": [{"id": "ch-harim", "status": "resolved"}], "assets": [{"id": "asset_missing", "status": "not_found"}]}), encoding="utf-8")
            with patch("tools.idea_production_worker.generate") as generate:
                process(job, ROOT, "test-model")
            generate.assert_not_called()
            result = json.loads((job / "storyboards.json").read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "failed")
            self.assertEqual(result["errors"][0]["code"], "reference_not_found")


if __name__ == "__main__":
    unittest.main()
