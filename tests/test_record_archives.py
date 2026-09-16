from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
import pytest
import record_archives


@pytest.mark.skipif(os.name != 'nt', reason='Windows junction contract')
def test_windows_junction_parent_is_rejected(tmp_path: Path):
    import subprocess
    root, source = _archive(tmp_path)
    junction = tmp_path / 'junction-parent'
    environment = dict(os.environ, XAI_TEST_JUNCTION=str(junction), XAI_TEST_TARGET=str(root.parent))
    subprocess.run(['powershell', '-NoProfile', '-NonInteractive', '-Command',
                    'New-Item -ItemType Junction -Path $env:XAI_TEST_JUNCTION -Target $env:XAI_TEST_TARGET -ErrorAction Stop | Out-Null'],
                   env=environment, check=True, capture_output=True)
    assert junction.lstat().st_file_attributes & 0x400
    with pytest.raises(ValueError, match='unsafe'):
        record_archives.resolve_recorded_path(junction / root.name, source / 'notes/prompt.txt')

def _archive(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "Library/characters/ch-test/generations/s1"; root.mkdir(parents=True); (root / "outputs").mkdir()
    member = root / "notes/prompt.txt"; member.parent.mkdir(); member.write_bytes(b"historical")
    source = tmp_path / "missing-runtime/s1"
    marker = {"schema_version": 1, "kind": "historical-record-archive", "character_id": "ch-test", "session_id": "s1", "source_root": str(source), "archive_root": str(root), "captured_at": "2026-09-15T00:00:00Z", "authority": "historical-snapshot", "files": [{"path": "notes/prompt.txt", "sha256": hashlib.sha256(member.read_bytes()).hexdigest(), "bytes": member.stat().st_size}], "outputs_root": str(root / "outputs"), "backup_plan_sha256": "a" * 64}
    (root / "record-archive.json").write_text(json.dumps(marker), encoding="utf-8")
    return root, source

def test_describe_and_resolve_source_absent(tmp_path: Path, monkeypatch) -> None:
    root, source = _archive(tmp_path); library = tmp_path / "Library"
    monkeypatch.setattr(record_archives, "_cm", lambda: SimpleNamespace(shared_creation_library=lambda: library))
    listed = record_archives.describe_archives("ch-test")
    assert listed[0]["record_count"] == 1 and listed[0]["source_path"] == str(source)
    assert record_archives.resolve_recorded_path(root, source / "notes/prompt.txt").read_bytes() == b"historical"


def test_schema_two_nested_raw_batch_source_absent_multiple_snapshots(tmp_path: Path, monkeypatch) -> None:
    session = tmp_path / "Library/characters/ch-test/generations/s2"; source = tmp_path / "gone/s2"
    for snapshot in ("20260915", "future-1"):
        root = session / "historical-records" / snapshot; root.mkdir(parents=True)
        batch = root / "batch.yaml"; batch.write_text(f"asset_root: {source / 'outputs'}\n", encoding="utf-8")
        marker = {"schema_version":2,"kind":"historical-record-archive","character_id":"ch-test","session_id":"s2","snapshot_id":snapshot,"source_root":str(source),"archive_root":str(root),"captured_at":"now","authority":"historical-snapshot","files":[{"path":"batch.yaml","sha256":hashlib.sha256(batch.read_bytes()).hexdigest(),"bytes":batch.stat().st_size}],"outputs_root":None,"backup_plan_sha256":"b"*64}
        (root / "record-archive.json").write_text(json.dumps(marker), encoding="utf-8")
    monkeypatch.setattr(record_archives,"_cm",lambda: SimpleNamespace(shared_creation_library=lambda: tmp_path / "Library"))
    rows = record_archives.describe_archives("ch-test")
    assert {row["snapshot_id"] for row in rows} == {"20260915", "future-1"} and all(row["outputs_path"] is None for row in rows)
    assert record_archives.resolve_recorded_path(session / "historical-records/20260915", source / "batch.yaml").read_bytes().startswith(b"asset_root")


@pytest.mark.parametrize("field,value", [("snapshot_id", "wrong"), ("session_id", "wrong"), ("character_id", "ch-other"), ("outputs_root", "missing")])
def test_schema_two_rejects_wrong_nesting_and_output_linkage(tmp_path: Path, field, value) -> None:
    session = tmp_path / "Library/characters/ch-test/generations/s2"; root = session / "historical-records/20260915"; root.mkdir(parents=True)
    batch = root / "batch.yaml"; batch.write_bytes(b"x"); outputs = session / "outputs"; outputs.mkdir()
    marker = {"schema_version":2,"kind":"historical-record-archive","character_id":"ch-test","session_id":"s2","snapshot_id":"20260915","source_root":str(tmp_path / "gone/s2"),"archive_root":str(root),"captured_at":"now","authority":"historical-snapshot","files":[{"path":"batch.yaml","sha256":hashlib.sha256(b"x").hexdigest(),"bytes":1}],"outputs_root":str(outputs),"backup_plan_sha256":"b"*64}
    marker[field] = value; (root / "record-archive.json").write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(ValueError): record_archives.resolve_recorded_path(root, tmp_path / "gone/s2/batch.yaml")


def test_schema_two_partial_folder_is_invisible(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; (library / "characters/ch-test/generations/s2/historical-records/partial").mkdir(parents=True)
    monkeypatch.setattr(record_archives,"_cm",lambda: SimpleNamespace(shared_creation_library=lambda: library))
    assert record_archives.describe_archives("ch-test") == []

@pytest.mark.parametrize("change", ["duplicate", "escape", "tamper"])
def test_archive_rejects_bad_members_and_tamper(tmp_path: Path, change: str) -> None:
    root, source = _archive(tmp_path); marker_path = root / "record-archive.json"; marker = json.loads(marker_path.read_text())
    if change == "duplicate": marker["files"].append(dict(marker["files"][0]))
    elif change == "escape": marker["files"][0]["path"] = "../outside.txt"
    else: (root / "notes/prompt.txt").write_bytes(b"changed")
    marker_path.write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(ValueError): record_archives.resolve_recorded_path(root, source / "notes/prompt.txt")


def test_archive_rejects_missing_marker_and_external_or_unlisted_paths(tmp_path: Path) -> None:
    root, source = _archive(tmp_path)
    with pytest.raises(ValueError):
        record_archives.resolve_recorded_path(root, tmp_path / "outside.txt")
    with pytest.raises(ValueError):
        record_archives.resolve_recorded_path(root, source / "other.txt")
    (root / "record-archive.json").unlink()
    with pytest.raises(ValueError):
        record_archives.resolve_recorded_path(root, source / "notes/prompt.txt")


@pytest.mark.parametrize("field,value", [("backup_plan_sha256", "bad"), ("outputs_root", "relative"), ("bytes", True)])
def test_archive_rejects_strict_marker_fields(tmp_path: Path, field: str, value) -> None:
    root, source = _archive(tmp_path); marker_path = root / "record-archive.json"; marker = json.loads(marker_path.read_text())
    if field == "bytes": marker["files"][0][field] = value
    else: marker[field] = value
    marker_path.write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(ValueError): record_archives.resolve_recorded_path(root, source / "notes/prompt.txt")


def test_archive_rejects_linked_archive_ancestor(tmp_path: Path) -> None:
    root, source = _archive(tmp_path); linked = tmp_path / "linked-session"
    try:
        os.symlink(root, linked, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"link creation unavailable: {exc}")
    with pytest.raises(ValueError, match="unsafe"):
        record_archives.resolve_recorded_path(linked, source / "notes/prompt.txt")


def test_archive_rejects_linked_parent_ancestor(tmp_path: Path) -> None:
    root, source = _archive(tmp_path); linked_parent = tmp_path / "linked-generations"
    try:
        os.symlink(root.parent, linked_parent, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"link creation unavailable: {exc}")
    with pytest.raises(ValueError, match="unsafe"):
        record_archives.resolve_recorded_path(linked_parent / root.name, source / "notes/prompt.txt")


@pytest.mark.parametrize("raw", ["notes/./prompt.txt", "notes//prompt.txt", "notes:bad.txt"])
def test_archive_rejects_noncanonical_member_paths(tmp_path: Path, raw: str) -> None:
    root, source = _archive(tmp_path); marker_path = root / "record-archive.json"; marker = json.loads(marker_path.read_text())
    marker["files"][0]["path"] = raw; marker_path.write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(ValueError): record_archives.resolve_recorded_path(root, source / "notes/prompt.txt")

def _null_output_archive(tmp_path: Path, artifact_path: Path, artifact_bytes: bytes = b"video", snapshot: str = "20260915", run_id: str = "r1") -> tuple[Path, Path, Path]:
    library = tmp_path / "Library"; root = library / f"characters/ch-test/generations/s2/historical-records/{snapshot}"; root.mkdir(parents=True)
    source = tmp_path / "gone/s2"; archived = root / "clip.mp4"; archived.write_bytes(artifact_bytes)
    run = root / f"runs/{run_id}/run.json"; run.parent.mkdir(parents=True)
    run.write_text(json.dumps({"status":"needs_review","artifacts":[{"path":str(artifact_path),"sha256":hashlib.sha256(artifact_bytes).hexdigest(),"byte_count":len(artifact_bytes)}]}), encoding="utf-8")
    files=[]
    for path in (archived, run):
        files.append({"path":path.relative_to(root).as_posix(),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size})
    marker={"schema_version":2,"kind":"historical-record-archive","character_id":"ch-test","session_id":"s2","snapshot_id":snapshot,"source_root":str(source),"archive_root":str(root),"captured_at":"now","authority":"historical-snapshot","files":files,"outputs_root":None,"backup_plan_sha256":"a"*64}
    (root / "record-archive.json").write_text(json.dumps(marker),encoding="utf-8")
    return root, source, library

def _refresh_run_member(root: Path, run: Path) -> None:
    marker_path = root / "record-archive.json"; marker = json.loads(marker_path.read_text(encoding="utf-8"))
    member = next(item for item in marker["files"] if item["path"] == run.relative_to(root).as_posix())
    member.update(sha256=hashlib.sha256(run.read_bytes()).hexdigest(), bytes=run.stat().st_size)
    marker_path.write_text(json.dumps(marker), encoding="utf-8")

def test_null_output_rows_resolve_archived_source_after_source_absent(tmp_path: Path, monkeypatch) -> None:
    source_artifact = tmp_path / "gone/s2/clip.mp4"; root, _, library = _null_output_archive(tmp_path, source_artifact)
    monkeypatch.setattr(record_archives,"_cm",lambda:SimpleNamespace(shared_creation_library=lambda:library))
    row = record_archives.describe_archives("ch-test")[0]["recorded_artifacts"][0]
    assert row["location"] == "archive" and row["status"] == "available" and row["integrity"] == "not_checked"
    assert record_archives.resolve_artifact_path(root,"runs/r1/run.json",0).read_bytes() == b"video"

def test_null_output_library_rows_block_cross_character_and_require_explicit_hash(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; allowed = library / "characters/ch-test/videos/a.mp4"; allowed.parent.mkdir(parents=True); allowed.write_bytes(b"video")
    root, _, _ = _null_output_archive(tmp_path, allowed)
    monkeypatch.setattr(record_archives,"_cm",lambda:SimpleNamespace(shared_creation_library=lambda:library))
    assert record_archives.describe_archives("ch-test")[0]["recorded_artifacts"][0]["location"] == "library"
    allowed.write_bytes(b"other")
    assert record_archives.describe_archives("ch-test")[0]["recorded_artifacts"][0]["integrity"] == "not_checked"
    with pytest.raises(ValueError, match="hash"):
        record_archives.resolve_artifact_path(root,"runs/r1/run.json",0)
    run=root/"runs/r1/run.json"; data=json.loads(run.read_text()); data["artifacts"][0]["path"]=str(library/"characters/ch-other/videos/a.mp4"); run.write_text(json.dumps(data),encoding="utf-8"); _refresh_run_member(root, run)
    blocked=record_archives.describe_archives("ch-test")[0]["recorded_artifacts"][0]
    assert blocked["status"] == "blocked" and blocked["resolved_path"] is None

def test_null_output_rejects_tampered_run_and_bad_index(tmp_path: Path, monkeypatch) -> None:
    library=tmp_path/"Library"; root, _, _ = _null_output_archive(tmp_path,tmp_path/"gone/s2/clip.mp4")
    monkeypatch.setattr(record_archives,"_cm",lambda:SimpleNamespace(shared_creation_library=lambda:library))
    (root/"runs/r1/run.json").write_text("{}",encoding="utf-8")
    with pytest.raises(ValueError): record_archives.describe_archives("ch-test")
    with pytest.raises(ValueError): record_archives.resolve_artifact_path(root,"runs/r1/run.json",True)

def test_null_output_wrong_size_never_lists_available(tmp_path: Path, monkeypatch) -> None:
    root, _, library = _null_output_archive(tmp_path, tmp_path / "gone/s2/clip.mp4")
    monkeypatch.setattr(record_archives,"_cm",lambda:SimpleNamespace(shared_creation_library=lambda:library))
    (root / "clip.mp4").write_bytes(b"too-long")
    archived = record_archives.describe_archives("ch-test")[0]["recorded_artifacts"][0]
    assert archived["location"] == "archive" and archived["status"] == "missing" and archived["integrity"] == "not_checked"
    library_target=library / "characters/ch-test/videos/a.mp4"; library_target.parent.mkdir(parents=True); library_target.write_bytes(b"video")
    root, _, _ = _null_output_archive(tmp_path, library_target, snapshot="future")
    library_target.write_bytes(b"too-long")
    listed=record_archives.describe_archives("ch-test")
    row=next(item for item in listed if item["records_path"] == str(root))["recorded_artifacts"][0]
    assert row["location"] == "library" and row["status"] == "missing"

@pytest.mark.parametrize("artifact", [
    "not-a-record", {"path": 3}, {"path": "x", "sha256": "bad"},
    {"path": "x", "byte_count": True},
])
def test_null_output_rejects_malformed_artifact_metadata(tmp_path: Path, monkeypatch, artifact) -> None:
    root, _, library = _null_output_archive(tmp_path, tmp_path / "gone/s2/clip.mp4")
    monkeypatch.setattr(record_archives, "_cm", lambda: SimpleNamespace(shared_creation_library=lambda: library))
    run = root / "runs/r1/run.json"; data = json.loads(run.read_text()); data["artifacts"] = [artifact]
    run.write_text(json.dumps(data), encoding="utf-8"); _refresh_run_member(root, run)
    with pytest.raises(ValueError): record_archives.describe_archives("ch-test")

def test_null_output_rejects_invalid_selection_and_preserves_duplicate_paths(tmp_path: Path, monkeypatch) -> None:
    root, source, library = _null_output_archive(tmp_path, tmp_path / "gone/s2/clip.mp4")
    monkeypatch.setattr(record_archives, "_cm", lambda: SimpleNamespace(shared_creation_library=lambda: library))
    run = root / "runs/r1/run.json"; data = json.loads(run.read_text())
    other = root / "runs/r2/run.json"; other.parent.mkdir(); other.write_text(json.dumps(data), encoding="utf-8")
    marker_path = root / "record-archive.json"; marker = json.loads(marker_path.read_text())
    marker["files"].append({"path":"runs/r2/run.json", "sha256":hashlib.sha256(other.read_bytes()).hexdigest(), "bytes":other.stat().st_size})
    marker_path.write_text(json.dumps(marker), encoding="utf-8")
    rows = record_archives.describe_archives("ch-test")[0]["recorded_artifacts"]
    assert [row["run_id"] for row in rows] == ["r1", "r2"] and rows[0]["recorded_path"] == rows[1]["recorded_path"]
    for path, index in (("runs/r1/run.json", -1), ("runs/r1/run.json", 1), ("runs/missing/run.json", 0), ("runs/r1/other.json", 0)):
        with pytest.raises(ValueError): record_archives.resolve_artifact_path(root, path, index)
    library_target = library / "characters/ch-test/videos/missing-checksum.mp4"; library_target.parent.mkdir(parents=True); library_target.write_bytes(b"video")
    data["artifacts"][0]["path"] = str(library_target); data["artifacts"][0].pop("sha256")
    run.write_text(json.dumps(data), encoding="utf-8"); _refresh_run_member(root, run)
    with pytest.raises(ValueError, match="unchecked"): record_archives.resolve_artifact_path(root, "runs/r1/run.json", 0)

@pytest.mark.skipif(os.name != "nt", reason="Windows junction contract")
def test_null_output_blocks_junction_library_target(tmp_path: Path, monkeypatch) -> None:
    library = tmp_path / "Library"; external = tmp_path / "external"; external.mkdir()
    linked = library / "characters/ch-test/videos"; linked.parent.mkdir(parents=True)
    environment = dict(os.environ, XAI_TEST_JUNCTION=str(linked), XAI_TEST_TARGET=str(external))
    import subprocess
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", "New-Item -ItemType Junction -Path $env:XAI_TEST_JUNCTION -Target $env:XAI_TEST_TARGET -ErrorAction Stop | Out-Null"], env=environment, check=True, capture_output=True)
    (external / "a.mp4").write_bytes(b"video")
    root, _, _ = _null_output_archive(tmp_path, linked / "a.mp4")
    monkeypatch.setattr(record_archives, "_cm", lambda: SimpleNamespace(shared_creation_library=lambda: library))
    row = record_archives.describe_archives("ch-test")[0]["recorded_artifacts"][0]
    assert row["status"] == "blocked" and row["resolved_path"] is None
