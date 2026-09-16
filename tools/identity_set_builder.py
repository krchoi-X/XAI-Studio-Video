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
from character_sets import reserve_destination, write_set_context, publish_manifest

ACCEPTABLE = {"same", "disagree"}

# A full side profile measures ~1.0 on the yaw proxy; past this the landmarks are not on a
# readable face. Measured: a clean profile peaks at 1.02, while a frame turned on past profile
# toward the back of the head measured 1.17 with the far eye and mouth already hidden.
MAX_YAW = 1.15


def build(args: argparse.Namespace) -> dict[str, Any]:
    # Reservation is deliberately first: a failed run leaves its incomplete folder
    # for inspection and can never erase a prior immutable set.
    out_dir = reserve_destination("identity", args.character, args.out_dir)
    report_path = Path(args.report)
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)

    verdicts = {name: shot["admission_verdict"] for name, shot in report["shots"].items()}
    admitted = {name for name, verdict in verdicts.items()
                if verdict in (ACCEPTABLE if args.include_disagree else {"same"})}
    if args.only:
        admitted &= set(args.only)
    if not admitted:
        raise ValueError("no clip was admitted; nothing to assemble")

    members = []
    dropped = []
    output_names: set[str] = set()
    for frame in report["frames"]:
        if frame["shot"] not in admitted:
            continue
        source = Path(frame["path"])
        if not source.is_file():
            raise FileNotFoundError(f"admitted identity frame is missing: {source}")
        # A full side profile measures about 1.0 on this proxy, so anything past MAX_YAW is the detector
        # placing landmarks on a head that is turned too far to read - a back-of-head frame in a clip that
        # rotates past profile, or an outright landmark failure. Both are useless as identity references and
        # would otherwise be counted as coverage of the side they are nominally on.
        if abs(frame["yaw_proxy"] or 0) > MAX_YAW:
            dropped.append({"shot": frame["shot"], "yaw_proxy": frame["yaw_proxy"],
                            "face_pixels": frame["face_pixels"], "path": str(source),
                            "reason": f"|yaw_proxy| > {MAX_YAW}: turned past profile or landmark failure"})
            continue
        side = "right" if (frame["yaw_proxy"] or 0) > 0 else "left"
        name = (f"{args.character}-{frame['yaw_bucket']}-{side}-{abs(frame['yaw_proxy']):.2f}"
                f"-{frame['shot']}-{source.stem[-6:]}.png")
        if Path(name).name != name or ".." in Path(name).parts:
            raise ValueError(f"unsafe identity member name from report: {name}")
        folded = name.casefold()
        if folded in output_names:
            raise ValueError(f"duplicate immutable identity member name: {name}")
        output_names.add(folded)
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
        "dropped_frames": dropped,
        "members": sorted(members, key=lambda member: member["yaw_proxy"] or 0),
    }
    flipped = balance_by_flip(args, out_dir, members)
    members.extend(flipped)
    if flipped:
        manifest["mirrored_frames"] = MIRROR_NOTE
    manifest["members"] = sorted(members, key=lambda member: member["yaw_proxy"] or 0)
    if args.sheet:
        if Path(args.sheet).exists():
            raise FileExistsError(f"immutable contact sheet already exists: {args.sheet}")
        draw(Path(args.sheet), out_dir, manifest, args.title or f"{args.character} identity set")
    write_set_context(
        out_dir, character_id=args.character, producer=Path(__file__), arguments=vars(args),
        source_manifest=report_path, source_bytes=report_bytes,
        output_files=[out_dir / member["file"] for member in members],
    )
    publish_manifest(out_dir / "identity-set.json", manifest)

    coverage: dict[str, int] = {}
    for member in members:
        coverage[f"{member['yaw_bucket']} {member['side']}"] = coverage.get(
            f"{member['yaw_bucket']} {member['side']}", 0) + 1
    return {"out_dir": str(out_dir), "clips": sorted(admitted), "frames": len(members),
            "dropped_frames": len(dropped),
            "coverage": dict(sorted(coverage.items())), "sheet": args.sheet}


MIRROR_NOTE = (
    "Some members are horizontal flips of frames from the opposite side, not separately generated views. "
    "They are marked `mirrored: true` and name the frame they came from. This is a legitimate substitute "
    "only while the character record carries no left/right asymmetric feature: check `distinctive_marks` "
    "and hair parting before relying on a mirrored frame, and never mirror a frame that shows an asymmetric "
    "mark. Mirroring also flips real facial asymmetry, so a mirrored frame is a usable reference for pose "
    "and structure but is not evidence about this character's own asymmetry."
)


def balance_by_flip(args: argparse.Namespace, out_dir: Path,
                    members: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Fill a one-sided bucket with horizontal flips of the other side's best frames.

    Only the buckets named on the command line are touched, and only up to parity - this never produces more
    mirrored frames than there are real ones on the full side, and never exceeds --max-flips per bucket.
    """
    if not args.balance_by_flip:
        return []
    import cv2
    import numpy as np

    added: list[dict[str, Any]] = []
    for bucket in args.balance_by_flip:
        sides = {"left": [m for m in members if m["yaw_bucket"] == bucket and m["side"] == "left"],
                 "right": [m for m in members if m["yaw_bucket"] == bucket and m["side"] == "right"]}
        thin, full = sorted(sides, key=lambda side: len(sides[side]))
        want = min(len(sides[full]) - len(sides[thin]), args.max_flips)
        if want <= 0:
            continue
        best = sorted(sides[full], key=lambda m: (-(m["scores_vs_frontal_prototype"].get("arcface") or 0),
                                                  -(m["face_pixels"][0])))[:want]
        for source in best:
            name = f"{args.character}-{bucket}-{thin}-{abs(source['yaw_proxy']):.2f}-mirrored-{source['clip']}.png"
            if Path(name).name != name or ".." in Path(name).parts:
                raise ValueError(f"unsafe mirrored member name: {name}")
            if (out_dir / name).exists():
                raise FileExistsError(f"duplicate immutable mirrored member: {name}")
            image = cv2.imdecode(np.fromfile(str(out_dir / source["file"]), dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imencode(".png", cv2.flip(image, 1))[1].tofile(str(out_dir / name))
            added.append(dict(source, file=name, side=thin, yaw_proxy=-source["yaw_proxy"], mirrored=True,
                              mirrored_from=source["file"], source_side=full))
    return added


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
        canvas.text((x + 2, y + height + 15),
                    ("MIRRORED " if member.get("mirrored") else "") + f"{member['clip'][:18]}",
                    fill="#f08080" if member.get("mirrored") else "#8b949e", font=font)
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path, quality=91)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--report", required=True, help="turnaround-report.json")
    parser.add_argument("--out-dir", help="new immutable set directory; optional with active shared Library")
    parser.add_argument("--character", required=True)
    parser.add_argument("--actor", default="claude")
    parser.add_argument("--sheet")
    parser.add_argument("--title")
    parser.add_argument("--include-disagree", action="store_true",
                        help="also take clips where the two recognisers split on the frontal frame")
    parser.add_argument("--only", nargs="+", help="restrict to these clip names")
    parser.add_argument("--balance-by-flip", nargs="+", metavar="BUCKET", default=[],
                        help="fill these buckets' thin side with horizontal flips of the other "
                             "side; members are marked `mirrored`. Read MIRROR_NOTE first.")
    parser.add_argument("--max-flips", type=int, default=12,
                        help="cap on mirrored frames added per bucket (default 12)")
    return parser


def main() -> int:
    print(json.dumps(build(build_parser().parse_args()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
