"""Build per-engine contact sheets for a Character Lab batch."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".avif"}


def image_files(folder: Path) -> list[Path]:
    return sorted(
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def build_sheet(files: list[Path], output: Path, title: str, columns: int = 4) -> None:
    thumb_width, thumb_height = 320, 400
    label_height, header_height, gap = 42, 64, 16
    rows = math.ceil(len(files) / columns)
    sheet_width = gap + columns * (thumb_width + gap)
    sheet_height = header_height + rows * (thumb_height + label_height + gap) + gap
    sheet = Image.new("RGB", (sheet_width, sheet_height), "#202124")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.text((gap, 22), title, fill="white", font=font)

    for index, path in enumerate(files):
        row, column = divmod(index, columns)
        x = gap + column * (thumb_width + gap)
        y = header_height + row * (thumb_height + label_height + gap)
        with Image.open(path) as source:
            rgb = ImageOps.exif_transpose(source).convert("RGB")
            thumb = ImageOps.contain(rgb, (thumb_width, thumb_height))
        tile = Image.new("RGB", (thumb_width, thumb_height), "#111111")
        tile.paste(thumb, ((thumb_width - thumb.width) // 2, (thumb_height - thumb.height) // 2))
        sheet.paste(tile, (x, y))
        label = f"{index + 1:02d}  {path.name}"
        draw.text((x, y + thumb_height + 10), label[:48], fill="white", font=font)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path, help="Path to one Character Lab batch directory")
    parser.add_argument("--engine", help="Only build one engine sheet")
    parser.add_argument("--columns", type=int, default=4)
    args = parser.parse_args()

    outputs = args.batch.resolve() / "outputs"
    if not outputs.is_dir():
        parser.error(f"outputs directory not found: {outputs}")
    engine_dirs = [outputs / args.engine] if args.engine else sorted(p for p in outputs.iterdir() if p.is_dir())
    built = 0
    for engine_dir in engine_dirs:
        files = image_files(engine_dir) if engine_dir.is_dir() else []
        if not files:
            print(f"skip {engine_dir.name}: no images")
            continue
        destination = args.batch.resolve() / "contact-sheets" / f"{engine_dir.name}.jpg"
        build_sheet(files, destination, f"{args.batch.name} / {engine_dir.name}", args.columns)
        print(f"wrote {destination}")
        built += 1
    if built == 0:
        print("No contact sheets created.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
