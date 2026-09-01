"""Prune the site to the Product Selector section only.

Run after build_data.py. Drops the About Us / Markets / Knowledge Centre
chapters (and cover page) from data/nav.json, data/pages.json and
public/data/search-index.json, and removes the now-unused screenshots /
content images those pages referenced.
"""
import json
import os

pages = json.load(open("data/pages.json"))
nav = json.load(open("data/nav.json"))

kept = [e for e in pages if e["chapter"] == "selector"]
removed = [e for e in pages if e["chapter"] != "selector"]
print("kept:", len(kept), "removed:", len(removed))

kept_screenshots = {e["screenshot"] for e in kept}
kept_images = {im["file"] for e in kept for im in e["images"]}

removed_pages = {e["page"] for e in removed}
removed_screens = 0
for p in removed_pages:
    path = f"public/pages/{p}.webp"
    if os.path.exists(path) and f"/pages/{p}.webp" not in kept_screenshots:
        os.remove(path)
        removed_screens += 1
print("removed screenshots:", removed_screens)

all_asset_files = {f"/assets/{f}" for f in os.listdir("public/assets")}
unused = all_asset_files - kept_images
removed_assets = 0
for f in unused:
    path = "public" + f
    if os.path.exists(path):
        os.remove(path)
        removed_assets += 1
print("removed unused content images:", removed_assets, "of", len(all_asset_files))

nav["chapters"] = [c for c in nav["chapters"] if c["slug"] == "selector"]

with open("data/pages.json", "w", encoding="utf-8") as f:
    json.dump(kept, f, ensure_ascii=False)
with open("data/nav.json", "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=1)

search_index = [
    {
        "title": e["title"],
        "slug": e["slug"],
        "chapter": e["chapter"],
        "category": e["category"],
        "page": e["page"],
        "text": e["text"][:220],
    }
    for e in kept
]
with open("public/data/search-index.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
