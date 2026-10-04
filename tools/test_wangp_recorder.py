from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import wangp_recorder


class RecorderTests(unittest.TestCase):
    def _role_split_artifacts(self, root: Path) -> tuple[Path, Path, Path]:
        source = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "shot-production-plan" / "lia-pack-contract-v2.json"
        plan = root / "plan.json"
        plan.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        treatment = root / "treatment.json"
        treatment_value = {
            "schema_version": 1,
            "treatment_id": "treatment_lia_quiet_exit",
            "status": "approved",
            "source": {"request_id": "req_lia_quiet_exit", "idea_sha256": hashlib.sha256(b"quiet exit").hexdigest()},
            "concept": {
                "premise": "A quiet departure.",
                "viewer_should_understand": "She has decided to leave.",
                "viewer_should_feel": "Quiet finality.",
            },
            "story_arc": ["hesitation", "departure"],
            "key_visual_moments": ["a final glance at the doorway"],
            "important_objects": [{"object_id": "door", "description": "one closed interior door", "continuity_importance": "high"}],
            "reference_grammar": {
                "pacing": "restrained", "framing_pattern": "medium to wide", "camera_language": "observational",
                "motion_language": "one purposeful walk", "transition_language": "hard cut",
                "environmental_motion": "subtle curtain motion", "performance_style": "underplayed", "temporal_density": "low",
            },
            "known_failure_risks": ["early lens contact"],
            "production_risks": ["door-state continuity"],
            "creative_freedom": {
                "hermes_may_decide": ["shot count", "lens family"],
                "requires_user_approval": ["production storyboard", "intent contract", "mature production details"],
            },
            "production_boundaries": {
                "must_preserve": ["quiet departure"], "must_not_add": ["reconciliation"],
                "mature_details_visibility": "not_applicable", "policy_evasion_prohibited": True,
            },
            "authorship": {"actor": "claude", "model": "claude-opus-5-5", "created_at": "2026-10-04T10:00:00+09:00"},
            "approval": {"approved_by": "user", "approved_at": "2026-10-04T10:10:00+09:00", "scope": "creative_direction_only_not_render_go"},
        }
        treatment.write_text(json.dumps(treatment_value), encoding="utf-8")
        roles = root / "roles.json"
        roles_value = {
            "schema_version": 1,
            "treatment_author": {"actor": "claude", "model": "claude-opus-5-5"},
            "storyboard_author": {"actor": "hermes", "model": "meromero26b-a4b-hermes"},
            "prompt_author": {"actor": "hermes", "model": "meromero26b-a4b-hermes"},
            "submitter": {"actor": "hermes", "model": "hermes-runtime"},
            "renderer": {"system": "WanGP", "model": "minimax_h3_ref2va_pruned"},
            "first_reviewer": {"actor": "hermes", "model": "meromero26b-a4b-hermes", "independent_context": True},
            "production_approval": {
                "approved_by": "user", "approved_at": "2026-10-04T10:20:00+09:00", "mature_details_reviewed": True,
                "approved_artifacts": [{"kind": "production_plan", "path": plan.name, "sha256": wangp_recorder.sha256_file(plan)}],
            },
        }
        roles.write_text(json.dumps(roles_value), encoding="utf-8")
        return plan, treatment, roles

    def test_session_can_register_an_approved_v2_production_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = root / "session"
            session.mkdir()
            source = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "shot-production-plan" / "lia-pack-contract-v2.json"
            plan = root / "plan.json"
            plan.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            result = wangp_recorder.write_session(argparse.Namespace(
                session_dir=str(session), requested_by="codex", executor="local_wangp",
                engine="WanGP", model="minimax_h3_ref2va_pruned", character_id="ch-lia",
                title="contract test", user_request=None, source_idea=None, status="planned",
                session_id="VIDEO-contract-test", production_plan=str(plan),
            ))
            self.assertEqual(result["production_plan"]["schema_version"], 2)
            self.assertEqual(result["production_plan"]["sha256"], wangp_recorder.sha256_file(plan))
            self.assertEqual(result["methodology"], "intent-preserving-v1")

    def test_session_records_intent_preserving_methodology(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            session = Path(directory) / "session"
            session.mkdir()
            result = wangp_recorder.write_session(argparse.Namespace(
                session_dir=str(session), requested_by="hermes", executor="local_wangp",
                engine="WanGP", model="minimax_h3_ref2va_pruned", character_id="ch-lia",
                title="intent gate", user_request=None, source_idea=None, status="prepared",
                session_id="VIDEO-intent-gate", production_plan=None, methodology="intent-preserving-v1",
            ))
            self.assertEqual(result["methodology"], "intent-preserving-v1")

    def test_treatment_backed_session_records_bound_roles_and_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = root / "session"
            session.mkdir()
            plan, treatment, roles = self._role_split_artifacts(root)
            result = wangp_recorder.write_session(argparse.Namespace(
                session_dir=str(session), requested_by="user", executor="hermes-runtime",
                engine="WanGP", model="minimax_h3_ref2va_pruned", character_id="ch-lia",
                title="role split", user_request="make a quiet exit", source_idea=None, status="prepared",
                session_id="VIDEO-role-split", production_plan=str(plan), methodology=None,
                creative_treatment=str(treatment), role_attribution=str(roles),
            ))
            self.assertEqual(result["creative_treatment"]["treatment_id"], "treatment_lia_quiet_exit")
            self.assertEqual(result["role_attribution"]["value"]["prompt_author"]["actor"], "hermes")
            self.assertEqual(result["methodology"], "intent-preserving-v1")

    def test_treatment_backed_session_rejects_non_hermes_prompt_author(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = root / "session"
            session.mkdir()
            plan, treatment, roles = self._role_split_artifacts(root)
            value = json.loads(roles.read_text(encoding="utf-8"))
            value["prompt_author"] = {"actor": "claude", "model": "claude-opus-5-5"}
            roles.write_text(json.dumps(value), encoding="utf-8")
            args = argparse.Namespace(
                session_dir=str(session), requested_by="user", executor="hermes-runtime",
                engine="WanGP", model="minimax_h3_ref2va_pruned", character_id="ch-lia",
                title="role split", user_request=None, source_idea=None, status="prepared",
                session_id="VIDEO-role-split", production_plan=str(plan), methodology=None,
                creative_treatment=str(treatment), role_attribution=str(roles),
            )
            with self.assertRaisesRegex(ValueError, "Hermes as prompt_author"):
                wangp_recorder.write_session(args)

    def test_treatment_backed_session_requires_visible_mature_details_to_be_reviewed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            session = root / "session"
            session.mkdir()
            plan, treatment, roles = self._role_split_artifacts(root)
            treatment_value = json.loads(treatment.read_text(encoding="utf-8"))
            treatment_value["production_boundaries"]["mature_details_visibility"] = (
                "production_storyboard_and_intent_contract"
            )
            treatment.write_text(json.dumps(treatment_value), encoding="utf-8")
            roles_value = json.loads(roles.read_text(encoding="utf-8"))
            roles_value["production_approval"]["mature_details_reviewed"] = False
            roles.write_text(json.dumps(roles_value), encoding="utf-8")
            args = argparse.Namespace(
                session_dir=str(session), requested_by="user", executor="hermes-runtime",
                engine="WanGP", model="minimax_h3_ref2va_pruned", character_id="ch-lia",
                title="role split", user_request=None, source_idea=None, status="prepared",
                session_id="VIDEO-role-split", production_plan=str(plan), methodology=None,
                creative_treatment=str(treatment), role_attribution=str(roles),
            )
            with self.assertRaisesRegex(ValueError, "visible and user-reviewed"):
                wangp_recorder.write_session(args)

    def test_prepare_writes_run_before_submission(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            prompt.write_text("exact prompt\n", encoding="utf-8")
            result = wangp_recorder.prepare_run(
                argparse.Namespace(
                    runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p1",
                    prompt_id="pr1", target="vast", settings_file=None, run_id="run-test",
                )
            )
            run_dir = Path(result["run_dir"])
            self.assertTrue((run_dir / "run.json").is_file())
            self.assertTrue((run_dir / "events.jsonl").is_file())
            self.assertEqual(result["status"], "queued")
            self.assertEqual(result["prompt"]["sha256"], wangp_recorder.sha256_file(prompt))

    def test_attach_marks_exact_embedded_prompt_as_succeeded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            prompt.write_text("same prompt", encoding="utf-8")
            prepared = wangp_recorder.prepare_run(
                argparse.Namespace(
                    runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p1",
                    prompt_id="pr1", target="local", settings_file=None, run_id="run-test",
                )
            )
            artifact = root / "result.mp4"
            artifact.write_bytes(b"fake-video")
            with patch.object(wangp_recorder, "ffprobe_metadata", return_value={"prompt": "same prompt"}):
                record = wangp_recorder.attach_artifact(
                    argparse.Namespace(run_dir=prepared["run_dir"], artifact=str(artifact), ffprobe="ffprobe")
                )
            self.assertEqual(record["status"], "succeeded")
            self.assertTrue(record["artifacts"][0]["prompt_exact_match"])

    def test_attach_does_not_silently_accept_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prompt = root / "prompt.txt"
            prompt.write_text("expected", encoding="utf-8")
            prepared = wangp_recorder.prepare_run(
                argparse.Namespace(
                    runs_root=str(root / "runs"), prompt_file=str(prompt), project_id="p1",
                    prompt_id="pr1", target="runpod", settings_file=None, run_id="run-test",
                )
            )
            artifact = root / "result.mp4"
            artifact.write_bytes(b"fake-video")
            with patch.object(wangp_recorder, "ffprobe_metadata", return_value={"prompt": "different"}):
                record = wangp_recorder.attach_artifact(
                    argparse.Namespace(run_dir=prepared["run_dir"], artifact=str(artifact), ffprobe="ffprobe")
                )
            self.assertEqual(record["status"], "needs_review")
            self.assertFalse(record["artifacts"][0]["prompt_exact_match"])


if __name__ == "__main__":
    unittest.main()
