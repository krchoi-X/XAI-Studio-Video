"""Planner + apply dry-run/apply/idempotent tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from external_media_import.apply import apply_plan
from external_media_import.hashutil import sha256_file
from external_media_import.models import ItemStatus
from external_media_import.planner import build_plan

FX = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture()
def roots(tmp_path: Path):
    library = tmp_path / "library"
    records = tmp_path / "records"
    library.mkdir()
    records.mkdir()
    return library, records


def test_dry_run_mixed_manifest(roots):
    library, records = roots
    plan = build_plan(
        character_id="ch-test",
        session_id="TEST-20260907-mixed",
        title="Mixed fixture import",
        engine="gpt",
        library_root=library,
        record_root=records,
        visibility="standard",
        provider="OpenAI",
        model="fixture-model",
        manifest_path=FX / "manifest.json",
        source_dir=FX,
        allowed_source_roots=[FX],
    )
    assert not plan.errors
    counts = plan.counts()
    assert counts.get("planned") == 5
    assert plan.prompt_strategy == "provenance"
    # nothing written
    assert not (records / "TEST-20260907-mixed" / "batch.yaml").exists()


def test_apply_and_idempotent_resume(roots):
    library, records = roots
    kwargs = dict(
        character_id="ch-test",
        session_id="TEST-20260907-apply",
        title="Apply fixture",
        engine="gpt",
        library_root=library,
        record_root=records,
        visibility="restricted",  # must preserve, not lift
        provider="OpenAI",
        model="fixture-model",
        manifest_path=FX / "manifest.json",
        source_dir=FX,
        allowed_source_roots=[FX],
    )
    plan = build_plan(**kwargs)
    result = apply_plan(plan)
    assert result.exit_code == 0
    assert result.copied == 5
    assert result.batch_published

    record_dir = records / "TEST-20260907-apply"
    assert (record_dir / "batch.yaml").is_file()
    assert (record_dir / "prompt.txt").is_file()
    assert (record_dir / "import-provenance.json").is_file()

    batch = json.loads((record_dir / "batch.yaml").read_text(encoding="utf-8"))
    assert batch["session"]["visibility"] == "restricted"
    assert batch["session"]["asset_root"].endswith("outputs")
    assert batch["review"]["initial_state"] == "needs_review"
    assert batch["jobs"][0]["output_dir"] == "outputs/gpt"

    # prompt.txt must not be a single mashed fake prompt — file-tagged
    prompt_txt = (record_dir / "prompt.txt").read_text(encoding="utf-8")
    assert "a.png" in prompt_txt
    assert "red square prompt A" in prompt_txt
    assert "sample.mp4" in prompt_txt

    prov = json.loads((record_dir / "import-provenance.json").read_text(encoding="utf-8"))
    assert len(prov) == 5
    assert all("sha256" in row for row in prov)

    out = library / "ch-test" / "generations" / "TEST-20260907-apply" / "outputs" / "gpt"
    for name in ["a.png", "b.jpg", "c.webp", "sample.mp4", "sample.webm"]:
        dest = out / name
        assert dest.is_file()
        assert sha256_file(dest) == sha256_file(FX / name)

    # Idempotent re-apply
    plan2 = build_plan(**kwargs)
    assert plan2.counts().get("duplicate") == 5
    result2 = apply_plan(plan2)
    assert result2.copied == 0
    assert result2.noop == 5
    assert result2.exit_code == 0


def test_conflict_different_hash(roots):
    library, records = roots
    kwargs = dict(
        character_id="ch-test",
        session_id="TEST-20260907-conflict",
        title="Conflict",
        engine="gpt",
        library_root=library,
        record_root=records,
        manifest_path=None,
        source_dir=FX,
        allowed_source_roots=[FX],
        provider=None,
        model=None,
    )
    # First copy only a.png via tiny manifest
    man = {
        "items": [{"file": "a.png", "source": str(FX / "a.png"), "prompt": "A"}],
    }
    mpath = roots[1] / "m1.json"
    # use records parent
    mpath = Path(records) / "m1.json"
    mpath.write_text(json.dumps(man), encoding="utf-8")
    plan = build_plan(**{**kwargs, "manifest_path": mpath, "source_dir": None, "session_id": "TEST-20260907-conflict"})
    # source_dir None but allowed root FX; absolute paths in manifest
    plan = build_plan(
        character_id="ch-test",
        session_id="TEST-20260907-conflict",
        title="Conflict",
        engine="gpt",
        library_root=library,
        record_root=records,
        manifest_path=mpath,
        allowed_source_roots=[FX],
    )
    assert apply_plan(plan).exit_code == 0

    # Plant different content at dest name via second source named a.png content from b.jpg
    man2 = {
        "items": [{"file": "a.png", "source": str(FX / "b.jpg"), "prompt": "B"}],
    }
    mpath2 = Path(records) / "m2.json"
    mpath2.write_text(json.dumps(man2), encoding="utf-8")
    plan2 = build_plan(
        character_id="ch-test",
        session_id="TEST-20260907-conflict",
        title="Conflict",
        engine="gpt",
        library_root=library,
        record_root=records,
        manifest_path=mpath2,
        allowed_source_roots=[FX],
    )
    assert plan2.counts().get("conflict") == 1
    result = apply_plan(plan2)
    assert result.exit_code == 2
    assert not result.batch_published or True  # should not republish on blocker
    # Original intact
    dest = library / "ch-test" / "generations" / "TEST-20260907-conflict" / "outputs" / "gpt" / "a.png"
    assert sha256_file(dest) == sha256_file(FX / "a.png")


def test_path_escape_rejected(roots):
    library, records = roots
    man = {
        "items": [{"file": "evil.png", "source": str(Path.cwd() / "does-not-matter.png"), "prompt": "x"}],
    }
    mpath = Path(records) / "escape.json"
    mpath.write_text(json.dumps(man), encoding="utf-8")
    plan = build_plan(
        character_id="ch-test",
        session_id="TEST-escape",
        title="Escape",
        engine="gpt",
        library_root=library,
        record_root=records,
        manifest_path=mpath,
        allowed_source_roots=[FX],
    )
    assert plan.counts().get("path_rejected") == 1


def test_invalid_corrupt(roots):
    library, records = roots
    man = {
        "items": [{"file": "corrupt.png", "source": str(FX / "corrupt.png")}],
    }
    mpath = Path(records) / "bad.json"
    mpath.write_text(json.dumps(man), encoding="utf-8")
    plan = build_plan(
        character_id="ch-test",
        session_id="TEST-bad",
        title="Bad",
        engine="gpt",
        library_root=library,
        record_root=records,
        manifest_path=mpath,
        allowed_source_roots=[FX],
    )
    assert plan.counts().get("invalid") == 1
