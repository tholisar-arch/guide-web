"""Generate French versions of the Product Selector data (data/nav.fr.json,
data/pages.fr.json, public/data/search-index.fr.json) from the English
data already in the repo.

Strategy: the catalog's breadcrumbs/labels/table headers are highly
repetitive technical vocabulary (a few hundred distinct terms across 458
pages), not free prose, so this is a glossary-substitution translation
rather than a per-string LLM call. Two dictionaries below were built by
enumerating every distinct label prefix ("Label: value") and standalone
phrase actually present in data/nav.json + data/pages.json (nav titles,
tail/breadcrumb segments, paragraph blocks, table headers, resource link
labels, category/chapter titles) - see the extraction commands in the
commit that added this file. Product codes/part numbers/catalog numbers
and physical values (voltages, currents, standard designators like BS88,
DIN NH, gG, L-N, TT...) are intentionally left unchanged - they are
international/standard notation, not English prose.

Unmatched fragments pass through unchanged (a product/brand name has
nothing to translate), but are logged so new vocabulary introduced by a
future data refresh can be reviewed and added here.
"""
import json
import re

# ---------- "Label: value" prefixes (value kept as-is) ----------
LABEL_DICT = {
    "Rated voltage": "Tension assignée",
    "Size": "Taille",
    "System type": "Type de schéma",
    "Type": "Type",
    "Assortment box Part Number": "Référence coffret d'assortiment",
    "BS type": "Type BS",
    "Connection type": "Type de raccordement",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Longueur",
    "Number of poles": "Nombre de pôles",
    "Range": "Gamme",
    "Back-up fuse": "Fusible amont",
    "Part Number": "Référence",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Sélecteur de produits",
    "Miniature fuses": "Fusibles miniatures",
    "IEC fuses": "Fusibles CEI",
    "UL/CSA fuses": "Fusibles UL/CSA",
    "High-speed fuses": "Fusibles ultra-rapides",
    "Medium voltage fuses": "Fusibles moyenne tension",
    "DC fuses": "Fusibles DC",
    "Photovoltaic Applications": "Applications photovoltaïques",
    "Surge Protection": "Protection contre les surtensions",
    "DC Distribution and Battery": "Distribution DC et batteries",
    "Industrial DC Fuses": "Fusibles DC industriels",
    # subcategory / type names
    "AC Rated": "Version AC",
    "DC Rated": "Version DC",
    "BS Feeder Pillar": "Armoire de branchement BS",
    "BS Street Lighting": "Éclairage public BS",
    "BS1361 Standard": "Norme BS1361",
    "BS88 Standard": "Norme BS88",
    "BS88-4 Standard": "Norme BS88-4",
    "Ceramic fuses": "Fusibles céramique",
    "Cylindrical": "Cylindrique",
    "Square body": "Corps carré",
    "DIN Back-Up for Motors": "DIN protection amont pour moteurs",
    "DIN D Standard": "Norme DIN D",
    "DIN D0 Standard": "Norme DIN D0",
    "DIN NH Standard": "Norme DIN NH",
    "DIN P Back-Up for transformers": "DIN P protection amont pour transformateurs",
    "DIN PD Back-Up for transformers": "DIN PD protection amont pour transformateurs",
    "DIN PT Back-Up for transformers": "DIN PT protection amont pour transformateurs",
    "DIN PTD Back-Up for transformers": "DIN PTD protection amont pour transformateurs",
    "DIN PTS Back-Up for transformers": "DIN PTS protection amont pour transformateurs",
    "Fast Acting": "Action rapide",
    "Medium Acting": "Action moyenne",
    "Very Fast Acting": "Action très rapide",
    "Time Delay": "Temporisé",
    "Ferrule fuse-links Standard": "Cartouches fusibles à ferrules standard",
    "Glass fuses": "Fusibles en verre",
    "House Service": "Branchement individuel",
    "Insulated tags": "Cosses isolées",
    "Non-insulated tags": "Cosses non isolées",
    "MV Street Lighting Fuses For transformers": "Fusibles MT éclairage public pour transformateurs",
    "Midget": "Midget",
    "Monitoring micro-contact": "Micro-contact de surveillance",
    "NF/UTE Back-Up fuses for transformers": "Fusibles NF/UTE de protection amont pour transformateurs",
    "Photovoltaic & Energy Storage": "Photovoltaïque et stockage d'énergie",
    "Power frequency overvoltage protection": "Protection contre les surtensions à fréquence industrielle",
    "Protection for LED lighting": "Protection pour éclairage LED",
    "Protection for Power Lines": "Protection des lignes électriques",
    "Protection for signal lines": "Protection des lignes de signal",
    "With built-in trip-indicator": "Avec indicateur de déclenchement intégré",
    "With indicator": "Avec indicateur",
    "With middle indicator": "Avec indicateur central",
    "With separated trip-indicator": "Avec indicateur de déclenchement séparé",
    "With stricker": "Avec percuteur",
    "With top indicator": "Avec indicateur supérieur",
    "Without indicator": "Sans indicateur",
    "Without stricker": "Sans percuteur",
    "Without trip-indicator": "Sans indicateur de déclenchement",
    "gPV Square body fuses": "Fusibles gPV corps carré",
    "gPV cylindrical fuses": "Fusibles gPV cylindriques",
    "Class C": "Classe C",
    "Class CC": "Classe CC",
    "Class J": "Classe J",
    "Class K5": "Classe K5",
    "Class L": "Classe L",
    "Class RK1": "Classe RK1",
    "Class RK5": "Classe RK5",
    "Class T": "Classe T",
    "Low Voltage": "Basse tension",
    "Assortment box": "Coffret d'assortiment",
    "Forklift Battery Fuses": "Fusibles batterie pour chariots élévateurs",
    "Protection for DC Distribution and Battery": "Protection pour distribution DC et batteries",
    "Surge-Trap® Pluggable": "Surge-Trap® Enfichable",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Enfichable Série STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Enfichable Série K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monobloc Série STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monobloc Série STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monobloc Série STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Enfichable Série K-K1",
    # paragraph-only phrases
    "Composition of the box": "Composition du coffret",
    "Fuse Base": "Socle fusible",
    "Fuse required": "Fusible requis",
    "No back-up": "Sans protection amont",
    # resource link labels
    "Datasheet": "Fiche technique",
    "Microswitches": "Microrupteurs",
    "NH fuse base": "Socle fusible NH",
    "Fuse bases": "Socles fusibles",
    "Fuse base": "Socle fusible",
    "BS fuse holder": "Porte-fusible BS",
    "Compact fuse holder": "Porte-fusible compact",
    "D fuse base": "Socle fusible D",
    "DIN D0 fuse base": "Socle fusible DIN D0",
    "Fuse holders": "Porte-fusibles",
    "Modular fuse holders": "Porte-fusibles modulaires",
    "Innozed® fuse holder": "Porte-fusible Innozed®",
    "Linocur® fuse holder": "Porte-fusible Linocur®",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Support",
    "Crimp Cap": "Capuchon à sertir",
    "DIN110 (DIN110 blades)": "DIN110 (lames DIN110)",
    "DIN110 Bracket": "Support DIN110",
    "DIN110 slotted blades": "Lames fendues DIN110",
    "DIN80 Bracket": "Support DIN80",
    "DIN80 slotted blades": "Lames fendues DIN80",
    "Direct mounting": "Montage direct",
    "EF (Bolted connections)": "EF (connexions boulonnées)",
    "EF French slotted blades": "Lames fendues françaises EF",
    "Ferrule Fuse": "Fusible à ferrule",
    "KI US short slotted blades": "Lames fendues courtes US KI",
    "LI US long slotted blades": "Lames fendues longues US LI",
    "Neutral Link": "Barrette de neutre",
    "PC Board Mount": "Montage circuit imprimé",
    "Plain blades": "Lames lisses",
    "Round Body Fuse": "Fusible corps rond",
    "Round Body for Metric Screws Fuse": "Fusible corps rond pour vis métriques",
    "Surface Mount Fuse": "Fusible montage en surface",
    "Threaded plates": "Plaques filetées",
    "TTF (Threaded Terminals)": "TTF (bornes filetées)",
    "TTF French threaded terminals": "Bornes filetées françaises TTF",
    "TTI US threaded terminals": "Bornes filetées US TTI",
    "Terminal": "Borne",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "Tension AC CEI",
    "Bandwidth": "Bande passante",
    "Catalog Number": "Référence catalogue",
    "Current (A)": "Courant (A)",
    "DC Voltage IEC": "Tension DC CEI",
    "Insulation voltage (V)": "Tension d'isolement (V)",
    "Part Number": "Référence",
    "Rated Current": "Courant assigné",
    "Remote": "Déporté",
}

LABEL_VALUE_RE = re.compile(r"^([^:]+):\s*(.+)$")
unmatched_log = set()


def split_compound(seg):
    if " - " in seg:
        a, b = seg.split(" - ", 1)
        return [a.strip(), b.strip()]
    return [seg]


def translate_atom(seg):
    """Translate one already-split (non-compound) segment."""
    seg = seg.strip()
    if seg in PHRASE_DICT:
        return PHRASE_DICT[seg]
    m = LABEL_VALUE_RE.match(seg)
    if m:
        label, value = m.group(1).strip(), m.group(2)
        if label in LABEL_DICT:
            value = VALUE_DICT.get(value.strip(), value)
            return f"{LABEL_DICT[label]} : {value}"
        unmatched_log.add(f"[label] {label!r}")
        return seg
    if any(c.isalpha() for c in seg) and seg not in PHRASE_DICT:
        # heuristic: flag anything alphabetic we didn't explicitly map,
        # so real English prose isn't silently left untranslated. Product
        # codes/brand names (Surge-Trap®, STPT12-...) are expected here
        # and are fine to pass through unchanged.
        unmatched_log.add(f"[phrase] {seg!r}")
    return seg


def translate_segment(seg):
    return " - ".join(translate_atom(a) for a in split_compound(seg))


def translate_header(h):
    return TABLE_HEADER_DICT.get(h, h)


def translate_paragraph(text):
    # a PDF line-wrap sometimes leaves a dangling separator with nothing
    # after it ("...STS 485 –"), which won't match the " – " split below
    text = re.sub(r"\s*[–-]\s*$", "", text)
    if " – " in text:
        # breadcrumb-repeat paragraph, same segments as the page's tail
        return " – ".join(translate_segment(s) for s in text.split(" – "))
    return translate_segment(text)


def translate_resource_label(label):
    return PHRASE_DICT.get(label, label)


FULL_TITLE_OVERRIDES = {
    "DC Distribution and Battery": "Distribution DC et batteries",
}


def translate_title(title, translated_tail):
    if title in FULL_TITLE_OVERRIDES:
        return FULL_TITLE_OVERRIDES[title]
    if translated_tail:
        return " - ".join(translated_tail)
    return title


# ---------- pages.json (translated first: nav.json's leaf items each
# duplicate a page's title, so build that translation once and reuse it -
# both for consistency and so leaf items in listing pages aren't left in
# English) ----------
pages = json.load(open("data/pages.json"))
for p in pages:
    new_tail = [translate_segment(s) for s in p["tail"]]
    p["title"] = translate_title(p["title"], new_tail)
    p["tail"] = new_tail
    if p.get("category"):
        p["category"] = PHRASE_DICT.get(p["category"], p["category"])
    if p.get("subcategory"):
        p["subcategory"] = PHRASE_DICT.get(p["subcategory"], p["subcategory"])

    table_cell_values = []
    fr_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            fr_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    # rebuild the flat search/preview text from already-translated blocks,
    # mirroring the original layout (table values, then paragraphs) rather
    # than translating the raw newline-joined PDF dump
    p["text"] = "\n".join(table_cell_values + fr_paragraphs)

with open("data/pages.fr.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_fr_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            fr_page = pages_fr_by_slug.get(item["slug"])
            if fr_page:
                item["title"] = fr_page["title"]
            else:
                unmatched_log.add(f"[leaf-no-page] {item['slug']!r}")
        return
    for child in node["children"]:
        child["title"] = translate_segment(child["title"])
        translate_nav_node(child["node"])


selector = next(c for c in nav["chapters"] if c["slug"] == "selector")
for cat in selector["categories"]:
    cat["title"] = PHRASE_DICT.get(cat["title"], cat["title"])
    translate_nav_node(cat["nav"])

with open("data/nav.fr.json", "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=1)

# ---------- search-index.json ----------
search_index = json.load(open("public/data/search-index.json"))
pages_by_slug = {p["slug"]: p for p in pages}
for e in search_index:
    p = pages_by_slug.get(e["slug"])
    if p:
        e["title"] = p["title"]
        e["category"] = p["category"]
        e["text"] = p["text"][:220]

with open("public/data/search-index.fr.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
