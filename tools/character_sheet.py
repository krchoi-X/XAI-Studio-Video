#!/usr/bin/env python3
"""Build a character sheet from an identity set, a body clip and the character record.

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/character_sheet.py \
        --character ch-shindo-noa \
        --identity-set LIBRARY/imports/derived/identity-set-YYYYMMDD \
        --body-video PATH.mp4 [--body-video PATH.mp4] \
        --out REPORT/character-sheet.jpg

The sheet is a **derived, regenerable artifact for people to look at**, not a model input. Everything on it
comes from the identity set and the record, so it can be thrown away and rebuilt; the individual frames and
`character.json` are the assets. This matters because a collage's individual panels land at 150-250 px,
which is far below what any training or reference-conditioning path can use.

Five sections, each answering a different question:

- **Identity anchors** - who is this, across the yaw range, at the sizes the recogniser can actually read.
- **Figure** - the whole body from front, side and back, which no portrait can establish.
- **Detail** - the features the record names as identity anchors, cropped from the largest frontal frame.
- **Palette** - hair, iris, skin and lip sampled as real hex values from the reference portrait. A swatch
  without a number cannot be reproduced, so the numbers are printed.
- **Specification** - the record's own text, so the sheet and the DNA cannot drift apart silently.

Mirrored members of the identity set are excluded from the anchor row: a flip is not evidence about this
face, and a sheet is exactly where that would be forgotten.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import identity_score

FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
INK = "#e6edf3"
DIM = "#8b949e"
ACCENT = "#ffd166"
BACKGROUND = "#16181d"
PANEL = "#202430"

# Yaw targets for the anchor row, left profile through frontal to right profile.
ANCHOR_YAWS = (-0.90, -0.62, -0.38, -0.18, 0.0, 0.18, 0.38, 0.62, 0.90)
# Where to sample the palette, as (name, landmark index pair or None, offset in inter-ocular units).
# YuNet landmarks are right eye, left eye, nose tip, right mouth corner, left mouth corner.
# The mouth sample is whatever the reference is actually wearing. For this character the record calls red
# lipstick a styling choice rather than a trait, so the swatch is labelled as makeup and not as lip colour.
PALETTE_POINTS = (("머리 hair", "above_brow"), ("홍채 iris", "right_eye"),
                  ("피부 skin", "cheek"), ("입술 lip (메이크업)", "mouth"))


def font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def read_image(path: str | Path):
    return cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)


def paste(sheet: Image.Image, bgr, box: tuple[int, int, int, int]) -> None:
    x, y, w, h = box
    sheet.paste(Image.fromarray(cv2.cvtColor(cv2.resize(bgr, (w, h)), cv2.COLOR_BGR2RGB)), (x, y))


def anchors(manifest: dict[str, Any], set_dir: Path) -> list[dict[str, Any]]:
    """One real, unmirrored frame per yaw target, preferring the largest face at that angle."""
    pool = [m for m in manifest["members"] if not m.get("mirrored")]
    chosen, taken = [], []
    for target in ANCHOR_YAWS:
        # Exclude anything already standing in for a neighbouring target: two columns showing the same yaw
        # would claim coverage the set does not have.
        near = [m for m in pool
                if abs((m["yaw_proxy"] or 0) - target) < 0.14
                and all(abs((m["yaw_proxy"] or 0) - y) > 0.06 for y in taken)]
        if not near:
            chosen.append({})
            continue
        best = max(near, key=lambda m: m["face_pixels"][0])
        taken.append(best["yaw_proxy"] or 0)
        chosen.append(dict(best, path=str(set_dir / best["file"])))
    return chosen


def body_frames(videos: list[str], work: Path) -> list[tuple[str, Any]]:
    """Front, three-quarter, side and back from the half-circle turn in each body clip."""
    work.mkdir(parents=True, exist_ok=True)
    labels = (("정면 front", 0.04), ("3/4", 0.30), ("측면 side", 0.52), ("후면 back", 0.92))
    out = []
    for index, video in enumerate(videos):
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", video], capture_output=True, text=True).stdout.strip()
        duration = float(probe) if probe else 7.5
        for label, fraction in labels:
            still = work / f"body{index}-{fraction}.png"
            if not still.is_file():
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{duration * fraction:.2f}",
                                "-i", video, "-frames:v", "1", str(still)], check=False)
            if still.is_file():
                out.append((label if index == 0 else "", read_image(still)))
    return out


def detail_crops(path: str) -> list[tuple[str, Any]]:
    """Crops of the features the record calls identity anchors, taken from one large frontal frame."""
    image = read_image(path)
    face, working = identity_score.detect(image)
    if face is None:
        return []
    scale = image.shape[1] / working.shape[1]
    right_eye, left_eye, nose = (np.asarray(face[4:6]) * scale, np.asarray(face[6:8]) * scale,
                                 np.asarray(face[8:10]) * scale)
    mouth = (np.asarray(face[10:12]) * scale + np.asarray(face[12:14]) * scale) / 2
    unit = float(np.linalg.norm(left_eye - right_eye)) or 1.0

    def cut(centre, half_w: float, half_h: float):
        cx, cy = centre
        x0, x1 = int(max(0, cx - half_w * unit)), int(min(image.shape[1], cx + half_w * unit))
        y0, y1 = int(max(0, cy - half_h * unit)), int(min(image.shape[0], cy + half_h * unit))
        return image[y0:y1, x0:x1] if x1 > x0 and y1 > y0 else None

    eyes_centre = (right_eye + left_eye) / 2
    candidates = [("눈매 eyes", cut(eyes_centre, 1.15, 0.55)),
                  ("눈썹 brow", cut(eyes_centre - np.array([0, unit * 0.45]), 1.15, 0.35)),
                  ("코 nose", cut(nose, 0.60, 0.60)),
                  ("입 mouth", cut(mouth, 0.70, 0.45))]
    return [(label, crop) for label, crop in candidates if crop is not None and crop.size]


def palette(portrait: str) -> list[tuple[str, str]]:
    """Hair, iris, skin and lip as hex, sampled from the reference portrait at landmark-relative points."""
    image = read_image(portrait)
    face, working = identity_score.detect(image)
    if face is None:
        return []
    scale = image.shape[1] / working.shape[1]
    right_eye, left_eye, nose = (np.asarray(face[4:6]) * scale, np.asarray(face[6:8]) * scale,
                                 np.asarray(face[8:10]) * scale)
    mouth = (np.asarray(face[10:12]) * scale + np.asarray(face[12:14]) * scale) / 2
    unit = float(np.linalg.norm(left_eye - right_eye)) or 1.0
    eyes_centre = (right_eye + left_eye) / 2
    points = {"above_brow": eyes_centre - np.array([0, unit * 1.30]),
              "right_eye": right_eye,
              "cheek": nose + np.array([-unit * 0.85, -unit * 0.10]),
              "mouth": mouth}

    out = []
    for label, key in PALETTE_POINTS:
        cx, cy = points[key]
        # A small median patch, because a single pixel on skin or hair is noise.
        radius = max(2, int(unit * 0.06))
        patch = image[max(0, int(cy) - radius):int(cy) + radius, max(0, int(cx) - radius):int(cx) + radius]
        if patch.size == 0:
            continue
        b, g, r = (int(np.median(patch[:, :, channel])) for channel in range(3))
        out.append((label, f"#{r:02X}{g:02X}{b:02X}"))
    return out


def spec_lines(record: dict[str, Any]) -> list[tuple[str, str]]:
    dna = record.get("stable_dna", record)
    rows: list[tuple[str, str]] = []
    for key in ("shape", "eyes", "eyebrows", "nose", "lips", "jaw", "profile"):
        if key in dna.get("face", {}):
            rows.append((f"face.{key}", dna["face"][key]))
    for key in ("height_impression", "bust", "waist", "pelvis_hips", "lower_body"):
        if key in dna.get("body", {}):
            rows.append((f"body.{key}", dna["body"][key]))
    if dna.get("hair"):
        rows.append(("hair", dna["hair"]))
    if dna.get("skin"):
        rows.append(("skin", dna["skin"]))
    for mark in dna.get("distinctive_marks", []):
        rows.append(("distinctive_marks", mark))
    posture = record.get("scene_defaults", {}).get("posture")
    if posture:
        rows.append(("scene_defaults.posture", posture))
    return rows


def wrap(canvas: ImageDraw.ImageDraw, text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if canvas.textlength(trial, font=face) <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def build(args: argparse.Namespace) -> dict[str, Any]:
    set_dir = Path(args.identity_set)
    manifest = json.loads((set_dir / "identity-set.json").read_text(encoding="utf-8"))
    record = json.loads(Path(args.record).read_text(encoding="utf-8"))
    work = Path(args.work or (Path(args.out).parent / "sheet-work"))

    picked = anchors(manifest, set_dir)
    largest = max((m for m in manifest["members"]
                   if not m.get("mirrored") and m["yaw_bucket"] == "frontal"),
                  key=lambda m: m["face_pixels"][0], default=None)
    details = detail_crops(str(set_dir / largest["file"])) if largest else []
    colours = palette(args.portrait) if args.portrait else []
    bodies = body_frames(args.body_video or [], work)
    rows = spec_lines(record)

    width = 1680
    margin, gap = 28, 10
    title_font, head_font, body_font, tiny = font(30), font(19), font(15), font(13)

    anchor_w = (width - 2 * margin - (len(ANCHOR_YAWS) - 1) * gap) // len(ANCHOR_YAWS)
    anchor_h = int(anchor_w * 4 / 3)
    body_columns = max(1, len(bodies))
    body_w = (width - 2 * margin - (body_columns - 1) * gap) // body_columns if bodies else 0
    body_h = int(body_w * 4 / 3) if bodies else 0
    detail_w = (width - 2 * margin - 3 * gap) // 4 if details else 0
    detail_h = int(detail_w * 0.62) if details else 0
    swatch = 108

    spec_font_height = 21
    spec_height = 0
    scratch = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    wrapped = [(key, wrap(scratch, value, body_font, width - 2 * margin - 230)) for key, value in rows]
    for _, lines in wrapped:
        spec_height += max(spec_font_height, len(lines) * spec_font_height) + 6

    height = (margin + 96
              + 34 + anchor_h + 30
              + (34 + body_h + 30 if bodies else 0)
              + (34 + detail_h + 30 if details else 0)
              + (34 + swatch + 34 if colours else 0)
              + 34 + spec_height + margin + 40)

    sheet = Image.new("RGB", (width, height), BACKGROUND)
    canvas = ImageDraw.Draw(sheet)
    dna = record.get("stable_dna", record)
    provenance = record.get("provenance", {})
    canvas.text((margin, margin), f"{record.get('character_id', args.character)} — character sheet",
                fill=INK, font=title_font)
    canvas.text((margin, margin + 40),
                f"DNA v{record.get('version', '?')} {provenance.get('stable_dna_hash', '')}   ·   "
                f"identity set {set_dir.name}, {len(manifest['members'])} frames   ·   built {identity_score.now()[:10]}",
                fill=DIM, font=tiny)
    canvas.text((margin, margin + 60),
                "사람이 보기 위한 파생물입니다. 모델 입력이 아니고, 개별 프레임과 character.json 이 정본입니다. "
                "승인된 레퍼런스가 아닙니다.", fill=DIM, font=tiny)

    y = margin + 96

    def section(label: str, note: str = "") -> int:
        nonlocal y
        canvas.text((margin, y), label, fill=ACCENT, font=head_font)
        if note:
            canvas.text((margin + canvas.textlength(label, font=head_font) + 14, y + 5), note,
                        fill=DIM, font=tiny)
        y += 34
        return y

    section("L0 · 아이덴티티 앵커", "좌측면 → 정면 → 우측면. 반전 프레임은 제외했습니다.")
    for index, member in enumerate(picked):
        x = margin + index * (anchor_w + gap)
        if not member:
            canvas.rectangle([x, y, x + anchor_w, y + anchor_h], fill=PANEL)
            canvas.text((x + 8, y + anchor_h // 2), "없음", fill=DIM, font=tiny)
            continue
        paste(sheet, read_image(member["path"]), (x, y, anchor_w, anchor_h))
        canvas.text((x + 3, y + anchor_h + 3),
                    f"yaw {member['yaw_proxy']:+.2f}  {member['face_pixels'][0]:.0f}px",
                    fill=DIM, font=tiny)
    y += anchor_h + 30

    if bodies:
        section("L1 · 전신", "반 바퀴 회전에서 추출. 얼굴은 측정 불가 크기입니다.")
        for index, (label, image) in enumerate(bodies):
            x = margin + index * (body_w + gap)
            paste(sheet, image, (x, y, body_w, body_h))
            if label:
                canvas.text((x + 3, y + body_h + 3), label, fill=DIM, font=tiny)
        y += body_h + 30

    if details:
        section("L1 · 디테일", "기록이 정체성 앵커로 지정한 부위, 가장 큰 정면 프레임에서 크롭.")
        for index, (label, image) in enumerate(details):
            x = margin + index * (detail_w + gap)
            paste(sheet, image, (x, y, detail_w, detail_h))
            canvas.text((x + 3, y + detail_h + 3), label, fill=DIM, font=tiny)
        y += detail_h + 30

    if colours:
        section("팔레트", "레퍼런스 원본에서 실측. 숫자 없는 스와치는 재현 불가. 값은 레퍼런스 자체 조명 아래이며 중성광 기준이 아닙니다.")
        for index, (label, hex_value) in enumerate(colours):
            x = margin + index * (swatch + 150)
            canvas.rectangle([x, y, x + swatch, y + swatch], fill=hex_value, outline="#30363d")
            canvas.text((x + swatch + 12, y + 28), label, fill=INK, font=body_font)
            canvas.text((x + swatch + 12, y + 52), hex_value, fill=ACCENT, font=body_font)
        y += swatch + 34

    section("L4 · 사양", "character.json 에서 그대로 가져옵니다. 시트와 DNA 가 따로 놀 수 없게 하기 위함입니다.")
    for key, lines in wrapped:
        canvas.text((margin, y), key, fill=ACCENT, font=body_font)
        for offset, line in enumerate(lines):
            canvas.text((margin + 230, y + offset * spec_font_height), line, fill=INK, font=body_font)
        y += max(spec_font_height, len(lines) * spec_font_height) + 6

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=93)
    return {"sheet": str(out), "size": list(sheet.size), "anchors": sum(1 for m in picked if m),
            "body_frames": len(bodies), "details": len(details),
            "palette": {label: value for label, value in colours}, "spec_rows": len(rows)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--character", required=True)
    parser.add_argument("--record", help="explicit historical character record (default: configured authority)")
    parser.add_argument("--identity-set", required=True, help="directory holding identity-set.json")
    parser.add_argument("--portrait", help="reference portrait, for the palette")
    parser.add_argument("--body-video", action="append", help="body clip; repeatable")
    parser.add_argument("--work", help="scratch directory for extracted stills")
    parser.add_argument("--out", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.record:
        import character_manager as cm
        args.record = str(cm.character_record_path(args.character))
    print(json.dumps(build(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
