"""Generate Polish versions of the Product Selector data (data/nav.pl.json,
data/pages.pl.json, public/data/search-index.pl.json) from the English data
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
    "Rated voltage": "Napięcie znamionowe",
    "Size": "Rozmiar",
    "System type": "Typ układu",
    "Type": "Typ",
    "Assortment box Part Number": "Numer katalogowy zestawu asortymentowego",
    "BS type": "Typ BS",
    "Connection type": "Typ przyłącza",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Długość",
    "Number of poles": "Liczba biegunów",
    "Range": "Seria",
    "Back-up fuse": "Bezpiecznik zabezpieczający",
    "Part Number": "Numer katalogowy",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Selektor produktów",
    "Miniature fuses": "Bezpieczniki miniaturowe",
    "IEC low voltage fuses": "Bezpieczniki niskiego napięcia IEC",
    "UL/CSA low voltage fuses": "Bezpieczniki niskiego napięcia UL/CSA",
    "High-speed fuses": "Bezpieczniki szybkie",
    "IEC medium voltage fuses": "Bezpieczniki średniego napięcia IEC",
    "DC fuses": "Bezpieczniki DC",
    "Photovoltaic Applications": "Zastosowania fotowoltaiczne",
    "Surge Protection": "Ochrona przeciwprzepięciowa",
    "DC Distribution and Battery": "Dystrybucja DC i baterie",
    "Industrial DC Fuses": "Przemysłowe bezpieczniki DC",
    # subcategory / type names
    "AC Rated": "Wersja AC",
    "DC Rated": "Wersja DC",
    "BS Feeder Pillar": "Szafka zasilająca BS",
    "BS Street Lighting": "Oświetlenie uliczne BS",
    "BS1361 Standard": "Norma BS1361",
    "BS88 Standard": "Norma BS88",
    "BS88-4 Standard": "Norma BS88-4",
    "Ceramic fuses": "Bezpieczniki ceramiczne",
    "Cylindrical": "Cylindryczny",
    "Square body": "Obudowa kwadratowa",
    "DIN Back-Up for Motors": "Zabezpieczenie DIN do silników",
    "DIN D Standard": "Norma DIN D",
    "DIN D0 Standard": "Norma DIN D0",
    "DIN NH Standard": "Norma DIN NH",
    "DIN Back-Up for transformers": "Zabezpieczenie DIN do transformatorów",
    "DIN P Back-Up for transformers": "Zabezpieczenie DIN P do transformatorów",
    "DIN PD Back-Up for transformers": "Zabezpieczenie DIN PD do transformatorów",
    "DIN PT Back-Up for transformers": "Zabezpieczenie DIN PT do transformatorów",
    "DIN PTD Back-Up for transformers": "Zabezpieczenie DIN PTD do transformatorów",
    "DIN PTS Back-Up for transformers": "Zabezpieczenie DIN PTS do transformatorów",
    "Fast Acting": "Szybki",
    "Medium Acting": "Średnio zwłoczny",
    "Very Fast Acting": "Bardzo szybki",
    "Time Delay": "Zwłoczny",
    "Ferrule fuse-links Standard": "Wkładki bezpiecznikowe cylindryczne",
    "Glass fuses": "Bezpieczniki szklane",
    "House Service": "Przyłącze domowe",
    "Insulated tags": "Końcówki izolowane",
    "Non-insulated tags": "Końcówki nieizolowane",
    "MV Street Lighting Fuses For transformers": "Bezpieczniki SN oświetlenia ulicznego do transformatorów",
    "Midget": "Midget",
    "Monitoring micro-contact": "Mikrostyk sygnalizacyjny",
    "NF/UTE Back-Up fuses for transformers": "Bezpieczniki zabezpieczające NF/UTE do transformatorów",
    "Photovoltaic & Energy Storage": "Fotowoltaika i magazynowanie energii",
    "Power frequency overvoltage protection": "Ochrona przed przepięciami o częstotliwości sieciowej",
    "Protection for LED lighting": "Ochrona oświetlenia LED",
    "Protection for Power Lines": "Ochrona linii zasilających",
    "Protection for signal lines": "Ochrona linii sygnałowych",
    "With built-in trip-indicator": "Ze zintegrowanym wskaźnikiem zadziałania",
    "With indicator": "Ze wskaźnikiem",
    "With middle indicator": "Ze środkowym wskaźnikiem",
    "With separated trip-indicator": "Z oddzielnym wskaźnikiem zadziałania",
    "With stricker": "Z iglicą uderzeniową",
    "With top indicator": "Z górnym wskaźnikiem",
    "Without indicator": "Bez wskaźnika",
    "Without stricker": "Bez iglicy uderzeniowej",
    "Without trip-indicator": "Bez wskaźnika zadziałania",
    "gPV Square body fuses": "Bezpieczniki gPV o obudowie kwadratowej",
    "gPV cylindrical fuses": "Bezpieczniki gPV cylindryczne",
    "Class C": "Klasa C",
    "Class CC": "Klasa CC",
    "Class J": "Klasa J",
    "Class K5": "Klasa K5",
    "Class L": "Klasa L",
    "Class RK1": "Klasa RK1",
    "Class RK5": "Klasa RK5",
    "Class T": "Klasa T",
    "Low Voltage": "Niskie napięcie",
    "Assortment box": "Zestaw asortymentowy",
    "Forklift Battery Fuses": "Bezpieczniki do baterii wózków widłowych",
    "Protection for DC Distribution and Battery": "Ochrona dystrybucji DC i baterii",
    "Surge-Trap® Pluggable": "Surge-Trap® Wtykowy",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Wtykowy Seria STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Wtykowy Seria K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monoblok Seria STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monoblok Seria STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monoblok Seria STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Wtykowy Seria K-K1",
    # paragraph-only phrases
    "Composition of the box": "Zawartość zestawu",
    "Fuse Base": "Podstawa bezpiecznikowa",
    "Fuse required": "Wymagany bezpiecznik",
    "No back-up": "Bez zabezpieczenia",
    # resource link labels
    "Datasheet": "Karta katalogowa",
    "Microswitches": "Mikrostyk",
    "NH fuse base": "Podstawa bezpiecznikowa NH",
    "Fuse bases": "Podstawy bezpiecznikowe",
    "Fuse base": "Podstawa bezpiecznikowa",
    "BS fuse holder": "Oprawka bezpiecznikowa BS",
    "Compact fuse holder": "Kompaktowa oprawka bezpiecznikowa",
    "D fuse base": "Podstawa bezpiecznikowa D",
    "DIN D0 fuse base": "Podstawa bezpiecznikowa DIN D0",
    "Fuse holders": "Oprawki bezpiecznikowe",
    "Modular fuse holders": "Modułowe oprawki bezpiecznikowe",
    "Innozed® fuse holder": "Oprawka bezpiecznikowa Innozed®",
    "Linocur® fuse holder": "Oprawka bezpiecznikowa Linocur®",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Uchwyt",
    "Crimp Cap": "Zaciskana nasadka",
    "DIN110 (DIN110 blades)": "DIN110 (styki nożowe DIN110)",
    "DIN110 Bracket": "Uchwyt DIN110",
    "DIN110 slotted blades": "Styki nożowe rowkowane DIN110",
    "DIN80 Bracket": "Uchwyt DIN80",
    "DIN80 slotted blades": "Styki nożowe rowkowane DIN80",
    "Direct mounting": "Montaż bezpośredni",
    "EF (Bolted connections)": "EF (połączenia śrubowe)",
    "EF French slotted blades": "Francuskie styki nożowe rowkowane EF",
    "Ferrule Fuse": "Bezpiecznik z tulejką",
    "KI US short slotted blades": "Krótkie styki nożowe rowkowane US KI",
    "LI US long slotted blades": "Długie styki nożowe rowkowane US LI",
    "Neutral Link": "Zworka neutralna",
    "PC Board Mount": "Montaż na płytce drukowanej",
    "Plain blades": "Styki nożowe gładkie",
    "Round Body Fuse": "Bezpiecznik o obudowie okrągłej",
    "Round Body for Metric Screws Fuse": "Bezpiecznik o obudowie okrągłej pod śruby metryczne",
    "Surface Mount Fuse": "Bezpiecznik SMD",
    "Threaded plates": "Płytki gwintowane",
    "TTF (Threaded Terminals)": "TTF (zaciski gwintowane)",
    "TTF French threaded terminals": "Francuskie zaciski gwintowane TTF",
    "TTI US threaded terminals": "Zaciski gwintowane US TTI",
    "Terminal": "Zacisk",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "Napięcie AC IEC",
    "Bandwidth": "Pasmo",
    "Catalog Number": "Numer katalogowy",
    "Current (A)": "Prąd (A)",
    "DC Voltage IEC": "Napięcie DC IEC",
    "Insulation voltage (V)": "Napięcie izolacji (V)",
    "Part Number": "Numer katalogowy",
    "Rated Current": "Prąd znamionowy",
    "Remote": "Zdalny",
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
    "DC Distribution and Battery": "Dystrybucja DC i baterie",
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
    pl_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            pl_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + pl_paragraphs)

with open("data/pages.pl.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_pl_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            pl_page = pages_pl_by_slug.get(item["slug"])
            if pl_page:
                item["title"] = pl_page["title"]
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

with open("data/nav.pl.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.pl.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
