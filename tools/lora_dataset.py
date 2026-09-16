#!/usr/bin/env python3
"""Assemble a LoRA training dataset from a character identity set.

    D:/AI/WanGP/env_uv/Scripts/python.exe tools/lora_dataset.py \
        --identity-set LIBRARY/imports/derived/identity-set-YYYYMMDD \
        --character ch-shindo-noa --trigger sxnoa \
        --out LIBRARY/training/ch-shindo-noa-YYYYMMDD

Training cannot run on this workstation - 8 GiB of VRAM, no trainer installed - so this produces the
portable thing instead: a snapshot with captions, a split and full lineage, which can be copied to rented
hardware and which outlives whichever base model is current. The identity set and `character.json` are the
assets; a LoRA built from them is a consumable.

Selection, in order:

1. **Mirrored members are dropped.** Trainers apply their own horizontal flip augmentation, so including a
   flip and its source teaches the same image twice, and for this character a flipped midriff frame would
   move `distinctive_marks` to the wrong side.
2. **Near-duplicates are dropped.** Consecutive frames of one clip are almost the same picture; anything
   within `--dup-threshold` cosine of a frame already taken from the same clip goes.
3. **Buckets are balanced.** Up to `--per-bucket` frames per yaw bucket per side, preferring the largest,
   sharpest faces, so the set does not collapse onto whichever angle happened to be over-rendered.
4. **Small faces are dropped.** Below `--min-face` pixels the face carries no trainable detail; the same
   threshold that makes the recogniser's scores meaningless makes the crop useless here.

Captions name the trigger token, the angle and the wardrobe, and deliberately do NOT describe the face.
A caption describing what should be learned teaches the model to rely on the words instead of the token.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import numpy as np

import identity_score
from character_sets import reserve_destination, write_set_context, publish_manifest, _relative_member

SPLIT_EVERY = 8  # every eighth selected frame is held out for validation


def select(manifest: dict[str, Any], args: argparse.Namespace) -> tuple[list[dict], dict[str, int]]:
    dropped = {"mirrored": 0, "small_face": 0, "duplicate": 0, "over_bucket": 0}
    pool = []
    for member in manifest["members"]:
        if member.get("mirrored"):
            dropped["mirrored"] += 1
            continue
        if member["face_pixels"][0] < args.min_face:
            dropped["small_face"] += 1
            continue
        pool.append(member)

    # Best first: a big, sharp face is worth more than a marginal one at the same angle.
    pool.sort(key=lambda m: (-m["face_pixels"][0], -m["sharpness"]))

    taken: list[dict] = []
    per_bucket: dict[str, int] = {}
    seen_by_clip: dict[str, list[np.ndarray]] = {}
    for member in pool:
        key = f"{member['yaw_bucket']}|{member['side']}"
        if per_bucket.get(key, 0) >= args.per_bucket:
            dropped["over_bucket"] += 1
            continue
        embedding = member["scores_vs_frontal_prototype"]
        # The manifest carries scores, not embeddings, so duplicate detection uses the frame itself.
        vector = _embedding(Path(member["_path"]))
        if vector is not None:
            near = any(float(np.dot(vector, other)) > args.dup_threshold
                       for other in seen_by_clip.get(member["clip"], []))
            if near:
                dropped["duplicate"] += 1
                continue
            seen_by_clip.setdefault(member["clip"], []).append(vector)
        per_bucket[key] = per_bucket.get(key, 0) + 1
        taken.append(dict(member, _scores=embedding))
    return taken, dropped


def _embedding(path: Path):
    """L2-normalised ArcFace embedding, or None when the face cannot be read."""
    measured = identity_score.measure(path)
    vector = (measured.get("embeddings") or {}).get("arcface")
    if not vector:
        return None
    array = np.asarray(vector, dtype=float)
    norm = float(np.linalg.norm(array))
    return array / norm if norm else None


def caption(member: dict[str, Any], args: argparse.Namespace) -> str:
    """Angle and framing only. The face is what the token must learn; naming it competes with the token."""
    angle = {"frontal": "facing the camera",
             "three_quarter": "in a three-quarter view",
             "deep_three_quarter": "in a deep three-quarter view",
             "profile": "in side profile"}[member["yaw_bucket"]]
    side = "" if member["yaw_bucket"] == "frontal" else f" turned to the {member['side']}"
    return (f"{args.trigger}, a photograph of one woman, head and shoulders, {angle}{side}, "
            f"natural light, plain background, sharp focus")


def build(args: argparse.Namespace) -> dict[str, Any]:
    set_dir = Path(args.identity_set)
    source_manifest = set_dir / "identity-set.json"
    source_bytes = source_manifest.read_bytes()
    manifest = json.loads(source_bytes)
    if manifest.get("character_id") != args.character:
        raise ValueError("identity set character does not match requested dataset character")
    for member in manifest["members"]:
        member_path = _relative_member(set_dir.resolve(), member["file"])
        member["_path"] = str(member_path)

    # Reserve before recognizer work.  Incomplete datasets intentionally remain
    # without dataset.json and are not discoverable as completed sets.
    out = reserve_destination("lora", args.character, args.out)
    taken, dropped = select(manifest, args)
    for split in ("train", "val"):
        (out / split).mkdir(parents=True, exist_ok=True)

    records = []
    for index, member in enumerate(sorted(taken, key=lambda m: m["yaw_proxy"] or 0)):
        split = "val" if index % SPLIT_EVERY == SPLIT_EVERY - 1 else "train"
        stem = f"{args.character}-{index:03d}"
        shutil.copyfile(member["_path"], out / split / f"{stem}.png")
        text = caption(member, args)
        (out / split / f"{stem}.txt").write_text(text + "\n", encoding="utf-8")
        records.append({"file": f"{split}/{stem}.png", "caption": text, "split": split,
                        "clip": member["clip"], "yaw_bucket": member["yaw_bucket"],
                        "yaw_proxy": member["yaw_proxy"], "side": member["side"],
                        "face_pixels": member["face_pixels"], "sharpness": member["sharpness"],
                        "source": member["source"], "identity_set_file": member["file"]})

    coverage: dict[str, int] = {}
    for record in records:
        key = f"{record['yaw_bucket']} {record['side']}"
        coverage[key] = coverage.get(key, 0) + 1

    snapshot = {
        "schema_version": 1, "created_at": identity_score.now(), "created_by": args.actor,
        "character_id": args.character, "trigger_token": args.trigger,
        "review_state": "needs_review",
        "review_note": ("No human has approved this dataset and none of it is an approved reference. "
                        "Training has not been run; this is a portable snapshot only."),
        "trainable_here": False,
        "environment_note": ("This workstation has 8 GiB of VRAM and no training harness installed "
                             "(no kohya/sd-scripts, musubi-tuner, ai-toolkit, diffusion-pipe or "
                             "OneTrainer); bitsandbytes is absent. Copy this directory to hardware that "
                             "can train and record the run there."),
        "selection": {
            "min_face_pixels": args.min_face, "per_bucket_per_side": args.per_bucket,
            "duplicate_cosine_threshold": args.dup_threshold,
            "mirrored_excluded": ("Trainers apply their own horizontal flip. Including a flip and its "
                                  "source teaches one image twice, and a flipped midriff frame would move "
                                  "this character's navel mole to the wrong side."),
            "dropped": dropped,
        },
        "caption_policy": ("Captions name the trigger, the angle and the framing, and never describe the "
                           "face. Describing what the token is supposed to learn teaches the model to lean "
                           "on the words instead."),
        "source_identity_set": str(set_dir),
        "source_prototype": manifest.get("prototype"),
        "split": {"rule": f"every {SPLIT_EVERY}th selected frame is validation",
                  "train": sum(1 for r in records if r["split"] == "train"),
                  "val": sum(1 for r in records if r["split"] == "val")},
        "coverage": dict(sorted(coverage.items())),
        "members": records,
    }
    output_files = [out / record["file"] for record in records]
    output_files.extend((out / record["file"]).with_suffix(".txt") for record in records)
    write_set_context(
        out, character_id=args.character, producer=Path(__file__), arguments=vars(args),
        source_manifest=source_manifest, source_bytes=source_bytes, output_files=output_files,
    )
    publish_manifest(out / "dataset.json", snapshot)
    return {"out": str(out), "selected": len(records), "dropped": dropped,
            "coverage": dict(sorted(coverage.items())), "split": snapshot["split"]}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--identity-set", required=True)
    parser.add_argument("--character", required=True)
    parser.add_argument("--trigger", required=True,
                        help="a token no tokenizer already knows, e.g. sxnoa")
    parser.add_argument("--out", help="new immutable dataset directory; optional with active shared Library")
    parser.add_argument("--actor", default="claude")
    parser.add_argument("--min-face", type=float, default=200.0)
    parser.add_argument("--per-bucket", type=int, default=10)
    parser.add_argument("--dup-threshold", type=float, default=0.96)
    return parser


def main() -> int:
    print(json.dumps(build(build_parser().parse_args()), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
