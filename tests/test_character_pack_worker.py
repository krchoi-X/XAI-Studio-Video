import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import character_pack_worker as worker


def test_scene_spec_has_stable_face_and_body_intent() -> None:
    assert "30 degrees" in worker.scene_spec("face_left30")["camera"]
    assert "full-body" in worker.scene_spec("body_back")["camera"]
    assert "no identity change" in worker.scene_spec("face_front")["negative_constraints"]
    with pytest.raises(Exception, match="unsupported character-pack slot"):
        worker.scene_spec("unknown")


def test_scene_renderer_uses_exact_engine_and_frozen_master(tmp_path: Path) -> None:
    output = tmp_path / "output.png"
    output.write_bytes(b"image")
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "run.json").write_text(json.dumps({
        "run_id": "run-1",
        "settings": {"value": {"seed": 42}},
        "artifacts": [{"path": str(output), "prompt_exact_match": True, "prompt_normalized_match": True}],
    }), encoding="utf-8")
    session = tmp_path / "SCENE-test"
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout=json.dumps({
            "session_dir": str(session), "runs": [{"run_dir": str(run_dir)}],
        }), stderr="")

    renderer = worker.SceneRenderer(tmp_path / "repo", runner=fake_run)
    result = renderer.render({
        "character_id": "ch-example", "prompt": "face slot", "engine": "krea2",
        "slot_id": "face_front", "model_type": "krea2_turbo_edit",
        "master_face": {"path": str(tmp_path / "master.png"), "asset_id": "ast-master"},
    })

    command = calls[0][0]
    assert command[command.index("--engines") + 1] == "krea2"
    assert command[command.index("--identity-reference") + 1] == str(tmp_path / "master.png")
    assert command[command.index("--reference-asset-id") + 1] == "ast-master"
    assert result["output_path"] == str(output.resolve())
    assert result["seed"] == 42
    assert result["session_id"] == "SCENE-test"


def test_gallery_sync_is_an_explicit_post() -> None:
    calls = []

    class Response:
        def read(self):
            return b"ok"

    def opener(request, timeout):
        calls.append((request, timeout))
        return Response()

    worker.request_gallery_sync("http://127.0.0.1:8787/api/sync", opener=opener)
    assert calls[0][0].get_method() == "POST"
    assert calls[0][1] == 120


def test_initial_build_uses_slot_defaults_and_keeps_partial_success() -> None:
    calls = []

    class Job:
        def default_engine_map(self):
            return {"face_front": "qwen21", "body_front": "krea2"}

        def generate(self, slot_id, *, engine, renderer, importer):
            calls.append((slot_id, engine, renderer, importer))
            if slot_id == "body_front":
                raise RuntimeError("body failed")
            return {"candidate_id": "face-1"}

    renderer = object()
    candidates, errors = worker.run_initial_build(Job(), renderer)

    assert [item[:2] for item in calls] == [("face_front", "qwen21"), ("body_front", "krea2")]
    assert candidates == [{"candidate_id": "face-1"}]
    assert errors == ["body_front: body failed"]

