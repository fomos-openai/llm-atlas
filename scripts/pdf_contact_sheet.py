#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted((ROOT / "tmp" / "pdfs").glob("page-*.png"))
OUT = ROOT / "tmp" / "pdfs" / "contact-sheets"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    thumb_w, thumb_h, caption = 210, 298, 22
    cols, rows = 5, 4
    for sheet_index in range(0, len(PAGES), cols * rows):
        batch = PAGES[sheet_index:sheet_index + cols * rows]
        sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + caption)), "#dbe4ef")
        draw = ImageDraw.Draw(sheet)
        for index, path in enumerate(batch):
            image = Image.open(path).convert("RGB")
            image.thumbnail((thumb_w - 8, thumb_h - 8))
            x = (index % cols) * thumb_w + (thumb_w - image.width) // 2
            y = (index // cols) * (thumb_h + caption) + 4
            sheet.paste(image, (x, y))
            draw.text((x, y + image.height + 2), path.stem, fill="#0f172a")
        sheet.save(OUT / f"sheet-{sheet_index // (cols * rows) + 1:02d}.png")
    print(f"wrote {len(list(OUT.glob('sheet-*.png')))} contact sheets")


if __name__ == "__main__":
    main()
