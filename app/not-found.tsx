"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { localeFromPathname, localeHref } from "@/lib/i18n";

export default function NotFound() {
  const pathname = usePathname() ?? "/";
  const locale = localeFromPathname(pathname);

  return (
    <div className="mx-auto flex max-w-lg flex-col items-center px-4 py-24 text-center">
      <h1 className="text-3xl font-bold text-ink-900 dark:text-white">404</h1>
      <p className="mt-2 text-ink-500 dark:text-ink-400">
        {locale === "fr"
          ? "Cette page du guide n'existe pas ou n'est plus disponible."
          : "This guide page doesn't exist or is no longer available."}
      </p>
      <Link
        href={localeHref(locale, "/")}
        className="mt-6 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
      >
        {locale === "fr" ? "Retour à l'accueil" : "Back to home"}
      </Link>
    </div>
  );
}
