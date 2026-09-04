"""Generate German versions of the Product Selector data (data/nav.de.json,
data/pages.de.json, public/data/search-index.de.json) from the English data
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
    "Rated voltage": "Bemessungsspannung",
    "Size": "Größe",
    "System type": "Systemtyp",
    "Type": "Typ",
    "Assortment box Part Number": "Artikelnummer Sortimentskasten",
    "BS type": "BS-Typ",
    "Connection type": "Anschlussart",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Länge",
    "Number of poles": "Polzahl",
    "Range": "Baureihe",
    "Back-up fuse": "Vorsicherung",
    "Part Number": "Artikelnummer",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Produktselektor",
    "Miniature fuses": "Feinsicherungen",
    "IEC low voltage fuses": "IEC-Niederspannungssicherungen",
    "UL/CSA low voltage fuses": "UL/CSA-Niederspannungssicherungen",
    "High-speed fuses": "Halbleiterschutzsicherungen",
    "IEC medium voltage fuses": "IEC-Mittelspannungssicherungen",
    "DC fuses": "DC-Sicherungen",
    "Photovoltaic Applications": "Photovoltaik-Anwendungen",
    "Surge Protection": "Überspannungsschutz",
    "DC Distribution and Battery": "DC-Verteilung und Batterien",
    "Industrial DC Fuses": "Industrielle DC-Sicherungen",
    # subcategory / type names
    "AC Rated": "AC-Ausführung",
    "DC Rated": "DC-Ausführung",
    "BS Feeder Pillar": "BS-Kabelverteilerschrank",
    "BS Street Lighting": "BS-Straßenbeleuchtung",
    "BS1361 Standard": "Norm BS1361",
    "BS88 Standard": "Norm BS88",
    "BS88-4 Standard": "Norm BS88-4",
    "Ceramic fuses": "Keramiksicherungen",
    "Cylindrical": "Zylindrisch",
    "Square body": "Quadratisches Gehäuse",
    "DIN Back-Up for Motors": "DIN-Vorsicherung für Motoren",
    "DIN D Standard": "Norm DIN D",
    "DIN D0 Standard": "Norm DIN D0",
    "DIN NH Standard": "Norm DIN NH",
    "DIN Back-Up for transformers": "DIN Vorsicherung für Transformatoren",
    "DIN P Back-Up for transformers": "DIN P Vorsicherung für Transformatoren",
    "DIN PD Back-Up for transformers": "DIN PD Vorsicherung für Transformatoren",
    "DIN PT Back-Up for transformers": "DIN PT Vorsicherung für Transformatoren",
    "DIN PTD Back-Up for transformers": "DIN PTD Vorsicherung für Transformatoren",
    "DIN PTS Back-Up for transformers": "DIN PTS Vorsicherung für Transformatoren",
    "Fast Acting": "Flink",
    "Medium Acting": "Mittelträge",
    "Very Fast Acting": "Superflink",
    "Time Delay": "Träge",
    "Ferrule fuse-links Standard": "Zylindrische Sicherungseinsätze",
    "Glass fuses": "Glassicherungen",
    "House Service": "Hausanschluss",
    "Insulated tags": "Isolierte Anschlussfahnen",
    "Non-insulated tags": "Nicht isolierte Anschlussfahnen",
    "MV Street Lighting Fuses For transformers": "MS-Straßenbeleuchtungssicherungen für Transformatoren",
    "Midget": "Midget",
    "Monitoring micro-contact": "Überwachungs-Mikroschalter",
    "NF/UTE Back-Up fuses for transformers": "NF/UTE-Vorsicherungen für Transformatoren",
    "Photovoltaic & Energy Storage": "Photovoltaik und Energiespeicher",
    "Power frequency overvoltage protection": "Überspannungsschutz bei Netzfrequenz",
    "Protection for LED lighting": "Schutz für LED-Beleuchtung",
    "Protection for Power Lines": "Schutz für Stromleitungen",
    "Protection for signal lines": "Schutz für Signalleitungen",
    "With built-in trip-indicator": "Mit eingebauter Auslöseanzeige",
    "With indicator": "Mit Anzeige",
    "With middle indicator": "Mit mittlerer Anzeige",
    "With separated trip-indicator": "Mit separater Auslöseanzeige",
    "With stricker": "Mit Schlagstift",
    "With top indicator": "Mit oberer Anzeige",
    "Without indicator": "Ohne Anzeige",
    "Without stricker": "Ohne Schlagstift",
    "Without trip-indicator": "Ohne Auslöseanzeige",
    "gPV Square body fuses": "gPV-Sicherungen mit quadratischem Gehäuse",
    "gPV cylindrical fuses": "gPV-Sicherungen zylindrisch",
    "Class C": "Klasse C",
    "Class CC": "Klasse CC",
    "Class J": "Klasse J",
    "Class K5": "Klasse K5",
    "Class L": "Klasse L",
    "Class RK1": "Klasse RK1",
    "Class RK5": "Klasse RK5",
    "Class T": "Klasse T",
    "Low Voltage": "Niederspannung",
    "Assortment box": "Sortimentskasten",
    "Forklift Battery Fuses": "Sicherungen für Gabelstaplerbatterien",
    "Protection for DC Distribution and Battery": "Schutz für DC-Verteilung und Batterien",
    "Surge-Trap® Pluggable": "Surge-Trap® Steckbar",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Steckbar Serie STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Steckbar Serie K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monoblock Serie STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monoblock Serie STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monoblock Serie STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Steckbar Serie K-K1",
    # paragraph-only phrases
    "Composition of the box": "Zusammensetzung des Sets",
    "Fuse Base": "Sicherungssockel",
    "Fuse required": "Erforderliche Sicherung",
    "No back-up": "Ohne Vorsicherung",
    # resource link labels
    "Datasheet": "Datenblatt",
    "Microswitches": "Mikroschalter",
    "NH fuse base": "NH-Sicherungssockel",
    "Fuse bases": "Sicherungssockel",
    "Fuse base": "Sicherungssockel",
    "BS fuse holder": "BS-Sicherungshalter",
    "Compact fuse holder": "Kompakter Sicherungshalter",
    "D fuse base": "D-Sicherungssockel",
    "DIN D0 fuse base": "DIN D0-Sicherungssockel",
    "Fuse holders": "Sicherungshalter",
    "Modular fuse holders": "Modulare Sicherungshalter",
    "Innozed® fuse holder": "Innozed®-Sicherungshalter",
    "Linocur® fuse holder": "Linocur®-Sicherungshalter",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Halterung",
    "Crimp Cap": "Crimpkappe",
    "DIN110 (DIN110 blades)": "DIN110 (DIN110-Messer)",
    "DIN110 Bracket": "DIN110-Halterung",
    "DIN110 slotted blades": "DIN110 Schlitzmesser",
    "DIN80 Bracket": "DIN80-Halterung",
    "DIN80 slotted blades": "DIN80 Schlitzmesser",
    "Direct mounting": "Direktmontage",
    "EF (Bolted connections)": "EF (Schraubanschlüsse)",
    "EF French slotted blades": "EF französische Schlitzmesser",
    "Ferrule Fuse": "Sicherung mit Kontaktkappen",
    "KI US short slotted blades": "KI US kurze Schlitzmesser",
    "LI US long slotted blades": "LI US lange Schlitzmesser",
    "Neutral Link": "Neutralleiterbrücke",
    "PC Board Mount": "Leiterplattenmontage",
    "Plain blades": "Glatte Messer",
    "Round Body Fuse": "Sicherung mit rundem Gehäuse",
    "Round Body for Metric Screws Fuse": "Sicherung rundes Gehäuse für metrische Schrauben",
    "Surface Mount Fuse": "SMD-Sicherung",
    "Threaded plates": "Gewindeplatten",
    "TTF (Threaded Terminals)": "TTF (Gewindeanschlüsse)",
    "TTF French threaded terminals": "TTF französische Gewindeanschlüsse",
    "TTI US threaded terminals": "TTI US-Gewindeanschlüsse",
    "Terminal": "Anschluss",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "AC-Spannung IEC",
    "Bandwidth": "Bandbreite",
    "Catalog Number": "Katalognummer",
    "Current (A)": "Strom (A)",
    "DC Voltage IEC": "DC-Spannung IEC",
    "Insulation voltage (V)": "Isolationsspannung (V)",
    "Part Number": "Artikelnummer",
    "Rated Current": "Bemessungsstrom",
    "Remote": "Fernmeldekontakt",
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
    "DC Distribution and Battery": "DC-Verteilung und Batterien",
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
    de_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            de_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + de_paragraphs)

with open("data/pages.de.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_de_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            de_page = pages_de_by_slug.get(item["slug"])
            if de_page:
                item["title"] = de_page["title"]
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

with open("data/nav.de.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.de.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
