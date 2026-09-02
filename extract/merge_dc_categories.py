"""Merge the "DC Distribution and Battery" and "Industrial DC Fuses" top
-level Product Selector categories into a single "DC fuses" category with
both as subcategories, matching how the source PDF groups them - without
losing any existing page slug (leaf items keep their own absolute slug,
independent of the nav path used to reach them).

Run after regroup_long_lists.py (or any time; order doesn't matter, this
only touches the "selector" categories list plus the "category" label
stored per page/search-index entry).
"""
import json

DC_DIST_SLUG = "protection-for-dc-distribution-and-battery"
DC_IND_SLUG = "industrial-dc-fuses"
NEW_TITLE = "DC fuses"
NEW_SLUG = "dc-fuses"


def count_leaves(node):
    if node["type"] == "leaves":
        return len(node["items"])
    return sum(count_leaves(c["node"]) for c in node["children"])


nav = json.load(open("data/nav.json"))
selector = next(c for c in nav["chapters"] if c["slug"] == "selector")

cats = selector["categories"]
idx = [i for i, c in enumerate(cats) if c["slug"] in (DC_DIST_SLUG, DC_IND_SLUG)]
assert len(idx) == 2, f"expected both DC categories, found indices {idx}"
insert_at = min(idx)
dc_dist = next(c for c in cats if c["slug"] == DC_DIST_SLUG)
dc_ind = next(c for c in cats if c["slug"] == DC_IND_SLUG)

merged = {
    "title": NEW_TITLE,
    "slug": NEW_SLUG,
    "count": dc_dist["count"] + dc_ind["count"],
    "nav": {
        "type": "group",
        "children": [
            {
                "title": dc_dist["title"],
                "slug": dc_dist["slug"],
                "count": dc_dist["count"],
                "node": dc_dist["nav"],
            },
            {
                "title": dc_ind["title"],
                "slug": dc_ind["slug"],
                "count": dc_ind["count"],
                "node": dc_ind["nav"],
            },
        ],
    },
}
assert count_leaves(merged["nav"]) == merged["count"]

new_cats = [c for c in cats if c["slug"] not in (DC_DIST_SLUG, DC_IND_SLUG)]
new_cats.insert(insert_at, merged)
selector["categories"] = new_cats

with open("data/nav.json", "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=1)

# keep the per-page "category" label (shown in search results) in sync
old_titles = {dc_dist["title"], dc_ind["title"]}
pages = json.load(open("data/pages.json"))
changed = 0
for p in pages:
    if p.get("category") in old_titles:
        p["subcategory"] = p["category"]
        p["category"] = NEW_TITLE
        changed += 1
with open("data/pages.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)
print("pages.json category updated on", changed, "entries")

search_index = json.load(open("public/data/search-index.json"))
changed = 0
for e in search_index:
    if e.get("category") in old_titles:
        e["category"] = NEW_TITLE
        changed += 1
with open("public/data/search-index.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)
print("search-index.json category updated on", changed, "entries")

print("done:", NEW_TITLE, "now has", merged["count"], "leaves")
