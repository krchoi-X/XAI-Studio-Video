from __future__ import annotations

import hashlib
import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import character_sets


def _manifest(character: str, members: list[dict]) -> dict:
    return {"schema_version": 1, "character_id": character, "review_state": "needs_review", "members": members}


def _shared(monkeypatch, library: Path) -> None:
    monkeypatch.setattr(character_sets, "_character_manager", lambda: SimpleNamespace(shared_creation_library=lambda: library))


def test_describe_sets_reads_complete_legacy_schema_one_sets(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; character = "ch-test"
    identity = library / "characters" / character / "imports" / "derived" / "old-identity"; identity.mkdir(parents=True)
    (identity / "a.png").write_bytes(b"identity")
    (identity / "identity-set.json").write_text(json.dumps(_manifest(character, [{"file": "a.png", "mirrored": True}]), ensure_ascii=False), encoding="utf-8")
    dataset = library / "characters" / character / "training" / "old-lora"; (dataset / "train").mkdir(parents=True)
    (dataset / "train/a.png").write_bytes(b"dataset"); (dataset / "train/a.txt").write_text("token\n", encoding="utf-8")
    (dataset / "dataset.json").write_text(json.dumps(_manifest(character, [{"file": "train/a.png"}]), ensure_ascii=False), encoding="utf-8")
    _shared(monkeypatch, library)

    sets = character_sets.describe_sets(character)

    assert [(item["kind"], item["member_count"], item["mirrored_count"]) for item in sets] == [("identity", 1, 1), ("lora", 1, 0)]
    assert sets[0]["manifest_sha256"] == hashlib.sha256((identity / "identity-set.json").read_bytes()).hexdigest()
    assert all(item["context_available"] is False for item in sets)


def test_describe_sets_rejects_escaping_member_and_ignores_incomplete(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; character = "ch-test"
    incomplete = library / "characters" / character / "imports" / "derived" / "partial"; incomplete.mkdir(parents=True)
    identity = library / "characters" / character / "imports" / "derived" / "bad"; identity.mkdir(parents=True)
    (identity / "identity-set.json").write_text(json.dumps(_manifest(character, [{"file": "../escape.png"}])), encoding="utf-8")
    _shared(monkeypatch, library)
    with pytest.raises(ValueError, match="escapes"):
        character_sets.describe_sets(character)


def test_describe_sets_rejects_dataset_caption_sidecar_mismatch(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; character = "ch-test"
    dataset = library / "characters" / character / "training" / "bad-caption"; (dataset / "train").mkdir(parents=True)
    (dataset / "train/a.png").write_bytes(b"dataset"); (dataset / "train/a.txt").write_text("wrong\n", encoding="utf-8")
    (dataset / "dataset.json").write_text(json.dumps(_manifest(character, [{"file": "train/a.png", "caption": "expected"}])), encoding="utf-8")
    _shared(monkeypatch, library)
    with pytest.raises(ValueError, match="caption sidecar"):
        character_sets.describe_sets(character)


def test_reserve_destination_rejects_existing_and_uses_shared_default(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; parent = library / "characters" / "ch-test" / "imports" / "derived"; parent.mkdir(parents=True)
    _shared(monkeypatch, library)
    destination = character_sets.reserve_destination("identity", "ch-test", None)
    assert destination.parent == parent.resolve() and destination.is_dir()
    with pytest.raises(FileExistsError):
        character_sets.reserve_destination("identity", "ch-test", destination)


def test_context_snapshots_exact_input_and_dna_version(tmp_path: Path, monkeypatch) -> None:
    set_dir = tmp_path / "set"; set_dir.mkdir(); source = tmp_path / "report.json"; source.write_bytes(b'{"report": 1}')
    output = set_dir / "member.png"; output.write_bytes(b"member")
    dna = tmp_path / "character.json"; dna.write_text('{"version": 7}', encoding="utf-8")
    monkeypatch.setattr(character_sets, "_character_manager", lambda: SimpleNamespace(character_record_path=lambda _: dna))
    character_sets.write_set_context(set_dir, character_id="ch-test", producer=Path(character_sets.__file__), arguments={"enabled": True, "limit": 2, "empty": None}, source_manifest=source, source_bytes=source.read_bytes(), output_files=[output])
    context = json.loads((set_dir / "set-context.json").read_text(encoding="utf-8"))
    assert context["inputs"]["character_dna"]["version"] == 7
    assert context["inputs"]["character_dna"]["context_only"] is True
    assert context["arguments"] == {"enabled": True, "limit": 2, "empty": None}
    assert context["output_members"][0]["sha256"] == hashlib.sha256(b"member").hexdigest()


def test_context_rejects_source_mutation_before_publication(tmp_path: Path, monkeypatch) -> None:
    set_dir = tmp_path / "set"; set_dir.mkdir(); source = tmp_path / "report.json"; source.write_bytes(b"before")
    output = set_dir / "member.png"; output.write_bytes(b"member")
    dna = tmp_path / "character.json"; dna.write_text('{"version": 1}', encoding="utf-8")
    monkeypatch.setattr(character_sets, "_character_manager", lambda: SimpleNamespace(character_record_path=lambda _: dna))
    source.write_bytes(b"after")
    with pytest.raises(ValueError, match="changed"):
        character_sets.write_set_context(set_dir, character_id="ch-test", producer=Path(character_sets.__file__), arguments={}, source_manifest=source, source_bytes=b"before", output_files=[output])
    assert not (set_dir / "set-context.json").exists()


def test_identity_builder_reserves_a_partial_directory_before_invalid_input(tmp_path: Path, monkeypatch) -> None:
    """The heavy recognizer boundary is stubbed; filesystem reservation is real."""
    monkeypatch.setitem(sys.modules, "identity_score", SimpleNamespace(now=lambda: "now", write_json=lambda *_: None))
    sys.modules.pop("identity_set_builder", None)
    builder = importlib.import_module("identity_set_builder")
    reserved = tmp_path / "reserved"
    monkeypatch.setattr(builder, "reserve_destination", lambda *_: (reserved.mkdir(), reserved)[1])
    report = tmp_path / "report.json"; report.write_text('{"shots": {}, "frames": []}', encoding="utf-8")
    args = SimpleNamespace(report=str(report), out_dir=None, character="ch-test", actor="test", include_disagree=False, only=None, balance_by_flip=[], max_flips=1, sheet=None, title=None)
    with pytest.raises(ValueError, match="no clip"):
        builder.build(args)
    assert reserved.is_dir() and not (reserved / "identity-set.json").exists()


def _builders(monkeypatch):
    def write_json(path, value):
        Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    monkeypatch.setitem(sys.modules, "identity_score", SimpleNamespace(now=lambda: "now", write_json=write_json))
    sys.modules.pop("identity_set_builder", None); sys.modules.pop("lora_dataset", None)
    return importlib.import_module("identity_set_builder"), importlib.import_module("lora_dataset")


def _report(path: Path, frame: Path, *, shots: list[str] | None = None) -> None:
    shots = shots or ["take"]
    frames = [{"shot": shot, "path": str(frame), "yaw_proxy": 0.0, "yaw_bucket": "frontal", "sharpness": 1.0,
               "face_pixels": [300, 300], "scores": {"arcface": 1.0}} for shot in shots]
    data = {"shots": {shot: {"admission_verdict": "same", "admission_scores": {}} for shot in shots},
            "frames": frames, "prototype": {"id": "p"}, "calibration": {}}
    path.write_text(json.dumps(data), encoding="utf-8")


def test_successful_identity_and_lora_build_publish_manifests_context_and_preserve_rerun(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; character = "ch-test"; derived = library / "characters" / character / "imports" / "derived"; derived.mkdir(parents=True)
    (library / "characters" / character / "training").mkdir(parents=True)
    dna = tmp_path / "dna.json"; dna.write_text('{"version": 3}', encoding="utf-8")
    _shared(monkeypatch, library); monkeypatch.setattr(character_sets, "_character_manager", lambda: SimpleNamespace(shared_creation_library=lambda: library, character_record_path=lambda _: dna))
    identity_builder, lora_builder = _builders(monkeypatch)
    frame = tmp_path / "frame.png"; frame.write_bytes(b"png fixture"); report = tmp_path / "report.json"; _report(report, frame)
    identity_out = derived / "set-a"
    identity_args = SimpleNamespace(report=str(report), out_dir=str(identity_out), character=character, actor="test", include_disagree=False, only=None, balance_by_flip=[], max_flips=1, sheet=None, title=None)
    identity_builder.build(identity_args)
    assert (identity_out / "identity-set.json").is_file() and (identity_out / "set-context.json").is_file()
    identity_context = json.loads((identity_out / "set-context.json").read_text(encoding="utf-8"))
    assert identity_context["inputs"]["character_dna"]["version"] == 3
    assert identity_context["output_members"]
    before = {p.relative_to(identity_out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in identity_out.rglob("*") if p.is_file()}
    with pytest.raises(FileExistsError):
        identity_builder.build(identity_args)
    after = {p.relative_to(identity_out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in identity_out.rglob("*") if p.is_file()}
    assert after == before

    monkeypatch.setattr(lora_builder, "_embedding", lambda _: None)
    lora_out = library / "characters" / character / "training" / "lora-a"
    lora_args = SimpleNamespace(identity_set=str(identity_out), character=character, trigger="sxtest", out=str(lora_out), actor="test", min_face=1.0, per_bucket=10, dup_threshold=0.96)
    lora_builder.build(lora_args)
    dataset = json.loads((lora_out / "dataset.json").read_text(encoding="utf-8"))
    assert dataset["members"] and (lora_out / dataset["members"][0]["file"]).with_suffix(".txt").is_file()
    assert (lora_out / "set-context.json").is_file()
    context = json.loads((lora_out / "set-context.json").read_text(encoding="utf-8"))
    assert (lora_out / context["inputs"]["source_manifest"]["snapshot"]).read_bytes() == (identity_out / "identity-set.json").read_bytes()
    for member in context["output_members"]:
        assert hashlib.sha256((lora_out / member["file"]).read_bytes()).hexdigest() == member["sha256"]
    before_lora = {p.relative_to(lora_out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in lora_out.rglob("*") if p.is_file()}
    with pytest.raises(FileExistsError):
        lora_builder.build(lora_args)
    assert before_lora == {p.relative_to(lora_out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in lora_out.rglob("*") if p.is_file()}


def test_identity_builder_mutation_duplicate_and_existing_sheet_leave_no_final_manifest(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; character = "ch-test"; parent = library / "characters" / character / "imports" / "derived"; parent.mkdir(parents=True)
    dna = tmp_path / "dna.json"; dna.write_text('{"version": 1}', encoding="utf-8")
    _shared(monkeypatch, library); monkeypatch.setattr(character_sets, "_character_manager", lambda: SimpleNamespace(shared_creation_library=lambda: library, character_record_path=lambda _: dna))
    builder, _ = _builders(monkeypatch)
    frame = tmp_path / "frame.png"; frame.write_bytes(b"frame")
    report = tmp_path / "report.json"; _report(report, frame)
    original_copy = builder.shutil.copyfile
    def mutate_copy(source, destination):
        original_copy(source, destination); report.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(builder.shutil, "copyfile", mutate_copy)
    mutation_out = parent / "mutation"
    args = SimpleNamespace(report=str(report), out_dir=str(mutation_out), character=character, actor="test", include_disagree=False, only=None, balance_by_flip=[], max_flips=1, sheet=None, title=None)
    with pytest.raises(ValueError, match="changed"):
        builder.build(args)
    assert not (mutation_out / "identity-set.json").exists()
    monkeypatch.setattr(builder.shutil, "copyfile", original_copy)

    report = tmp_path / "report-duplicate.json"; _report(report, frame, shots=["A", "a"])
    duplicate_out = parent / "duplicate"; args.report = str(report); args.out_dir = str(duplicate_out)
    with pytest.raises(ValueError, match="duplicate"):
        builder.build(args)
    assert not (duplicate_out / "identity-set.json").exists()

    report = tmp_path / "report-sheet.json"; _report(report, frame)
    sheet = tmp_path / "sheet.jpg"; sheet.write_bytes(b"keep")
    sheet_out = parent / "sheet"; args.report = str(report); args.out_dir = str(sheet_out); args.sheet = str(sheet)
    with pytest.raises(FileExistsError, match="sheet"):
        builder.build(args)
    assert sheet.read_bytes() == b"keep" and not (sheet_out / "identity-set.json").exists()
