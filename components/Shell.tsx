"use client";

import { useEffect, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { Menu, X, Globe, Check } from "lucide-react";
import Image from "next/image";
import type { ReactNode } from "react";
import SearchBox from "@/components/SearchBox";
import {
  LOCALES,
  LOCALE_LABELS,
  localeFromPathname,
  localeHref,
  switchLocalePath,
  t,
} from "@/lib/i18n";

function LanguageSwitcher({ pathname }: { pathname: string }) {
  const locale = localeFromPathname(pathname);
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  return (
    <div ref={ref} className="relative shrink-0">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex h-9 items-center gap-1.5 rounded-full border border-ink-200 px-3 text-sm font-medium text-ink-600 transition hover:border-ink-300 hover:bg-ink-100 dark:border-ink-700 dark:text-ink-300 dark:hover:bg-ink-800"
        aria-label="Select language"
        aria-expanded={open}
      >
        <Globe size={15} />
        <span className="hidden sm:inline">{locale.toUpperCase()}</span>
      </button>
      {open && (
        <div className="absolute right-0 top-full z-30 mt-2 w-44 overflow-hidden rounded-xl border border-ink-200/80 bg-white/95 py-1 shadow-elevated backdrop-blur-md dark:border-ink-700/80 dark:bg-ink-900/95">
          {LOCALES.map((l) => (
            <Link
              key={l}
              href={switchLocalePath(pathname, l)}
              onClick={() => setOpen(false)}
              className="flex items-center justify-between px-3 py-2 text-sm text-ink-700 transition-colors hover:bg-brand-50 hover:text-brand-700 dark:text-ink-200 dark:hover:bg-brand-950 dark:hover:text-brand-300"
            >
              {LOCALE_LABELS[l]}
              {l === locale && <Check size={14} className="text-brand-600 dark:text-brand-400" />}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default function Shell({
  sidebar,
  children,
}: {
  sidebar: ReactNode;
  children: ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname() ?? "/";
  const locale = localeFromPathname(pathname);
  const dict = t(locale);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-40 flex h-16 items-center gap-3 border-b border-ink-200/70 bg-white/80 px-3 backdrop-blur-md backdrop-saturate-150 dark:border-ink-800/70 dark:bg-ink-950/80 sm:px-5">
        <button
          onClick={() => setOpen((v) => !v)}
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-ink-600 transition hover:bg-ink-100 lg:hidden dark:text-ink-300 dark:hover:bg-ink-800"
          aria-label="Open menu"
        >
          {open ? <X size={19} /> : <Menu size={19} />}
        </button>
        <Link
          href={localeHref(locale, "/")}
          className="flex shrink-0 items-center gap-3 transition-opacity hover:opacity-80"
        >
          <Image
            src="/brand/mersen-logo.png"
            alt="Mersen"
            width={84}
            height={32}
            className="h-6 w-auto"
            priority
          />
          <span className="hidden h-6 w-px bg-ink-200 sm:block dark:bg-ink-800" />
          <span className="hidden text-sm font-medium tracking-tight text-ink-800 sm:block dark:text-ink-50">
            {dict.heroTitle1}{" "}
            <span className="font-normal text-ink-400">{dict.siteSubtitle}</span>
          </span>
        </Link>
        <div className="ml-auto flex min-w-0 flex-1 items-center justify-end gap-2 sm:flex-none sm:w-auto">
          <div className="min-w-0 flex-1 sm:w-80 sm:flex-none">
            <SearchBox />
          </div>
          <LanguageSwitcher pathname={pathname} />
        </div>
      </header>

      <div className="flex w-full flex-1">
        <div
          className={`fixed inset-0 z-30 bg-black/30 transition-opacity lg:hidden ${
            open ? "opacity-100" : "pointer-events-none opacity-0"
          }`}
          onClick={() => setOpen(false)}
        />
        <aside
          className={`fixed inset-y-0 left-0 z-30 w-72 -translate-x-full border-r border-ink-200/70 bg-white pt-16 transition-transform lg:static lg:z-0 lg:h-[calc(100vh-4rem)] lg:translate-x-0 lg:pt-0 dark:border-ink-800/70 dark:bg-ink-950 ${
            open ? "translate-x-0" : ""
          }`}
        >
          <div className="sticky top-16 h-[calc(100vh-4rem)] lg:top-0">
            {sidebar}
          </div>
        </aside>
        <main className="min-w-0 flex-1">{children}</main>
      </div>
    </div>
  );
}
