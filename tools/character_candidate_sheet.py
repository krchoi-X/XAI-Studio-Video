#!/usr/bin/env python3
"""Build numbered candidate contact sheets for one character's existing images.

Used to pick the master identity reference before locking a character: the operator looks at the sheets,
names one number, and `index.json` resolves that number back to an absolute path. Read-only over the
library; writes only the sheets and the index into the chosen output directory.

    python tools/character_candidate_sheet.py --character ch-lia --out D:/AI_Studio/reports/lia-candidates
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ASSET_LIBRARY = Path(r"D:\AI_Studio\library\characters")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
# Session-name fragments that usually mean a face-forward or neutral portrait: the strongest master material.
PORTRAIT_HINTS = ("portrait", "close-up", "close", "face", "skin-texture", "identity", "base-identity")


def stamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def collect(character_root: Path) -> list[dict]:
    """Every still that belongs to the character, newest session first, with its origin."""
    items: list[dict] = []
    imports = character_root / "imports"
    if imports.is_dir():
        for path in sorted(p for p in imports.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS):
            items.append({"path": path, "group": "imports", "session": path.parent.name, "kind": "import"})
    generations = character_root / "generations"
    if generations.is_dir():
        for session in sorted((p for p in generations.iterdir() if p.is_dir()), reverse=True):
            outputs = session / "outputs"
            if not outputs.is_dir():
                continue
            name = session.name.lower()
            group = "portraits" if any(hint in name for hint in PORTRAIT_HINTS) else "scenes"
            for path in sorted(p for p in outputs.rglob("*") if p.suffix.lower() in IMAGE_EXTENSIONS):
                items.append({"path": path, "group": group, "session": session.name, "kind": "generated"})
    return items


def build_sheet(entries: list[dict], output: Path, title: str, columns: int, thumb: tuple[int, int]) -> None:
    thumb_width, thumb_height = thumb
    label_height, header_height, gap = 30, 56, 12
    rows = max(1, math.ceil(len(entries) / columns))
    sheet = Image.new("RGB", (gap + columns * (thumb_width + gap),
                              header_height + rows * (thumb_height + label_height + gap) + gap), "#202124")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((gap, 20), title, fill="white", font=font)
    for index, entry in enumerate(entries):
        row, column = divmod(index, columns)
        x = gap + column * (thumb_width + gap)
        y = header_height + row * (thumb_height + label_height + gap)
        try:
            with Image.open(entry["path"]) as source:
                rgb = ImageOps.exif_transpose(source).convert("RGB")
                preview = ImageOps.contain(rgb, (thumb_width, thumb_height))
        except OSError:
            continue
        tile = Image.new("RGB", (thumb_width, thumb_height), "#111111")
        tile.paste(preview, ((thumb_width - preview.width) // 2, (thumb_height - preview.height) // 2))
        sheet.paste(tile, (x, y))
        draw.text((x + 2, y + thumb_height + 4), f"#{entry['number']}", fill="#ffd166", font=font)
        draw.text((x + 40, y + thumb_height + 4), entry["session"][:34], fill="#aab2bd", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=90)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--character", required=True, help="character id, e.g. ch-lia")
    parser.add_argument("--library", type=Path, default=ASSET_LIBRARY)
    parser.add_argument("--out", type=Path, required=True, help="directory for the sheets and index.json")
    parser.add_argument("--columns", type=int, default=6)
    parser.add_argument("--thumb-width", type=int, default=300)
    parser.add_argument("--thumb-height", type=int, default=380)
    parser.add_argument("--max-per-sheet", type=int, default=36)
    args = parser.parse_args(argv)

    character_root = args.library / args.character
    if not character_root.is_dir():
        print(f"error: character library not found: {character_root}", file=sys.stderr)
        return 2

    items = collect(character_root)
    if not items:
        print(f"error: no images found under {character_root}", file=sys.stderr)
        return 2
    for number, item in enumerate(items, 1):
        item["number"] = number

    out = args.out.resolve()
    sheets: list[dict] = []
    for group in ("imports", "portraits", "scenes"):
        entries = [i for i in items if i["group"] == group]
        for part, start in enumerate(range(0, len(entries), args.max_per_sheet), 1):
            chunk = entries[start:start + args.max_per_sheet]
            suffix = f"-{part}" if len(entries) > args.max_per_sheet else ""
            path = out / f"{args.character}-{group}{suffix}.jpg"
            title = f"{args.character}  {group}{suffix}   #{chunk[0]['number']}-#{chunk[-1]['number']}   {len(chunk)} images"
            build_sheet(chunk, path, title, args.columns, (args.thumb_width, args.thumb_height))
            sheets.append({"group": group, "path": str(path), "count": len(chunk),
                           "first_number": chunk[0]["number"], "last_number": chunk[-1]["number"]})

    index = {
        "schema_version": 1,
        "character_id": args.character,
        "created_at": stamp(),
        "library_root": str(character_root),
        "sheets": sheets,
        "images": [{"number": i["number"], "group": i["group"], "session": i["session"],
                    "kind": i["kind"], "path": str(i["path"])} for i in items],
    }
    index_path = out / "index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"index": str(index_path), "images": len(items), "sheets": sheets}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
