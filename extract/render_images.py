import fitz, os
from PIL import Image
import io

PDF = "Selection Guide - 2026 Europe - English.pdf"
OUT = "web_data/pages_img"
os.makedirs(OUT, exist_ok=True)

doc = fitz.open(PDF)
WIDTH = 1400

total_before = 0
total_after = 0
for i, page in enumerate(doc):
    pno = i + 1
    out_path = f"{OUT}/{pno}.webp"
    rect = page.rect
    zoom = WIDTH / rect.width
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img.save(out_path, "WEBP", quality=74, method=4)
    total_after += os.path.getsize(out_path)
    if pno % 100 == 0:
        print("rendered", pno)

print("done. total webp bytes:", total_after, "=", round(total_after / 1024 / 1024, 1), "MB")
