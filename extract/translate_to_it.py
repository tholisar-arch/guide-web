"""Generate Italian versions of the Product Selector data (data/nav.it.json,
data/pages.it.json, public/data/search-index.it.json) from the English data
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
    "Rated voltage": "Tensione nominale",
    "Size": "Misura",
    "System type": "Tipo di sistema",
    "Type": "Tipo",
    "Assortment box Part Number": "Codice cofanetto assortimento",
    "BS type": "Tipo BS",
    "Connection type": "Tipo di collegamento",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Lunghezza",
    "Number of poles": "Numero di poli",
    "Range": "Gamma",
    "Back-up fuse": "Fusibile a monte",
    "Part Number": "Codice articolo",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Selettore di prodotti",
    "Miniature fuses": "Fusibili miniatura",
    "IEC low voltage fuses": "Fusibili bassa tensione IEC",
    "UL/CSA low voltage fuses": "Fusibili bassa tensione UL/CSA",
    "High-speed fuses": "Fusibili ultrarapidi",
    "IEC medium voltage fuses": "Fusibili media tensione IEC",
    "DC fuses": "Fusibili DC",
    "Photovoltaic Applications": "Applicazioni fotovoltaiche",
    "Surge Protection": "Protezione da sovratensione",
    "DC Distribution and Battery": "Distribuzione DC e batterie",
    "Industrial DC Fuses": "Fusibili DC industriali",
    # subcategory / type names
    "AC Rated": "Versione AC",
    "DC Rated": "Versione DC",
    "BS Feeder Pillar": "Armadio di derivazione BS",
    "BS Street Lighting": "Illuminazione pubblica BS",
    "BS1361 Standard": "Norma BS1361",
    "BS88 Standard": "Norma BS88",
    "BS88-4 Standard": "Norma BS88-4",
    "Ceramic fuses": "Fusibili in ceramica",
    "Cylindrical": "Cilindrico",
    "Square body": "Corpo quadrato",
    "DIN Back-Up for Motors": "DIN protezione a monte per motori",
    "DIN D Standard": "Norma DIN D",
    "DIN D0 Standard": "Norma DIN D0",
    "DIN NH Standard": "Norma DIN NH",
    "DIN Back-Up for transformers": "DIN protezione a monte per trasformatori",
    "DIN P Back-Up for transformers": "DIN P protezione a monte per trasformatori",
    "DIN PD Back-Up for transformers": "DIN PD protezione a monte per trasformatori",
    "DIN PT Back-Up for transformers": "DIN PT protezione a monte per trasformatori",
    "DIN PTD Back-Up for transformers": "DIN PTD protezione a monte per trasformatori",
    "DIN PTS Back-Up for transformers": "DIN PTS protezione a monte per trasformatori",
    "Fast Acting": "Azione rapida",
    "Medium Acting": "Semiritardato",
    "Very Fast Acting": "Azione ultra rapida",
    "Time Delay": "Ritardato",
    "Ferrule fuse-links Standard": "Fusibili cilindrici",
    "Glass fuses": "Fusibili in vetro",
    "House Service": "Allacciamento domestico",
    "Insulated tags": "Terminali isolati",
    "Non-insulated tags": "Terminali non isolati",
    "MV Street Lighting Fuses For transformers": "Fusibili MT illuminazione pubblica per trasformatori",
    "Midget": "Midget",
    "Monitoring micro-contact": "Micro-contatto di monitoraggio",
    "NF/UTE Back-Up fuses for transformers": "Fusibili NF/UTE di protezione a monte per trasformatori",
    "Photovoltaic & Energy Storage": "Fotovoltaico e accumulo di energia",
    "Power frequency overvoltage protection": "Protezione da sovratensioni a frequenza industriale",
    "Protection for LED lighting": "Protezione per illuminazione LED",
    "Protection for Power Lines": "Protezione delle linee elettriche",
    "Protection for signal lines": "Protezione delle linee di segnale",
    "With built-in trip-indicator": "Con indicatore di intervento integrato",
    "With indicator": "Con indicatore",
    "With middle indicator": "Con indicatore centrale",
    "With separated trip-indicator": "Con indicatore di intervento separato",
    "With stricker": "Con percussore",
    "With top indicator": "Con indicatore superiore",
    "Without indicator": "Senza indicatore",
    "Without stricker": "Senza percussore",
    "Without trip-indicator": "Senza indicatore di intervento",
    "gPV Square body fuses": "Fusibili gPV corpo quadrato",
    "gPV cylindrical fuses": "Fusibili gPV cilindrici",
    "Class C": "Classe C",
    "Class CC": "Classe CC",
    "Class J": "Classe J",
    "Class K5": "Classe K5",
    "Class L": "Classe L",
    "Class RK1": "Classe RK1",
    "Class RK5": "Classe RK5",
    "Class T": "Classe T",
    "Low Voltage": "Bassa tensione",
    "Assortment box": "Cofanetto assortimento",
    "Forklift Battery Fuses": "Fusibili per batterie di carrelli elevatori",
    "Protection for DC Distribution and Battery": "Protezione per distribuzione DC e batterie",
    "Surge-Trap® Pluggable": "Surge-Trap® Innestabile",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Innestabile Serie STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Innestabile Serie K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monoblocco Serie STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monoblocco Serie STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monoblocco Serie STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Innestabile Serie K-K1",
    # paragraph-only phrases
    "Composition of the box": "Composizione del cofanetto",
    "Fuse Base": "Base portafusibile",
    "Fuse required": "Fusibile richiesto",
    "No back-up": "Senza protezione a monte",
    # resource link labels
    "Datasheet": "Scheda tecnica",
    "Microswitches": "Micro-contatto",
    "NH fuse base": "Base portafusibile NH",
    "Fuse bases": "Basi portafusibile",
    "Fuse base": "Base portafusibile",
    "BS fuse holder": "Portafusibile BS",
    "Compact fuse holder": "Portafusibile compatto",
    "D fuse base": "Base portafusibile D",
    "DIN D0 fuse base": "Base portafusibile DIN D0",
    "Fuse holders": "Portafusibili",
    "Modular fuse holders": "Portafusibili modulari",
    "Innozed® fuse holder": "Portafusibile Innozed®",
    "Linocur® fuse holder": "Portafusibile Linocur®",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Staffa",
    "Crimp Cap": "A crimpare",
    "DIN110 (DIN110 blades)": "DIN110 (lame DIN110)",
    "DIN110 Bracket": "Staffa DIN110",
    "DIN110 slotted blades": "Lame scanalate DIN110",
    "DIN80 Bracket": "Staffa DIN80",
    "DIN80 slotted blades": "Lame scanalate DIN80",
    "Direct mounting": "Montaggio diretto",
    "EF (Bolted connections)": "EF (collegamenti imbullonati)",
    "EF French slotted blades": "Lame scanalate francesi EF",
    "Ferrule Fuse": "Fusibile a ferrula",
    "KI US short slotted blades": "Lame scanalate corte US KI",
    "LI US long slotted blades": "Lame scanalate lunghe US LI",
    "Neutral Link": "Barretta di neutro",
    "PC Board Mount": "Montaggio su circuito stampato",
    "Plain blades": "Lame lisce",
    "Round Body Fuse": "Fusibile corpo tondo",
    "Round Body for Metric Screws Fuse": "Fusibile corpo tondo per viti metriche",
    "Surface Mount Fuse": "Fusibile per montaggio superficiale",
    "Threaded plates": "Piastre filettate",
    "TTF (Threaded Terminals)": "TTF (terminali filettati)",
    "TTF French threaded terminals": "Terminali filettati francesi TTF",
    "TTI US threaded terminals": "Terminali filettati US TTI",
    "Terminal": "Terminale",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "Tensione AC IEC",
    "Bandwidth": "Larghezza di banda",
    "Catalog Number": "Codice a catalogo",
    "Current (A)": "Corrente (A)",
    "DC Voltage IEC": "Tensione DC IEC",
    "Insulation voltage (V)": "Tensione di isolamento (V)",
    "Part Number": "Codice articolo",
    "Rated Current": "Corrente nominale",
    "Remote": "Remoto",
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
    "DC Distribution and Battery": "Distribuzione DC e batterie",
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
    it_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            it_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + it_paragraphs)

with open("data/pages.it.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_it_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            it_page = pages_it_by_slug.get(item["slug"])
            if it_page:
                item["title"] = it_page["title"]
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

with open("data/nav.it.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.it.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
