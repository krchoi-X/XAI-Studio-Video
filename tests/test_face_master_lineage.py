import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "face_master_lineage.py"
SPEC = importlib.util.spec_from_file_location("face_master_lineage", MODULE_PATH)
fml = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(fml)

DNA = {"character_id": "ch-test", "record_path": "D:/records/ch-test/character.json",
       "character_version": 3, "stable_dna_sha256": "a" * 64}
LOCAL = {"provider": "local-wangp", "model": "krea2_turbo", "prompt_sent": "exact text sent"}


class LineageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.record = fml.new_record("lin-1", DNA, created_by="claude")

    def image(self, name, payload):
        path = self.dir / name
        path.write_bytes(payload)
        return path

    def chain(self):
        r = self.record
        fml.add_artifact(r, artifact_id="face-a", role="face_candidate", path=self.image("a.png", b"face-a"), provenance=LOCAL)
        fml.add_selection(r, role="base_face_selection", artifact_id="face-a", selected_by="user")
        fml.add_artifact(
            r, artifact_id="face-s", role="sculpted_face_candidate", path=self.image("s.png", b"face-sculpted"),
            parents=["face-a"], provenance={"tool": {"name": "Xpade Face Liquify", "version": "1.9.5"},
                                            "edit_note": "jaw slightly longer", "replayable": False})
        fml.add_artifact(r, artifact_id="body-1", role="body_target", path=self.image("b.png", b"body"),
                         provenance={**LOCAL, "model": "qwen_image_21"})
        return fml.add_artifact(
            r, artifact_id="comp-1", role="composite_candidate", path=self.image("c.png", b"composite"),
            parents=["body-1", "face-s"],
            provenance={"operation": "head_swap", "provider": "local-wangp", "model": "krea2_turbo_edit",
                        "prompt_sent": "head_swap: replace the head with the reference head.",
                        "ordered_inputs": [{"position": 1, "artifact_id": "body-1"}, {"position": 2, "artifact_id": "face-s"}],
                        "loras": [{"filename": "bfs_head_swap_v1.1_krea2.safetensors", "sha256": "b" * 64,
                                   "byte_count": 914159816, "strength": 1.0}],
                        "render_settings": {"steps": 10, "guidance_scale": 0, "seed": 1}})

    def test_full_chain_is_consistent_and_needs_review(self):
        self.chain()
        self.assertEqual(fml.validate(self.record), [])
        self.assertEqual(fml.verify_files(self.record), [])
        self.assertTrue(all(a["status"] == "needs_review" for a in self.record["artifacts"]))
        self.assertEqual(self.record["approvals"], [])
        self.assertEqual(self.record["selections"][0]["role"], "base_face_selection")

    def test_approval_roles_are_refused(self):
        for role in fml.APPROVAL_ROLES:
            with self.assertRaises(fml.LineageError):
                fml.add_artifact(self.record, artifact_id="x", role=role, path=self.image("x.png", b"x"), provenance=LOCAL)

    def test_face_candidate_requires_exact_prompt_and_model(self):
        with self.assertRaises(fml.LineageError):
            fml.add_artifact(self.record, artifact_id="f", role="face_candidate", path=self.image("f.png", b"f"),
                             provenance={"provider": "gemini", "model": "x"})

    def test_sculpted_copy_needs_tool_note_and_replay_flag_and_a_distinct_file(self):
        face = fml.add_artifact(self.record, artifact_id="face-a", role="face_candidate", path=self.image("a.png", b"face"), provenance=LOCAL)
        base = {"tool": {"name": "Xpade"}, "edit_note": "n", "replayable": False}
        for broken in ({**base, "edit_note": ""}, {k: v for k, v in base.items() if k != "replayable"}, {"edit_note": "n", "replayable": False}):
            with self.assertRaises(fml.LineageError):
                fml.add_artifact(self.record, artifact_id="s", role="sculpted_face_candidate", path=self.image("s.png", b"s"),
                                 parents=[face["id"]], provenance=broken)
        with self.assertRaises(fml.LineageError):  # byte-identical "derivative" is not a derivative
            fml.add_artifact(self.record, artifact_id="s", role="sculpted_face_candidate", path=self.image("same.png", b"face"),
                             parents=[face["id"]], provenance=base)

    def test_original_path_cannot_be_registered_twice(self):
        path = self.image("a.png", b"face")
        fml.add_artifact(self.record, artifact_id="a", role="face_candidate", path=path, provenance=LOCAL)
        with self.assertRaises(fml.LineageError):
            fml.add_artifact(self.record, artifact_id="a2", role="face_candidate", path=path, provenance=LOCAL)

    def test_composite_rules(self):
        self.chain()
        swap = self.record["artifacts"][-1]["provenance"]
        for mutate in (
            lambda p: p.update(ordered_inputs=list(reversed(p["ordered_inputs"]))),
            lambda p: p.update(operation="face-swap"),
            lambda p: p.update(loras=[{"filename": "x"}]),
            lambda p: p.pop("render_settings"),
        ):
            bad = json.loads(json.dumps(swap))
            mutate(bad)
            with self.assertRaises(fml.LineageError):
                fml.add_artifact(self.record, artifact_id="comp-bad", role="composite_candidate", path=self.image("bad.png", b"bad"),
                                 parents=["body-1", "face-s"], provenance=bad)
        with self.assertRaises(fml.LineageError):  # a failed attempt leaves the record untouched
            fml.add_artifact(self.record, artifact_id="comp-3", role="composite_candidate", path=self.image("c3.png", b"c3"),
                             parents=["body-1"], provenance=swap)
        self.assertEqual(len(self.record["artifacts"]), 4)

    def test_selection_does_not_change_status_and_checks_role(self):
        self.chain()
        with self.assertRaises(fml.LineageError):
            fml.add_selection(self.record, role="base_face_selection", artifact_id="body-1", selected_by="user")
        self.assertTrue(all(a["status"] == "needs_review" for a in self.record["artifacts"]))

    def test_verify_detects_changed_and_missing_inputs(self):
        self.chain()
        (self.dir / "b.png").write_bytes(b"tampered")
        (self.dir / "a.png").unlink()
        problems = fml.verify_files(self.record)
        self.assertEqual(len(problems), 2)

    def test_round_trip_and_minimal_old_style_record(self):
        self.chain()
        target = self.dir / "lineage.json"
        fml.save(target, self.record)
        self.assertEqual(fml.load(target), self.record)
        # A record written before any optional field existed (no brief, no selections, no tool) still validates.
        minimal = {"schema_version": 1, "kind": "face_master_lineage", "lineage_id": "old", "artifacts": [], "approvals": []}
        self.assertEqual(fml.validate(minimal), [])
        self.assertEqual(fml.verify_files(minimal), [])

    def test_save_refuses_a_forged_approval(self):
        self.chain()
        self.record["approvals"].append({"role": "face_master", "artifact_id": "face-s"})
        with self.assertRaises(fml.LineageError):
            fml.save(self.dir / "x.json", self.record)

    def test_brief_hash_and_dna_requirements(self):
        fml.set_brief(self.record, {"text": "soft, calm eyes", "exclusions": ["ch-other"]})
        self.assertEqual(len(self.record["face_discovery_brief"]["text_sha256"]), 64)
        with self.assertRaises(fml.LineageError):
            fml.new_record("l", {"character_id": "ch-test"}, created_by="claude")


if __name__ == "__main__":
    unittest.main()
