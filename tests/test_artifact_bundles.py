from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

import artifact_bundles


def _bundle(tmp_path: Path, bundle_id: str = "reports", snapshot: str = "20260915") -> tuple[Path, Path]:
    root = tmp_path / "Library/records" / bundle_id / snapshot
    root.mkdir(parents=True)
    source = tmp_path / "missing-source" / bundle_id
    report = root / "raw/run.json"; report.parent.mkdir(); report.write_bytes(b'{"status":"failed"}')
    external = root / "external-inputs/run-1/prompt.txt"; external.parent.mkdir(parents=True); external.write_bytes(b"prompt")
    files = [
        {"path": "raw/run.json", "source_path": str(source / "runs/run-1/run.json"), "bytes": report.stat().st_size, "sha256": hashlib.sha256(report.read_bytes()).hexdigest(), "role": "source-record"},
        {"path": "external-inputs/run-1/prompt.txt", "source_path": str(source / "prompt.txt"), "bytes": external.stat().st_size, "sha256": hashlib.sha256(external.read_bytes()).hexdigest(), "role": "external-input-at-archive-time"},
    ]
    marker = {"schema_version": 1, "kind": "historical-artifact-bundle", "bundle_id": bundle_id, "snapshot_id": snapshot, "authority": "historical-snapshot", "captured_at": "2026-09-15T00:00:00Z", "archive_root": str(root), "source_roots": [str(source)], "files": files}
    (root / "archive-bundle.json").write_text(json.dumps(marker), encoding="utf-8")
    return root, source


def test_describe_mixed_roles_source_absent_and_multiple_snapshots(tmp_path: Path, monkeypatch) -> None:
    reports, source = _bundle(tmp_path)
    standalone, _ = _bundle(tmp_path, "standalone-runs", "20260916")
    (tmp_path / "Library/records/reports/partial").mkdir(parents=True)
    monkeypatch.setattr(artifact_bundles, "_cm", lambda: SimpleNamespace(shared_creation_library=lambda: tmp_path / "Library"))
    rows = artifact_bundles.describe_bundles()
    assert {(row["bundle_id"], row["snapshot_id"]) for row in rows} == {("reports", "20260915"), ("standalone-runs", "20260916")}
    report_row = next(row for row in rows if row["records_path"] == str(reports))
    assert report_row["record_count"] == 2 and report_row["total_bytes"] == len(b'{"status":"failed"}') + len(b"prompt")
    assert artifact_bundles.resolve_source_path(reports, source / "runs/run-1/run.json").read_bytes() == b'{"status":"failed"}'
    assert standalone.is_dir()


@pytest.mark.parametrize("mutation", ["bool", "bad-root", "root-alias", "bad-member", "duplicate", "traversal", "pending-marker", "source-traversal", "roots-traversal", "missing"])
def test_marker_rejects_malformed_members_and_roots(tmp_path: Path, mutation: str) -> None:
    root, source = _bundle(tmp_path); marker_path = root / "archive-bundle.json"; marker = json.loads(marker_path.read_text())
    if mutation == "bool": marker["schema_version"] = True
    elif mutation == "bad-root": marker["archive_root"] = str(root.parent / "other")
    elif mutation == "root-alias": marker["archive_root"] = str(root.parent / "../" / root.parent.name / root.name)
    elif mutation == "bad-member": marker["files"][0]["role"] = "approved"
    elif mutation == "duplicate": marker["files"].append(dict(marker["files"][0], path="RAW/run.json"))
    elif mutation == "traversal": marker["files"][0]["path"] = "../raw/run.json"
    elif mutation == "pending-marker": marker["files"][0]["path"] = ".ARCHIVE-BUNDLE.PENDING.JSON"
    elif mutation == "source-traversal": marker["files"][0]["source_path"] = str(source / "../outside.txt")
    elif mutation == "roots-traversal": marker["source_roots"] = [str(source / "../outside")]
    elif mutation == "missing": (root / "raw/run.json").unlink()
    marker_path.write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(ValueError): artifact_bundles.resolve_source_path(root, source / "runs/run-1/run.json")


def test_rejects_tamper_unlisted_and_marker_alias(tmp_path: Path) -> None:
    root, source = _bundle(tmp_path)
    (root / "raw/run.json").write_bytes(b"changed")
    with pytest.raises(ValueError, match="hash"): artifact_bundles.resolve_source_path(root, source / "runs/run-1/run.json")
    with pytest.raises(ValueError): artifact_bundles.resolve_source_path(root, source / "unknown.txt")


@pytest.mark.skipif(os.name != "nt", reason="Windows junction contract")
def test_windows_junction_parent_is_rejected(tmp_path: Path) -> None:
    import subprocess
    root, source = _bundle(tmp_path); junction = tmp_path / "junction"
    env = dict(os.environ, XAI_TEST_JUNCTION=str(junction), XAI_TEST_TARGET=str(root.parent))
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", "New-Item -ItemType Junction -Path $env:XAI_TEST_JUNCTION -Target $env:XAI_TEST_TARGET -ErrorAction Stop | Out-Null"], env=env, check=True, capture_output=True)
    assert junction.lstat().st_file_attributes & 0x400
    with pytest.raises(ValueError, match="unsafe"):
        artifact_bundles.resolve_source_path(junction / root.name, source / "runs/run-1/run.json")
