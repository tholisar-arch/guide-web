"""Generate Hungarian versions of the Product Selector data (data/nav.hu.json,
data/pages.hu.json, public/data/search-index.hu.json) from the English data
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
    "Rated voltage": "Névleges feszültség",
    "Size": "Méret",
    "System type": "Rendszertípus",
    "Type": "Típus",
    "Assortment box Part Number": "Készletdoboz cikkszáma",
    "BS type": "BS típus",
    "Connection type": "Csatlakozás típusa",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Hossz",
    "Number of poles": "Pólusok száma",
    "Range": "Sorozat",
    "Back-up fuse": "Előtétbiztosíték",
    "Part Number": "Cikkszám",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Termékválasztó",
    "Miniature fuses": "Miniatűr biztosítékok",
    "IEC low voltage fuses": "IEC kisfeszültségű biztosítékok",
    "UL/CSA low voltage fuses": "UL/CSA kisfeszültségű biztosítékok",
    "High-speed fuses": "Gyorsbiztosítékok",
    "IEC medium voltage fuses": "IEC középfeszültségű biztosítékok",
    "DC fuses": "DC biztosítékok",
    "Photovoltaic Applications": "Fotovoltaikus alkalmazások",
    "Surge Protection": "Túlfeszültség-védelem",
    "DC Distribution and Battery": "DC elosztás és akkumulátorok",
    "Industrial DC Fuses": "Ipari DC biztosítékok",
    # subcategory / type names
    "AC Rated": "AC kivitel",
    "DC Rated": "DC kivitel",
    "BS Feeder Pillar": "BS elosztószekrény",
    "BS Street Lighting": "BS közvilágítás",
    "BS1361 Standard": "BS1361 szabvány",
    "BS88 Standard": "BS88 szabvány",
    "BS88-4 Standard": "BS88-4 szabvány",
    "Ceramic fuses": "Kerámia biztosítékok",
    "Cylindrical": "Hengeres",
    "Square body": "Négyzet alakú ház",
    "DIN Back-Up for Motors": "DIN előtétbiztosíték motorokhoz",
    "DIN D Standard": "DIN D szabvány",
    "DIN D0 Standard": "DIN D0 szabvány",
    "DIN NH Standard": "DIN NH szabvány",
    "DIN P Back-Up for transformers": "DIN P előtétbiztosíték transzformátorokhoz",
    "DIN PD Back-Up for transformers": "DIN PD előtétbiztosíték transzformátorokhoz",
    "DIN PT Back-Up for transformers": "DIN PT előtétbiztosíték transzformátorokhoz",
    "DIN PTD Back-Up for transformers": "DIN PTD előtétbiztosíték transzformátorokhoz",
    "DIN PTS Back-Up for transformers": "DIN PTS előtétbiztosíték transzformátorokhoz",
    "Fast Acting": "Gyors kioldású",
    "Medium Acting": "Félig lomha",
    "Very Fast Acting": "Extra gyors kioldású",
    "Time Delay": "Lomha",
    "Ferrule fuse-links Standard": "Hengeres biztosítóbetétek",
    "Glass fuses": "Üveg biztosítékok",
    "House Service": "Házi bekötés",
    "Insulated tags": "Szigetelt csatlakozósarukkal",
    "Non-insulated tags": "Szigeteletlen csatlakozósarukkal",
    "MV Street Lighting Fuses For transformers": "KF közvilágítási biztosítékok transzformátorokhoz",
    "Midget": "Midget",
    "Monitoring micro-contact": "Felügyeleti mikrokapcsoló",
    "NF/UTE Back-Up fuses for transformers": "NF/UTE előtétbiztosítékok transzformátorokhoz",
    "Photovoltaic & Energy Storage": "Fotovoltaikus és energiatárolás",
    "Power frequency overvoltage protection": "Hálózati frekvenciás túlfeszültség-védelem",
    "Protection for LED lighting": "LED-világítás védelme",
    "Protection for Power Lines": "Tápvezetékek védelme",
    "Protection for signal lines": "Jelvezetékek védelme",
    "With built-in trip-indicator": "Beépített kioldásjelzővel",
    "With indicator": "Jelzővel",
    "With middle indicator": "Középső jelzővel",
    "With separated trip-indicator": "Külön kioldásjelzővel",
    "With stricker": "Ütőszeggel",
    "With top indicator": "Felső jelzővel",
    "Without indicator": "Jelző nélkül",
    "Without stricker": "Ütőszeg nélkül",
    "Without trip-indicator": "Kioldásjelző nélkül",
    "gPV Square body fuses": "gPV négyzet alakú házas biztosítékok",
    "gPV cylindrical fuses": "gPV hengeres biztosítékok",
    "Class C": "C osztály",
    "Class CC": "CC osztály",
    "Class J": "J osztály",
    "Class K5": "K5 osztály",
    "Class L": "L osztály",
    "Class RK1": "RK1 osztály",
    "Class RK5": "RK5 osztály",
    "Class T": "T osztály",
    "Low Voltage": "Kisfeszültség",
    "Assortment box": "Készletdoboz",
    "Forklift Battery Fuses": "Targonca akkumulátor biztosítékok",
    "Protection for DC Distribution and Battery": "Védelem DC elosztáshoz és akkumulátorokhoz",
    "Surge-Trap® Pluggable": "Surge-Trap® Dugaszolható",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Dugaszolható STPT sorozat",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Dugaszolható K–K2 sorozat",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monoblokk STMT sorozat",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monoblokk STET sorozat",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monoblokk STPT sorozat",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Dugaszolható K-K1 sorozat",
    # paragraph-only phrases
    "Composition of the box": "A doboz tartalma",
    "Fuse Base": "Biztosítékfoglalat",
    "Fuse required": "Szükséges biztosíték",
    "No back-up": "Előtétbiztosíték nélkül",
    # resource link labels
    "Datasheet": "Adatlap",
    "Microswitches": "Mikrokapcsoló",
    "NH fuse base": "NH biztosítékfoglalat",
    "Fuse bases": "Biztosítékfoglalatok",
    "Fuse base": "Biztosítékfoglalat",
    "BS fuse holder": "BS biztosítéktartó",
    "Compact fuse holder": "Kompakt biztosítéktartó",
    "D fuse base": "D biztosítékfoglalat",
    "DIN D0 fuse base": "DIN D0 biztosítékfoglalat",
    "Fuse holders": "Biztosítéktartók",
    "Modular fuse holders": "Moduláris biztosítéktartók",
    "Innozed® fuse holder": "Innozed® biztosítéktartó",
    "Linocur® fuse holder": "Linocur® biztosítéktartó",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Tartókeret",
    "Crimp Cap": "Krimpelt sapka",
    "DIN110 (DIN110 blades)": "DIN110 (DIN110 késekkel)",
    "DIN110 Bracket": "DIN110 tartókeret",
    "DIN110 slotted blades": "DIN110 hornyolt kések",
    "DIN80 Bracket": "DIN80 tartókeret",
    "DIN80 slotted blades": "DIN80 hornyolt kések",
    "Direct mounting": "Közvetlen szerelés",
    "EF (Bolted connections)": "EF (csavaros csatlakozás)",
    "EF French slotted blades": "EF francia hornyolt kések",
    "Ferrule Fuse": "Hüvelyes biztosíték",
    "KI US short slotted blades": "KI US rövid hornyolt kések",
    "LI US long slotted blades": "LI US hosszú hornyolt kések",
    "Neutral Link": "Nullavezető híd",
    "PC Board Mount": "Nyomtatott áramköri szerelés",
    "Plain blades": "Sima kések",
    "Round Body Fuse": "Kerek házas biztosíték",
    "Round Body for Metric Screws Fuse": "Kerek házas biztosíték metrikus csavarokhoz",
    "Surface Mount Fuse": "SMD biztosíték",
    "Threaded plates": "Menetes lemezek",
    "TTF (Threaded Terminals)": "TTF (menetes csatlakozók)",
    "TTF French threaded terminals": "TTF francia menetes csatlakozók",
    "TTI US threaded terminals": "TTI US menetes csatlakozók",
    "Terminal": "Csatlakozó",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "AC feszültség IEC",
    "Bandwidth": "Sávszélesség",
    "Catalog Number": "Katalógusszám",
    "Current (A)": "Áram (A)",
    "DC Voltage IEC": "DC feszültség IEC",
    "Insulation voltage (V)": "Szigetelési feszültség (V)",
    "Part Number": "Cikkszám",
    "Rated Current": "Névleges áram",
    "Remote": "Táv",
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
    "DC Distribution and Battery": "DC elosztás és akkumulátorok",
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
    hu_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            hu_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + hu_paragraphs)

with open("data/pages.hu.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_hu_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            hu_page = pages_hu_by_slug.get(item["slug"])
            if hu_page:
                item["title"] = hu_page["title"]
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

with open("data/nav.hu.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.hu.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
