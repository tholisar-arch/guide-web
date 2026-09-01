import fitz, json, re, os
from collections import defaultdict, Counter
from PIL import Image
import io

PDF = "Selection Guide - 2026 Europe - English.pdf"
doc = fitz.open(PDF)
NPAGES = doc.page_count

NAV_WORDS = {"About us","Selector","Markets","Knowledge","Web","Back","Next",
             "PRODUCT SELECTOR","KNOWLEDGE CENTRE","MARKETS","------------------",
             "+","---------------","Datasheet"}

MIN_VISIBLE_FONT = 4.0  # PowerPoint AI-alt-text / file-path metadata is embedded at ~1.2pt

JUNK_LINE_RE = re.compile(
    r"\\|\.(jpe?g|png|gif|bmp)\b|generado por IA|Interfaz de usuario|"
    r"contenido generado|^[A-Za-z]:\\",
    re.IGNORECASE,
)

IMG_DIR = "web_data/assets"
os.makedirs(IMG_DIR, exist_ok=True)

# ---------- pass 1: find template/chrome images (logo, banners, nav buttons) ----------
# and soft-mask (alpha channel) objects, which PyMuPDF also lists as if they
# were standalone images -- rendering one directly yields a flat black tile.
_xref_freq = Counter()
MASK_XREFS = set()
XREF_SMASK = {}
for _page in doc:
    for _im in _page.get_images(full=True):
        _xref_freq[_im[0]] += 1
        if _im[1]:
            MASK_XREFS.add(_im[1])
            XREF_SMASK[_im[0]] = _im[1]
_xref_freq = Counter({x: c for x, c in _xref_freq.items() if x not in MASK_XREFS})
CHROME_XREFS = {x for x, c in _xref_freq.items() if c >= 300}

_saved_images = {}  # xref -> {"file", "w", "h"}

def extract_page_images(page):
    """Return list of {file,w,h} for non-chrome images on this page.

    PowerPoint-exported slides often stack several images (a coloured badge
    shape, then an icon glyph) at the *same* position. get_images() is
    returned in roughly paint order, so when several images share a bbox we
    keep only the last one (the one actually visible on top) instead of
    showing every layer as a separate, confusingly blank/duplicate tile.
    """
    candidates = []  # (xref, rect) in paint order
    for img in page.get_images(full=True):
        xref = img[0]
        if xref in CHROME_XREFS or xref in MASK_XREFS:
            continue
        rects = page.get_image_rects(xref)
        if not rects:
            continue
        r = rects[0]
        if r.width < 12 or r.height < 12:
            continue  # skip specks
        candidates.append((xref, r))

    by_pos = {}
    for xref, r in candidates:
        key = (round(r.x0 / 3), round(r.y0 / 3), round(r.x1 / 3), round(r.y1 / 3))
        by_pos[key] = (xref, r)  # later entries overwrite earlier ones at same slot

    winners = list(by_pos.values())
    winners.sort(key=lambda t: (round(t[1].y0), round(t[1].x0)))

    out = []
    seen = set()
    for xref, r in winners:
        if xref in seen:
            continue
        seen.add(xref)
        if xref not in _saved_images:
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.colorspace is None or pix.colorspace.n not in (1, 3):
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                base_n = pix.colorspace.n if pix.colorspace else 1
                mode = {1: "L", 3: "RGB"}[base_n] + ("A" if pix.alpha else "")
                im = Image.frombytes(mode, (pix.width, pix.height), pix.samples).convert("RGB")

                smask_xref = XREF_SMASK.get(xref)
                alpha_im = None
                if smask_xref:
                    try:
                        mpix = fitz.Pixmap(doc, smask_xref)
                        alpha_im = Image.frombytes("L", (mpix.width, mpix.height), mpix.samples)
                        if alpha_im.size != im.size:
                            alpha_im = alpha_im.resize(im.size)
                    except Exception:
                        alpha_im = None
                if alpha_im is not None:
                    bg = Image.new("RGB", im.size, (255, 255, 255))
                    bg.paste(im, mask=alpha_im)
                    im = bg
            except Exception:
                continue
            small = im.resize((32, 32))
            if small.getcolors(maxcolors=2) is not None:
                # flat single-colour raster: a drop-shadow/blend artefact,
                # never meaningful standalone content
                _saved_images[xref] = None
                continue
            max_sat = max(px[1] for px in small.convert("HSV").getdata())
            if max_sat < 18:
                # near-greyscale blur/shadow layer with no real colour of its
                # own -- also not meaningful standalone content
                _saved_images[xref] = None
                continue
            fname = f"img-{xref}.webp"
            im.save(f"{IMG_DIR}/{fname}", "WEBP", quality=82, method=4)
            _saved_images[xref] = {"file": f"/assets/{fname}", "w": im.width, "h": im.height}
        if _saved_images[xref] is not None:
            out.append(_saved_images[xref])
    return out

# ---------- span extraction ----------

def get_spans(page):
    d = page.get_text("dict")
    spans = []
    for b in d["blocks"]:
        if "lines" not in b:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                t = s["text"].strip()
                if not t:
                    continue
                if s["size"] < MIN_VISIBLE_FONT:
                    continue
                spans.append({
                    "size": round(s["size"], 1), "text": t,
                    "x": round(s["bbox"][0], 1), "y": round(s["bbox"][1], 1),
                    "x1": round(s["bbox"][2], 1),
                })
    return spans

def extract_breadcrumb(spans):
    cand = [s for s in spans if s["size"] == 14.0]
    if not cand:
        return ""
    cand.sort(key=lambda s: (s["y"], s["x"]))
    lines = []
    cur_y = None
    cur = []
    for s in cand:
        if cur_y is None or abs(s["y"] - cur_y) < 3:
            cur.append(s["text"]); cur_y = s["y"]
        elif s["y"] - cur_y < 20:
            lines.append(" ".join(cur)); cur = [s["text"]]; cur_y = s["y"]
        else:
            break
    if cur:
        lines.append(" ".join(cur))
    return " ".join(lines).strip()

def extract_main(spans):
    cand = [s["text"] for s in spans if s["size"] >= 27 and s["y"] < 40]
    return cand[0] if cand else ""

def extract_fallback_title(spans):
    cand = [s for s in spans
            if s["text"] not in NAV_WORDS
            and len(s["text"]) > 3
            and s["y"] < 300
            and not re.fullmatch(r"[\W_]+", s["text"])]
    cand.sort(key=lambda s: (-s["size"], s["y"]))
    return cand[0]["text"] if cand else ""

PRIVATE_USE_RE = re.compile(r"[-]")

def clean_text(t):
    lines = [PRIVATE_USE_RE.sub("", l).strip() for l in t.split("\n")]
    out = []
    for l in lines:
        if not l:
            continue
        if l in NAV_WORDS:
            continue
        if JUNK_LINE_RE.search(l):
            continue
        if re.fullmatch(r"[\W_]+", l) and l not in ("?",):
            continue
        out.append(l)
    return "\n".join(out)

def slugify(s):
    s = s.lower()
    s = s.replace("&", "and").replace("+", "plus").replace("/", "-").replace("®", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "x"

# ---------- content block reconstruction (real text + real tables, no screenshots) ----------

def cluster_rows(spans):
    spans = sorted(spans, key=lambda s: (s["y"], s["x"]))
    rows = []
    for s in spans:
        if rows and abs(s["y"] - rows[-1]["y"]) < 3.0:
            rows[-1]["spans"].append(s)
        else:
            rows.append({"y": s["y"], "spans": [s]})
    for r in rows:
        r["spans"].sort(key=lambda s: s["x"])
    return rows

def assign_to_bins(spans, bin_centers, tol=32):
    assignment = {}
    for s in spans:
        best_i, best_d = None, tol + 1
        for i, c in enumerate(bin_centers):
            dist = abs(s["x"] - c)
            if dist < best_d:
                best_d, best_i = dist, i
        if best_i is None or best_i in assignment:
            return None
        assignment[best_i] = s["text"]
    return assignment

def build_table_and_paragraphs(rows):
    """Try to find one repeating tabular grid among `rows`. Returns (table_block_or_None, consumed_row_ids)."""
    colcounts = Counter(len(r["spans"]) for r in rows if len(r["spans"]) >= 2)
    if not colcounts:
        return None, set()
    mode_val, support = colcounts.most_common(1)[0]
    if support < 3:
        return None, set()

    exact_rows = [r for r in rows if len(r["spans"]) == mode_val]
    bin_centers = [
        sorted(r["spans"][i]["x"] for r in exact_rows)[len(exact_rows) // 2]
        for i in range(mode_val)
    ]

    qualifying = []
    for r in rows:
        if len(r["spans"]) < 2:
            continue
        assignment = assign_to_bins(r["spans"], bin_centers)
        if assignment is not None:
            qualifying.append((r, assignment))

    if len(qualifying) < 3:
        return None, set()

    headers = None
    data = qualifying
    first_row, first_assignment = qualifying[0]
    if len(first_assignment) == mode_val and len(qualifying) >= 3:
        headers = [first_assignment.get(i, "") for i in range(mode_val)]
        data = qualifying[1:]

    table_rows = [[a.get(i, "") for i in range(mode_val)] for _, a in data]
    consumed = {id(r) for r, _ in qualifying}
    return {"type": "table", "headers": headers, "rows": table_rows}, consumed

def build_blocks_tabular(spans):
    """For product-selector pages: real font, may contain a genuine spec table."""
    rows = cluster_rows(spans)
    table_block, consumed = build_table_and_paragraphs(rows)
    blocks = []
    emitted_table = False
    for r in rows:
        if id(r) in consumed:
            if not emitted_table:
                blocks.append(table_block)
                emitted_table = True
            continue
        kept = [s for s in r["spans"] if s["text"] not in NAV_WORDS]
        if not kept:
            continue
        text = PRIVATE_USE_RE.sub("", " ".join(s["text"] for s in kept)).strip()
        if not text:
            continue
        size = max(s["size"] for s in kept)
        blocks.append({"type": "paragraph", "text": text, "size": size})
    return blocks

def build_blocks_simple(text):
    """For about/markets/knowledge/cover pages: rely on PyMuPDF's reading-order text
    (robust even for decorative/stylised headings), one paragraph per line."""
    blocks = []
    for line in text.split("\n"):
        line = line.strip()
        if line:
            blocks.append({"type": "paragraph", "text": line, "size": 12})
    return blocks

TABULAR_PAGE_RANGE = set(range(8, 769))

pages = []
for i in range(NPAGES):
    pno = i + 1
    page = doc[i]
    spans = get_spans(page)
    text = clean_text(page.get_text("text"))
    images = extract_page_images(page)
    if pno in TABULAR_PAGE_RANGE:
        blocks = build_blocks_tabular(spans)
    else:
        blocks = build_blocks_simple(text)
    pages.append({
        "page": pno,
        "spans": spans,
        "breadcrumb": extract_breadcrumb(spans),
        "main": extract_main(spans),
        "fallback": extract_fallback_title(spans),
        "text": text,
        "blocks": blocks,
        "images": images,
    })
    if pno % 100 == 0:
        print("processed", pno)

# ---- Chapter boundaries ----
# 1 cover | 2-7 about | 8-756 selector (product families) | 757-768 selector applications
# 769 markets index | 770-774 markets | 775-814 knowledge

entries = []  # final flat list

def add_entry(p, chapter, category, subcategory, tail_segments, title, slug_parts):
    d = pages[p - 1]
    slug = "/".join(slugify(s) for s in slug_parts)
    entries.append({
        "page": p,
        "chapter": chapter,
        "category": category,
        "subcategory": subcategory,
        "tail": tail_segments,
        "title": title.strip(),
        "text": d["text"][:4000],
        "blocks": d["blocks"],
        "images": d["images"],
        "screenshot": f"/pages/{p}.webp",
        "slug": slug,
    })

# Cover
add_entry(1, "cover", None, None, [], "Selection Guide 2026 Europe", ["cover"])

# About us (2-7)
for p in range(2, 8):
    d = pages[p - 1]
    title = d["main"] or f"About us - page {p}"
    add_entry(p, "about", None, None, [], title, ["about", title])

# Applications mapping for 757-768
APPLICATIONS_MAP = {
    757: ("Overview", "Applications overview"),
    758: ("Industrial", "Overview"),
    759: ("Industrial", "Highly Protected"),
    760: ("Industrial", "Moderately Protected"),
    761: ("Industrial", "Basic Protection"),
    762: ("Commercial / Residential", "Overview"),
    763: ("Commercial / Residential", "Highly Protected"),
    764: ("Commercial / Residential", "Moderately Protected"),
    765: ("Commercial / Residential", "Basic Protection"),
    766: ("Street Lighting", "Overview"),
    767: ("Street Lighting", "Panel Builder / Installer"),
    768: ("Photovoltaic", "Overview"),
}

# Product selector pages with breadcrumb (8-756), category tree items
selector_items = defaultdict(list)  # category -> list of (page, remaining_segments)
CATEGORY_ALIASES = {
    "Medium voltage fuses & Fuse Holders": "Medium voltage fuses",
    "Medium voltage fuses & fuse holders": "Medium voltage fuses",
}

for p in range(8, 757):
    d = pages[p - 1]
    bc = d["breadcrumb"]
    if p == 8:
        add_entry(p, "selector", "Overview", None, [], "Product Selector - Categories", ["selector", "overview", f"page-{p}"])
        continue
    if not bc:
        title = d["fallback"] or d["main"] or f"Product Selector - page {p}"
        add_entry(p, "selector", "Overview", None, [], title, ["selector", "overview", f"page-{p}"])
        continue
    segs = [s.strip() for s in bc.split(" – ") if s.strip()]
    if not segs:
        continue
    cat = CATEGORY_ALIASES.get(segs[0], segs[0])
    if len(cat) > 60 or cat.count(" ") > 8:
        # malformed / index page (e.g. two categories concatenated)
        title = d["fallback"] or d["main"] or f"Product Selector - page {p}"
        add_entry(p, "selector", "Overview", None, [], title, ["selector", "overview", f"page-{p}"])
        continue
    selector_items[cat].append((p, segs[1:]))

# applications -> Surge Protection category
for p, (ctx, sub) in APPLICATIONS_MAP.items():
    selector_items["Surge Protection"].append((p, ["Applications", ctx, sub]))

def build_children(items, depth):
    """items: list of (page, remaining_segments). Returns tree node."""
    if depth <= 0 or all(len(seg) == 0 for _, seg in items):
        leaves = []
        for p, seg in items:
            leaves.append({"page": p, "tail": seg})
        return {"type": "leaves", "leaves": leaves}
    first_vals = set(seg[0] for _, seg in items if seg)
    if len(first_vals) <= 1:
        new_items = [(p, seg[1:] if seg else seg) for p, seg in items]
        return build_children(new_items, depth)
    groups = defaultdict(list)
    for p, seg in items:
        key = seg[0] if seg else "Other"
        groups[key].append((p, seg[1:] if seg else seg))
    children = {}
    for key, sub_items in groups.items():
        children[key] = build_children(sub_items, depth - 1)
    return {"type": "group", "children": children}

category_trees = {}
for cat, items in selector_items.items():
    category_trees[cat] = build_children(items, depth=2)

# Now walk category_trees to produce flat page entries with subcategory + tail + slug + nav json
def walk(node, cat_slug, cat_title, path_titles, subcategory_title):
    if node["type"] == "leaves":
        for leaf in node["leaves"]:
            p = leaf["page"]
            tail = leaf["tail"]
            title = " - ".join(path_titles + tail) if (path_titles or tail) else cat_title
            if not title:
                title = f"{cat_title} - page {p}"
            slug_parts = ["selector", cat_slug] + [slugify(t) for t in path_titles] + [f"p{p}"]
            add_entry(p, "selector", cat_title, subcategory_title, path_titles + tail, title, slug_parts)
    else:
        for key, child in node["children"].items():
            sub_title = subcategory_title or key
            walk(child, cat_slug, cat_title, path_titles + [key], sub_title)

for cat, tree in category_trees.items():
    walk(tree, slugify(cat), cat, [], None)

# Markets (769 index + 770-774)
add_entry(769, "markets", "Overview", None, [], "Markets overview", ["markets", "overview"])
for p in range(770, 775):
    d = pages[p - 1]
    title = d["main"].replace("MARKETS: ", "").title() if d["main"] else f"Market {p}"
    add_entry(p, "markets", None, None, [], title, ["markets", title])

# Knowledge centre (775-814)
def strip_icon_chars(s):
    return re.sub(r"^[^\w]+", "", s).strip()

seen_titles = defaultdict(int)
for p in range(775, 815):
    d = pages[p - 1]
    main = d["main"]
    title = ""
    if main and main != "KNOWLEDGE CENTRE" and len(main) > 4:
        title = strip_icon_chars(main)
    else:
        for line in d["text"].split("\n"):
            line = line.strip()
            if len(strip_icon_chars(line)) > 3:
                title = strip_icon_chars(line)
                break
    title = title or f"Knowledge Centre - page {p}"
    seen_titles[title] += 1
    disp = title if seen_titles[title] == 1 else f"{title} ({seen_titles[title]})"
    add_entry(p, "knowledge", None, None, [], disp, ["knowledge", disp])

entries.sort(key=lambda e: e["page"])
print("Total entries:", len(entries), "of", NPAGES, "pages")

# sanity: all pages covered exactly once
covered = sorted(e["page"] for e in entries)
missing = [p for p in range(1, NPAGES + 1) if p not in covered]
dups = [p for p in covered if covered.count(p) > 1]
print("missing:", missing[:20], "dup count:", len(set(dups)))

os.makedirs("web_data", exist_ok=True)
with open("web_data/pages.json", "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False)

# ---------- Build nav tree JSON ----------
nav = {"chapters": []}
by_chapter = defaultdict(list)
for e in entries:
    by_chapter[e["chapter"]].append(e)

# about
about_items = sorted(by_chapter["about"], key=lambda e: e["page"])
nav["chapters"].append({
    "slug": "about", "title": "About Us",
    "items": [{"title": e["title"], "slug": e["slug"], "page": e["page"]} for e in about_items]
})

# selector: rebuild category/subcategory nested nav using category_trees (with counts)
def node_to_nav(node, cat_slug, path_titles):
    if node["type"] == "leaves":
        items = []
        for leaf in node["leaves"]:
            p = leaf["page"]
            match = next(e for e in entries if e["page"] == p)
            items.append({"title": match["title"], "slug": match["slug"], "page": p})
        items.sort(key=lambda x: x["title"])
        return {"type": "leaves", "items": items}
    children = []
    for key, child in node["children"].items():
        children.append({
            "title": key,
            "slug": slugify(key),
            "count": count_leaves(child),
            "node": node_to_nav(child, cat_slug, path_titles + [key]),
        })
    children.sort(key=lambda c: -c["count"])
    return {"type": "group", "children": children}

def count_leaves(node):
    if node["type"] == "leaves":
        return len(node["leaves"])
    return sum(count_leaves(c) for c in node["children"].values())

selector_categories = []
overview_pages = [e for e in by_chapter["selector"] if e["category"] == "Overview"]
for cat, tree in sorted(category_trees.items(), key=lambda kv: -count_leaves(kv[1])):
    selector_categories.append({
        "title": cat,
        "slug": slugify(cat),
        "count": count_leaves(tree),
        "nav": node_to_nav(tree, slugify(cat), []),
    })

nav["chapters"].append({
    "slug": "selector", "title": "Product Selector",
    "overview": [{"title": e["title"], "slug": e["slug"], "page": e["page"]} for e in sorted(overview_pages, key=lambda e: e["page"])],
    "categories": selector_categories,
})

# markets
markets_items = sorted([e for e in by_chapter["markets"] if e["page"] != 769], key=lambda e: e["page"])
nav["chapters"].append({
    "slug": "markets", "title": "Markets",
    "overviewSlug": next(e["slug"] for e in by_chapter["markets"] if e["page"] == 769),
    "items": [{"title": e["title"], "slug": e["slug"], "page": e["page"]} for e in markets_items]
})

# knowledge
knowledge_items = sorted(by_chapter["knowledge"], key=lambda e: e["page"])
nav["chapters"].append({
    "slug": "knowledge", "title": "Knowledge Centre",
    "items": [{"title": e["title"], "slug": e["slug"], "page": e["page"]} for e in knowledge_items]
})

with open("web_data/nav.json", "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=1)

# ---------- Search index (lightweight) ----------
search_index = [{"title": e["title"], "slug": e["slug"], "chapter": e["chapter"],
                  "category": e["category"], "page": e["page"],
                  "text": e["text"][:220]} for e in entries]
with open("web_data/search-index.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done. categories:", [(c["title"], c["count"]) for c in selector_categories])
print("unique content images saved:", len(_saved_images))
