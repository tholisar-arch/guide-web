import type { Locale } from "@/lib/i18n";

export type ContactCountry = {
  key: string;
  label: string;
  email: string;
};

const UK_IRELAND = "naomi.cuff@mersen.com";
const NETHERLANDS = "sunil.ramsoedit@mersen.com";
const BELGIUM_LUX = "fabien.buisseret@mersen.com";
const FRANCE = "nordine.souar@mersen.com";
const ITALY = "stefano.paolini@mersen.com";
const SPAIN = "almudena.herranz@mersen.com";
const PORTUGAL = "sergio.jimenez@mersen.com";
const NORDICS_BALTICS = "afshin.pourarsalan@mersen.com";
const FINLAND = "ville.honka@mersen.com";
const GERMANY = "torsten.frank@mersen.com";
const OTHER = "karoly.galle@mersen.com";

// Every sovereign state of Europe, each mapped to its own contact.
// Countries not covered by a named contact route to OTHER.
const COUNTRIES: {
  key: string;
  email: string;
  en: string;
  fr: string;
  it: string;
  de: string;
}[] = [
  { key: "albania", email: OTHER, en: "Albania", fr: "Albanie", it: "Albania", de: "Albanien" },
  { key: "andorra", email: OTHER, en: "Andorra", fr: "Andorre", it: "Andorra", de: "Andorra" },
  { key: "austria", email: OTHER, en: "Austria", fr: "Autriche", it: "Austria", de: "Österreich" },
  {
    key: "belarus",
    email: OTHER,
    en: "Belarus",
    fr: "Biélorussie",
    it: "Bielorussia",
    de: "Belarus",
  },
  {
    key: "belgium",
    email: BELGIUM_LUX,
    en: "Belgium",
    fr: "Belgique",
    it: "Belgio",
    de: "Belgien",
  },
  {
    key: "bosnia-herzegovina",
    email: OTHER,
    en: "Bosnia and Herzegovina",
    fr: "Bosnie-Herzégovine",
    it: "Bosnia ed Erzegovina",
    de: "Bosnien und Herzegowina",
  },
  {
    key: "bulgaria",
    email: OTHER,
    en: "Bulgaria",
    fr: "Bulgarie",
    it: "Bulgaria",
    de: "Bulgarien",
  },
  { key: "croatia", email: OTHER, en: "Croatia", fr: "Croatie", it: "Croazia", de: "Kroatien" },
  { key: "cyprus", email: OTHER, en: "Cyprus", fr: "Chypre", it: "Cipro", de: "Zypern" },
  {
    key: "czech-republic",
    email: OTHER,
    en: "Czech Republic",
    fr: "République tchèque",
    it: "Repubblica Ceca",
    de: "Tschechien",
  },
  {
    key: "denmark",
    email: NORDICS_BALTICS,
    en: "Denmark",
    fr: "Danemark",
    it: "Danimarca",
    de: "Dänemark",
  },
  {
    key: "estonia",
    email: NORDICS_BALTICS,
    en: "Estonia",
    fr: "Estonie",
    it: "Estonia",
    de: "Estland",
  },
  { key: "finland", email: FINLAND, en: "Finland", fr: "Finlande", it: "Finlandia", de: "Finnland" },
  { key: "france", email: FRANCE, en: "France", fr: "France", it: "Francia", de: "Frankreich" },
  { key: "germany", email: GERMANY, en: "Germany", fr: "Allemagne", it: "Germania", de: "Deutschland" },
  { key: "greece", email: OTHER, en: "Greece", fr: "Grèce", it: "Grecia", de: "Griechenland" },
  { key: "hungary", email: OTHER, en: "Hungary", fr: "Hongrie", it: "Ungheria", de: "Ungarn" },
  {
    key: "iceland",
    email: NORDICS_BALTICS,
    en: "Iceland",
    fr: "Islande",
    it: "Islanda",
    de: "Island",
  },
  { key: "ireland", email: UK_IRELAND, en: "Ireland", fr: "Irlande", it: "Irlanda", de: "Irland" },
  { key: "italy", email: ITALY, en: "Italy", fr: "Italie", it: "Italia", de: "Italien" },
  { key: "kosovo", email: OTHER, en: "Kosovo", fr: "Kosovo", it: "Kosovo", de: "Kosovo" },
  {
    key: "latvia",
    email: NORDICS_BALTICS,
    en: "Latvia",
    fr: "Lettonie",
    it: "Lettonia",
    de: "Lettland",
  },
  {
    key: "liechtenstein",
    email: OTHER,
    en: "Liechtenstein",
    fr: "Liechtenstein",
    it: "Liechtenstein",
    de: "Liechtenstein",
  },
  {
    key: "lithuania",
    email: NORDICS_BALTICS,
    en: "Lithuania",
    fr: "Lituanie",
    it: "Lituania",
    de: "Litauen",
  },
  {
    key: "luxembourg",
    email: BELGIUM_LUX,
    en: "Luxembourg",
    fr: "Luxembourg",
    it: "Lussemburgo",
    de: "Luxemburg",
  },
  { key: "malta", email: OTHER, en: "Malta", fr: "Malte", it: "Malta", de: "Malta" },
  {
    key: "moldova",
    email: OTHER,
    en: "Moldova",
    fr: "Moldavie",
    it: "Moldavia",
    de: "Republik Moldau",
  },
  { key: "monaco", email: OTHER, en: "Monaco", fr: "Monaco", it: "Monaco", de: "Monaco" },
  {
    key: "montenegro",
    email: OTHER,
    en: "Montenegro",
    fr: "Monténégro",
    it: "Montenegro",
    de: "Montenegro",
  },
  {
    key: "netherlands",
    email: NETHERLANDS,
    en: "Netherlands",
    fr: "Pays-Bas",
    it: "Paesi Bassi",
    de: "Niederlande",
  },
  {
    key: "north-macedonia",
    email: OTHER,
    en: "North Macedonia",
    fr: "Macédoine du Nord",
    it: "Macedonia del Nord",
    de: "Nordmazedonien",
  },
  {
    key: "norway",
    email: NORDICS_BALTICS,
    en: "Norway",
    fr: "Norvège",
    it: "Norvegia",
    de: "Norwegen",
  },
  { key: "poland", email: OTHER, en: "Poland", fr: "Pologne", it: "Polonia", de: "Polen" },
  {
    key: "portugal",
    email: PORTUGAL,
    en: "Portugal",
    fr: "Portugal",
    it: "Portogallo",
    de: "Portugal",
  },
  { key: "romania", email: OTHER, en: "Romania", fr: "Roumanie", it: "Romania", de: "Rumänien" },
  { key: "russia", email: OTHER, en: "Russia", fr: "Russie", it: "Russia", de: "Russland" },
  {
    key: "san-marino",
    email: OTHER,
    en: "San Marino",
    fr: "Saint-Marin",
    it: "San Marino",
    de: "San Marino",
  },
  { key: "serbia", email: OTHER, en: "Serbia", fr: "Serbie", it: "Serbia", de: "Serbien" },
  {
    key: "slovakia",
    email: OTHER,
    en: "Slovakia",
    fr: "Slovaquie",
    it: "Slovacchia",
    de: "Slowakei",
  },
  {
    key: "slovenia",
    email: OTHER,
    en: "Slovenia",
    fr: "Slovénie",
    it: "Slovenia",
    de: "Slowenien",
  },
  { key: "spain", email: SPAIN, en: "Spain", fr: "Espagne", it: "Spagna", de: "Spanien" },
  {
    key: "sweden",
    email: NORDICS_BALTICS,
    en: "Sweden",
    fr: "Suède",
    it: "Svezia",
    de: "Schweden",
  },
  {
    key: "switzerland",
    email: OTHER,
    en: "Switzerland",
    fr: "Suisse",
    it: "Svizzera",
    de: "Schweiz",
  },
  { key: "ukraine", email: OTHER, en: "Ukraine", fr: "Ukraine", it: "Ucraina", de: "Ukraine" },
  {
    key: "united-kingdom",
    email: UK_IRELAND,
    en: "United Kingdom",
    fr: "Royaume-Uni",
    it: "Regno Unito",
    de: "Vereinigtes Königreich",
  },
  {
    key: "vatican-city",
    email: OTHER,
    en: "Vatican City",
    fr: "Cité du Vatican",
    it: "Città del Vaticano",
    de: "Vatikanstadt",
  },
];

export function getContactCountries(locale: Locale): ContactCountry[] {
  return COUNTRIES.map((c) => ({
    key: c.key,
    email: c.email,
    label: c[locale],
  })).sort((a, b) => a.label.localeCompare(b.label, locale));
}
