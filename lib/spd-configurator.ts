// Recreates the PDF's "SPD Configurator" decision tree (source pages
// 757-768, "Surge Protection: Applications"). Several of the PDF's own
// internal link targets are self-referencing or point at an unrelated
// page (a leftover authoring bug in the source deck -- e.g. the
// "Industrial" box on page 757 links back to page 757 itself instead of
// page 758, which is literally titled "Surge Protection: Industrial").
// Each such case below is resolved using the destination page's own
// title as ground truth, or by elimination among its verified siblings
// when the title itself was the ambiguous one.
//
// Terminal answers that landed on a pruned PDF "choose a sub-type" page
// (no real reference table of its own) point at that subcategory's
// listing page on this site instead of a dead reference; terminal
// answers that landed on a real kept reference page link to it directly.

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
        to: "industrial-basic",
      },
      {
        label: "Installation supplied by overhead transmission lines",
        to: "industrial-highly",
      },
      { label: "Installation with underground distribution", to: "industrial-moderate" },
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
        to: "commercial-basic",
      },
      {
        label: "Installation supplied by overhead transmission lines",
        to: "commercial-highly",
      },
      { label: "Installation with underground distribution", to: "commercial-moderate" },
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
        href: "/guide/selector/surge-protection/type-2plus3/protection-for-power-lines/p706",
      },
      {
        label: "Panel Board",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines/p695",
      },
    ],
  },
  photovoltaic: {
    title: "Photovoltaic",
    options: [
      {
        label: "Junction Box (DC)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
      {
        label: "Distribution Board (AC)",
        href: "/guide/selector/surge-protection/type-2/protection-for-power-lines",
      },
    ],
  },
};
