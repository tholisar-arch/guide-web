"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { localeFromPathname, localeHref, type Locale } from "@/lib/i18n";

const MESSAGE: Record<Locale, string> = {
  en: "This guide page doesn't exist or is no longer available.",
  fr: "Cette page du guide n'existe pas ou n'est plus disponible.",
  it: "Questa pagina del catalogo non esiste o non è più disponibile.",
  de: "Diese Katalogseite existiert nicht oder ist nicht mehr verfügbar.",
  nl: "Deze cataloguspagina bestaat niet of is niet meer beschikbaar.",
  hu: "Ez a katalógusoldal nem létezik, vagy már nem érhető el.",
  pt: "Esta página do catálogo não existe ou já não está disponível.",
  pl: "Ta strona katalogu nie istnieje lub nie jest już dostępna.",
  ro: "Această pagină din catalog nu există sau nu mai este disponibilă.",
  cs: "Tato stránka katalogu neexistuje nebo již není dostupná.",
};

const BACK_HOME: Record<Locale, string> = {
  en: "Back to home",
  fr: "Retour à l'accueil",
  it: "Torna alla home",
  de: "Zurück zur Startseite",
  nl: "Terug naar home",
  hu: "Vissza a kezdőlapra",
  pt: "Voltar ao início",
  pl: "Powrót do strony głównej",
  ro: "Înapoi la pagina principală",
  cs: "Zpět na domovskou stránku",
};

export default function NotFound() {
  const pathname = usePathname() ?? "/";
  const locale = localeFromPathname(pathname);

  return (
    <div className="mx-auto flex max-w-lg flex-col items-center px-4 py-24 text-center">
      <h1 className="text-3xl font-bold text-ink-900 dark:text-white">404</h1>
      <p className="mt-2 text-ink-500 dark:text-ink-400">{MESSAGE[locale]}</p>
      <Link
        href={localeHref(locale, "/")}
        className="mt-6 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
      >
        {BACK_HOME[locale]}
      </Link>
    </div>
  );
}
