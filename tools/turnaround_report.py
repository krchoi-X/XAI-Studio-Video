#!/usr/bin/env python3
"""Compare several turnaround harvests and derive the off-axis thresholds a frontal calibration cannot give.

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/turnaround_report.py \
        --prototype ch-lia.json --thresholds docs/identity-scoring-calibration.json \
        --out-dir REPORT HARVEST_DIR [HARVEST_DIR ...]

Three questions, each of which needs more than one clip to answer:

1. **Does one clip hold its own face while it rotates?** Frames of a continuous clip are the same person by
   construction, so their within-clip cross-bucket scores measure what the *recogniser* loses off-axis rather
   than what the model loses. That is the missing half of `docs/identity-scoring-calibration.json`, whose
   positive set is frontal-only, and it is what the proposed thresholds here are built from.

2. **Do independent rotations agree?** Two clips turning the same way from different seeds, or turning
   opposite ways, are separate acts of invention. If their profiles agree the geometry is being read out of
   the reference; if they disagree each clip is inventing a different skull, which is the Phase 1 failure
   moved from stills to video.

3. **Does any of it still resemble the master?** Every kept frame is scored against the prototype, so a clip
   that is beautifully consistent with itself and consistently somebody else cannot pass unnoticed.
"""
from __future__ import annotations

import argparse
import json
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any

import identity_score

BUCKET_ORDER = ("frontal", "three_quarter", "deep_three_quarter", "profile", "undetected")


def bucket_key(name: str) -> int:
    return BUCKET_ORDER.index(name) if name in BUCKET_ORDER else len(BUCKET_ORDER)


def summarise(values: list[float]) -> dict[str, float] | None:
    if not values:
        return None
    ordered = sorted(values)
    return {"n": len(ordered), "min": round(ordered[0], 4), "median": round(statistics.median(ordered), 4),
            "max": round(ordered[-1], 4)}


def collect(harvest_dirs: list[Path], reference: dict[str, Any]) -> list[dict[str, Any]]:
    """Re-measure the kept stills so the embeddings are in hand for every pairing this report needs."""
    frames = []
    for directory in harvest_dirs:
        harvest = json.loads((directory / "harvest.json").read_text(encoding="utf-8"))
        clip = Path(harvest["video"]).stem
        for kept in harvest["kept"]:
            path = Path(kept["path"])
            if not path.is_file():
                continue
            record = identity_score.measure(path)
            record.pop("aligned", None)
            embeddings = record.pop("embeddings")
            frames.append({
                "clip": clip, "shot": directory.name, "stem": kept["stem"], "path": str(path),
                "yaw_proxy": record["yaw_proxy"], "yaw_bucket": record["yaw_bucket"],
                "sharpness": record["sharpness"], "face_pixels": record["face_pixels"],
                "scores": {name: round(identity_score.cosine(reference[name], vector), 4)
                           for name, vector in embeddings.items()
                           if vector is not None and reference.get(name) is not None},
                "_embeddings": embeddings,
            })
    return frames


def pair_scores(a: dict[str, Any], b: dict[str, Any]) -> dict[str, float]:
    return {name: round(identity_score.cosine(a["_embeddings"][name], b["_embeddings"][name]), 4)
            for name in identity_score.RECOGNISERS
            if a["_embeddings"].get(name) is not None and b["_embeddings"].get(name) is not None}


def report(args: argparse.Namespace) -> dict[str, Any]:
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    prototype = json.loads(Path(args.prototype).read_text(encoding="utf-8"))
    calibration = identity_score.load_calibration(args.thresholds)
    frames = collect([Path(item).resolve() for item in args.harvests], prototype["embeddings"])

    for frame in frames:
        bucket = calibration["thresholds"].get(frame["yaw_bucket"], {})
        frame["verdict"] = identity_score.classify(frame["scores"], bucket, calibration["drift_band_ceiling"])

    # 1. within-clip pairs: the same person by construction, so this is the recogniser's own off-axis loss.
    within: dict[str, dict[str, list[float]]] = {}
    for shot in {frame["shot"] for frame in frames}:
        for a, b in combinations([f for f in frames if f["shot"] == shot], 2):
            key = "+".join(sorted({a["yaw_bucket"], b["yaw_bucket"]}, key=bucket_key))
            for name, value in pair_scores(a, b).items():
                within.setdefault(key, {}).setdefault(name, []).append(value)

    # 2. cross-clip pairs inside one bucket: separate acts of invention, so agreement is evidence of readout.
    across: dict[str, dict[str, list[float]]] = {}
    for a, b in combinations(frames, 2):
        if a["shot"] == b["shot"] or a["yaw_bucket"] != b["yaw_bucket"]:
            continue
        for name, value in pair_scores(a, b).items():
            across.setdefault(a["yaw_bucket"], {}).setdefault(name, []).append(value)

    # The proposed off-axis line comes only from pairs where BOTH frames sit in the same bucket - the worst
    # score two frames of one person produced while both were at that angle. Mixed-bucket pairs are excluded
    # deliberately: frontal-to-profile pairs of the same person fall to 0.07, so letting them set the profile
    # threshold would produce a line that accepts anything. The corollary is that a profile can only ever be
    # scored against a profile reference, never against the frontal prototype.
    proposed = {}
    for key, recognisers in within.items():
        if "+" in key or key in calibration["thresholds"] or key == "undetected":
            continue
        proposed[key] = {name: round(min(values), 2) for name, values in recognisers.items()}

    # Clip admission. A profile cannot be judged against a frontal prototype, but a clip is one continuous
    # take, so its profile frames are the same person as its own frontal frames whatever the angle costs the
    # recogniser. The decision therefore runs through the frontal bucket: admit the clip on its frontal frames,
    # and the rest of the clip inherits. `continuity` is the weakest same-bucket pair inside the clip - if the
    # face changed mid-take that is where it shows.
    per_shot = {}
    for shot in sorted({frame["shot"] for frame in frames}):
        members = [frame for frame in frames if frame["shot"] == shot]
        frontal = [frame for frame in members if frame["yaw_bucket"] == "frontal"]
        continuity = [value for a, b in combinations(members, 2) if a["yaw_bucket"] == b["yaw_bucket"]
                      for value in pair_scores(a, b).values()]
        admission = max((frame["scores"] for frame in frontal),
                        key=lambda s: s.get("arcface") or 0, default={})
        per_shot[shot] = {
            "frames": len(members),
            "buckets": sorted({frame["yaw_bucket"] for frame in members}, key=bucket_key),
            "admission_scores": admission,
            "admission_verdict": identity_score.classify(
                admission, calibration["thresholds"].get("frontal", {}), calibration["drift_band_ceiling"]),
            "weakest_same_bucket_pair": round(min(continuity), 4) if continuity else None,
            "face_pixels_median": round(statistics.median(
                [frame["face_pixels"][0] for frame in members if frame["face_pixels"]]), 1),
        }

    document = {
        "schema_version": 1, "created_at": identity_score.now(),
        "prototype": {"path": str(Path(args.prototype).resolve()), "label": prototype.get("label")},
        "calibration": calibration,
        "shots": per_shot,
        "within_clip_same_person": {key: {name: summarise(values) for name, values in recognisers.items()}
                                    for key, recognisers in sorted(within.items())},
        "across_clip_same_bucket": {key: {name: summarise(values) for name, values in recognisers.items()}
                                    for key, recognisers in sorted(across.items(), key=lambda kv: bucket_key(kv[0]))},
        "proposed_offaxis_thresholds": proposed,
        "frames": [{key: value for key, value in frame.items() if not key.startswith("_")} for frame in frames],
    }
    identity_score.write_json(out_dir / "turnaround-report.json", document)

    if args.sheet:
        tiles = []
        for frame in sorted(frames, key=lambda f: (bucket_key(f["yaw_bucket"]), f["shot"])):
            measurement = identity_score.measure(Path(frame["path"]))
            aligned = measurement.pop("aligned", None)
            if aligned is not None:
                tiles.append((dict(frame, path=frame["stem"]), aligned))
        identity_score.draw_sheet(Path(args.sheet), args.title or "turnaround harvest", tiles, "input")

    return {"report": str(out_dir / "turnaround-report.json"), "frames": len(frames),
            "shots": sorted(per_shot), "proposed_offaxis_thresholds": proposed, "sheet": args.sheet}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], fromfile_prefix_chars="@")
    parser.add_argument("--prototype", required=True)
    parser.add_argument("--thresholds")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--title")
    parser.add_argument("harvests", nargs="+", help="directories written by video_frame_harvest.py")
    return parser


def main() -> int:
    print(json.dumps(report(build_parser().parse_args()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
