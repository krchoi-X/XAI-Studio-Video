#!/usr/bin/env python3
"""Harvest identity reference stills out of a turnaround clip.

Run it with the WanGP interpreter, which carries OpenCV 5 and onnxruntime:

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/video_frame_harvest.py \
        --video CLIP.mp4 --prototype ch-lia.json --out-dir DIR

Why this exists: a front photograph does not contain the profile, and both Krea2 edit paths invent a different
skull every time they are asked for one. A video does not - temporal consistency carries one face continuously
through the intermediate angles. So the clip is not the deliverable; the *frames* are, and picking them is the
work. Every frame is detected, bucketed by the yaw proxy from `identity_score`, ranked inside its bucket by
identity score and then by focus, and the survivors are written out as stills with a durable record.

The pairwise block in the report is deliberate. Frames of one continuous clip are the same person by
construction, so their cross-bucket scores are the only same-identity profile measurements this project can
make without a human labelling them - which is what a frontal-only calibration is missing.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import identity_score

FFMPEG_FALLBACK = Path(r"D:\AI\WanGP\ffmpeg_bins\ffmpeg.exe")
FFPROBE_FALLBACK = Path(r"D:\AI\WanGP\ffmpeg_bins\ffprobe.exe")


def tool(name: str, fallback: Path) -> str:
    return name if shutil.which(name) else str(fallback)


def probe(video: Path) -> dict[str, Any]:
    result = subprocess.run(
        [tool("ffprobe", FFPROBE_FALLBACK), "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,nb_frames,avg_frame_rate,duration",
         "-of", "json", str(video)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    stream = json.loads(result.stdout)["streams"][0]
    numerator, _, denominator = (stream.get("avg_frame_rate") or "0/1").partition("/")
    fps = float(numerator) / float(denominator) if float(denominator or 0) else 0.0
    return {"width": stream.get("width"), "height": stream.get("height"),
            "frames": int(stream["nb_frames"]) if stream.get("nb_frames") else None,
            "fps": round(fps, 3), "duration": float(stream["duration"]) if stream.get("duration") else None}


def extract(video: Path, target: Path, every: int) -> list[Path]:
    """PNG, not JPEG: these frames become identity references and may be re-encoded several more times."""
    target.mkdir(parents=True, exist_ok=True)
    command = [tool("ffmpeg", FFMPEG_FALLBACK), "-v", "error", "-y", "-i", str(video)]
    if every > 1:
        command += ["-vf", f"select=not(mod(n\\,{every}))", "-vsync", "0", "-frame_pts", "1"]
    command += [str(target / "frame-%05d.png")]
    subprocess.run(command, check=True, capture_output=True)
    return sorted(target.glob("frame-*.png"))


def harvest(args: argparse.Namespace) -> dict[str, Any]:
    video = Path(args.video).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    prototype = json.loads(Path(args.prototype).read_text(encoding="utf-8"))
    reference = prototype["embeddings"]
    calibration = identity_score.load_calibration(args.thresholds)
    thresholds = calibration["thresholds"]
    media = probe(video)

    scratch = Path(tempfile.mkdtemp(prefix="frame-harvest-"))
    try:
        frames = extract(video, scratch, args.every)
        measured = []
        for index, frame in enumerate(frames):
            record = identity_score.measure(frame)
            aligned = record.pop("aligned", None)
            embeddings = record.pop("embeddings")
            if not record["detected"]:
                continue
            record["frame_index"] = index * args.every
            record["scores"] = {name: round(identity_score.cosine(reference[name], vector), 4)
                                for name, vector in embeddings.items()
                                if vector is not None and reference.get(name) is not None}
            record["_embeddings"] = embeddings
            record["_aligned"] = aligned
            record["_source"] = frame
            measured.append(record)

        def rank(record: dict[str, Any]) -> tuple:
            # Identity first, focus as the tie-break: a sharp frame of the wrong face is worthless, but among
            # frames that hold the identity the sharp one is the better reference and the better training image.
            best = record["scores"].get("arcface") or record["scores"].get("sface") or 0.0
            return (-round(best, 3), -(record["sharpness"] or 0.0))

        buckets: dict[str, list[dict[str, Any]]] = {}
        for record in measured:
            buckets.setdefault(record["yaw_bucket"], []).append(record)
        kept = []
        for name in sorted(buckets):
            for position, record in enumerate(sorted(buckets[name], key=rank)[:args.per_bucket]):
                stem = f"{video.stem}-{name}-{position + 1:02d}-f{record['frame_index']:05d}"
                destination = out_dir / f"{stem}.png"
                shutil.copyfile(record["_source"], destination)
                record["path"] = str(destination)
                record["stem"] = stem
                kept.append(record)

        pairs = []
        for i in range(len(kept)):
            for j in range(i + 1, len(kept)):
                scores = {}
                for name in identity_score.RECOGNISERS:
                    a, b = kept[i]["_embeddings"].get(name), kept[j]["_embeddings"].get(name)
                    if a is not None and b is not None:
                        scores[name] = round(identity_score.cosine(a, b), 4)
                pairs.append({"a": kept[i]["stem"], "b": kept[j]["stem"], "scores": scores,
                              "buckets": [kept[i]["yaw_bucket"], kept[j]["yaw_bucket"]]})

        tiles = []
        for record in kept:
            bucket_thresholds = thresholds.get(record["yaw_bucket"], {})
            record["verdicts"] = {name: (value >= bucket_thresholds[name])
                                  for name, value in record["scores"].items() if name in bucket_thresholds}
            record["verdict"] = identity_score.classify(record["scores"], bucket_thresholds,
                                                        calibration["drift_band_ceiling"])
            tiles.append((record, record.pop("_aligned")))
            record.pop("_embeddings")
            record.pop("_source")

        report = {
            "schema_version": 1, "created_at": identity_score.now(), "video": str(video), "media": media,
            "sampling": {"every": args.every, "extracted": len(frames), "with_face": len(measured),
                         "kept_per_bucket": args.per_bucket},
            "prototype": {"path": str(Path(args.prototype).resolve()), "label": prototype.get("label")},
            "calibration": calibration,
            "bucket_counts": {name: len(items) for name, items in sorted(buckets.items())},
            "kept": kept, "pairs": pairs,
        }
        identity_score.write_json(out_dir / "harvest.json", report)
        if args.sheet:
            identity_score.draw_sheet(Path(args.sheet), args.title or f"{video.stem} harvest", tiles, "yaw")
        return {"out_dir": str(out_dir), "extracted": len(frames), "with_face": len(measured),
                "kept": len(kept), "buckets": report["bucket_counts"], "sheet": args.sheet}
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--video", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--prototype", required=True)
    parser.add_argument("--thresholds")
    parser.add_argument("--every", type=int, default=1, help="sample every Nth frame")
    parser.add_argument("--per-bucket", type=int, default=4, help="stills to keep per yaw bucket")
    parser.add_argument("--sheet")
    parser.add_argument("--title")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    print(json.dumps(harvest(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
