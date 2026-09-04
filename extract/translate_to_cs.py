"""Generate Czech versions of the Product Selector data (data/nav.cs.json,
data/pages.cs.json, public/data/search-index.cs.json) from the English data
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
    "Rated voltage": "Jmenovité napětí",
    "Size": "Velikost",
    "System type": "Typ soustavy",
    "Type": "Typ",
    "Assortment box Part Number": "Katalogové číslo sady pojistek",
    "BS type": "Typ BS",
    "Connection type": "Typ připojení",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Délka",
    "Number of poles": "Počet pólů",
    "Range": "Řada",
    "Back-up fuse": "Předřadná pojistka",
    "Part Number": "Katalogové číslo",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Výběr produktů",
    "Miniature fuses": "Miniaturní pojistky",
    "IEC low voltage fuses": "Pojistky nízkého napětí IEC",
    "UL/CSA low voltage fuses": "Pojistky nízkého napětí UL/CSA",
    "High-speed fuses": "Rychlé pojistky",
    "IEC medium voltage fuses": "Pojistky vysokého napětí IEC",
    "DC fuses": "DC pojistky",
    "Photovoltaic Applications": "Fotovoltaické aplikace",
    "Surge Protection": "Přepěťová ochrana",
    "DC Distribution and Battery": "DC rozvody a baterie",
    "Industrial DC Fuses": "Průmyslové DC pojistky",
    # subcategory / type names
    "AC Rated": "Verze AC",
    "DC Rated": "Verze DC",
    "BS Feeder Pillar": "Rozvodná skříň BS",
    "BS Street Lighting": "Veřejné osvětlení BS",
    "BS1361 Standard": "Norma BS1361",
    "BS88 Standard": "Norma BS88",
    "BS88-4 Standard": "Norma BS88-4",
    "Ceramic fuses": "Keramické pojistky",
    "Cylindrical": "Válcové",
    "Square body": "Čtvercové tělo",
    "DIN Back-Up for Motors": "Předřadná pojistka DIN pro motory",
    "DIN D Standard": "Norma DIN D",
    "DIN D0 Standard": "Norma DIN D0",
    "DIN NH Standard": "Norma DIN NH",
    "DIN Back-Up for transformers": "Předřadná pojistka DIN pro transformátory",
    "DIN P Back-Up for transformers": "Předřadná pojistka DIN P pro transformátory",
    "DIN PD Back-Up for transformers": "Předřadná pojistka DIN PD pro transformátory",
    "DIN PT Back-Up for transformers": "Předřadná pojistka DIN PT pro transformátory",
    "DIN PTD Back-Up for transformers": "Předřadná pojistka DIN PTD pro transformátory",
    "DIN PTS Back-Up for transformers": "Předřadná pojistka DIN PTS pro transformátory",
    "Fast Acting": "Rychlá",
    "Medium Acting": "Středně pomalá",
    "Very Fast Acting": "Velmi rychlá",
    "Time Delay": "Pomalá",
    "Ferrule fuse-links Standard": "Válcové pojistkové vložky",
    "Glass fuses": "Skleněné pojistky",
    "House Service": "Domovní přípojka",
    "Insulated tags": "Izolované koncovky",
    "Non-insulated tags": "Neizolované koncovky",
    "MV Street Lighting Fuses For transformers": "Pojistky VN veřejného osvětlení pro transformátory",
    "Midget": "Midget",
    "Monitoring micro-contact": "Signalizační mikrospínač",
    "NF/UTE Back-Up fuses for transformers": "Předřadné pojistky NF/UTE pro transformátory",
    "Photovoltaic & Energy Storage": "Fotovoltaika a akumulace energie",
    "Power frequency overvoltage protection": "Ochrana proti přepětí síťového kmitočtu",
    "Protection for LED lighting": "Ochrana pro LED osvětlení",
    "Protection for Power Lines": "Ochrana napájecích vedení",
    "Protection for signal lines": "Ochrana signálových vedení",
    "With built-in trip-indicator": "S integrovanou signalizací vybavení",
    "With indicator": "S indikátorem",
    "With middle indicator": "Se středovým indikátorem",
    "With separated trip-indicator": "S oddělenou signalizací vybavení",
    "With stricker": "S úderníkem",
    "With top indicator": "S horním indikátorem",
    "Without indicator": "Bez indikátoru",
    "Without stricker": "Bez úderníku",
    "Without trip-indicator": "Bez signalizace vybavení",
    "gPV Square body fuses": "Pojistky gPV se čtvercovým tělem",
    "gPV cylindrical fuses": "Válcové pojistky gPV",
    "Class C": "Třída C",
    "Class CC": "Třída CC",
    "Class J": "Třída J",
    "Class K5": "Třída K5",
    "Class L": "Třída L",
    "Class RK1": "Třída RK1",
    "Class RK5": "Třída RK5",
    "Class T": "Třída T",
    "Low Voltage": "Nízké napětí",
    "Assortment box": "Sada pojistek",
    "Forklift Battery Fuses": "Pojistky pro baterie vysokozdvižných vozíků",
    "Protection for DC Distribution and Battery": "Ochrana pro DC rozvody a baterie",
    "Surge-Trap® Pluggable": "Surge-Trap® Zásuvný",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Zásuvný Řada STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Zásuvný Řada K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monoblok Řada STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monoblok Řada STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monoblok Řada STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Zásuvný Řada K-K1",
    # paragraph-only phrases
    "Composition of the box": "Obsah sady",
    "Fuse Base": "Pojistková patice",
    "Fuse required": "Požadovaná pojistka",
    "No back-up": "Bez předřadné pojistky",
    # resource link labels
    "Datasheet": "Datový list",
    "Microswitches": "Mikrospínač",
    "NH fuse base": "Pojistková patice NH",
    "Fuse bases": "Pojistkové patice",
    "Fuse base": "Pojistková patice",
    "BS fuse holder": "Pojistkový držák BS",
    "Compact fuse holder": "Kompaktní pojistkový držák",
    "D fuse base": "Pojistková patice D",
    "DIN D0 fuse base": "Pojistková patice DIN D0",
    "Fuse holders": "Pojistkové držáky",
    "Modular fuse holders": "Modulární pojistkové držáky",
    "Innozed® fuse holder": "Pojistkový držák Innozed®",
    "Linocur® fuse holder": "Pojistkový držák Linocur®",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Držák",
    "Crimp Cap": "Lisovaná krytka",
    "DIN110 (DIN110 blades)": "DIN110 (nože DIN110)",
    "DIN110 Bracket": "Držák DIN110",
    "DIN110 slotted blades": "Drážkované nože DIN110",
    "DIN80 Bracket": "Držák DIN80",
    "DIN80 slotted blades": "Drážkované nože DIN80",
    "Direct mounting": "Přímá montáž",
    "EF (Bolted connections)": "EF (šroubové spoje)",
    "EF French slotted blades": "Francouzské drážkované nože EF",
    "Ferrule Fuse": "Pojistka s objímkou",
    "KI US short slotted blades": "Krátké drážkované nože US KI",
    "LI US long slotted blades": "Dlouhé drážkované nože US LI",
    "Neutral Link": "Nulový můstek",
    "PC Board Mount": "Montáž na desku plošných spojů",
    "Plain blades": "Hladké nože",
    "Round Body Fuse": "Pojistka s kulatým tělem",
    "Round Body for Metric Screws Fuse": "Pojistka s kulatým tělem pro metrické šrouby",
    "Surface Mount Fuse": "SMD pojistka",
    "Threaded plates": "Závitové destičky",
    "TTF (Threaded Terminals)": "TTF (závitové svorky)",
    "TTF French threaded terminals": "Francouzské závitové svorky TTF",
    "TTI US threaded terminals": "Závitové svorky US TTI",
    "Terminal": "Svorka",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "Napětí AC IEC",
    "Bandwidth": "Šířka pásma",
    "Catalog Number": "Katalogové číslo",
    "Current (A)": "Proud (A)",
    "DC Voltage IEC": "Napětí DC IEC",
    "Insulation voltage (V)": "Izolační napětí (V)",
    "Part Number": "Katalogové číslo",
    "Rated Current": "Jmenovitý proud",
    "Remote": "Dálkový kontakt",
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
    "DC Distribution and Battery": "DC rozvody a baterie",
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
    cs_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            cs_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + cs_paragraphs)

with open("data/pages.cs.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_cs_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            cs_page = pages_cs_by_slug.get(item["slug"])
            if cs_page:
                item["title"] = cs_page["title"]
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

with open("data/nav.cs.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.cs.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
