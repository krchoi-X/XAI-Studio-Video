"""Boundary tests use synthetic records, never the operator's authority."""
import hashlib
import json
from pathlib import Path

import pytest
import character_manager as cm


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


@pytest.fixture
def shared(tmp_path, monkeypatch):
    runtime = tmp_path / "runtime"
    private = tmp_path / "authority"
    catalog = {"version": 1, "status": "active", "characters": {"authority_root": "records"},
               "skills": {"source_root": "skills", "definitions": ["example"]}}
    locator = tmp_path / "workspace.yaml"
    put(locator, {"private_repo": "authority", "workspace_root": str(tmp_path)})
    put(private / "control/shared-resources.json", catalog)
    (private / "records").mkdir()
    monkeypatch.setenv("XAI_WORKSPACE_FILE", str(locator))
    monkeypatch.setattr(cm, "ROOT", runtime)
    monkeypatch.setattr(cm, "CHARACTERS", runtime / "characters")
    monkeypatch.setattr(cm, "DRAFTS", runtime / "characters/.drafts")
    monkeypatch.setattr(cm, "INDEX", runtime / "characters/index.json")
    return runtime, private, catalog


def sample():
    return {"schema_version": 1, "id": "ch-synthetic", "name": "Synthetic", "status": "approved", "version": 2,
            "stable_dna": {"adult_age_range": "adult", "visual_background": "adult", "face": {k:"a" for k in cm.FACE_FIELDS},
                           "body": {k:"a" for k in cm.BODY_FIELDS}, "hair":"a", "skin":"a", "distinctive_marks":[]},
            "scene_defaults": {}, "provenance": {"created_at":"before"}, "future_extension":{"keep":True},
            "reference_defaults":{"identity":{"path":"external-reference", "state":"candidate"}},
            "approved_references":[]}


def test_writer_history_index_and_session_separation(shared):
    runtime, private, _ = shared
    target = private / "records/ch-synthetic/character.json"
    put(target, sample())
    put(runtime / "characters/ch-synthetic/character.json", {"legacy":"untouched"})
    old = target.read_bytes()
    put(cm.DRAFTS / "one/character.json", sample())
    assert cm.promote(cm.DRAFTS / "one/character.json", False, "scene only") == target
    assert cm.load(target)["version"] == 3
    assert cm.load(target)["future_extension"] == {"keep": True}
    assert (target.parent / "history" / hashlib.sha256(old).hexdigest() / "character.json").read_bytes() == old
    assert cm.load(runtime / "characters/ch-synthetic/character.json") == {"legacy":"untouched"}
    assert not cm.INDEX.exists()
    index = cm.load(private / "records/index.json")["characters"][0]
    assert index["record_sha256"] == hashlib.sha256(target.read_bytes()).hexdigest()
    assert index["reference_defaults"] == sample()["reference_defaults"]
    assert index["approved_references"] == []
    assert cm.character_session_root("ch-synthetic") == runtime / "characters/ch-synthetic"
    before_refresh = target.read_bytes()
    cm.refresh("ch-synthetic")
    assert (target.parent / "history" / hashlib.sha256(before_refresh).hexdigest() / "character.json").read_bytes() == before_refresh


def test_stable_drift_needs_both_approval_and_reason(shared):
    _, private, _ = shared
    target = private / "records/ch-synthetic/character.json"
    put(target, sample()); old = target.read_bytes()
    draft = sample(); draft["stable_dna"]["hair"] = "changed"
    put(cm.DRAFTS / "one/character.json", draft)
    for allowed, reason in [(False,"requested"), (True, "")]:
        with pytest.raises(cm.CharacterError, match="drift blocked"):
            cm.promote(cm.DRAFTS / "one/character.json", allowed, reason)
    assert target.read_bytes() == old


def test_missing_active_record_never_falls_back(shared):
    runtime, _, _ = shared
    put(runtime / "characters/ch-synthetic/character.json", sample())
    with pytest.raises(cm.CharacterError, match="missing"):
        cm.character_record_path("ch-synthetic")


@pytest.mark.parametrize("root", ["absent", "../runtime"])
def test_bad_authority_root_fails(shared, root):
    _, private, catalog = shared
    catalog["characters"]["authority_root"] = root
    put(private / "control/shared-resources.json", catalog)
    with pytest.raises(cm.CharacterError): cm.shared_authority_root()


def test_malformed_catalog_and_deleted_active_catalog_fail(shared):
    _, private, _ = shared
    path = private / "control/shared-resources.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(cm.CharacterError): cm.shared_authority_root()
    path.unlink()
    put(private / "control/characters.yaml", {"mode":"shared"})
    with pytest.raises(cm.CharacterError, match="catalog is missing"): cm.shared_authority_root()


def test_pending_and_old_locator_preserve_legacy(shared):
    runtime, private, catalog = shared
    catalog["status"] = "pending-root-activation"
    put(private / "control/shared-resources.json", catalog)
    assert cm.character_record_path("ch-synthetic") == runtime / "characters/ch-synthetic/character.json"
    (private / "control/shared-resources.json").unlink()
    assert cm.shared_authority_root() is None


def test_unrelated_cwd_and_shared_skill(shared, tmp_path, monkeypatch):
    _, private, _ = shared
    path = private / "skills/example/SKILL.md"; path.parent.mkdir(parents=True); path.write_text("Shared source")
    monkeypatch.chdir(tmp_path.parent)
    assert cm.shared_skill_path("example") == path
    with pytest.raises(cm.CharacterError): cm.shared_skill_path("../escape")
    with pytest.raises(cm.CharacterError): cm.character_record_path("../escape")


def test_relative_knowledge_locator_is_independent_of_cwd(shared, tmp_path, monkeypatch):
    import shared_resources
    _, private, catalog = shared
    catalog.update({"knowledge":{"repository":"knowledge"},"creation_records":{"status":"pending"}})
    put(private / "control/shared-resources.json", catalog)
    put(private / "control/repositories.yaml", {"repositories":{"knowledge":{"path":"notes"}}})
    put(tmp_path / "workspace.yaml", {"private_repo":"authority","workspace_root":"workspace"})
    (tmp_path / "workspace/notes").mkdir(parents=True)
    path = private / "skills/example/SKILL.md"; path.parent.mkdir(parents=True); path.write_text("shared")
    monkeypatch.chdir(tmp_path.parent)
    assert shared_resources.describe()["knowledge"] == str(tmp_path / "workspace/notes")
