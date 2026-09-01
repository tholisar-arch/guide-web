"""Keep only pages that show a real product reference table (Part
Number / Catalog Number rows), dropping intermediate "choose a size /
choose a voltage" pages and summary-range tables that have no purchasable
references. Run after filter_selector_only.py.
"""
import json
import re
import os

CODE_RE_MIN, CODE_RE_MAX = 4, 16


def looks_like_code(s):
    s = s.strip()
    if not s or " " in s:
        return False
    if not re.search(r"\d", s):
        return False
    if len(s) < CODE_RE_MIN or len(s) > CODE_RE_MAX:
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9./,\-]+", s))


def is_range_row(row):
    # summary/overview tables spell out spec ranges ("2A to 100A", "Size:
    # NDZ to DV") instead of one purchasable reference per row
    return any(" to " in (cell or "") for cell in row)


def has_real_reference_table(entry):
    for b in entry["blocks"]:
        if b["type"] != "table":
            continue
        rows = b["rows"]
        if not rows:
            continue
        n_range = sum(1 for r in rows if is_range_row(r))
        if n_range / len(rows) >= 0.3:
            continue
        firstcol = [r[0] for r in rows if r and r[0]]
        if not firstcol:
            continue
        n_code = sum(1 for v in firstcol if looks_like_code(v))
        if n_code / len(firstcol) >= 0.6:
            return True
    return False


def extract_codes(entry):
    """All table cell values (Part Number, Catalog Number, etc.) for this
    page, so the search index can match an exact reference even when it
    isn't among the first characters of the page's free text."""
    seen = []
    seen_set = set()
    for b in entry["blocks"]:
        if b["type"] != "table":
            continue
        for row in b["rows"]:
            for cell in row:
                cell = (cell or "").strip()
                if cell and cell not in seen_set:
                    seen_set.add(cell)
                    seen.append(cell)
    return " ".join(seen)


pages = json.load(open("data/pages.json"))
nav = json.load(open("data/nav.json"))

kept = [e for e in pages if has_real_reference_table(e)]
removed = [e for e in pages if not has_real_reference_table(e)]
kept_slugs = {e["slug"] for e in kept}
print("kept:", len(kept), "removed:", len(removed))


def count_leaves(node):
    if node["type"] == "leaves":
        return len(node["items"])
    return sum(c["count"] for c in node["children"])


def prune_node(node):
    if node["type"] == "leaves":
        node["items"] = [it for it in node["items"] if it["slug"] in kept_slugs]
        return node if node["items"] else None
    new_children = []
    for child in node["children"]:
        pruned = prune_node(child["node"])
        if pruned is not None:
            child["node"] = pruned
            child["count"] = count_leaves(pruned)
            new_children.append(child)
    node["children"] = new_children
    return node if new_children else None


CATEGORY_ORDER = [
    "Miniature fuses",
    "IEC fuses",
    "UL/CSA fuses",
    "High-speed fuses",
    "Medium voltage fuses",
    "DC Distribution and Battery",
    "Industrial DC Fuses",
    "Photovoltaic Applications",
    "Surge Protection",
]

SURGE_TYPE_ORDER = [
    "Type: 1",
    "Type: 1+2",
    "Type: 2",
    "Type: 2+3",
    "Protection for signal lines",
]


def min_page_in_node(node):
    if node["type"] == "leaves":
        return min(it["page"] for it in node["items"])
    return min(min_page_in_node(c["node"]) for c in node["children"])


def resort_node(node, cat_slug, is_top):
    """build_data.py orders group children by each subtree's earliest PDF
    page, computed *before* this script prunes out the "no real reference
    table" pages (overview/index pages, which often have a lower page
    number than the detail pages under them). Once those are pruned, a
    subtree's true earliest page can shift, so re-sort using the
    already-pruned tree instead of trusting the pre-prune order."""
    if node["type"] == "leaves":
        return
    if cat_slug == "surge-protection" and is_top:
        node["children"].sort(
            key=lambda c: SURGE_TYPE_ORDER.index(c["title"])
            if c["title"] in SURGE_TYPE_ORDER
            else len(SURGE_TYPE_ORDER)
        )
    else:
        node["children"].sort(key=lambda c: min_page_in_node(c["node"]))
    for child in node["children"]:
        resort_node(child["node"], cat_slug, False)


selector = next(c for c in nav["chapters"] if c["slug"] == "selector")
selector["overview"] = [
    it for it in selector["overview"] if it["slug"] in kept_slugs
]
new_categories = []
for cat in selector["categories"]:
    pruned = prune_node(cat["nav"])
    if pruned is not None:
        cat["nav"] = pruned
        cat["count"] = count_leaves(pruned)
        resort_node(cat["nav"], cat["slug"], True)
        new_categories.append(cat)
new_categories.sort(key=lambda c: CATEGORY_ORDER.index(c["title"]) if c["title"] in CATEGORY_ORDER else len(CATEGORY_ORDER))
selector["categories"] = new_categories
print("categories kept:", [c["title"] for c in new_categories])

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

all_asset_files = {f"/assets/{f}" for f in os.listdir("public/assets")} if os.path.isdir("public/assets") else set()
unused = all_asset_files - kept_images
removed_assets = 0
for f in unused:
    path = "public" + f
    if os.path.exists(path):
        os.remove(path)
        removed_assets += 1
print("removed unused content images:", removed_assets, "of", len(all_asset_files))

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
        "codes": extract_codes(e),
    }
    for e in kept
]
with open("public/data/search-index.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
