import argparse
import hashlib
import json
import shutil
from pathlib import Path

import pytest
import character_manager as cm
import character_scene as scene
import creation_records
import local_wangp
import wangp_recorder
from test_shared_authority import shared, put, sample


@pytest.fixture
def creation(shared, monkeypatch):
    runtime, private, catalog = shared
    library = private.parent / "library"; library.mkdir()
    catalog["creation_records"] = {"status":"shared-new-sessions","version":1,"layout":"character-generations-v1","library_root":str(library)}
    catalog["skills"]["definitions"] = ["character-manager"]
    put(private / "control/shared-resources.json", catalog)
    put(private / "records/ch-synthetic/character.json", sample())
    skill = private / "skills/character-manager/SKILL.md"; skill.parent.mkdir(parents=True); skill.write_bytes(b"# Historical skill\r\n")
    reference = skill.parent / "references/guide.md"; reference.parent.mkdir(); reference.write_bytes(b"exact reference\r\n")
    monkeypatch.setattr(scene, "ASSET_LIBRARY", library)
    return runtime, private, catalog, library


def test_shared_prepare_inputs_and_isolated_recorder(creation):
    runtime, private, _, library = creation
    original = (private / "records/ch-synthetic/character.json").read_bytes()
    session = scene.prepare("ch-synthetic", "An adult seated by a window", cm.DEFAULT_MODEL, 1, ["z-image"])
    assert session.parent == library / "characters/ch-synthetic/generations"
    assert not (runtime / "characters").exists()
    assert not (session / "outputs").exists()
    assert cm.validate_generation_session(session) == session
    assert local_wangp._session_character_id(session) == "ch-synthetic"
    context = cm.load(session / "creation-context.json")
    assert context["character"] == {"id":"ch-synthetic","version":2,"role":"identity_input"}
    for row in context["inputs"]:
        assert hashlib.sha256((session / row["snapshot"]).read_bytes()).hexdigest() == row["sha256"]
    assert (session / "inputs/character.json").read_bytes() == original
    (private / "skills/character-manager/SKILL.md").write_text("later skill")
    assert (session / "inputs/skills/character-manager/SKILL.md").read_bytes() == b"# Historical skill\r\n"
    args = argparse.Namespace(runs_root=str(session / "runs"), prompt_file=str(session / "prompt.txt"), settings_file=None,
                              run_id="run-fixture", project_id=session.name, prompt_id="fixture", target="local", requested_by="codex",executor="fixture")
    run = wangp_recorder.prepare_run(args)
    assert Path(run["run_dir"]).parent == session / "runs"
    assert (Path(run["run_dir"]) / "run.json").is_file()
    assert (private / "records/ch-synthetic/character.json").read_bytes() == original
    restored = library.parent / "isolated-restore"
    shutil.copytree(session, restored)
    for original_file in session.rglob("*"):
        if original_file.is_file():
            assert (restored / original_file.relative_to(session)).read_bytes() == original_file.read_bytes()


def test_face_preparation_records_workflow_and_context_only_dna(creation, monkeypatch):
    import face_discovery
    _, _, _, library = creation
    monkeypatch.setattr(face_discovery, "discovery_prompt", lambda *_: "Direction prompt from workflow")
    session = face_discovery.prepare("ch-synthetic", "TEST-A", 1, ["z-image"])
    assert session.parent == library / "characters/ch-synthetic/generations"
    context = cm.load(session / "creation-context.json")
    assert context["character"]["role"] == "context_only"
    assert (session / "inputs/workflow" / face_discovery.WORKFLOW.name).read_bytes() == face_discovery.WORKFLOW.read_bytes()


def test_existing_legacy_resume_retains_exact_path(creation):
    runtime, _, _, _ = creation
    root = runtime / "characters/ch-synthetic/02_generations/OLD-1"
    put(root / "batch.yaml", {"session":{"id":"OLD-1","character_id":"ch-synthetic"}})
    (root / "prompt.txt").write_text("unchanged")
    assert cm.validate_generation_session(root) == root
    put(root / "batch.yaml", {"session":{"id":"historical-label","character_id":"historical-alias"}})
    assert cm.validate_generation_session(root) == root
    assert local_wangp._session_character_id(root) == "ch-synthetic"
    with pytest.raises(cm.CharacterError, match="legacy"):
        cm.reserve_generation_session("ch-synthetic", "OLD-1")


def test_existing_outputs_only_and_conflicting_library_not_overwritten(creation):
    _, _, _, library = creation
    root = library / "characters/ch-synthetic/generations/OLD-OUTPUTS"
    (root / "outputs").mkdir(parents=True)
    with pytest.raises(cm.CharacterError, match="already exists"):
        cm.reserve_generation_session("ch-synthetic", "OLD-OUTPUTS")
    with pytest.raises(cm.CharacterError, match="conflicts"):
        cm.generation_session_path("ch-synthetic", "NEW", library / "other")


@pytest.mark.parametrize("field,value", [("layout","unknown"),("version",2),("library_root","relative"),("status","broken")])
def test_invalid_shared_config_fails(creation, field, value):
    _, private, catalog, _ = creation
    catalog["creation_records"][field] = value
    put(private / "control/shared-resources.json", catalog)
    with pytest.raises(cm.CharacterError): cm.shared_creation_library()


def test_bad_session_ids_and_manifest_mismatch(creation):
    _, _, _, library = creation
    with pytest.raises(cm.CharacterError): cm.generation_session_path("ch-synthetic", "../escape")
    root = library / "characters/ch-synthetic/generations/NEW"
    put(root / "batch.yaml", {"session":{"id":"OTHER","character_id":"ch-synthetic"}})
    (root / "prompt.txt").write_text("fixture")
    with pytest.raises(cm.CharacterError, match="identifier"): cm.validate_generation_session(root)


def test_context_snapshot_cannot_be_mistaken_for_used_dna(creation):
    _, private, _, _ = creation
    root = cm.reserve_generation_session("ch-synthetic", "CONTEXT")
    creation_records.snapshot_inputs(root, sample(), Path(creation_records.__file__), identity_role="context_only")
    assert cm.load(root / "creation-context.json")["character"]["role"] == "context_only"


def test_legacy_catalog_keeps_previous_writer_path(shared):
    runtime, _, _ = shared
    assert cm.shared_creation_library() is None
    assert cm.generation_session_path("ch-synthetic", "NEW") == runtime / "characters/ch-synthetic/02_generations/NEW"


def test_reference_worker_uses_shared_session_without_gpu_or_http(creation, monkeypatch):
    import reference_variation_worker as worker
    from types import SimpleNamespace
    runtime, _, _, library = creation
    job = library.parent / "queued-job"; job.mkdir()
    reference = job / "source.png"; reference.write_bytes(b"fixture image bytes")
    request = {"variation_id":"var-test","character_id":"ch-synthetic","reference_asset_id":"ast-test",
               "reference_path":str(reference),"reference_sha256":hashlib.sha256(reference.read_bytes()).hexdigest(),
               "reference_byte_count":reference.stat().st_size,"operator_request":"Darker eyebrows",
               "preserve":["identity"],"changes":{"eyebrows":"darker"},"strength":"subtle","source_resolution":"768x1024",
               "session_slug":"VAR-TEST","count":1,"created_at":"2026-01-01"}
    put(job / "request.json", request)
    engine = library.parent / "fake-engine"
    for relative in ["ckpts/Krea2Turbo_quanto_bf16_int8.safetensors", "loras/krea2/krea2_identity_edit_v1_2.safetensors", "ckpts/Qwen3-VL-4B-Instruct/Qwen3-VL-4B-Instruct_vision_bf16.safetensors"]:
        path=engine/relative; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(b"fixture, never loaded")
    session = library / "characters/ch-synthetic/generations/VAR-TEST"
    monkeypatch.setattr(worker, "settings_for", lambda *_: {"model_type":"fixture"})
    def submit(command, **_):
        assert command[command.index("--runs-root")+1] == str(session / "runs")
        return SimpleNamespace(returncode=0,stdout=json.dumps({"run_id":"run-test","run_dir":str(session / "runs/run-test")}),stderr="")
    monkeypatch.setattr(worker.subprocess, "run", submit)
    monkeypatch.setattr(worker, "wait_for_run", lambda _: {"run_id":"run-test","status":"needs_review","artifacts":[]})
    monkeypatch.setattr(worker.urllib.request, "urlopen", lambda *_args,**_kwargs: SimpleNamespace(read=lambda:b"{}"))
    args=SimpleNamespace(job_dir=str(job),repo_root=str(runtime),library_root=str(library),wangp_root=str(engine),wangp_python="unused",sync_url="http://fixture.invalid/sync")
    assert worker.run(args) == 0
    assert not (runtime / "characters").exists()
    assert cm.load(session / "creation-context.json")["character"]["role"] == "context_only"
    assert cm.load(session / "request.json")["operator_request"] == request["operator_request"]
