"""Add intermediate nav categories under any "leaves" list that's grown too
long to browse comfortably (many Surge Protection / IEC fuses / High-speed
fuses lists ended up with 10-80 items, each labelled with its full leftover
breadcrumb tail, so entries were truncated and hard to tell apart).

Does not touch pages.json or any existing group/leaf slug: it only walks
data/nav.json, and for every "leaves" node with more than LIST_THRESHOLD
items, re-derives extra group levels from the *same* breadcrumb tail data
already recorded per page (data/pages.json's "tail" field), so the result
is exactly what a deeper `build_data.py` depth would have produced -
without needing the source PDF, which isn't available in this environment.

Run after filter_reference_tables_only.py.
"""
import json
import re
from collections import defaultdict

LIST_THRESHOLD = 8


def slugify(s):
    s = s.lower()
    s = s.replace("&", "and").replace("+", "plus").replace("/", "-").replace("®", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "x"


def split_compound(seg):
    """A few breadcrumb segments glue two distinct dimensions together with
    a plain " - " (e.g. "System type: TT - Surge-Trap® Pluggable STPT
    Series"), because the source PDF only used an en-dash between *real*
    breadcrumb levels and a plain hyphen here. Split those back into two
    levels so each can be grouped on independently."""
    if " - " in seg:
        a, b = seg.split(" - ", 1)
        return [a.strip(), b.strip()]
    return [seg]


def normalize_tail(tail):
    out = []
    for seg in tail:
        out.extend(split_compound(seg))
    return out


pages = json.load(open("data/pages.json"))
nav = json.load(open("data/nav.json"))

tail_by_slug = {}
for p in pages:
    if p["chapter"] != "selector":
        continue
    tail_by_slug[p["slug"]] = normalize_tail(p["tail"])


def regroup(items, ancestor_len):
    """items: list of leaf dicts {title, slug, page}. ancestor_len: how many
    normalized-tail segments are already accounted for by this node's
    ancestors. Returns a nav node (leaves or group)."""
    if len(items) <= LIST_THRESHOLD:
        return {"type": "leaves", "items": items}

    # find the next tail segment (if any) whose values actually cluster
    # the list (more than one distinct value, but not one-per-item, or
    # this level is a no-op - either every item agrees, which is a
    # passthrough, or every item differs, which is not a real category)
    max_len = max(len(tail_by_slug[it["slug"]]) for it in items)
    split_index = None
    for i in range(ancestor_len, max_len):
        vals = [tail_by_slug[it["slug"]][i] if i < len(tail_by_slug[it["slug"]]) else None for it in items]
        distinct = set(vals)
        if 1 < len(distinct) < len(items):
            split_index = i
            break

    if split_index is None:
        return {"type": "leaves", "items": items}

    groups = defaultdict(list)
    order = []
    for it in items:
        t = tail_by_slug[it["slug"]]
        key = t[split_index] if split_index < len(t) else "Other"
        if key not in groups:
            order.append(key)
        groups[key].append(it)

    children = []
    for key in order:
        sub_items = groups[key]
        children.append({
            "title": key,
            "slug": slugify(key),
            "count": len(sub_items),
            "node": regroup(sub_items, split_index + 1),
        })
    # keep the original PDF page order between sibling groups
    children.sort(key=lambda c: min(it["page"] for it in groups[c["title"]]))
    return {"type": "group", "children": children}


def count_leaves(node):
    if node["type"] == "leaves":
        return len(node["items"])
    return sum(count_leaves(c["node"]) for c in node["children"])


def walk(node, ancestor_len):
    if node["type"] == "leaves":
        if len(node["items"]) > LIST_THRESHOLD:
            return regroup(node["items"], ancestor_len)
        return node
    for child in node["children"]:
        child["node"] = walk(child["node"], ancestor_len + 1)
        child["count"] = count_leaves(child["node"])
    return node


selector = next(c for c in nav["chapters"] if c["slug"] == "selector")
expanded = 0
for cat in selector["categories"]:
    before = json.dumps(cat["nav"])
    cat["nav"] = walk(cat["nav"], 0)
    if json.dumps(cat["nav"]) != before:
        expanded += 1
    cat["count"] = count_leaves(cat["nav"])

print("categories with newly-expanded lists:", expanded)

with open("data/nav.json", "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=1)

print("done")
