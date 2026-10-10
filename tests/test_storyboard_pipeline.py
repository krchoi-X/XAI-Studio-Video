from __future__ import annotations

import subprocess
from pathlib import Path

from tools import storyboard_pipeline


def test_pipeline_rejects_false_write_reports_and_stops_after_two_attempts(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "scenarios" / "TEST-001.md"
    source.parent.mkdir()
    source.write_text(
        "#### S01\n- **예상 길이**: 5초\n- **시간순 행동**:\n  1. 문이 열린다.\n",
        encoding="utf-8",
    )
    storyboard = tmp_path / "storyboards" / "TEST-001" / "storyboard-r001.md"
    plan = tmp_path / "storyboards" / "TEST-001" / "storyboard-r001.preflight.json"
    calls: list[list[str]] = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="written", stderr="")

    monkeypatch.setattr(storyboard_pipeline, "ROOT", tmp_path)
    monkeypatch.setattr(storyboard_pipeline.subprocess, "run", fake_run)
    report = storyboard_pipeline.run_pipeline(source=source, storyboard=storyboard, plan=plan)

    assert report["ready"] is False
    assert report["attempts"] == 2
    assert len(calls) == 2
    assert "not created or changed" in report["repair_items"][0]


def test_pipeline_blocks_unstructured_source_before_calling_hermes(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "scenarios" / "TEST-001.md"
    source.parent.mkdir()
    source.write_text("A loose paragraph without stable scene or action IDs.\n", encoding="utf-8")
    called = False

    def fake_run(command, **kwargs):
        nonlocal called
        called = True
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(storyboard_pipeline, "ROOT", tmp_path)
    monkeypatch.setattr(storyboard_pipeline.subprocess, "run", fake_run)
    report = storyboard_pipeline.run_pipeline(
        source=source,
        storyboard=tmp_path / "storyboard.md",
        plan=tmp_path / "plan.json",
    )

    assert report["blocked"] is True
    assert report["attempts"] == 0
    assert called is False
