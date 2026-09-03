import type { Locale } from "@/lib/i18n";

export type ContactCountry = {
  key: string;
  label: string;
  email: string;
};

// Same routing (key -> email) for both locales; only the displayed label
// is translated. "other" is always last - it's the catch-all.
const ROUTES: { key: string; email: string }[] = [
  { key: "belgium-luxembourg", email: "fabien.buisseret@mersen.com" },
  { key: "nordics-baltics", email: "afshin.pourarsalan@mersen.com" },
  { key: "finland", email: "ville.honka@mersen.com" },
  { key: "france", email: "nordine.souar@mersen.com" },
  { key: "germany", email: "torsten.frank@mersen.com" },
  { key: "italy", email: "stefano.paolini@mersen.com" },
  { key: "netherlands", email: "sunil.ramsoedit@mersen.com" },
  { key: "portugal", email: "sergio.jimenez@mersen.com" },
  { key: "spain", email: "almudena.herranz@mersen.com" },
  { key: "uk-ireland", email: "naomi.cuff@mersen.com" },
  { key: "other", email: "karoly.galle@mersen.com" },
];

const LABELS: Record<Locale, Record<string, string>> = {
  en: {
    "belgium-luxembourg": "Belgium & Luxembourg",
    "nordics-baltics": "Norway, Sweden, Iceland, Denmark & Baltic countries",
    finland: "Finland",
    france: "France",
    germany: "Germany",
    italy: "Italy",
    netherlands: "Netherlands",
    portugal: "Portugal",
    spain: "Spain",
    "uk-ireland": "United Kingdom & Ireland",
    other: "Other European countries",
  },
  fr: {
    "belgium-luxembourg": "Belgique et Luxembourg",
    "nordics-baltics": "Norvège, Suède, Islande, Danemark et pays baltes",
    finland: "Finlande",
    france: "France",
    germany: "Allemagne",
    italy: "Italie",
    netherlands: "Pays-Bas",
    portugal: "Portugal",
    spain: "Espagne",
    "uk-ireland": "Royaume-Uni et Irlande",
    other: "Autres pays d'Europe",
  },
};

export function getContactCountries(locale: Locale): ContactCountry[] {
  return ROUTES.map((r) => ({
    key: r.key,
    email: r.email,
    label: LABELS[locale][r.key],
  }));
}
