#!/usr/bin/env python3
"""Check whether a folder of candidate reference images is actually one person, before spending GPU on it.

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/reference_set_check.py \
        --source INBOX/Hae-Won --out REPORT/hae-won --label ch-jung-haewon

The workflow this serves: the operator generates images they like elsewhere, and they become the references a
video model is conditioned on. If two of them are not the same face, that disagreement is passed straight into
every clip - and it is invisible until hours of rendering later. Measuring first costs nothing.

Two rules make the reading honest, both learned the hard way here:

* **Only same-bucket pairs count.** The same person photographed frontally and in profile scores as low as
  0.07, so a cross-angle number says nothing about identity. Cross-angle pairs are printed but never judged.
* **A closed eye or a tiny face depresses the score.** Both are flagged per image so a low pair can be read as
  a measurement problem rather than a different face.

It also reports what a reference set needs and often lacks: coverage of both sides of the face, a usable
frontal, enough face pixels, and no duplicates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import identity_score

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
SMALL_FACE = 220          # below this the recogniser starts losing detail it needs
CLOSED_EYE = 0.30         # validated blink cut, frontal and three-quarter only


def measure_all(source: Path) -> list[dict[str, Any]]:
    records, seen = [], {}
    for path in sorted(p for p in source.rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        record = identity_score.measure(path)
        aligned = record.pop("aligned", None)
        embeddings = record.pop("embeddings")
        records.append({
            "file": str(path.relative_to(source)), "path": str(path), "sha256": digest[:16],
            "duplicate_of": seen.get(digest), "group": path.parent.name,
            "detected": record["detected"], "yaw_proxy": record["yaw_proxy"],
            "yaw_bucket": record["yaw_bucket"], "eye_aperture": record["eye_aperture"],
            "face_pixels": record["face_pixels"], "sharpness": record["sharpness"],
            "_embeddings": embeddings, "_aligned": aligned,
        })
        seen.setdefault(digest, str(path.relative_to(source)))
    return records


def warnings_for(record: dict[str, Any]) -> list[str]:
    out = []
    if not record["detected"]:
        return ["no face detected"]
    if record["duplicate_of"]:
        out.append(f"identical to {record['duplicate_of']}")
    if record["face_pixels"] and record["face_pixels"][0] < SMALL_FACE:
        out.append(f"small face ({record['face_pixels'][0]:.0f} px)")
    if (record["yaw_bucket"] in {"frontal", "three_quarter"}
            and (record["eye_aperture"] or 0) < CLOSED_EYE):
        out.append("eyes shut or half-lidded")
    return out


def check(args: argparse.Namespace) -> dict[str, Any]:
    source = Path(args.source).resolve()
    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    calibration = identity_score.load_calibration(args.thresholds)
    records = measure_all(source)
    usable = [r for r in records if r["detected"] and not r["duplicate_of"]]

    pairs = []
    for a, b in combinations(usable, 2):
        scores = {name: round(identity_score.cosine(a["_embeddings"][name], b["_embeddings"][name]), 4)
                  for name in identity_score.RECOGNISERS
                  if a["_embeddings"].get(name) and b["_embeddings"].get(name)}
        comparable = a["yaw_bucket"] == b["yaw_bucket"]
        verdict = (identity_score.classify(scores, calibration["thresholds"].get(a["yaw_bucket"], {}),
                                           calibration["drift_band_ceiling"])
                   if comparable else "not comparable across angles")
        pairs.append({"a": a["file"], "b": b["file"], "buckets": [a["yaw_bucket"], b["yaw_bucket"]],
                      "same_bucket": comparable, "scores": scores, "verdict": verdict,
                      "groups": [a["group"], b["group"]]})

    judged = [p for p in pairs if p["same_bucket"]]
    coverage: dict[str, int] = {}
    for r in usable:
        side = "right" if (r["yaw_proxy"] or 0) > 0 else "left"
        coverage[f"{r['yaw_bucket']} {side}"] = coverage.get(f"{r['yaw_bucket']} {side}", 0) + 1

    gaps = []
    if not any(r["yaw_bucket"] == "frontal" and not warnings_for(r) for r in usable):
        gaps.append("no clean frontal: a set without one cannot anchor identity for any later comparison")
    sides = {"right" if (r["yaw_proxy"] or 0) > 0 else "left" for r in usable}
    if len(sides) < 2:
        gaps.append(f"every image turns the same way ({sides.pop()}); the other side of the face is missing")
    if not judged:
        gaps.append("no two images share a yaw bucket, so nothing here can be checked for identity at all")

    report = {
        "schema_version": 1, "created_at": identity_score.now(), "source": str(source), "label": args.label,
        "calibration": calibration,
        "counts": {"files": len(records), "with_face": sum(r["detected"] for r in records),
                   "duplicates": sum(bool(r["duplicate_of"]) for r in records), "usable": len(usable),
                   "comparable_pairs": len(judged)},
        "coverage": dict(sorted(coverage.items())),
        "gaps": gaps,
        "images": [{k: v for k, v in r.items() if not k.startswith("_")} | {"warnings": warnings_for(r)}
                   for r in records],
        "pairs": sorted(pairs, key=lambda p: (not p["same_bucket"],
                                              -(p["scores"].get("arcface") or 0))),
    }
    identity_score.write_json(out_dir / "reference-set-check.json", report)
    if args.sheet:
        draw(Path(args.sheet), usable, args.label)
    return {"report": str(out_dir / "reference-set-check.json"), **report["counts"],
            "coverage": report["coverage"], "gaps": gaps,
            "same_bucket_verdicts": {p["verdict"]: sum(1 for q in judged if q["verdict"] == p["verdict"])
                                     for p in judged}}


def draw(sheet_path: Path, records: list[dict[str, Any]], label: str) -> None:
    """Every face at the same scale and in turn order: the eye reads a set faster than a table does."""
    records = sorted(records, key=lambda r: r["yaw_proxy"] or 0)
    side, gap, caption, header = 190, 6, 40, 26
    columns = min(10, max(1, len(records)))
    rows = (len(records) + columns - 1) // columns
    sheet = Image.new("RGB", (gap + columns * (side + gap), header + rows * (side + caption + gap)), "#202124")
    canvas = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    canvas.text((gap, 8), f"{label}: every face at matched scale, ordered by how far the head is turned",
                fill="white", font=font)
    for index, record in enumerate(records):
        row, column = divmod(index, columns)
        x, y = gap + column * (side + gap), header + row * (side + caption + gap)
        if record["_aligned"] is not None:
            sheet.paste(Image.fromarray(cv2.cvtColor(cv2.resize(record["_aligned"], (side, side)),
                                                     cv2.COLOR_BGR2RGB)), (x, y))
        canvas.text((x + 2, y + side + 3), Path(record["file"]).stem[:28], fill="#ffd166", font=font)
        canvas.text((x + 2, y + side + 15), f"yaw {record['yaw_proxy']:+.2f}  {record['yaw_bucket'][:12]}",
                    fill="#8b949e", font=font)
        issues = warnings_for(record)
        canvas.text((x + 2, y + side + 27), issues[0][:30] if issues else
                    f"face {record['face_pixels'][0]:.0f}px", fill="#ff7b72" if issues else "#8b949e", font=font)
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path, quality=92)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--thresholds",
                        default=str(Path(__file__).resolve().parents[1] / "docs" / "identity-scoring-calibration.json"))
    return parser


def main() -> int:
    print(json.dumps(check(build_parser().parse_args()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
