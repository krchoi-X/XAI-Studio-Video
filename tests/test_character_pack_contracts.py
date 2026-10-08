import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

import character_manager as cm


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = Path(__file__).parent / "fixtures" / "character-pack"


@pytest.mark.parametrize(
    ("schema_name", "fixture_name"),
    [
        ("character-v1.schema.json", "legacy-character-path-only.json"),
        ("master-face-approval-v1.schema.json", "master-face-approval-v1.json"),
        ("character-pack-job-v1.schema.json", "character-pack-job-v1.json"),
        ("character-pack-candidate-manifest-v1.schema.json", "character-pack-candidate-manifest-v1.json"),
    ],
)
def test_contract_fixtures_validate(schema_name: str, fixture_name: str) -> None:
    schema_path = SCHEMAS / schema_name
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    fixture = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(fixture)


def _put(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _record() -> dict:
    return {
        "schema_version": 1,
        "id": "ch-synthetic",
        "name": "Synthetic",
        "status": "candidate",
        "version": 2,
        "stable_dna": {
            "adult_age_range": "adult",
            "visual_background": "fictional adult",
            "face": {key: "value" for key in cm.FACE_FIELDS},
            "body": {key: "value" for key in cm.BODY_FIELDS},
            "hair": "dark",
            "skin": "natural",
            "distinctive_marks": [],
        },
        "scene_defaults": {},
        "reference_defaults": {},
        "approved_references": [],
        "provenance": {
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
            "created_by": "user",
            "sources": [],
        },
    }


@pytest.fixture
def authority(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    runtime = tmp_path / "runtime"
    private = tmp_path / "private"
    locator = tmp_path / "workspace.yaml"
    _put(locator, {"private_repo": "private"})
    _put(
        private / "control" / "shared-resources.json",
        {
            "version": 1,
            "status": "active",
            "characters": {"authority_root": "characters"},
            "skills": {"source_root": "skills", "definitions": []},
        },
    )
    target = private / "characters" / "ch-synthetic" / "character.json"
    _put(target, _record())
    monkeypatch.setenv("XAI_WORKSPACE_FILE", str(locator))
    monkeypatch.setattr(cm, "ROOT", runtime)
    monkeypatch.setattr(cm, "CHARACTERS", runtime / "characters")
    monkeypatch.setattr(cm, "DRAFTS", runtime / "characters" / ".drafts")
    monkeypatch.setattr(cm, "INDEX", runtime / "characters" / "index.json")
    return target, private


def _approval(path: Path, image: Path, *, expected_previous: dict | None = None) -> Path:
    content = image.read_bytes()
    value = {
        "schema_version": 1,
        "kind": "master_face_approval",
        "approval_id": "mfa-test-001",
        "character_id": "ch-synthetic",
        "asset": {
            "asset_id": "ast-test-001",
            "path": str(image.resolve()),
            "sha256": hashlib.sha256(content).hexdigest(),
            "byte_count": len(content),
            "media_type": "image",
        },
        "approved_by": "user",
        "approved_at": "2026-10-07T12:00:00+09:00",
        "requested_via": "gallery",
        "reason": "Operator approved the Gallery asset.",
        "expected_previous": expected_previous,
    }
    _put(path, value)
    return path


def test_master_face_dry_run_then_apply_preserves_history_and_stable_dna(authority, tmp_path: Path) -> None:
    target, private = authority
    image = tmp_path / "master.png"
    image.write_bytes(b"synthetic-image")
    approval = _approval(tmp_path / "approval.json", image)
    before = target.read_bytes()
    before_stable = cm.stable_hash(cm.load(target))

    preview = cm.set_master_face(approval, dry_run=True)
    assert preview["changed"] is True and preview["version_after"] == 3
    assert target.read_bytes() == before

    applied = cm.set_master_face(approval)
    updated = cm.load(target)
    assert applied["changed"] is True and updated["version"] == 3
    assert cm.stable_hash(updated) == before_stable
    assert updated["reference_defaults"]["identity"]["asset_id"] == "ast-test-001"
    assert updated["reference_defaults"]["identity"]["sha256"] == hashlib.sha256(image.read_bytes()).hexdigest()
    history = target.parent / "history" / hashlib.sha256(before).hexdigest() / "character.json"
    assert history.read_bytes() == before
    index = cm.load(private / "characters" / "index.json")["characters"][0]
    assert index["reference_defaults"]["identity"]["approval_id"] == "mfa-test-001"


def test_master_face_writer_rejects_stale_previous_and_changed_bytes(authority, tmp_path: Path) -> None:
    target, _ = authority
    image = tmp_path / "master.png"
    image.write_bytes(b"first")
    approval = _approval(tmp_path / "approval.json", image)
    cm.set_master_face(approval)
    with pytest.raises(cm.CharacterError, match="changed after approval"):
        cm.set_master_face(approval)
    current = cm.load(target)["reference_defaults"]["identity"]
    replacement = _approval(tmp_path / "replacement.json", image, expected_previous=current)
    image.write_bytes(b"changed")
    with pytest.raises(cm.CharacterError, match="SHA-256"):
        cm.set_master_face(replacement)


def test_master_face_writer_requires_human_gallery_approval(authority, tmp_path: Path) -> None:
    image = tmp_path / "master.png"
    image.write_bytes(b"synthetic")
    approval = _approval(tmp_path / "approval.json", image)
    value = json.loads(approval.read_text(encoding="utf-8"))
    value["approved_by"] = "codex"
    _put(approval, value)
    with pytest.raises(cm.CharacterError, match="explicit user decision"):
        cm.set_master_face(approval)
