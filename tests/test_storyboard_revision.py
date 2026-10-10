from __future__ import annotations

from pathlib import Path

import yaml

from tools.storyboard_revision import ROOT, sha256, validate_storyboard


SCHEMA = ROOT / "schemas" / "screenplay-storyboard-v1.schema.json"


def digest(path: Path) -> str:
    return sha256(path)


def write_storyboard(
    path: Path,
    *,
    source_path: str,
    source_hash: str,
    revision: int = 1,
    parent: dict | None = None,
    storyboard_id: str = "sb_TEST-001_main",
) -> None:
    metadata = {
        "schema_version": 1,
        "artifact_type": "screenplay_storyboard",
        "storyboard_id": storyboard_id,
        "revision": revision,
        "status": "draft",
        "source_scenario": {
            "path": source_path,
            "scenario_id": "TEST-001",
            "revision": 1,
            "sha256": source_hash,
        },
        "parent_storyboard": parent,
        "author": {"actor": "hermes", "model": "test-model"},
        "created_at": "2026-10-10T12:00:00+09:00",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n" + yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True) + "---\n\n# Draft\n",
        encoding="utf-8",
    )


def test_valid_revision_one_binds_exact_scenario(tmp_path: Path) -> None:
    source = tmp_path / "scenarios" / "TEST-001-source.md"
    source.parent.mkdir()
    source.write_text("writer source\n", encoding="utf-8")
    storyboard = tmp_path / "storyboards" / "TEST-001" / "storyboard-r001.md"
    write_storyboard(
        storyboard,
        source_path="scenarios/TEST-001-source.md",
        source_hash=digest(source),
    )

    report = validate_storyboard(storyboard, root=tmp_path, schema_path=SCHEMA)

    assert report["ok"] is True
    assert report["revision"] == 1


def test_source_edit_makes_existing_storyboard_stale(tmp_path: Path) -> None:
    source = tmp_path / "scenarios" / "TEST-001-source.md"
    source.parent.mkdir()
    source.write_text("revision one\n", encoding="utf-8")
    storyboard = tmp_path / "storyboards" / "TEST-001" / "storyboard-r001.md"
    write_storyboard(
        storyboard,
        source_path="scenarios/TEST-001-source.md",
        source_hash=digest(source),
    )
    source.write_text("silently overwritten\n", encoding="utf-8")

    report = validate_storyboard(storyboard, root=tmp_path, schema_path=SCHEMA)

    assert report["ok"] is False
    assert any("source hash mismatch" in error for error in report["errors"])


def test_hash_is_stable_across_bom_crlf_and_lf(tmp_path: Path) -> None:
    source = tmp_path / "scenarios" / "TEST-001-source.md"
    source.parent.mkdir()
    source.write_bytes(b"\xef\xbb\xbfline one\r\nline two\r\n")
    canonical_hash = digest(source)
    storyboard = tmp_path / "storyboards" / "TEST-001" / "storyboard-r001.md"
    write_storyboard(
        storyboard,
        source_path="scenarios/TEST-001-source.md",
        source_hash=canonical_hash,
    )
    assert validate_storyboard(storyboard, root=tmp_path, schema_path=SCHEMA)["ok"] is True

    source.write_bytes(b"line one\nline two\n")
    report = validate_storyboard(storyboard, root=tmp_path, schema_path=SCHEMA)

    assert digest(source) == canonical_hash
    assert report["ok"] is True


def test_revision_two_binds_parent_and_detects_parent_edit(tmp_path: Path) -> None:
    source = tmp_path / "scenarios" / "TEST-001-source.md"
    source.parent.mkdir()
    source.write_text("writer source\n", encoding="utf-8")
    first = tmp_path / "storyboards" / "TEST-001" / "storyboard-r001.md"
    write_storyboard(first, source_path="scenarios/TEST-001-source.md", source_hash=digest(source))
    second = tmp_path / "storyboards" / "TEST-001" / "storyboard-r002.md"
    write_storyboard(
        second,
        source_path="scenarios/TEST-001-source.md",
        source_hash=digest(source),
        revision=2,
        parent={
            "path": "storyboards/TEST-001/storyboard-r001.md",
            "revision": 1,
            "sha256": digest(first),
        },
    )
    assert validate_storyboard(second, root=tmp_path, schema_path=SCHEMA)["ok"] is True

    first.write_text(first.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
    report = validate_storyboard(second, root=tmp_path, schema_path=SCHEMA)

    assert report["ok"] is False
    assert any("parent hash mismatch" in error for error in report["errors"])


def test_revision_two_requires_parent_binding(tmp_path: Path) -> None:
    source = tmp_path / "scenarios" / "TEST-001-source.md"
    source.parent.mkdir()
    source.write_text("writer source\n", encoding="utf-8")
    storyboard = tmp_path / "storyboards" / "TEST-001" / "storyboard-r002.md"
    write_storyboard(
        storyboard,
        source_path="scenarios/TEST-001-source.md",
        source_hash=digest(source),
        revision=2,
    )

    report = validate_storyboard(storyboard, root=tmp_path, schema_path=SCHEMA)

    assert report["ok"] is False
    assert any("parent_storyboard" in error for error in report["errors"])


def test_storyboard_outside_collection_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "scenarios" / "TEST-001-source.md"
    source.parent.mkdir()
    source.write_text("writer source\n", encoding="utf-8")
    storyboard = tmp_path / "elsewhere" / "storyboard-r001.md"
    write_storyboard(
        storyboard,
        source_path="scenarios/TEST-001-source.md",
        source_hash=digest(source),
    )

    report = validate_storyboard(storyboard, root=tmp_path, schema_path=SCHEMA)

    assert report["ok"] is False
    assert any("under storyboards" in error for error in report["errors"])
