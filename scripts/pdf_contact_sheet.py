#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent.parent
files = sorted((root / "tmp" / "pdfs").glob("llm-atlas-*.png"))
thumb_w = 320
margin = 18
label_h = 24
columns = 4
thumbs = []
for file in files:
    image = Image.open(file).convert("RGB")
    ratio = thumb_w / image.width
    size = (thumb_w, round(image.height * ratio))
    thumbs.append((file, image.resize(size, Image.Resampling.LANCZOS)))

cell_h = max(image.height for _, image in thumbs) + label_h
rows = (len(thumbs) + columns - 1) // columns
sheet = Image.new("RGB", (columns * thumb_w + (columns + 1) * margin, rows * cell_h + (rows + 1) * margin), "#e2e8f0")
draw = ImageDraw.Draw(sheet)
for index, (file, image) in enumerate(thumbs):
    col = index % columns
    row = index // columns
    x = margin + col * (thumb_w + margin)
    y = margin + row * (cell_h + margin)
    sheet.paste(image, (x, y + label_h))
    draw.text((x, y + 4), f"Page {index + 1}", fill="#0f172a")

out = root / "tmp" / "pdfs" / "contact-sheet.png"
sheet.save(out)
print(out)

