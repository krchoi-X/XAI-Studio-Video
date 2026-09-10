#!/usr/bin/env python3
"""Identity similarity scoring that can decide, not only rank.

Run it with the WanGP interpreter, which carries OpenCV 5 and onnxruntime:

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/identity_score.py score --prototype p.json --out r.json IMAGE...

This is the Phase 2 successor to `tools/face_identity_check.py`, which scored every image against one
reference photograph with one recogniser and one borrowed threshold. Four differences, each of them a
correction to a measurement error that showed up in the Phase 1 identity-lock batch:

* **Two independent recognisers.** OpenCV SFace plus ArcFace (`w600k_r50`) run through onnxruntime on the
  same aligned 112x112 crop SFace already produces, so the second opinion needs no extra package. Where the
  two disagree the image goes to the operator instead of being culled automatically.
* **A prototype, not a photograph.** Scores are taken against the mean of several accepted embeddings, so
  one reference image's lighting and expression stop counting as identity.
* **Yaw buckets.** A 90-degree profile scored against a frontal reference is depressed by the measurement as
  much as by drift. Frames are bucketed by a landmark-derived yaw proxy and compared within a bucket.
* **A durable record.** The scores are written as JSON next to the work, not printed and lost.

Models live in `D:\\AI_Studio\\models\\face`: YuNet detector, SFace recogniser, ArcFace recogniser.
Scores remain evidence, not a verdict - a recogniser trained on real photographs applied to synthetic faces.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image, ImageDraw, ImageFont

MODELS = Path(r"D:\AI_Studio\models\face")
DETECTOR_PATH = MODELS / "face_detection_yunet_2023mar.onnx"
SFACE_PATH = MODELS / "face_recognition_sface_2021dec.onnx"
ARCFACE_PATH = MODELS / "arcface_w600k_r50.onnx"

# Yaw proxy: the nose tip's displacement from the eye midpoint along the eye axis, in inter-ocular units.
# Boundaries measured on the Phase 1 identity-lock batch, whose shots carry a known requested angle:
# the five no-change/wardrobe shots land at 0.007-0.074, the requested 45-degree turns at 0.39-0.70, and the
# two requested 90-degree profiles at 0.74 and 1.08.
YAW_BUCKETS = (("frontal", 0.12), ("three_quarter", 0.45), ("deep_three_quarter", 0.80), ("profile", float("inf")))

RECOGNISERS = ("sface", "arcface")
_sface: Any = None
_arcface: Any = None


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sface():
    global _sface
    if _sface is None:
        _sface = cv2.FaceRecognizerSF.create(str(SFACE_PATH), "")
    return _sface


def arcface():
    """Optional: absent weights degrade to a single recogniser rather than failing the run."""
    global _arcface
    if _arcface is None and ARCFACE_PATH.is_file():
        _arcface = ort.InferenceSession(str(ARCFACE_PATH), providers=["CPUExecutionProvider"])
    return _arcface


def read(path: Path):
    """imdecode, not imread: the library holds Korean filenames that cv2.imread cannot open on Windows."""
    image = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise OSError(path)
    return image


def detect(bgr, long_edge: int = 1024):
    """Strongest face as a YuNet row plus the image it was found in. YuNet needs its input size per call."""
    height, width = bgr.shape[:2]
    scale = long_edge / max(height, width)
    working = cv2.resize(bgr, (int(width * scale), int(height * scale))) if scale < 1 else bgr
    detector = cv2.FaceDetectorYN.create(str(DETECTOR_PATH), "", (working.shape[1], working.shape[0]),
                                         score_threshold=0.6)
    _, faces = detector.detect(working)
    if faces is None or len(faces) == 0:
        return None, working
    return max(faces, key=lambda f: f[2] * f[3]), working


def yaw_proxy(face) -> float:
    """Signed nose displacement along the eye axis, in inter-ocular units. 0 is frontal; sign is the turn side."""
    right_eye, left_eye, nose = face[4:6], face[6:8], face[8:10]
    axis = np.asarray(left_eye, dtype=float) - np.asarray(right_eye, dtype=float)
    interocular = float(np.linalg.norm(axis))
    if interocular < 1e-6:
        return 0.0
    midpoint = (np.asarray(left_eye, dtype=float) + np.asarray(right_eye, dtype=float)) / 2
    return float(np.dot(np.asarray(nose, dtype=float) - midpoint, axis / interocular) / interocular)


def pitch_proxy(face) -> float:
    """Where the nose tip sits between the eye line and the mouth line, as a fraction of that distance.

    Informational only, and deliberately not used for bucketing. It does track pitch - the level face reads
    about 0.57-0.62, chin down rises to about 0.75, chin up falls to about 0.53 - but yaw confounds it, because
    turning the head also foreshortens the eye-to-mouth axis: a level face at a deep three-quarter reads 0.50,
    which is indistinguishable from a frontal face looking up. Separating the two needs more than five
    landmarks, so the number is recorded and left to the reader rather than turned into a verdict.
    """
    right_eye, left_eye, nose = face[4:6], face[6:8], face[8:10]
    right_mouth, left_mouth = face[10:12], face[12:14]
    eye_mid = (np.asarray(right_eye, dtype=float) + np.asarray(left_eye, dtype=float)) / 2
    mouth_mid = (np.asarray(right_mouth, dtype=float) + np.asarray(left_mouth, dtype=float)) / 2
    axis = mouth_mid - eye_mid
    length = float(np.linalg.norm(axis))
    if length < 1e-6:
        return 0.0
    return float(np.dot(np.asarray(nose, dtype=float) - eye_mid, axis / length) / length)


# Where the aligned 112x112 crop puts the eyes. Fixed by the alignment, so a box around each is reliable.
ALIGNED_EYES = ((38.3, 51.7), (73.5, 51.5))


def eye_aperture(aligned) -> float:
    """How far the eyes are open: the tallest run of iris-dark pixels in a box that excludes the eyebrow.

    Validated as a *closed-eye detector*, and only that. On a clip containing blinks it ranks the shut and
    half-lidded frames at the bottom (0.32-0.36) and the open ones at the top (0.46-0.50) with no mistakes.
    What it cannot do is rank among open eyes - it saturates - and it carries no information about which frame
    reads most like the character to a person: tested against 23 operator-chosen frames it scored AUC 0.50,
    which is chance. Use it to drop blinks, never to choose a favourite. It is also unreliable at a profile,
    where one eye leaves the crop.
    """
    grey = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY).astype(float)
    scores = []
    for x, y in ALIGNED_EYES:
        box = grey[int(y) - 6:int(y) + 8, int(x) - 9:int(x) + 9]
        if box.size == 0:
            continue
        spread = box.max() - box.min()
        if spread < 20:  # a flat box carries no lid/iris boundary; a relative cut there marks everything dark
            continue
        dark = box <= box.min() + 0.40 * spread
        runs = []
        for column in dark.T:
            longest = current = 0
            for value in column:
                current = current + 1 if value else 0
                longest = max(longest, current)
            runs.append(longest)
        scores.append(sorted(runs)[-3] / box.shape[0])  # third tallest column, so one stray lash cannot set it
    return round(float(np.mean(scores)), 4) if scores else 0.0


def yaw_bucket(proxy: float | None) -> str:
    if proxy is None:
        return "undetected"
    for name, limit in YAW_BUCKETS:
        if abs(proxy) <= limit:
            return name
    return "profile"


def embed(aligned) -> dict[str, list[float] | None]:
    """Both recognisers on the same aligned crop. ArcFace wants RGB scaled to [-1, 1]; SFace takes the crop."""
    out: dict[str, list[float] | None] = {"sface": None, "arcface": None}
    vector = sface().feature(aligned).flatten().astype(float)
    out["sface"] = (vector / np.linalg.norm(vector)).tolist()
    session = arcface()
    if session is not None:
        blob = cv2.dnn.blobFromImage(aligned, 1.0 / 127.5, (112, 112), (127.5, 127.5, 127.5), swapRB=True)
        vector = np.asarray(session.run(None, {session.get_inputs()[0].name: blob})[0]).flatten().astype(float)
        out["arcface"] = (vector / np.linalg.norm(vector)).tolist()
    return out


def sharpness(aligned) -> float:
    return float(cv2.Laplacian(cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())


def measure(path: Path) -> dict[str, Any]:
    """Everything derivable from one image without a reference."""
    bgr = read(path)
    face, working = detect(bgr)
    record: dict[str, Any] = {
        "path": str(path),
        "detected": face is not None,
        "yaw_proxy": None,
        "yaw_bucket": "undetected",
        "pitch_proxy": None,
        "eye_aperture": None,
        "face_pixels": None,
        "detector_score": None,
        "sharpness": None,
        "embeddings": {"sface": None, "arcface": None},
    }
    if face is None:
        return record
    aligned = sface().alignCrop(working, face)
    proxy = yaw_proxy(face)
    record.update({
        "yaw_proxy": round(proxy, 4),
        "yaw_bucket": yaw_bucket(proxy),
        "pitch_proxy": round(pitch_proxy(face), 4),
        "eye_aperture": eye_aperture(aligned),
        "face_pixels": [round(float(face[2]), 1), round(float(face[3]), 1)],
        "detector_score": round(float(face[14]), 4),
        "sharpness": round(sharpness(aligned), 2),
        "embeddings": embed(aligned),
        "aligned": aligned,
    })
    return record


def cosine(a, b) -> float:
    return float(np.dot(np.asarray(a, dtype=float), np.asarray(b, dtype=float)))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_prototype(args: argparse.Namespace) -> dict[str, Any]:
    members, sums = [], {name: [] for name in RECOGNISERS}
    for path in [Path(item).resolve() for item in args.images]:
        record = measure(path)
        if not record["detected"]:
            print(f"skipped, no face: {path}", file=sys.stderr)
            continue
        members.append({"path": str(path), "sha256": sha256_file(path), "yaw_bucket": record["yaw_bucket"],
                        "yaw_proxy": record["yaw_proxy"]})
        for name in RECOGNISERS:
            if record["embeddings"][name] is not None:
                sums[name].append(record["embeddings"][name])
    if not members:
        raise ValueError("no face was detected in any prototype member")
    embeddings = {}
    for name in RECOGNISERS:
        if sums[name]:
            mean = np.mean(np.asarray(sums[name], dtype=float), axis=0)
            embeddings[name] = (mean / np.linalg.norm(mean)).tolist()
    prototype = {"schema_version": 1, "label": args.label, "created_at": now(),
                 "members": members, "embeddings": embeddings}
    write_json(Path(args.out), prototype)
    return {"prototype": args.out, "members": len(members), "recognisers": sorted(embeddings)}


def load_calibration(path: str | None) -> dict[str, Any]:
    """Accepts the calibration document itself or a bare {yaw_bucket: {recogniser: threshold}} map."""
    if not path:
        return {"thresholds": {}, "drift_band_ceiling": None}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and "thresholds" in data:
        return {"thresholds": data["thresholds"], "drift_band_ceiling": data.get("drift_band_ceiling")}
    return {"thresholds": data if isinstance(data, dict) else {}, "drift_band_ceiling": None}


def classify(scores: dict[str, float], thresholds: dict[str, float], ceiling: float | None) -> str:
    """Three bands, not a pass/fail line.

    The calibration found no overlap between same-character and different-character pairs, and a wide empty
    gap between them. An image that lands in that gap is the failure this project keeps hitting: not another
    person, not this person either. Calling it "different" hides that, and calling it "same" is worse.
    """
    if not thresholds:
        return "uncalibrated"
    above = [value >= thresholds[name] for name, value in scores.items() if name in thresholds]
    if not above:
        return "uncalibrated"
    if all(above):
        return "same"
    if any(above):
        return "disagree"
    if ceiling is not None and all(value <= ceiling for value in scores.values()):
        return "different"
    return "drift"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def score(args: argparse.Namespace) -> dict[str, Any]:
    prototype = json.loads(Path(args.prototype).read_text(encoding="utf-8"))
    reference = prototype["embeddings"]
    calibration = load_calibration(args.thresholds)
    thresholds = calibration["thresholds"]

    items, tiles = [], []
    for path in [Path(item).resolve() for item in args.images]:
        try:
            record = measure(path)
        except OSError:
            print(f"unreadable: {path}", file=sys.stderr)
            continue
        aligned = record.pop("aligned", None)
        scores: dict[str, float] = {}
        for name in RECOGNISERS:
            vector = record["embeddings"].get(name)
            if vector is not None and reference.get(name) is not None:
                scores[name] = round(cosine(reference[name], vector), 4)
        record.pop("embeddings")
        record["scores"] = scores
        # Both recognisers are cosine on a unit sphere but not on the same scale; the useful signal is whether
        # they place the image on the same side of their own bucket threshold, not the raw gap between them.
        bucket = thresholds.get(record["yaw_bucket"], {})
        record["verdicts"] = {name: (value >= bucket[name]) for name, value in scores.items() if name in bucket}
        record["verdict"] = classify(scores, bucket, calibration["drift_band_ceiling"])
        items.append(record)
        if aligned is not None:
            tiles.append((record, aligned))

    report = {"schema_version": 1, "created_at": now(), "title": args.title,
              "calibration": calibration,
              "prototype": {"path": str(Path(args.prototype).resolve()), "label": prototype.get("label"),
                            "members": len(prototype.get("members", []))},
              "thresholds": thresholds, "items": items}
    write_json(Path(args.out), report)
    if args.sheet:
        draw_sheet(Path(args.sheet), args.title or prototype.get("label") or "identity", tiles, args.sort)
        report["sheet"] = str(Path(args.sheet).resolve())
    return {"report": args.out, "scored": len(items), "sheet": args.sheet}


def draw_sheet(out_path: Path, title: str, tiles: list[tuple[dict[str, Any], Any]], sort: str) -> None:
    """Faces at matched scale with their numbers, best first when sorting by score."""
    if not tiles:
        return
    if sort == "score":
        tiles = sorted(tiles, key=lambda pair: -(pair[0]["scores"].get("arcface")
                                                 or pair[0]["scores"].get("sface") or 0))
    elif sort == "yaw":
        tiles = sorted(tiles, key=lambda pair: pair[0]["yaw_proxy"] or 0)
    side, gap, caption, header = 220, 8, 46, 34
    columns = min(8, len(tiles))
    rows = (len(tiles) + columns - 1) // columns
    sheet = Image.new("RGB", (gap + columns * (side + gap), header + rows * (side + caption + gap)), "#202124")
    canvas = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    canvas.text((gap, 12), title, fill="white", font=font)
    for index, (record, aligned) in enumerate(tiles):
        row, column = divmod(index, columns)
        x, y = gap + column * (side + gap), header + row * (side + caption + gap)
        face = Image.fromarray(cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)).resize((side, side), Image.LANCZOS)
        sheet.paste(face, (x, y))
        colour = {"same": "#7ee787", "drift": "#d29922", "disagree": "#a371f7",
                  "different": "#ff7b72"}.get(record["verdict"], "#8b949e")
        canvas.text((x + 2, y + side + 4), Path(record["path"]).stem[:34], fill="#ffd166", font=font)
        canvas.text((x + 2, y + side + 17),
                    "  ".join(f"{name[:3]} {value:.3f}" for name, value in record["scores"].items()),
                    fill=colour, font=font)
        canvas.text((x + 2, y + side + 30), f"{record['yaw_bucket']} {record['yaw_proxy']}", fill="#8b949e", font=font)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=93)


def matrix(args: argparse.Namespace) -> dict[str, Any]:
    """Every pair, both recognisers - the input to choosing a threshold from our own faces."""
    records = []
    for path in [Path(item).resolve() for item in args.images]:
        try:
            record = measure(path)
        except OSError:
            continue
        record.pop("aligned", None)
        if record["detected"]:
            records.append(record)
    pairs = []
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            scores = {}
            for name in RECOGNISERS:
                a, b = records[i]["embeddings"].get(name), records[j]["embeddings"].get(name)
                if a is not None and b is not None:
                    scores[name] = round(cosine(a, b), 4)
            pairs.append({"a": records[i]["path"], "b": records[j]["path"], "scores": scores,
                          "buckets": [records[i]["yaw_bucket"], records[j]["yaw_bucket"]]})
    for record in records:
        record.pop("embeddings")
    report = {"schema_version": 1, "created_at": now(), "images": records, "pairs": pairs}
    write_json(Path(args.out), report)
    return {"report": args.out, "images": len(records), "pairs": len(pairs)}


def build_parser() -> argparse.ArgumentParser:
    # @list.txt expands to one argument per line: the image sets here are long and hold Korean filenames
    # that do not survive a shell round trip.
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], fromfile_prefix_chars="@")
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("prototype", help="average several accepted images into one identity prototype")
    build.add_argument("--label", required=True)
    build.add_argument("--out", required=True)
    build.add_argument("images", nargs="+")
    build.set_defaults(handler=build_prototype)

    run = sub.add_parser("score", help="score images against a prototype")
    run.add_argument("--prototype", required=True)
    run.add_argument("--out", required=True)
    run.add_argument("--sheet")
    run.add_argument("--title")
    run.add_argument("--thresholds", help="docs/identity-scoring-calibration.json, or a bare threshold map")
    run.add_argument("--sort", choices=("input", "score", "yaw"), default="score")
    run.add_argument("images", nargs="+")
    run.set_defaults(handler=score)

    pairs = sub.add_parser("matrix", help="pairwise scores over a labelled set, for calibration")
    pairs.add_argument("--out", required=True)
    pairs.add_argument("images", nargs="+")
    pairs.set_defaults(handler=matrix)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    print(json.dumps(args.handler(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
