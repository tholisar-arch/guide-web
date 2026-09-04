"""Generate Portuguese versions of the Product Selector data (data/nav.pt.json,
data/pages.pt.json, public/data/search-index.pt.json) from the English data
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
    "Rated voltage": "Tensão nominal",
    "Size": "Tamanho",
    "System type": "Tipo de sistema",
    "Type": "Tipo",
    "Assortment box Part Number": "Referência da caixa de sortido",
    "BS type": "Tipo BS",
    "Connection type": "Tipo de ligação",
    "IL": "IL",
    "Icc": "Icc",
    "Iimp (10/350)": "Iimp (10/350)",
    "Imax (8/20)": "Imax (8/20)",
    "In (8/20)": "In (8/20)",
    "Length": "Comprimento",
    "Number of poles": "Número de polos",
    "Range": "Gama",
    "Back-up fuse": "Fusível de proteção a montante",
    "Part Number": "Referência",
}

# ---------- standalone phrases (exact match, whole segment) ----------
PHRASE_DICT = {
    # top-level categories / chapter
    "Product Selector": "Seletor de produtos",
    "Miniature fuses": "Fusíveis miniatura",
    "IEC low voltage fuses": "Fusíveis de baixa tensão IEC",
    "UL/CSA low voltage fuses": "Fusíveis de baixa tensão UL/CSA",
    "High-speed fuses": "Fusíveis ultrarrápidos",
    "IEC medium voltage fuses": "Fusíveis de média tensão IEC",
    "DC fuses": "Fusíveis DC",
    "Photovoltaic Applications": "Aplicações fotovoltaicas",
    "Surge Protection": "Proteção contra sobretensões",
    "DC Distribution and Battery": "Distribuição DC e baterias",
    "Industrial DC Fuses": "Fusíveis DC industriais",
    # subcategory / type names
    "AC Rated": "Versão AC",
    "DC Rated": "Versão DC",
    "BS Feeder Pillar": "Armário de distribuição BS",
    "BS Street Lighting": "Iluminação pública BS",
    "BS1361 Standard": "Norma BS1361",
    "BS88 Standard": "Norma BS88",
    "BS88-4 Standard": "Norma BS88-4",
    "Ceramic fuses": "Fusíveis cerâmicos",
    "Cylindrical": "Cilíndrico",
    "Square body": "Corpo quadrado",
    "DIN Back-Up for Motors": "Proteção a montante DIN para motores",
    "DIN D Standard": "Norma DIN D",
    "DIN D0 Standard": "Norma DIN D0",
    "DIN NH Standard": "Norma DIN NH",
    "DIN P Back-Up for transformers": "Proteção a montante DIN P para transformadores",
    "DIN PD Back-Up for transformers": "Proteção a montante DIN PD para transformadores",
    "DIN PT Back-Up for transformers": "Proteção a montante DIN PT para transformadores",
    "DIN PTD Back-Up for transformers": "Proteção a montante DIN PTD para transformadores",
    "DIN PTS Back-Up for transformers": "Proteção a montante DIN PTS para transformadores",
    "Fast Acting": "Ação rápida",
    "Medium Acting": "Semirretardado",
    "Very Fast Acting": "Ação ultrarrápida",
    "Time Delay": "Retardado",
    "Ferrule fuse-links Standard": "Fusíveis cilíndricos",
    "Glass fuses": "Fusíveis de vidro",
    "House Service": "Ramal individual",
    "Insulated tags": "Terminais isolados",
    "Non-insulated tags": "Terminais não isolados",
    "MV Street Lighting Fuses For transformers": "Fusíveis MT de iluminação pública para transformadores",
    "Midget": "Midget",
    "Monitoring micro-contact": "Micro-contacto de monitorização",
    "NF/UTE Back-Up fuses for transformers": "Fusíveis de proteção a montante NF/UTE para transformadores",
    "Photovoltaic & Energy Storage": "Fotovoltaico e armazenamento de energia",
    "Power frequency overvoltage protection": "Proteção contra sobretensões à frequência industrial",
    "Protection for LED lighting": "Proteção para iluminação LED",
    "Protection for Power Lines": "Proteção de linhas elétricas",
    "Protection for signal lines": "Proteção de linhas de sinal",
    "With built-in trip-indicator": "Com indicador de disparo integrado",
    "With indicator": "Com indicador",
    "With middle indicator": "Com indicador central",
    "With separated trip-indicator": "Com indicador de disparo separado",
    "With stricker": "Com percutor",
    "With top indicator": "Com indicador superior",
    "Without indicator": "Sem indicador",
    "Without stricker": "Sem percutor",
    "Without trip-indicator": "Sem indicador de disparo",
    "gPV Square body fuses": "Fusíveis gPV de corpo quadrado",
    "gPV cylindrical fuses": "Fusíveis gPV cilíndricos",
    "Class C": "Classe C",
    "Class CC": "Classe CC",
    "Class J": "Classe J",
    "Class K5": "Classe K5",
    "Class L": "Classe L",
    "Class RK1": "Classe RK1",
    "Class RK5": "Classe RK5",
    "Class T": "Classe T",
    "Low Voltage": "Baixa tensão",
    "Assortment box": "Caixa de sortido",
    "Forklift Battery Fuses": "Fusíveis para baterias de empilhadoras",
    "Protection for DC Distribution and Battery": "Proteção para distribuição DC e baterias",
    "Surge-Trap® Pluggable": "Surge-Trap® Enfichável",
    "Surge-Trap® Pluggable STPT Series": "Surge-Trap® Enfichável Série STPT",
    "Surge-Trap® Pluggable K–K2 Series": "Surge-Trap® Enfichável Série K–K2",
    "Surge-Trap® Monobloc STMT Series": "Surge-Trap® Monobloco Série STMT",
    "Surge-Trap® Monobloc STET Series": "Surge-Trap® Monobloco Série STET",
    "Surge-Trap® Monobloc STPT Series": "Surge-Trap® Monobloco Série STPT",
    "Surge-Trap® Pluggable K-K1 Series": "Surge-Trap® Enfichável Série K-K1",
    # paragraph-only phrases
    "Composition of the box": "Composição da caixa",
    "Fuse Base": "Base porta-fusível",
    "Fuse required": "Fusível necessário",
    "No back-up": "Sem proteção a montante",
    # resource link labels
    "Datasheet": "Ficha técnica",
    "Microswitches": "Micro-contacto",
    "NH fuse base": "Base porta-fusível NH",
    "Fuse bases": "Bases porta-fusível",
    "Fuse base": "Base porta-fusível",
    "BS fuse holder": "Porta-fusível BS",
    "Compact fuse holder": "Porta-fusível compacto",
    "D fuse base": "Base porta-fusível D",
    "DIN D0 fuse base": "Base porta-fusível DIN D0",
    "Fuse holders": "Porta-fusíveis",
    "Modular fuse holders": "Porta-fusíveis modulares",
    "Innozed® fuse holder": "Porta-fusível Innozed®",
    "Linocur® fuse holder": "Porta-fusível Linocur®",
}

# ---------- "Label: value" values that are real English words rather than
# a standard code/designator (IEC categories like gG/aM/aR, grounding
# schemes like TT/TNC, BS/DIN designators, part numbers, ... are left
# untouched deliberately: international standard notation, not prose) ----------
VALUE_DICT = {
    "Bracket": "Suporte",
    "Crimp Cap": "Tampa de crimpar",
    "DIN110 (DIN110 blades)": "DIN110 (lâminas DIN110)",
    "DIN110 Bracket": "Suporte DIN110",
    "DIN110 slotted blades": "Lâminas ranhuradas DIN110",
    "DIN80 Bracket": "Suporte DIN80",
    "DIN80 slotted blades": "Lâminas ranhuradas DIN80",
    "Direct mounting": "Montagem direta",
    "EF (Bolted connections)": "EF (ligações aparafusadas)",
    "EF French slotted blades": "Lâminas ranhuradas francesas EF",
    "Ferrule Fuse": "Fusível com casquilho",
    "KI US short slotted blades": "Lâminas ranhuradas curtas US KI",
    "LI US long slotted blades": "Lâminas ranhuradas longas US LI",
    "Neutral Link": "Ponte de neutro",
    "PC Board Mount": "Montagem em placa de circuito impresso",
    "Plain blades": "Lâminas lisas",
    "Round Body Fuse": "Fusível de corpo redondo",
    "Round Body for Metric Screws Fuse": "Fusível de corpo redondo para parafusos métricos",
    "Surface Mount Fuse": "Fusível de montagem superficial",
    "Threaded plates": "Placas roscadas",
    "TTF (Threaded Terminals)": "TTF (terminais roscados)",
    "TTF French threaded terminals": "Terminais roscados franceses TTF",
    "TTI US threaded terminals": "Terminais roscados US TTI",
    "Terminal": "Terminal",
}

TABLE_HEADER_DICT = {
    "AC Voltage IEC": "Tensão AC IEC",
    "Bandwidth": "Largura de banda",
    "Catalog Number": "Referência de catálogo",
    "Current (A)": "Corrente (A)",
    "DC Voltage IEC": "Tensão DC IEC",
    "Insulation voltage (V)": "Tensão de isolamento (V)",
    "Part Number": "Referência",
    "Rated Current": "Corrente nominal",
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
    "DC Distribution and Battery": "Distribuição DC e baterias",
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
    pt_paragraphs = []
    for b in p["blocks"]:
        if b["type"] == "table":
            if b["headers"]:
                b["headers"] = [translate_header(h) for h in b["headers"]]
            for row in b["rows"]:
                table_cell_values.extend(v for v in row if v)
        elif b["type"] == "paragraph":
            b["text"] = translate_paragraph(b["text"])
            pt_paragraphs.append(b["text"])
    for rl in p.get("resourceLinks", []):
        rl["label"] = translate_resource_label(rl["label"])

    p["text"] = "\n".join(table_cell_values + pt_paragraphs)

with open("data/pages.pt.json", "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False)

# ---------- nav.json ----------
nav = json.load(open("data/nav.json"))
for chapter in nav["chapters"]:
    if chapter["slug"] == "selector":
        chapter["title"] = PHRASE_DICT.get(chapter["title"], chapter["title"])

pages_pt_by_slug = {p["slug"]: p for p in pages}


def translate_nav_node(node):
    if node["type"] == "leaves":
        for item in node["items"]:
            pt_page = pages_pt_by_slug.get(item["slug"])
            if pt_page:
                item["title"] = pt_page["title"]
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

with open("data/nav.pt.json", "w", encoding="utf-8") as f:
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

with open("public/data/search-index.pt.json", "w", encoding="utf-8") as f:
    json.dump(search_index, f, ensure_ascii=False)

print("done")
if unmatched_log:
    print(f"\n{len(unmatched_log)} unmatched fragment(s) to review:")
    for u in sorted(unmatched_log):
        print(" ", u)
