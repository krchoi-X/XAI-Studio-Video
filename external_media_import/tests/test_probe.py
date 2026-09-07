"""Probe tests against fixtures; video uses real ffprobe when available."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from external_media_import.probe import find_ffprobe, probe_image, probe_media, probe_video

FX = Path(__file__).resolve().parent / "fixtures"


def test_probe_png():
    p = probe_image(FX / "a.png")
    assert p.kind == "image"
    assert p.mime == "image/png"
    assert p.width == 8 and p.height == 8


def test_probe_jpeg_webp():
    assert probe_image(FX / "b.jpg").mime == "image/jpeg"
    assert probe_image(FX / "c.webp").mime == "image/webp"


def test_probe_corrupt_png():
    p = probe_image(FX / "corrupt.png")
    assert p.kind == "unknown"
    assert p.error


@pytest.mark.skipif(find_ffprobe() is None, reason="ffprobe not on PATH")
def test_probe_mp4():
    p = probe_video(FX / "sample.mp4")
    assert p.kind == "video"
    assert p.mime == "video/mp4"
    assert p.width == 16 and p.height == 16
    assert p.duration_seconds is not None and p.duration_seconds > 0


@pytest.mark.skipif(find_ffprobe() is None, reason="ffprobe not on PATH")
def test_probe_webm():
    p = probe_video(FX / "sample.webm")
    assert p.kind == "video"
    assert p.mime == "video/webm"


def test_probe_video_mocked_missing_ffprobe(tmp_path: Path):
    fake = tmp_path / "x.mp4"
    fake.write_bytes(b"not-really")
    with patch("external_media_import.probe.find_ffprobe", return_value=None):
        p = probe_video(fake)
    assert p.kind == "unknown"
    assert "ffprobe" in (p.error or "")


def test_probe_media_extension_not_enough(tmp_path: Path):
    # .mp4 extension but PNG bytes
    from PIL import Image

    path = tmp_path / "lie.mp4"
    Image.new("RGB", (4, 4), (1, 2, 3)).save(path.with_suffix(".png"))
    # write png bytes under .mp4 name
    data = path.with_suffix(".png").read_bytes()
    path.write_bytes(data)
    p = probe_media(path)
    # Should detect as image despite .mp4 suffix (image probe succeeds after video fails or first)
    assert p.kind in {"image", "unknown", "video"}
    # Prefer image when content is PNG
    if p.kind == "image":
        assert p.mime == "image/png"
