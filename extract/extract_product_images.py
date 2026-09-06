import hashlib
import io
import json
import os

import fitz
import numpy as np
from PIL import Image
from scipy.ndimage import label

PDF = "Selection Guide - 2026 Europe - English.pdf"
OUT_DIR = "public/images/products"
MAP_PATH = "data/product-images.json"
ZOOM = 6
PAD = 5
# Chroma-key thresholds (Euclidean RGB distance) for cutting the product
# photo out of its flat page background: below LOW is definitely
# background (fully transparent), above HIGH is definitely product
# (fully opaque), and the ramp between the two smooths the antialiased
# edge instead of leaving a hard/jagged cutout line.
BG_LOW = 8.0
BG_HIGH = 45.0


def remove_background(rgba: Image.Image) -> Image.Image:
    """Make the page background behind a cropped product photo transparent.

    The PDF renders these crops on a flat (near-)white page background, not
    the site's own background color, so placing them as-is leaves a visible
    white box around every product. Only the background region connected to
    the crop's border is keyed out (via connected-component labeling), so
    legitimately light/white parts fully enclosed by the product itself
    (labels, reflections, punched mounting holes) are left alone - or, in
    the case of a real punched hole, correctly rendered as see-through.
    """
    arr = np.array(rgba).astype(np.float32)
    rgb = arr[:, :, :3]
    border = np.concatenate(
        [arr[0, :, :3], arr[-1, :, :3], arr[:, 0, :3], arr[:, -1, :3]], axis=0
    )
    bg_color = np.median(border, axis=0)

    dist = np.sqrt(((rgb - bg_color) ** 2).sum(axis=2))
    candidate = dist < BG_HIGH
    labeled, _ = label(candidate)
    border_labels = (
        set(labeled[0, :]) | set(labeled[-1, :]) | set(labeled[:, 0]) | set(labeled[:, -1])
    )
    border_labels.discard(0)
    bg_mask = np.isin(labeled, list(border_labels))

    alpha = np.full(dist.shape, 255.0)
    ramp = np.clip((dist - BG_LOW) / (BG_HIGH - BG_LOW), 0, 1) * 255.0
    alpha[bg_mask] = ramp[bg_mask]

    out = arr.copy()
    out[:, :, 3] = alpha
    return Image.fromarray(out.astype(np.uint8), "RGBA")


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
    cutout = remove_background(Image.open(io.BytesIO(png_bytes)).convert("RGBA"))

    digest = hashlib.sha1(cutout.tobytes()).hexdigest()[:16]
    if digest not in hash_to_filename:
        filename = f"{digest}.webp"
        cutout.save(os.path.join(OUT_DIR, filename), "WEBP", quality=90, method=6)
        hash_to_filename[digest] = filename
        saved += 1
    mapping[str(pno)] = hash_to_filename[digest]

with open(MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(mapping, f)

print(f"pages processed: {len(pages)}")
print(f"pages with a product image: {len(mapping)}")
print(f"unique images saved: {saved}")
