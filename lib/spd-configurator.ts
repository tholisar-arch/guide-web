// Recreates the PDF's "SPD Configurator" decision tree (source pages
// 757-768, "Surge Protection: Applications").
//
// Root cause of every earlier mismatch: PyMuPDF's link dict returns the
// target page of an internal ("GoTo") link 0-indexed, but every page
// number elsewhere in this codebase (breadcrumbs, entry.page, nav.json)
// is the natural 1-indexed page number. Reading a link's raw `page`
// field as if it were already 1-indexed silently landed one page early
// every time -- which also happened to make a very large fraction of
// these links look like they pointed at themselves (an off-by-one
// looks exactly like a self-link when the source page itself is at
// index target+1). Adding 1 to every internal link target here removes
// every apparent "self-link" or off-topic target in this whole section:
// each box now points at a page whose own title is an exact content
// match (e.g. Photovoltaic's "Junction Box (DC)" -> a page literally
// titled "Photovoltaic & Energy Storage", not "Protection for Power
// Lines" as the unadjusted index suggested).
//
// Each "Level 1/2/3" or "Panel Board" style answer lands on a PDF page
// that is itself a "choose your system type" sub-menu (L-N / TT / TNC /
// TNS / IT / N-PE) rather than one specific product -- true in the PDF
// too, one more click is needed there -- so those answers link to that
// subcategory's listing page on this site (verified to contain exactly
// the same set of system-type pages the PDF's own sub-menu links to).
// Where the PDF's answer is itself a single specific reference page
// (Street Lighting's Pole and Panel Board), it links there directly.

export type SpdOption = {
  label: string;
  to?: string;
  href?: string;
  external?: boolean;
};

export type SpdNode = {
  title: string;
  options: SpdOption[];
};

export const SPD_START = "hub";

export const SPD_NODES: Record<string, SpdNode> = {
  hub: {
    title: "What kind of installation is this for?",
    options: [
      { label: "Industrial", to: "industrial" },
      { label: "Commercial / Residential", to: "commercial" },
      { label: "Street Lighting", to: "street-lighting" },
      { label: "Photovoltaic", to: "photovoltaic" },
    ],
  },
  industrial: {
    title: "Industrial — installation exposure",
    options: [
      {
        label:
          "Installation with lightning protection or near an element exposed to impacts",
        to: "industrial-highly",
      },
      {
        label: "Installation supplied by overhead transmission lines",
        to: "industrial-moderate",
      },
      { label: "Installation with underground distribution", to: "industrial-basic" },
    ],
  },
  "industrial-highly": {
    title: "Industrial — Highly Protected",
    options: [
      {
        label: "Level 1: Main Panel",
        href: "/guide/selector/surge-protection/type-1plus2/protection-for-power-lines",
      },
      {
        label: "Level 2: Distribution Board (if >10m from main panel)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Level 3: Sensitive Equipment",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "industrial-moderate": {
    title: "Industrial — Moderately Protected",
    options: [
      {
        label: "Level 1: Main Panel",
        href: "/guide/selector/surge-protection/type-1plus2/protection-for-power-lines",
      },
      {
        label: "Level 2: Distribution Board (if >10m from main panel)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Level 3: Sensitive Equipment",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "industrial-basic": {
    title: "Industrial — Basic Protection",
    options: [
      {
        label: "Level 1: Main Panel",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Level 3: Sensitive Equipment",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  commercial: {
    title: "Commercial / Residential — installation exposure",
    options: [
      {
        label:
          "Installation with lightning protection or near an element exposed to impacts",
        to: "commercial-highly",
      },
      {
        label: "Installation supplied by overhead transmission lines",
        to: "commercial-moderate",
      },
      { label: "Installation with underground distribution", to: "commercial-basic" },
    ],
  },
  "commercial-highly": {
    title: "Commercial / Residential — Highly Protected",
    options: [
      {
        label: "Panel Board",
        href: "/guide/selector/surge-protection/type-1plus2/protection-for-power-lines",
      },
      {
        label: "Sensitive Equipment",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "commercial-moderate": {
    title: "Commercial / Residential — Moderately Protected",
    options: [
      {
        label: "Panel Board",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Sensitive Equipment",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "commercial-basic": {
    title: "Commercial / Residential — Basic Protection",
    options: [
      {
        label: "Panel Board",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Sensitive Equipment",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "street-lighting": {
    title: "Street Lighting",
    options: [
      {
        label: "Outdoor Luminaire Manufacturer",
        href: "https://www.mersen.com/sites/default/files/medias/PIM/files/DS-Surge-Trap-STL-T23-PP-SERIES-EN.pdf",
        external: true,
      },
      { label: "Panel Builder / Installer", to: "street-lighting-installer" },
    ],
  },
  "street-lighting-installer": {
    title: "Street Lighting — Panel Builder / Installer",
    options: [
      {
        label: "Pole",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-led-lighting/p707",
      },
      {
        label: "Panel Board",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines/p696",
      },
    ],
  },
  photovoltaic: {
    title: "Photovoltaic",
    options: [
      {
        label: "Junction Box (DC)",
        href: "/guide/selector/surge-protection/type-2/photovoltaic-and-energy-storage",
      },
      {
        label: "Distribution Board (AC)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
    ],
  },
};

// French translation of the same tree: every `to`/`href`/`external` value
// is identical to SPD_NODES above (the site's slugs don't change between
// locales - see lib/data.ts), only `title`/`label` text is translated.
export const SPD_NODES_FR: Record<string, SpdNode> = {
  hub: {
    title: "Pour quel type d'installation ?",
    options: [
      { label: "Industriel", to: "industrial" },
      { label: "Tertiaire / Résidentiel", to: "commercial" },
      { label: "Éclairage public", to: "street-lighting" },
      { label: "Photovoltaïque", to: "photovoltaic" },
    ],
  },
  industrial: {
    title: "Industriel — exposition de l'installation",
    options: [
      {
        label:
          "Installation avec protection foudre ou proche d'un élément exposé aux impacts",
        to: "industrial-highly",
      },
      {
        label: "Installation alimentée par lignes aériennes",
        to: "industrial-moderate",
      },
      { label: "Installation avec distribution souterraine", to: "industrial-basic" },
    ],
  },
  "industrial-highly": {
    title: "Industriel — Fortement protégé",
    options: [
      {
        label: "Niveau 1 : Tableau principal",
        href: "/guide/selector/surge-protection/type-1plus2/protection-for-power-lines",
      },
      {
        label: "Niveau 2 : Tableau de distribution (si >10 m du tableau principal)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Niveau 3 : Équipement sensible",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "industrial-moderate": {
    title: "Industriel — Moyennement protégé",
    options: [
      {
        label: "Niveau 1 : Tableau principal",
        href: "/guide/selector/surge-protection/type-1plus2/protection-for-power-lines",
      },
      {
        label: "Niveau 2 : Tableau de distribution (si >10 m du tableau principal)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Niveau 3 : Équipement sensible",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "industrial-basic": {
    title: "Industriel — Protection de base",
    options: [
      {
        label: "Niveau 1 : Tableau principal",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Niveau 3 : Équipement sensible",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  commercial: {
    title: "Tertiaire / Résidentiel — exposition de l'installation",
    options: [
      {
        label:
          "Installation avec protection foudre ou proche d'un élément exposé aux impacts",
        to: "commercial-highly",
      },
      {
        label: "Installation alimentée par lignes aériennes",
        to: "commercial-moderate",
      },
      { label: "Installation avec distribution souterraine", to: "commercial-basic" },
    ],
  },
  "commercial-highly": {
    title: "Tertiaire / Résidentiel — Fortement protégé",
    options: [
      {
        label: "Tableau électrique",
        href: "/guide/selector/surge-protection/type-1plus2/protection-for-power-lines",
      },
      {
        label: "Équipement sensible",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "commercial-moderate": {
    title: "Tertiaire / Résidentiel — Moyennement protégé",
    options: [
      {
        label: "Tableau électrique",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Équipement sensible",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "commercial-basic": {
    title: "Tertiaire / Résidentiel — Protection de base",
    options: [
      {
        label: "Tableau électrique",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Équipement sensible",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines",
      },
    ],
  },
  "street-lighting": {
    title: "Éclairage public",
    options: [
      {
        label: "Fabricant de luminaire extérieur",
        href: "https://www.mersen.com/sites/default/files/medias/PIM/files/DS-Surge-Trap-STL-T23-PP-SERIES-EN.pdf",
        external: true,
      },
      { label: "Tableautier / Installateur", to: "street-lighting-installer" },
    ],
  },
  "street-lighting-installer": {
    title: "Éclairage public — Tableautier / Installateur",
    options: [
      {
        label: "Mât",
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-led-lighting/p707",
      },
      {
        label: "Tableau électrique",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines/p696",
      },
    ],
  },
  photovoltaic: {
    title: "Photovoltaïque",
    options: [
      {
        label: "Boîte de jonction (DC)",
        href: "/guide/selector/surge-protection/type-2/photovoltaic-and-energy-storage",
      },
      {
        label: "Tableau de distribution (AC)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
    ],
  },
};

export function getSpdNodes(locale: "en" | "fr"): Record<string, SpdNode> {
  return locale === "fr" ? SPD_NODES_FR : SPD_NODES;
}
