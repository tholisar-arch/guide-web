"""Generate Spanish versions of the Product Selector data (data/nav.es.json,
data/pages.es.json, public/data/search-index.es.json,
public/data/xref-index.es.json) from the English data already in the repo.

Same glossary-substitution approach as extract/translate_to_fr.py (see that
file's docstring for the rationale): the catalog's breadcrumbs/labels/table
headers are repetitive technical vocabulary, not free prose, so every
distinct label/phrase/value/header is translated once here rather than via
a per-string LLM call. Product codes/part numbers and physical values
(voltages, currents, standard designators like BS88, DIN NH, gG, L-N, TT...)
are intentionally left unchanged - international/standard notation, not
English prose.

Unlike every other locale, the Spanish site excludes Surge Protection
entirely (product request from the user: no SPD Configurator, no Surge
Protection category, no surge-related cross references for Spanish) - so
this script drops every page under selector/surge-protection/... and the
"Surge Protection" nav category before translating, and also emits a
filtered xref-index.es.json with any competitor reference that maps to a
dropped Part Number removed (the base xref-index.json is shared by every
other locale and is intentionally left untouched).

Unmatched fragments pass through unchanged but are logged for review.
"""
import json
import re

# ---------- "Label: value" prefixes (value kept as-is) ----------
LABEL_DICT = {
    "Rated voltage": "Tensión asignada",
    "Size": "Tamaño",
    "System type": "Tipo de esquema",
    "Type": "Tipo",
    "Assortment box Part Number": "Referencia del estuche surtido",
    "BS type": "Tipo BS",
    "Connection type": "Tipo de conexión",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Longitud",
    "Number of poles": "Número de polos",
    "Range": "Gama",
    "Back-up fuse": "Fusible de protección aguas arriba",
    "Part Number": "Referencia",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Selector de productos",
    "Miniature fuses": "Fusibles miniatura",
    "IEC low voltage fuses": "Fusibles de baja tensión IEC",
    "UL/CSA low voltage fuses": "Fusibles de baja tensión UL/CSA",
    "High-speed fuses": "Fusibles ultrarrápidos",
    "IEC medium voltage fuses": "Fusibles de media tensión IEC",
    "DC fuses": "Fusibles DC",
    "Photovoltaic Applications": "Aplicaciones fotovoltaicas",
    "DC Distribution and Battery": "Distribución DC y baterías",
    "Industrial DC Fuses": "Fusibles DC industriales",
    # subcategory / type names
    "AC Rated": "Versión AC",
    "DC Rated": "Versión DC",
    "BS1361 Standard": "Norma BS1361",
    "BS88 Standard": "Norma BS88",
    "BS88-4 Standard": "Norma BS88-4",
    "BS Feeder Pillar": "Armario de distribución BS",
    "BS Street Lighting": "Alumbrado público BS",
    "Ceramic fuses": "Fusibles cerámicos",
    "Cylindrical": "Cilíndrico",
    "Square body": "Cuerpo cuadrado",
    "DIN Back-Up for Motors": "Protección aguas arriba DIN para motores",
    "DIN D Standard": "Norma DIN D",
    "DIN D0 Standard": "Norma DIN D0",
    "DIN NH Standard": "Norma DIN NH",
    "DIN P Back-Up for transformers": "Protección aguas arriba DIN P para transformadores",
    "DIN PD Back-Up for transformers": "Protección aguas arriba DIN PD para transformadores",
    "DIN PT Back-Up for transformers": "Protección aguas arriba DIN PT para transformadores",
    "DIN PTD Back-Up for transformers": "Protección aguas arriba DIN PTD para transformadores",
    "DIN PTS Back-Up for transformers": "Protección aguas arriba DIN PTS para transformadores",
    "Fast Acting": "Acción rápida",
    "Medium Acting": "Semirretardado",
    "Very Fast Acting": "Acción ultrarrápida",
    "Time Delay": "Retardado",
    "Ferrule fuse-links Standard": "Fusibles cilíndricos",
    "Glass fuses": "Fusibles de vidrio",
    "House Service": "Acometida individual",
    "Insulated tags": "Terminales aislados",
    "Non-insulated tags": "Terminales no aislados",
    "MV Street Lighting Fuses For transformers": "Fusibles MT de alumbrado público para transformadores",
    "Midget": "Midget",
    "Monitoring micro-contact": "Microcontacto de señalización",
    "NF/UTE Back-Up fuses for transformers": "Fusibles de protección aguas arriba NF/UTE para transformadores",
    "Photovoltaic & Energy Storage": "Fotovoltaico y almacenamiento de energía",
    "With built-in trip-indicator": "Con indicador de disparo integrado",
    "With indicator": "Con indicador",
    "With middle indicator": "Con indicador central",
    "With separated trip-indicator": "Con indicador de disparo separado",
    "With stricker": "Con percutor",
    "With top indicator": "Con indicador superior",
    "Without indicator": "Sin indicador",
    "Without stricker": "Sin percutor",
    "Without trip-indicator": "Sin indicador de disparo",
    "gPV Square body fuses": "Fusibles gPV de cuerpo cuadrado",
    "gPV cylindrical fuses": "Fusibles gPV cilíndricos",
    "Class C": "Clase C",
    "Class CC": "Clase CC",
    "Class J": "Clase J",
    "Class K5": "Clase K5",
    "Class L": "Clase L",
    "Class RK1": "Clase RK1",
    "Class RK5": "Clase RK5",
    "Class T": "Clase T",
    "Low Voltage": "Baja tensión",
    "Assortment box": "Estuche surtido",
    "Forklift Battery Fuses": "Fusibles para baterías de carretillas elevadoras",
    "Protection for DC Distribution and Battery": "Protección para distribución DC y baterías",
    # paragraph-only phrases
    "Composition of the box": "Composición del estuche",
    "Fuse Base": "Base portafusibles",
    "Fuse required": "Fusible necesario",
    "No back-up": "Sin protección aguas arriba",
    # resource link labels
    "Datasheet": "Ficha técnica",
    "Microswitches": "Microcontacto",
    "NH fuse base": "Base portafusibles NH",
    "Fuse bases": "Bases portafusibles",
    "Fuse base": "Base portafusibles",
    "BS fuse holder": "Portafusibles BS",
    "Compact fuse holder": "Portafusibles compacto",
    "D fuse base": "Base portafusibles D",
    "DIN D0 fuse base": "Base portafusibles DIN D0",
    "Fuse holders": "Portafusibles",
    "Modular fuse holders": "Portafusibles modulares",
    "Innozed® fuse holder": "Portafusibles Innozed®",
    "Linocur® fuse holder": "Portafusibles Linocur®",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Soporte",
    "Crimp Cap": "Tapa a crimpar",
    "DIN110 (DIN110 blades)": "DIN110 (cuchillas DIN110)",
    "DIN110 Bracket": "Soporte DIN110",
    "DIN110 slotted blades": "Cuchillas ranuradas DIN110",
    "DIN80 Bracket": "Soporte DIN80",
    "DIN80 slotted blades": "Cuchillas ranuradas DIN80",
    "Direct mounting": "Montaje directo",
    "EF (Bolted connections)": "EF (conexiones atornilladas)",
    "EF French slotted blades": "Cuchillas ranuradas francesas EF",
    "Ferrule Fuse": "Fusible con casquillo",
    "KI US short slotted blades": "Cuchillas ranuradas cortas US KI",
    "LI US long slotted blades": "Cuchillas ranuradas largas US LI",
    "Neutral Link": "Puente de neutro",
    "PC Board Mount": "Montaje en placa de circuito impreso",
    "Plain blades": "Cuchillas lisas",
    "Round Body Fuse": "Fusible de cuerpo redondo",
    "Round Body for Metric Screws Fuse": "Fusible de cuerpo redondo para tornillos métricos",
    "Surface Mount Fuse": "Fusible de montaje superficial",
    "Threaded plates": "Placas roscadas",
    "TTF (Threaded Terminals)": "TTF (terminales roscados)",
    "TTF French threaded terminals": "Terminales roscados franceses TTF",
    "TTI US threaded terminals": "Terminales roscados US TTI",
    "Terminal": "Terminal",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "Tensión AC IEC",
    "Catalog Number": "Referencia de catálogo",
    "Current (A)": "Corriente (A)",
    "DC Voltage IEC": "Tensión DC IEC",
    "Insulation voltage (V)": "Tensión de aislamiento (V)",
    "Part Number": "Referencia",
    "Rated Current": "Corriente asignada",
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
    "DC Distribution and Battery": "Distribución DC y baterías",
}


def translate_title(title, translated_tail):
    if title in FULL_TITLE_OVERRIDES:
        return FULL_TITLE_OVERRIDES[title]
    if translated_tail:
        return " - ".join(translated_tail)
    return title


# ---------- pages.json: drop every Surge Protection page first, then
# translate exactly like every other locale ----------
all_pages = json.load(open("data/pages.json"))
pages = [p for p in all_pages if not p["slug"].startswith("selector/surge-protection/")]
dropped_codes = set()
for p in all_pages:
    if p["slug"].startswith("selector/surge-protection/"):
        for b in p["blocks"]:
            if b["type"] == "table":
                for row in b["rows"]:
                    if row and row[0]:
                        dropped_codes.add(row[0])

for p in pages:
    new_tail = [translate_segment(s) for s in p["tail"]]
    p["title"] = translate_title(p["title"], new_tail)
    p["tail"] = new_tail
    if p.get("category"):
        p["category"] = PHRASE_DICT.get(p["category"], p["category"])
    if p.get("subcategory"):
        p["subcategory"] = PHRASE_DICT.get(p["subcategory"], p["subcategory"])

    table_cell_values = []
    es_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            es_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + es_paragraphs)

with open("data/pages.es.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json: drop the Surge Protection category, translate the rest ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_es_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            es_page = pages_es_by_slug.get(item["slug"])
            if es_page:
                item["title"] = es_page["title"]
            else:
                unmatched_log.add(f"[leaf-no-page] {item['slug']!r}")
        return
    for child in node["children"]:
        child["title"] = translate_segment(child["title"])
        translate_nav_node(child["node"])


selector = next(c for c in nav["chapters"] if c["slug"] == "selector")
selector["categories"] = [
    c for c in selector["categories"] if c["slug"] != "surge-protection"
]
for cat in selector["categories"]:
    cat["title"] = PHRASE_DICT.get(cat["title"], cat["title"])
    translate_nav_node(cat["nav"])

with open("data/nav.es.json", "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=1)

# ---------- search-index.json (only the pages that survived the drop) ----------
search_index = json.load(open("public/data/search-index.json"))
pages_by_slug = {p["slug"]: p for p in pages}
es_search_index = []
for e in search_index:
    p = pages_by_slug.get(e["slug"])
    if p:
        e["title"] = p["title"]
        e["category"] = p["category"]
        e["text"] = p["text"][:220]
        es_search_index.append(e)

with open("public/data/search-index.es.json", "w", encoding="utf-8") as f:
    json.dump(es_search_index, f, ensure_ascii=False)

# ---------- xref-index.json: drop any competitor reference that points at
# a dropped (Surge Protection) Part Number - every other locale keeps using
# the shared, un-filtered xref-index.json ----------
xref_index = json.load(open("public/data/xref-index.json"))
es_xref_index = [x for x in xref_index if x["pn"] not in dropped_codes]

with open("public/data/xref-index.es.json", "w", encoding="utf-8") as f:
    json.dump(es_xref_index, f, ensure_ascii=False)

print("done")
print(f"dropped {len(all_pages) - len(pages)} surge-protection pages")
print(
    f"xref-index.es.json: {len(es_xref_index)} entries "
    f"(dropped {len(xref_index) - len(es_xref_index)} surge-protection cross references)"
)
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
