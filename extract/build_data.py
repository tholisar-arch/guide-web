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

# Display-name overrides for a Product Selector category: keyed by the exact
# heading text as it appears in the PDF, so slugs/sort order (still keyed on
# the PDF text) stay stable while only the shown title changes.
CATEGORY_TITLE_OVERRIDES = {
    "Protection for DC Distribution and Battery": "DC Distribution and Battery",
}

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

def _bbox_intersects(a, b, pad=6):
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    return not (ax1 + pad < bx0 or bx1 + pad < ax0 or ay1 + pad < by0 or by1 + pad < ay0)

GENERIC_URIS = {"https://www.mersen.com/en"}  # footer "Web" link, not a product resource

def extract_resource_links(page):
    """Datasheet / accessory (fuse base, microswitches, ...) links the PDF
    points at each product page's icon+caption pair. We match each hyperlink
    rect to the caption text sitting on top of it (bbox intersection) rather
    than trusting link order, since every link appears twice in the PDF (an
    icon rect and a text rect) and pages can host several stacked datasheets.
    Includes any external link with a matched caption -- not just PDFs, since
    several accessories (Multivert(R) FSD, Multibloc(R) FSD, ProGrid Smart
    FSD, ...) link to a mersen.com catalog page rather than a downloadable
    file. Datasheet is always sorted first per the site's convention."""
    links = [
        l for l in page.get_links()
        if l.get("kind") == 2 and l.get("uri", "") not in GENERIC_URIS
    ]
    if not links:
        return []
    d = page.get_text("dict")
    spans = []
    for b in d["blocks"]:
        if "lines" not in b:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    spans.append({"text": t, "bbox": s["bbox"]})

    uris = {}
    for l in links:
        uris.setdefault(l["uri"], []).append(l["from"])

    results = []
    for uri, rects in uris.items():
        label = None
        for r in rects:
            rbbox = (r.x0, r.y0, r.x1, r.y1)
            cands = [s for s in spans if _bbox_intersects(rbbox, s["bbox"])]
            if cands:
                label = cands[0]["text"]
                break
        if not label:
            continue
        results.append({"label": label, "url": uri, "_y": min(r.y0 for r in rects)})

    results.sort(key=lambda r: (r["label"] != "Datasheet", r["_y"]))
    for r in results:
        del r["_y"]
    return results

def caption_texts_near_links(page):
    """Text captions the PDF places next to any external hyperlink icon
    (Datasheet, or an accessory name like "Multivert(R) FSD" that links to a
    mersen.com catalog page rather than a downloadable file). These are
    layout chrome for the icon, not real body text -- whether or not they
    end up in the Documentation list -- so callers strip them from
    paragraph blocks rather than showing them as stray, meaningless lines."""
    links = [l for l in page.get_links() if l.get("kind") == 2]
    if not links:
        return set()
    d = page.get_text("dict")
    spans = []
    for b in d["blocks"]:
        if "lines" not in b:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    spans.append({"text": t, "bbox": s["bbox"]})
    captions = set()
    for l in links:
        rbbox = (l["from"].x0, l["from"].y0, l["from"].x1, l["from"].y1)
        for s in spans:
            if _bbox_intersects(rbbox, s["bbox"]):
                captions.add(s["text"])
    return captions

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
    """Map each span to its nearest column bin. A span with no bin within
    tolerance is a stray caption that drifted into this row during y
    clustering (e.g. a left-margin note landing within 3pt of a data row) --
    drop it rather than voiding the whole row. Two spans genuinely competing
    for the same column is a real misalignment, so that still fails."""
    assignment = {}
    for s in spans:
        best_i, best_d = None, tol + 1
        for i, c in enumerate(bin_centers):
            dist = abs(s["x"] - c)
            if dist < best_d:
                best_d, best_i = dist, i
        if best_i is None:
            continue
        if best_i in assignment:
            return None
        assignment[best_i] = s["text"]
    return assignment if assignment else None

def find_repeating_header(rows, scan_limit=6):
    """Some pages lay out two (or three) side-by-side sub-tables sharing the
    same columns (e.g. 'Part Number Catalog Number ... Part Number Catalog
    Number ...') to fit more references per page. Detect that duplicated
    header among the first few content rows and return (header_row,
    unit_width) so the row-splitter can treat every `unit_width`-wide slice
    of a row as its own table row."""
    for r in rows[:scan_limit]:
        n = len(r["spans"])
        if n < 4:
            continue
        texts = [s["text"] for s in r["spans"]]
        for repeat in (2, 3, 4):
            if n % repeat != 0:
                continue
            k = n // repeat
            if k < 2:
                continue
            groups = [texts[i * k:(i + 1) * k] for i in range(repeat)]
            if all(g == groups[0] for g in groups):
                return r, k
    return None, None

def split_by_vertical_gaps(rows):
    """A page can stack two unrelated tables with different columns (e.g. a
    fuse-reference table followed by a separate "Fuse Base" accessory
    table further down). Column-binning them together skews both tables'
    bins toward whichever has more rows, misaligning or dropping the
    other's cells. Split rows into contiguous groups wherever consecutive
    multi-span rows are separated by an unusually large vertical gap, so
    each candidate table is column-binned independently."""
    candidates = sorted([r for r in rows if len(r["spans"]) >= 2], key=lambda r: r["y"])
    if len(candidates) < 4:
        return [rows]
    gaps = [candidates[i + 1]["y"] - candidates[i]["y"] for i in range(len(candidates) - 1)]
    typical = sorted(gaps)[len(gaps) // 2]
    threshold = max(3 * typical, 25)
    break_ys = [candidates[i + 1]["y"] for i, g in enumerate(gaps) if g > threshold]
    if not break_ys:
        return [rows]
    boundaries = [-1] + break_ys + [float("inf")]
    groups = []
    for i in range(len(boundaries) - 1):
        lo, hi = boundaries[i], boundaries[i + 1]
        groups.append([r for r in rows if lo <= r["y"] < hi])
    return [g for g in groups if g]

def build_table_and_paragraphs(rows):
    """Find one or more tabular grids among `rows` (see split_by_vertical_gaps
    for why a page can hold more than one). Returns a list of
    (table_block, consumed_row_ids) pairs, in page order."""
    rows = [r for r in rows if any(s["text"] not in NAV_WORDS for s in r["spans"])]
    groups = split_by_vertical_gaps(rows)
    # A lone header+1-data-row table (e.g. a single-reference "Protection
    # for LED lighting" product, or a "Fuse Base" accessory section) is a
    # real, if small, reference table -- 2 rows sharing at least 2 aligned
    # columns (checked further down) is already a reasonably strict bar,
    # so don't require a 3rd row just because the page has only one such
    # section.
    min_rows = 2
    tables = []
    for group in groups:
        block, consumed = _build_one_table(group, min_rows=min_rows)
        if block is not None:
            tables.append((block, consumed))
    return tables

def _build_one_table(rows, min_rows=3):
    """Try to find one repeating tabular grid among `rows`. Returns (table_block_or_None, consumed_row_ids)."""
    header_row, unit_width = find_repeating_header(rows)
    if header_row is not None:
        headers = [s["text"] for s in header_row["spans"][:unit_width]]
        repeat = len(header_row["spans"]) // unit_width
        # PDF reading order for side-by-side sub-tables is left column top
        # to bottom, then right column top to bottom (e.g. Part Number
        # OTS1..OTS200 on the left, OTS225..OTS600 on the right) -- not
        # interleaved row by row, which is what a naive per-row split
        # would produce.
        columns = [[] for _ in range(repeat)]
        consumed = {id(header_row)}
        for r in rows:
            if r is header_row:
                continue
            n = len(r["spans"])
            if n == 0 or n % unit_width != 0:
                continue
            texts = [s["text"] for s in r["spans"]]
            for i in range(n // unit_width):
                group = texts[i * unit_width:(i + 1) * unit_width]
                if group != headers:  # a repeated header row further down the page
                    columns[i].append(group)
            consumed.add(id(r))
        table_rows = [group for col in columns for group in col]
        if len(table_rows) >= 2:
            return {"type": "table", "headers": headers, "rows": table_rows}, consumed

    colcounts = Counter(len(r["spans"]) for r in rows if len(r["spans"]) >= 2)
    if not colcounts:
        return None, set()
    mode_val, support = colcounts.most_common(1)[0]
    if support < min_rows:
        return None, set()

    exact_rows = [r for r in rows if len(r["spans"]) == mode_val]
    bin_centers = [
        sorted(r["spans"][i]["x"] for r in exact_rows)[len(exact_rows) // 2]
        for i in range(mode_val)
    ]

    min_matched = min(2, mode_val)
    qualifying = []
    for r in rows:
        if len(r["spans"]) < 2:
            continue
        assignment = assign_to_bins(r["spans"], bin_centers)
        # a single matched bin is too weak a signal -- a stray caption that
        # happens to land near one column (e.g. "Number of poles: 2" close
        # to the Part Number column) would otherwise leak in as a row
        if assignment is not None and len(assignment) >= min_matched:
            qualifying.append((r, assignment))

    if len(qualifying) < min_rows:
        return None, set()

    headers = None
    data = qualifying
    first_row, first_assignment = qualifying[0]
    if len(first_assignment) == mode_val and len(qualifying) >= min_rows:
        headers = [first_assignment.get(i, "") for i in range(mode_val)]
        data = qualifying[1:]

    table_rows = [[a.get(i, "") for i in range(mode_val)] for _, a in data]
    if headers is not None:
        # a repeated header row further down a multi-section page (e.g. a
        # second "Number of poles: 4" block) looks like ordinary data here
        table_rows = [row for row in table_rows if row != headers]
    consumed = {id(r) for r, _ in qualifying}
    return {"type": "table", "headers": headers, "rows": table_rows}, consumed

def build_blocks_tabular(spans, extra_excluded=frozenset()):
    """For product-selector pages: real font, may contain a genuine spec table."""
    rows = cluster_rows(spans)
    tables = build_table_and_paragraphs(rows)  # [(block, consumed_ids), ...] in page order
    consumed = set().union(*[c for _, c in tables]) if tables else set()
    pending = list(tables)
    blocks = []
    for r in rows:
        if id(r) in consumed:
            if pending and id(r) in pending[0][1]:
                blocks.append(pending[0][0])
                pending.pop(0)
            continue
        kept = [s for s in r["spans"] if s["text"] not in NAV_WORDS and s["text"] not in extra_excluded]
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
        blocks = build_blocks_tabular(spans, caption_texts_near_links(page))
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
        "resource_links": extract_resource_links(page),
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
        "resourceLinks": d["resource_links"],
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
    walk(tree, slugify(cat), CATEGORY_TITLE_OVERRIDES.get(cat, cat), [], None)

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

# selector: rebuild category/subcategory nested nav using category_trees (with counts)
def node_to_nav(node, cat_slug, path_titles):
    if node["type"] == "leaves":
        items = []
        for leaf in node["leaves"]:
            p = leaf["page"]
            match = next(e for e in entries if e["page"] == p)
            items.append({"title": match["title"], "slug": match["slug"], "page": p})
        items.sort(key=lambda x: x["page"])
        return {"type": "leaves", "items": items}
    children = []
    for key, child in node["children"].items():
        children.append({
            "title": key,
            "slug": slugify(key),
            "count": count_leaves(child),
            "node": node_to_nav(child, cat_slug, path_titles + [key]),
        })
    if cat_slug == "surge-protection" and not path_titles:
        children.sort(key=lambda c: SURGE_TYPE_ORDER.index(c["title"]) if c["title"] in SURGE_TYPE_ORDER else len(SURGE_TYPE_ORDER))
    else:
        children.sort(key=lambda c: min_page_in_node(c["node"]))
    return {"type": "group", "children": children}

def count_leaves(node):
    if node["type"] == "leaves":
        return len(node["leaves"])
    return sum(count_leaves(c) for c in node["children"].values())

CATEGORY_ORDER = [
    "Miniature fuses",
    "IEC fuses",
    "UL/CSA fuses",
    "High-speed fuses",
    "Medium voltage fuses",
    "Protection for DC Distribution and Battery",
    "Industrial DC Fuses",
    "Photovoltaic Applications",
    "Surge Protection",
]

def category_sort_key(cat):
    try:
        return CATEGORY_ORDER.index(cat)
    except ValueError:
        return len(CATEGORY_ORDER)

selector_categories = []
overview_pages = [e for e in by_chapter["selector"] if e["category"] == "Overview"]
for cat, tree in sorted(category_trees.items(), key=lambda kv: category_sort_key(kv[0])):
    selector_categories.append({
        "title": CATEGORY_TITLE_OVERRIDES.get(cat, cat),
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
