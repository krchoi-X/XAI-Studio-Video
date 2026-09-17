from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.director_skill_router import finalize_routing, load_manifest, route_request


ROOT = Path(__file__).resolve().parents[1]


class DirectorSkillRouterTests(unittest.TestCase):
    def request(self, **updates: object) -> dict:
        request = {
            "schema_version": 1,
            "request_id": "req_router_1",
            "action": "create_storyboards",
            "idea": "노아가 조용한 아침에 창밖 바다를 본 뒤 커피를 준비한다.",
            "character_ids": ["ch-shindo-noa"],
            "candidate_count": 2,
            "mode": "creative_expansion",
            "constraints": {},
            "reference_asset_ids": [],
            "output_intent": "video",
        }
        request.update(updates)
        return request

    def test_routes_bounded_distinct_candidate_skill_subsets(self) -> None:
        routing, context = route_request(ROOT, self.request())
        schema = json.loads((ROOT / "schemas/director-routing-v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(routing)), [])
        self.assertEqual(len(routing["candidate_routes"]), 2)
        subsets = [set(item["selected_skills"]) for item in routing["candidate_routes"]]
        self.assertTrue(all(2 <= len(item) <= 4 for item in subsets))
        self.assertNotEqual(subsets[0], subsets[1])
        self.assertEqual(len(context["candidates"]), 2)
        selected = set().union(*subsets)
        context_ids = {
            skill["skill_id"]
            for candidate in context["candidates"]
            for skill in candidate["skills"]
        }
        self.assertEqual(context_ids, selected)

    def test_exact_mode_routes_one_candidate(self) -> None:
        routing, _ = route_request(ROOT, self.request(mode="exact"))
        self.assertEqual(len(routing["candidate_routes"]), 1)
        self.assertEqual(routing["candidate_routes"][0]["candidate_key"], "A")

    def test_finalization_maps_storyboard_ids_by_candidate_order(self) -> None:
        routing, _ = route_request(ROOT, self.request())
        finalized = finalize_routing(routing, [{"id": "sb_a"}, {"id": "sb_b"}])
        self.assertEqual(
            [item["storyboard_id"] for item in finalized["candidate_routes"]],
            ["sb_a", "sb_b"],
        )

    def test_manifest_references_only_known_skills(self) -> None:
        manifest, manifest_hash = load_manifest(ROOT)
        self.assertEqual(len(manifest_hash), 64)
        known = {item["skill_id"] for item in manifest["skills"]}
        for mode in manifest["modes"]:
            self.assertLessEqual(set(mode["skill_ids"]), known)


if __name__ == "__main__":
    unittest.main()
