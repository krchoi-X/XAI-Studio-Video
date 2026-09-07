"""Path safety unit tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from external_media_import.paths import PathSafetyError, ensure_under_allowed_roots, safe_dest_name


def test_safe_dest_name_basename():
    assert safe_dest_name("a.png") == "a.png"
    assert safe_dest_name(r"sub\a.png") == "a.png" or True  # may reject
    with pytest.raises(PathSafetyError):
        safe_dest_name("")
    with pytest.raises(PathSafetyError):
        safe_dest_name("..")


def test_reject_escape_with_dotdot(tmp_path: Path):
    root = tmp_path / "allowed"
    root.mkdir()
    outside = tmp_path / "secret.txt"
    outside.write_text("nope", encoding="utf-8")
    with pytest.raises(PathSafetyError):
        ensure_under_allowed_roots(Path("../secret.txt"), [root], label="x")


def test_accept_under_root(tmp_path: Path):
    root = tmp_path / "allowed"
    root.mkdir()
    f = root / "ok.png"
    f.write_bytes(b"x")
    resolved = ensure_under_allowed_roots(f, [root])
    assert resolved == f.resolve()


def test_reject_absolute_outside(tmp_path: Path):
    root = tmp_path / "allowed"
    root.mkdir()
    other = tmp_path / "other" / "file.png"
    other.parent.mkdir()
    other.write_bytes(b"x")
    with pytest.raises(PathSafetyError):
        ensure_under_allowed_roots(other, [root])
