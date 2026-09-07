"""Media probing: images via PIL header; video via ffprobe (never trust extension alone)."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .models import MediaProbe

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_SUFFIXES = {".mp4", ".webm"}
SUPPORTED_SUFFIXES = IMAGE_SUFFIXES | VIDEO_SUFFIXES

IMAGE_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def find_ffprobe() -> str | None:
    return shutil.which("ffprobe")


def probe_image(path: Path) -> MediaProbe:
    try:
        from PIL import Image

        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            width, height = img.size
            fmt = (img.format or "").upper()
        mime = IMAGE_MIME.get(path.suffix.lower())
        if fmt == "PNG":
            mime = "image/png"
        elif fmt in {"JPEG", "JPG"}:
            mime = "image/jpeg"
        elif fmt == "WEBP":
            mime = "image/webp"
        if mime is None:
            return MediaProbe(kind="unknown", error=f"unsupported image format {fmt!r}")
        return MediaProbe(kind="image", mime=mime, width=width, height=height, container=fmt.lower())
    except Exception as exc:  # noqa: BLE001 — surface as invalid media
        return MediaProbe(kind="unknown", error=f"image probe failed: {exc}")


def probe_video(path: Path, *, ffprobe_bin: str | None = None) -> MediaProbe:
    bin_path = ffprobe_bin or find_ffprobe()
    if not bin_path:
        return MediaProbe(kind="unknown", error="ffprobe not found on PATH")
    cmd = [
        bin_path,
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return MediaProbe(kind="unknown", error=f"ffprobe failed: {exc}")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()[:500]
        return MediaProbe(kind="unknown", error=f"ffprobe exit {proc.returncode}: {err}")
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        return MediaProbe(kind="unknown", error=f"ffprobe JSON parse failed: {exc}")

    streams = data.get("streams") or []
    fmt = data.get("format") or {}
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if video_stream is None:
        return MediaProbe(kind="unknown", error="no video stream found (extension alone is not enough)")

    width = video_stream.get("width")
    height = video_stream.get("height")
    try:
        width = int(width) if width is not None else None
        height = int(height) if height is not None else None
    except (TypeError, ValueError):
        width = height = None

    duration = None
    for candidate in (fmt.get("duration"), video_stream.get("duration")):
        if candidate is None:
            continue
        try:
            duration = float(candidate)
            break
        except (TypeError, ValueError):
            continue

    frame_rate = None
    avg = video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate")
    if isinstance(avg, str) and avg not in {"0/0", "N/A"}:
        if "/" in avg:
            num, den = avg.split("/", 1)
            try:
                n, d = float(num), float(den)
                if d:
                    frame_rate = n / d
            except ValueError:
                frame_rate = None
        else:
            try:
                frame_rate = float(avg)
            except ValueError:
                frame_rate = None

    format_name = str(fmt.get("format_name") or "")
    mime = None
    lower = format_name.lower()
    if "webm" in lower or path.suffix.lower() == ".webm":
        # Prefer probed format; still set mime for known containers
        mime = "video/webm"
    if "mp4" in lower or "mov" in lower or "isom" in lower or path.suffix.lower() == ".mp4":
        if mime is None or "mp4" in lower or "isom" in lower:
            mime = "video/mp4"
    if mime is None:
        mime = "video/mp4" if path.suffix.lower() == ".mp4" else ("video/webm" if path.suffix.lower() == ".webm" else None)

    # Extension lying: if suffix says mp4 but format is clearly webm (or vice versa), trust probe
    if "webm" in lower:
        mime = "video/webm"
    elif any(tok in lower for tok in ("mp4", "mov", "isom", "m4a")):
        mime = "video/mp4"

    return MediaProbe(
        kind="video",
        mime=mime,
        width=width,
        height=height,
        duration_seconds=duration,
        codec=video_stream.get("codec_name"),
        frame_rate=frame_rate,
        has_audio=audio_stream is not None,
        container=format_name.split(",")[0] if format_name else None,
    )


def probe_media(path: Path, *, ffprobe_bin: str | None = None) -> MediaProbe:
    """Probe by content. Extension only selects first attempt; video always uses ffprobe."""
    suffix = path.suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        result = probe_image(path)
        if result.kind == "image":
            return result
        # Maybe mislabeled video
        video_try = probe_video(path, ffprobe_bin=ffprobe_bin)
        if video_try.kind == "video":
            return video_try
        return result
    if suffix in VIDEO_SUFFIXES:
        result = probe_video(path, ffprobe_bin=ffprobe_bin)
        if result.kind == "video":
            return result
        # Maybe mislabeled image
        img_try = probe_image(path)
        if img_try.kind == "image":
            return img_try
        return result
    # Unknown suffix: try image then video
    img = probe_image(path)
    if img.kind == "image":
        return img
    vid = probe_video(path, ffprobe_bin=ffprobe_bin)
    if vid.kind == "video":
        return vid
    return MediaProbe(kind="unknown", error=f"unsupported or unreadable media ({suffix or 'no suffix'})")
