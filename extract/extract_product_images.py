import hashlib
import io
import json
import os

import fitz
from PIL import Image

PDF = "Selection Guide - 2026 Europe - English.pdf"
OUT_DIR = "public/images/products"
MAP_PATH = "data/product-images.json"
ZOOM = 6
PAD = 5

os.makedirs(OUT_DIR, exist_ok=True)

pages = json.load(open("data/pages.json", encoding="utf-8"))
doc = fitz.open(PDF)

mapping = {}
hash_to_filename = {}
saved = 0

for p in pages:
    pno = p["page"]
    page = doc[pno - 1]
    cand = []
    for img in page.get_images(full=True):
        xref = img[0]
        for r in page.get_image_rects(xref):
            if r.x0 < 110 and 55 <= r.y0 <= 135:
                cand.append(r)
    if not cand:
        continue

    x0 = min(r.x0 for r in cand) - PAD
    y0 = min(r.y0 for r in cand) - PAD
    x1 = max(r.x1 for r in cand) + PAD
    y1 = max(r.y1 for r in cand) + PAD
    clip = fitz.Rect(x0, y0, x1, y1)

    mat = fitz.Matrix(ZOOM, ZOOM)
    pix = page.get_pixmap(matrix=mat, clip=clip, alpha=True)
    png_bytes = pix.tobytes("png")

    digest = hashlib.sha1(png_bytes).hexdigest()[:16]
    if digest not in hash_to_filename:
        img = Image.open(io.BytesIO(png_bytes))
        filename = f"{digest}.webp"
        img.save(os.path.join(OUT_DIR, filename), "WEBP", quality=90, method=6)
        hash_to_filename[digest] = filename
        saved += 1
    mapping[str(pno)] = hash_to_filename[digest]

with open(MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(mapping, f)

print(f"pages processed: {len(pages)}")
print(f"pages with a product image: {len(mapping)}")
print(f"unique images saved: {saved}")
