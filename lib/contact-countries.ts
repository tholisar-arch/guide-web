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
const COUNTRIES: { key: string; email: string; en: string; fr: string }[] = [
  { key: "albania", email: OTHER, en: "Albania", fr: "Albanie" },
  { key: "andorra", email: OTHER, en: "Andorra", fr: "Andorre" },
  { key: "austria", email: OTHER, en: "Austria", fr: "Autriche" },
  { key: "belarus", email: OTHER, en: "Belarus", fr: "Biélorussie" },
  { key: "belgium", email: BELGIUM_LUX, en: "Belgium", fr: "Belgique" },
  {
    key: "bosnia-herzegovina",
    email: OTHER,
    en: "Bosnia and Herzegovina",
    fr: "Bosnie-Herzégovine",
  },
  { key: "bulgaria", email: OTHER, en: "Bulgaria", fr: "Bulgarie" },
  { key: "croatia", email: OTHER, en: "Croatia", fr: "Croatie" },
  { key: "cyprus", email: OTHER, en: "Cyprus", fr: "Chypre" },
  { key: "czech-republic", email: OTHER, en: "Czech Republic", fr: "République tchèque" },
  { key: "denmark", email: NORDICS_BALTICS, en: "Denmark", fr: "Danemark" },
  { key: "estonia", email: NORDICS_BALTICS, en: "Estonia", fr: "Estonie" },
  { key: "finland", email: FINLAND, en: "Finland", fr: "Finlande" },
  { key: "france", email: FRANCE, en: "France", fr: "France" },
  { key: "germany", email: GERMANY, en: "Germany", fr: "Allemagne" },
  { key: "greece", email: OTHER, en: "Greece", fr: "Grèce" },
  { key: "hungary", email: OTHER, en: "Hungary", fr: "Hongrie" },
  { key: "iceland", email: NORDICS_BALTICS, en: "Iceland", fr: "Islande" },
  { key: "ireland", email: UK_IRELAND, en: "Ireland", fr: "Irlande" },
  { key: "italy", email: ITALY, en: "Italy", fr: "Italie" },
  { key: "kosovo", email: OTHER, en: "Kosovo", fr: "Kosovo" },
  { key: "latvia", email: NORDICS_BALTICS, en: "Latvia", fr: "Lettonie" },
  { key: "liechtenstein", email: OTHER, en: "Liechtenstein", fr: "Liechtenstein" },
  { key: "lithuania", email: NORDICS_BALTICS, en: "Lithuania", fr: "Lituanie" },
  { key: "luxembourg", email: BELGIUM_LUX, en: "Luxembourg", fr: "Luxembourg" },
  { key: "malta", email: OTHER, en: "Malta", fr: "Malte" },
  { key: "moldova", email: OTHER, en: "Moldova", fr: "Moldavie" },
  { key: "monaco", email: OTHER, en: "Monaco", fr: "Monaco" },
  { key: "montenegro", email: OTHER, en: "Montenegro", fr: "Monténégro" },
  { key: "netherlands", email: NETHERLANDS, en: "Netherlands", fr: "Pays-Bas" },
  {
    key: "north-macedonia",
    email: OTHER,
    en: "North Macedonia",
    fr: "Macédoine du Nord",
  },
  { key: "norway", email: NORDICS_BALTICS, en: "Norway", fr: "Norvège" },
  { key: "poland", email: OTHER, en: "Poland", fr: "Pologne" },
  { key: "portugal", email: PORTUGAL, en: "Portugal", fr: "Portugal" },
  { key: "romania", email: OTHER, en: "Romania", fr: "Roumanie" },
  { key: "russia", email: OTHER, en: "Russia", fr: "Russie" },
  { key: "san-marino", email: OTHER, en: "San Marino", fr: "Saint-Marin" },
  { key: "serbia", email: OTHER, en: "Serbia", fr: "Serbie" },
  { key: "slovakia", email: OTHER, en: "Slovakia", fr: "Slovaquie" },
  { key: "slovenia", email: OTHER, en: "Slovenia", fr: "Slovénie" },
  { key: "spain", email: SPAIN, en: "Spain", fr: "Espagne" },
  { key: "sweden", email: NORDICS_BALTICS, en: "Sweden", fr: "Suède" },
  { key: "switzerland", email: OTHER, en: "Switzerland", fr: "Suisse" },
  { key: "ukraine", email: OTHER, en: "Ukraine", fr: "Ukraine" },
  { key: "united-kingdom", email: UK_IRELAND, en: "United Kingdom", fr: "Royaume-Uni" },
  { key: "vatican-city", email: OTHER, en: "Vatican City", fr: "Cité du Vatican" },
];

export function getContactCountries(locale: Locale): ContactCountry[] {
  return COUNTRIES.map((c) => ({
    key: c.key,
    email: c.email,
    label: locale === "fr" ? c.fr : c.en,
  })).sort((a, b) => a.label.localeCompare(b.label, locale));
}
