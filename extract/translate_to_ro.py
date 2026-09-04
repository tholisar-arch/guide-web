"""Generate Romanian versions of the Product Selector data (data/nav.ro.json,
data/pages.ro.json, public/data/search-index.ro.json) from the English data
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
    "Rated voltage": "Tensiune nominală",
    "Size": "Dimensiune",
    "System type": "Tip de sistem",
    "Type": "Tip",
    "Assortment box Part Number": "Cod cutie de asortiment",
    "BS type": "Tip BS",
    "Connection type": "Tip de conexiune",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Lungime",
    "Number of poles": "Număr de poli",
    "Range": "Gamă",
    "Back-up fuse": "Siguranță de protecție amonte",
    "Part Number": "Cod produs",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Selector de produse",
    "Miniature fuses": "Siguranțe miniaturale",
    "IEC low voltage fuses": "Siguranțe de joasă tensiune IEC",
    "UL/CSA low voltage fuses": "Siguranțe de joasă tensiune UL/CSA",
    "High-speed fuses": "Siguranțe ultrarapide",
    "IEC medium voltage fuses": "Siguranțe de medie tensiune IEC",
    "DC fuses": "Siguranțe DC",
    "Photovoltaic Applications": "Aplicații fotovoltaice",
    "Surge Protection": "Protecție la supratensiuni",
    "DC Distribution and Battery": "Distribuție DC și baterii",
    "Industrial DC Fuses": "Siguranțe DC industriale",
    # subcategory / type names
    "AC Rated": "Versiune AC",
    "DC Rated": "Versiune DC",
    "BS Feeder Pillar": "Dulap de distribuție BS",
    "BS Street Lighting": "Iluminat stradal BS",
    "BS1361 Standard": "Standard BS1361",
    "BS88 Standard": "Standard BS88",
    "BS88-4 Standard": "Standard BS88-4",
    "Ceramic fuses": "Siguranțe ceramice",
    "Cylindrical": "Cilindric",
    "Square body": "Corp pătrat",
    "DIN Back-Up for Motors": "Protecție amonte DIN pentru motoare",
    "DIN D Standard": "Standard DIN D",
    "DIN D0 Standard": "Standard DIN D0",
    "DIN NH Standard": "Standard DIN NH",
    "DIN Back-Up for transformers": "Protecție amonte DIN pentru transformatoare",
    "DIN P Back-Up for transformers": "Protecție amonte DIN P pentru transformatoare",
    "DIN PD Back-Up for transformers": "Protecție amonte DIN PD pentru transformatoare",
    "DIN PT Back-Up for transformers": "Protecție amonte DIN PT pentru transformatoare",
    "DIN PTD Back-Up for transformers": "Protecție amonte DIN PTD pentru transformatoare",
    "DIN PTS Back-Up for transformers": "Protecție amonte DIN PTS pentru transformatoare",
    "Fast Acting": "Acțiune rapidă",
    "Medium Acting": "Semitemporizat",
    "Very Fast Acting": "Acțiune ultrarapidă",
    "Time Delay": "Temporizat",
    "Ferrule fuse-links Standard": "Siguranțe cilindrice",
    "Glass fuses": "Siguranțe din sticlă",
    "House Service": "Branșament individual",
    "Insulated tags": "Papuci izolați",
    "Non-insulated tags": "Papuci neizolați",
    "MV Street Lighting Fuses For transformers": "Siguranțe MT iluminat stradal pentru transformatoare",
    "Midget": "Midget",
    "Monitoring micro-contact": "Micro-contact de semnalizare",
    "NF/UTE Back-Up fuses for transformers": "Siguranțe de protecție amonte NF/UTE pentru transformatoare",
    "Photovoltaic & Energy Storage": "Fotovoltaic și stocare de energie",
    "Power frequency overvoltage protection": "Protecție la supratensiuni de frecvență industrială",
    "Protection for LED lighting": "Protecție pentru iluminat LED",
    "Protection for Power Lines": "Protecția liniilor electrice",
    "Protection for signal lines": "Protecția liniilor de semnal",
    "With built-in trip-indicator": "Cu indicator de declanșare integrat",
    "With indicator": "Cu indicator",
    "With middle indicator": "Cu indicator central",
    "With separated trip-indicator": "Cu indicator de declanșare separat",
    "With stricker": "Cu percutor",
    "With top indicator": "Cu indicator superior",
    "Without indicator": "Fără indicator",
    "Without stricker": "Fără percutor",
    "Without trip-indicator": "Fără indicator de declanșare",
    "gPV Square body fuses": "Siguranțe gPV cu corp pătrat",
    "gPV cylindrical fuses": "Siguranțe gPV cilindrice",
    "Class C": "Clasa C",
    "Class CC": "Clasa CC",
    "Class J": "Clasa J",
    "Class K5": "Clasa K5",
    "Class L": "Clasa L",
    "Class RK1": "Clasa RK1",
    "Class RK5": "Clasa RK5",
    "Class T": "Clasa T",
    "Low Voltage": "Joasă tensiune",
    "Assortment box": "Cutie de asortiment",
    "Forklift Battery Fuses": "Siguranțe pentru baterii de stivuitoare",
    "Protection for DC Distribution and Battery": "Protecție pentru distribuție DC și baterii",
    "Surge-Trap® Pluggable": "Surge-Trap® Conectabil",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Conectabil Seria STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Conectabil Seria K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monobloc Seria STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monobloc Seria STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monobloc Seria STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Conectabil Seria K-K1",
    # paragraph-only phrases
    "Composition of the box": "Componența cutiei",
    "Fuse Base": "Soclu de siguranță",
    "Fuse required": "Siguranță necesară",
    "No back-up": "Fără protecție amonte",
    # resource link labels
    "Datasheet": "Fișă tehnică",
    "Microswitches": "Micro-contact",
    "NH fuse base": "Soclu de siguranță NH",
    "Fuse bases": "Socluri de siguranțe",
    "Fuse base": "Soclu de siguranță",
    "BS fuse holder": "Suport de siguranță BS",
    "Compact fuse holder": "Suport de siguranță compact",
    "D fuse base": "Soclu de siguranță D",
    "DIN D0 fuse base": "Soclu de siguranță DIN D0",
    "Fuse holders": "Suporturi de siguranțe",
    "Modular fuse holders": "Suporturi modulare de siguranțe",
    "Innozed® fuse holder": "Suport de siguranță Innozed®",
    "Linocur® fuse holder": "Suport de siguranță Linocur®",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Suport",
    "Crimp Cap": "Capac sertizat",
    "DIN110 (DIN110 blades)": "DIN110 (lame DIN110)",
    "DIN110 Bracket": "Suport DIN110",
    "DIN110 slotted blades": "Lame canelate DIN110",
    "DIN80 Bracket": "Suport DIN80",
    "DIN80 slotted blades": "Lame canelate DIN80",
    "Direct mounting": "Montare directă",
    "EF (Bolted connections)": "EF (conexiuni cu șurub)",
    "EF French slotted blades": "Lame canelate franceze EF",
    "Ferrule Fuse": "Siguranță cu manșon",
    "KI US short slotted blades": "Lame canelate scurte US KI",
    "LI US long slotted blades": "Lame canelate lungi US LI",
    "Neutral Link": "Punte de nul",
    "PC Board Mount": "Montare pe placă de circuit imprimat",
    "Plain blades": "Lame netede",
    "Round Body Fuse": "Siguranță cu corp rotund",
    "Round Body for Metric Screws Fuse": "Siguranță cu corp rotund pentru șuruburi metrice",
    "Surface Mount Fuse": "Siguranță pentru montare pe suprafață",
    "Threaded plates": "Plăci filetate",
    "TTF (Threaded Terminals)": "TTF (borne filetate)",
    "TTF French threaded terminals": "Borne filetate franceze TTF",
    "TTI US threaded terminals": "Borne filetate US TTI",
    "Terminal": "Bornă",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "Tensiune AC IEC",
    "Bandwidth": "Lățime de bandă",
    "Catalog Number": "Cod de catalog",
    "Current (A)": "Curent (A)",
    "DC Voltage IEC": "Tensiune DC IEC",
    "Insulation voltage (V)": "Tensiune de izolație (V)",
    "Part Number": "Cod produs",
    "Rated Current": "Curent nominal",
    "Remote": "Telecomandă",
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
    "DC Distribution and Battery": "Distribuție DC și baterii",
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
    ro_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            ro_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + ro_paragraphs)

with open("data/pages.ro.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_ro_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            ro_page = pages_ro_by_slug.get(item["slug"])
            if ro_page:
                item["title"] = ro_page["title"]
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

with open("data/nav.ro.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.ro.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
