"""Generate Dutch versions of the Product Selector data (data/nav.nl.json,
data/pages.nl.json, public/data/search-index.nl.json) from the English data
already in the repo.

Same glossary-substitution approach as extract/translate_to_fr.py (see that
file's docstring for the rationale): the catalog's breadcrumbs/labels/table
headers are repetitive technical vocabulary, not free prose, so every
distinct label/phrase/value/header is translated once here rather than via
a per-string LLM call. Product codes/part numbers and physical values
(voltages, currents, standard designators like BS88, DIN NH, gG, L-N, TT...)
are intentionally left unchanged - international/standard notation, not
English prose.

Unmatched fragments pass through unchanged but are logged for review.
"""
import json
import re

# ---------- "Label: value" prefixes (value kept as-is) ----------
LABEL_DICT = {
    "Rated voltage": "Nominale spanning",
    "Size": "Maat",
    "System type": "Systeemtype",
    "Type": "Type",
    "Assortment box Part Number": "Artikelnummer assortimentsdoos",
    "BS type": "BS-type",
    "Connection type": "Aansluittype",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Lengte",
    "Number of poles": "Aantal polen",
    "Range": "Serie",
    "Back-up fuse": "Voorzekering",
    "Part Number": "Artikelnummer",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Productselector",
    "Miniature fuses": "Miniatuurzekeringen",
    "IEC low voltage fuses": "IEC laagspanningszekeringen",
    "UL/CSA low voltage fuses": "UL/CSA laagspanningszekeringen",
    "High-speed fuses": "Snelle zekeringen",
    "IEC medium voltage fuses": "IEC middenspanningszekeringen",
    "DC fuses": "DC-zekeringen",
    "Photovoltaic Applications": "Fotovoltaïsche toepassingen",
    "Surge Protection": "Overspanningsbeveiliging",
    "DC Distribution and Battery": "DC-distributie en batterijen",
    "Industrial DC Fuses": "Industriële DC-zekeringen",
    # subcategory / type names
    "AC Rated": "AC-uitvoering",
    "DC Rated": "DC-uitvoering",
    "BS Feeder Pillar": "BS-verdeelkast",
    "BS Street Lighting": "BS-straatverlichting",
    "BS1361 Standard": "Norm BS1361",
    "BS88 Standard": "Norm BS88",
    "BS88-4 Standard": "Norm BS88-4",
    "Ceramic fuses": "Keramische zekeringen",
    "Cylindrical": "Cilindrisch",
    "Square body": "Vierkante behuizing",
    "DIN Back-Up for Motors": "DIN voorzekering voor motoren",
    "DIN D Standard": "Norm DIN D",
    "DIN D0 Standard": "Norm DIN D0",
    "DIN NH Standard": "Norm DIN NH",
    "DIN P Back-Up for transformers": "DIN P voorzekering voor transformatoren",
    "DIN PD Back-Up for transformers": "DIN PD voorzekering voor transformatoren",
    "DIN PT Back-Up for transformers": "DIN PT voorzekering voor transformatoren",
    "DIN PTD Back-Up for transformers": "DIN PTD voorzekering voor transformatoren",
    "DIN PTS Back-Up for transformers": "DIN PTS voorzekering voor transformatoren",
    "Fast Acting": "Snel",
    "Medium Acting": "Halftraag",
    "Very Fast Acting": "Extra snel",
    "Time Delay": "Traag",
    "Ferrule fuse-links Standard": "Cilindrische zekeringspatronen",
    "Glass fuses": "Glaszekeringen",
    "House Service": "Huisaansluiting",
    "Insulated tags": "Geïsoleerde aansluitlippen",
    "Non-insulated tags": "Niet-geïsoleerde aansluitlippen",
    "MV Street Lighting Fuses For transformers": "MS-straatverlichtingszekeringen voor transformatoren",
    "Midget": "Midget",
    "Monitoring micro-contact": "Bewakingsmicroschakelaar",
    "NF/UTE Back-Up fuses for transformers": "NF/UTE-voorzekeringen voor transformatoren",
    "Photovoltaic & Energy Storage": "Fotovoltaïsch en energieopslag",
    "Power frequency overvoltage protection": "Overspanningsbeveiliging bij netfrequentie",
    "Protection for LED lighting": "Bescherming voor LED-verlichting",
    "Protection for Power Lines": "Bescherming van stroomleidingen",
    "Protection for signal lines": "Bescherming van signaallijnen",
    "With built-in trip-indicator": "Met ingebouwde uitschakelindicator",
    "With indicator": "Met indicator",
    "With middle indicator": "Met middenindicator",
    "With separated trip-indicator": "Met aparte uitschakelindicator",
    "With stricker": "Met slagpin",
    "With top indicator": "Met bovenindicator",
    "Without indicator": "Zonder indicator",
    "Without stricker": "Zonder slagpin",
    "Without trip-indicator": "Zonder uitschakelindicator",
    "gPV Square body fuses": "gPV-zekeringen vierkante behuizing",
    "gPV cylindrical fuses": "gPV-zekeringen cilindrisch",
    "Class C": "Klasse C",
    "Class CC": "Klasse CC",
    "Class J": "Klasse J",
    "Class K5": "Klasse K5",
    "Class L": "Klasse L",
    "Class RK1": "Klasse RK1",
    "Class RK5": "Klasse RK5",
    "Class T": "Klasse T",
    "Low Voltage": "Laagspanning",
    "Assortment box": "Assortimentsdoos",
    "Forklift Battery Fuses": "Zekeringen voor heftruckbatterijen",
    "Protection for DC Distribution and Battery": "Bescherming voor DC-distributie en batterijen",
    "Surge-Trap® Pluggable": "Surge-Trap® Insteekbaar",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Insteekbaar Serie STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Insteekbaar Serie K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monoblock Serie STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monoblock Serie STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monoblock Serie STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Insteekbaar Serie K-K1",
    # paragraph-only phrases
    "Composition of the box": "Samenstelling van de doos",
    "Fuse Base": "Zekeringvoet",
    "Fuse required": "Vereiste zekering",
    "No back-up": "Zonder voorzekering",
    # resource link labels
    "Datasheet": "Datasheet",
    "Microswitches": "Microschakelaar",
    "NH fuse base": "NH-zekeringvoet",
    "Fuse bases": "Zekeringvoeten",
    "Fuse base": "Zekeringvoet",
    "BS fuse holder": "BS-zekeringhouder",
    "Compact fuse holder": "Compacte zekeringhouder",
    "D fuse base": "D-zekeringvoet",
    "DIN D0 fuse base": "DIN D0-zekeringvoet",
    "Fuse holders": "Zekeringhouders",
    "Modular fuse holders": "Modulaire zekeringhouders",
    "Innozed® fuse holder": "Innozed®-zekeringhouder",
    "Linocur® fuse holder": "Linocur®-zekeringhouder",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Beugel",
    "Crimp Cap": "Krimpdop",
    "DIN110 (DIN110 blades)": "DIN110 (DIN110-messen)",
    "DIN110 Bracket": "DIN110-beugel",
    "DIN110 slotted blades": "DIN110 gesleufde messen",
    "DIN80 Bracket": "DIN80-beugel",
    "DIN80 slotted blades": "DIN80 gesleufde messen",
    "Direct mounting": "Directe montage",
    "EF (Bolted connections)": "EF (boutverbindingen)",
    "EF French slotted blades": "EF Franse gesleufde messen",
    "Ferrule Fuse": "Zekering met huls",
    "KI US short slotted blades": "KI US korte gesleufde messen",
    "LI US long slotted blades": "LI US lange gesleufde messen",
    "Neutral Link": "Nulbrug",
    "PC Board Mount": "Printplaatmontage",
    "Plain blades": "Gladde messen",
    "Round Body Fuse": "Zekering met ronde behuizing",
    "Round Body for Metric Screws Fuse": "Zekering ronde behuizing voor metrische schroeven",
    "Surface Mount Fuse": "SMD-zekering",
    "Threaded plates": "Schroefdraadplaten",
    "TTF (Threaded Terminals)": "TTF (schroefdraadaansluitingen)",
    "TTF French threaded terminals": "TTF Franse schroefdraadaansluitingen",
    "TTI US threaded terminals": "TTI US-schroefdraadaansluitingen",
    "Terminal": "Aansluiting",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "AC-spanning IEC",
    "Bandwidth": "Bandbreedte",
    "Catalog Number": "Catalogusnummer",
    "Current (A)": "Stroom (A)",
    "DC Voltage IEC": "DC-spanning IEC",
    "Insulation voltage (V)": "Isolatiespanning (V)",
    "Part Number": "Artikelnummer",
    "Rated Current": "Nominale stroom",
    "Remote": "Afstandscontact",
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
            return f"{LABEL_DICT[label]}: {value}"
        unmatched_log.add(f"[label] {label!r}")
        return seg
    if any(c.isalpha() for c in seg) and seg not in PHRASE_DICT:
        unmatched_log.add(f"[phrase] {seg!r}")
    return seg


def translate_segment(seg):
    return " - ".join(translate_atom(a) for a in split_compound(seg))


def translate_header(h):
    return TABLE_HEADER_DICT.get(h, h)


def translate_paragraph(text):
    text = re.sub(r"\s*[–-]\s*$", "", text)
    if " – " in text:
        return " – ".join(translate_segment(s) for s in text.split(" – "))
    return translate_segment(text)


def translate_resource_label(label):
    return PHRASE_DICT.get(label, label)


FULL_TITLE_OVERRIDES = {
    "DC Distribution and Battery": "DC-distributie en batterijen",
}


def translate_title(title, translated_tail):
    if title in FULL_TITLE_OVERRIDES:
        return FULL_TITLE_OVERRIDES[title]
    if translated_tail:
        return " - ".join(translated_tail)
    return title


# ---------- pages.json (translated first: nav.json's leaf items each
# duplicate a page's title, so build that translation once and reuse it) ----------
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
    nl_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            nl_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + nl_paragraphs)

with open("data/pages.nl.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_nl_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            nl_page = pages_nl_by_slug.get(item["slug"])
            if nl_page:
                item["title"] = nl_page["title"]
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

with open("data/nav.nl.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.nl.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
