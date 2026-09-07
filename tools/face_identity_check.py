#!/usr/bin/env python3
"""Matched face-crop sheet plus an identity-similarity score against a reference.

Run it with the WanGP interpreter, which carries OpenCV 5:

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/face_identity_check.py <spec.json> <out.jpg>

The spec is {"title": str, "cells": [{"path": str, "label": str}, ...]}; the first cell is the reference.
Models live in D:/AI_Studio/models/face (YuNet detector, SFace recogniser, ~37 MB, from the OpenCV zoo).

Purpose: cull an identity set without judging by eye alone. Scores are relative evidence - a face recogniser
trained on real photographs, applied to synthetic faces, and degraded by profile views. Read the ranking and
the gaps, not the pass/fail line.

Detection: OpenCV YuNet. Recognition: OpenCV SFace, cosine similarity against the first cell (the master).
The score is a proxy trained on real faces and is evidence, not a verdict - the operator's eye decides.
OpenCV's own guidance treats cosine >= 0.363 as "same identity" for SFace.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

MODELS = Path(r"D:\AI_Studio\models\face")
DETECTOR_PATH = MODELS / "face_detection_yunet_2023mar.onnx"
RECOGNIZER_PATH = MODELS / "face_recognition_sface_2021dec.onnx"
SAME_IDENTITY_COSINE = 0.363

recognizer = cv2.FaceRecognizerSF.create(str(RECOGNIZER_PATH), "")


def read(path: Path):
    image = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise OSError(path)
    return image


def detect(bgr):
    """Strongest face as a YuNet row, or None. YuNet needs its input size set before each detect call."""
    height, width = bgr.shape[:2]
    scale = 640 / max(height, width)
    small = cv2.resize(bgr, (int(width * scale), int(height * scale))) if scale < 1 else bgr
    detector = cv2.FaceDetectorYN.create(str(DETECTOR_PATH), "", (small.shape[1], small.shape[0]),
                                         score_threshold=0.6)
    _, faces = detector.detect(small)
    if faces is None or len(faces) == 0:
        return None, None
    face = max(faces, key=lambda f: f[2] * f[3])
    return face, (small if scale < 1 else bgr)


def crop_and_embed(path: Path, size=(340, 400), pad=0.9):
    bgr = read(path)
    face, working = detect(bgr)
    embedding = None
    if face is None:
        height, width = bgr.shape[:2]
        side = int(min(width, height) * 0.45)
        cx, cy, detected = width // 2, int(height * 0.28), False
    else:
        aligned = recognizer.alignCrop(working, face)
        embedding = recognizer.feature(aligned).flatten()
        x, y, w, h = face[:4]
        cx, cy = int(x + w / 2), int(y + h * 0.45)
        side, detected = int(max(w, h) * (1 + pad)), True
        bgr = working
    half = side // 2
    height, width = bgr.shape[:2]
    crop = bgr[max(0, cy - half):min(height, cy + half), max(0, cx - half):min(width, cx + half)]
    image = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    image.thumbnail(size, Image.LANCZOS)
    tile = Image.new("RGB", size, "#111111")
    tile.paste(image, ((size[0] - image.width) // 2, (size[1] - image.height) // 2))
    return tile, detected, embedding


def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main() -> int:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out_path = Path(sys.argv[2])
    TW, TH, gap, cap, hdr = 340, 400, 10, 40, 34
    cols = min(4, len(spec["cells"]))
    rows = (len(spec["cells"]) + cols - 1) // cols
    sheet = Image.new("RGB", (gap + cols * (TW + gap), hdr + rows * (TH + cap + gap)), "#202124")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((gap, 12), spec["title"], fill="white", font=font)

    reference = None
    report = []
    for index, cell in enumerate(spec["cells"]):
        row, col = divmod(index, cols)
        x, y = gap + col * (TW + gap), hdr + row * (TH + cap + gap)
        try:
            tile, detected, embedding = crop_and_embed(Path(cell["path"]))
        except OSError:
            continue
        sheet.paste(tile, (x, y))
        if index == 0:
            reference = embedding
            score_text, colour = "reference", "#7ee787"
        elif embedding is not None and reference is not None:
            score = cosine(reference, embedding)
            verdict = "same" if score >= SAME_IDENTITY_COSINE else "different"
            score_text = f"cosine {score:.3f}  ({verdict})"
            colour = "#7ee787" if score >= SAME_IDENTITY_COSINE else "#ff7b72"
            report.append({"label": cell["label"], "cosine": round(score, 4), "verdict": verdict})
        else:
            score_text, colour = "no face detected", "#8b949e"
        draw.text((x + 2, y + TH + 6), cell["label"][:52], fill="#ffd166", font=font)
        draw.text((x + 2, y + TH + 21), score_text, fill=colour, font=font)
    sheet.save(out_path, quality=93)
    print(json.dumps({"sheet": str(out_path), "scores": report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
