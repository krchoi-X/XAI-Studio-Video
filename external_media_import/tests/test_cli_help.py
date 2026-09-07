"""CLI smoke tests."""

from __future__ import annotations

from external_media_import.cli import build_parser, main


def test_help_exits_zero():
    parser = build_parser()
    help_text = parser.format_help()
    assert "dry-run" in help_text
    assert "apply" in help_text
    assert "resume" in help_text


def test_dry_run_cli(tmp_path):
    from pathlib import Path

    FX = Path(__file__).resolve().parent / "fixtures"
    code = main(
        [
            "dry-run",
            "--manifest",
            str(FX / "manifest.json"),
            "--source-dir",
            str(FX),
            "--character-id",
            "ch-test",
            "--session-id",
            "CLI-DRY",
            "--title",
            "CLI dry",
            "--engine",
            "gpt",
            "--library-root",
            str(tmp_path / "lib"),
            "--record-root",
            str(tmp_path / "rec"),
            "--allowed-source-root",
            str(FX),
            "--json",
        ]
    )
    assert code == 0
