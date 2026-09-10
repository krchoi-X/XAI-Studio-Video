#!/usr/bin/env python3
"""Assemble the frames of admitted clips into one character identity set.

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/identity_set_builder.py \
        --report REPORT/turnaround-report.json --out-dir LIBRARY/imports/derived/identity-set-YYYYMMDD \
        --character ch-lia --sheet REPORT/identity-set-sheet.jpg

Admission is decided per clip, not per frame, and `turnaround_report.py` has already done it: a clip is
admitted on its frontal frames against the frontal prototype, and the rest of that clip is the same person by
temporal continuity. This tool takes the clips whose admission verdict is good enough, copies their frames
out under names that carry the angle, and writes a manifest recording why each frame is in the set.

The manifest states the review state explicitly. Nothing here is an approved reference: promoting any of it
to `character.json.approved_references` is a human decision with its own workflow.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import identity_score

ACCEPTABLE = {"same", "disagree"}


def build(args: argparse.Namespace) -> dict[str, Any]:
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    verdicts = {name: shot["admission_verdict"] for name, shot in report["shots"].items()}
    admitted = {name for name, verdict in verdicts.items()
                if verdict in (ACCEPTABLE if args.include_disagree else {"same"})}
    if args.only:
        admitted &= set(args.only)
    if not admitted:
        raise ValueError("no clip was admitted; nothing to assemble")

    for stale in out_dir.glob("*.png"):
        stale.unlink()

    members = []
    for frame in report["frames"]:
        if frame["shot"] not in admitted:
            continue
        source = Path(frame["path"])
        if not source.is_file():
            continue
        side = "right" if (frame["yaw_proxy"] or 0) > 0 else "left"
        name = (f"{args.character}-{frame['yaw_bucket']}-{side}-{abs(frame['yaw_proxy']):.2f}"
                f"-{frame['shot']}-{source.stem[-6:]}.png")
        shutil.copyfile(source, out_dir / name)
        members.append({"file": name, "clip": frame["shot"], "yaw_bucket": frame["yaw_bucket"],
                        "yaw_proxy": frame["yaw_proxy"], "side": side, "sharpness": frame["sharpness"],
                        "face_pixels": frame["face_pixels"],
                        "scores_vs_frontal_prototype": frame["scores"], "source": str(source)})

    manifest = {
        "schema_version": 1, "created_at": identity_score.now(), "character_id": args.character,
        "created_by": args.actor, "review_state": "needs_review",
        "review_note": ("No human has approved any frame here. This set is not `approved_references` and "
                        "promoting any of it is a separate, explicit operator decision."),
        "admission": {
            "rule": ("A clip is admitted on its frontal frames against the frontal prototype; its off-axis "
                     "frames inherit that admission through temporal continuity within the same take. Their "
                     "low scores against the frontal prototype are an artefact of comparing across yaw, "
                     "measured at 0.07 for the same person in the same clip, and are not drift."),
            "accepted_verdicts": sorted(ACCEPTABLE if args.include_disagree else {"same"}),
            "clips": {name: {"verdict": verdicts[name],
                             "admission_scores": report["shots"][name]["admission_scores"]}
                      for name in sorted(admitted)},
        },
        "prototype": report["prototype"], "calibration": report["calibration"],
        "members": sorted(members, key=lambda member: member["yaw_proxy"] or 0),
    }
    identity_score.write_json(out_dir / "identity-set.json", manifest)

    coverage: dict[str, int] = {}
    for member in members:
        coverage[f"{member['yaw_bucket']} {member['side']}"] = coverage.get(
            f"{member['yaw_bucket']} {member['side']}", 0) + 1
    if args.sheet:
        draw(Path(args.sheet), out_dir, manifest, args.title or f"{args.character} identity set")
    return {"out_dir": str(out_dir), "clips": sorted(admitted), "frames": len(members),
            "coverage": dict(sorted(coverage.items())), "sheet": args.sheet}


def draw(sheet_path: Path, out_dir: Path, manifest: dict[str, Any], title: str) -> None:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

    members = manifest["members"]
    width, height, pad, caption, header = 196, 238, 5, 26, 30
    columns = min(10, max(1, len(members)))
    rows = (len(members) + columns - 1) // columns
    sheet = Image.new("RGB", (pad + columns * (width + pad), header + rows * (height + caption + pad)), "#202124")
    canvas = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    canvas.text((pad, 9), f"{title} - {len(members)} frames from {len(manifest['admission']['clips'])} "
                          f"admitted clips, left profile to right profile", fill="white", font=font)
    for index, member in enumerate(members):
        row, column = divmod(index, columns)
        x, y = pad + column * (width + pad), header + row * (height + caption + pad)
        image = cv2.imdecode(np.fromfile(str(out_dir / member["file"]), dtype=np.uint8), cv2.IMREAD_COLOR)
        sheet.paste(Image.fromarray(cv2.cvtColor(cv2.resize(image, (width, height)), cv2.COLOR_BGR2RGB)), (x, y))
        canvas.text((x + 2, y + height + 3), f"{member['yaw_bucket'][:12]} {member['yaw_proxy']:+.2f}",
                    fill="#ffd166", font=font)
        canvas.text((x + 2, y + height + 15), f"{member['clip'][:18]}  sharp {member['sharpness']:.0f}",
                    fill="#8b949e", font=font)
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path, quality=91)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--report", required=True, help="turnaround-report.json")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--character", required=True)
    parser.add_argument("--actor", default="claude")
    parser.add_argument("--sheet")
    parser.add_argument("--title")
    parser.add_argument("--include-disagree", action="store_true",
                        help="also take clips where the two recognisers split on the frontal frame")
    parser.add_argument("--only", nargs="+", help="restrict to these clip names")
    return parser


def main() -> int:
    print(json.dumps(build(build_parser().parse_args()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
