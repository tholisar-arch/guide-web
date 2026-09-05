import Image from "next/image";
import Link from "next/link";
import { ArrowLeftRight, ArrowRight, ExternalLink, Mail, Sliders, Zap } from "lucide-react";
import SearchBox from "@/components/SearchBox";
import { getData } from "@/lib/data";
import type { ChapterSelector } from "@/lib/types";
import { localeHref, t, type Locale } from "@/lib/i18n";

export default function HomeContent({ locale }: { locale: Locale }) {
  const dict = t(locale);
  const { nav } = getData(locale);
  const selector = nav.chapters.find(
    (c) => c.slug === "selector"
  ) as ChapterSelector;

  return (
    <div>
      <section className="relative overflow-hidden border-b border-ink-200/70 bg-white dark:border-ink-800/70 dark:bg-ink-950">
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 bg-glow-orange dark:opacity-60"
        />
        <div className="relative flex flex-col items-end gap-2 px-4 pt-6 sm:px-6 sm:pt-8">
          <Image
            src="/brand/mersen-logo.png"
            alt="Mersen"
            width={128}
            height={49}
            priority
          />
          <a
            href={dict.mersenWebsiteUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-xs font-medium text-ink-500 transition-colors hover:text-brand-600 dark:text-ink-400 dark:hover:text-brand-400"
          >
            {dict.mersenWebsiteLabel}
            <ExternalLink size={12} />
          </a>
        </div>
        <div className="relative mx-auto max-w-4xl px-4 pb-16 pt-8 text-center sm:pb-24 sm:pt-10">
          <span className="mb-5 inline-block rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700 dark:border-brand-900 dark:bg-brand-950/60 dark:text-brand-400">
            {dict.heroBadge}
          </span>
          <h1 className="text-4xl font-bold tracking-tight text-ink-900 sm:text-6xl sm:leading-[1.05] dark:text-white">
            {dict.heroTitle1}
            <span className="block bg-gradient-to-r from-brand-600 to-brand-500 bg-clip-text text-transparent dark:from-brand-400 dark:to-brand-300">
              {dict.heroTitle2}
            </span>
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-base text-ink-600 sm:text-lg dark:text-ink-300">
            {dict.heroDescription}
          </p>
          <div className="mx-auto mt-9 max-w-xl">
            <SearchBox variant="hero" />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:py-20">
        <h2 className="mb-1.5 text-xl font-semibold tracking-tight text-ink-900 dark:text-white">
          {dict.productFamilies}
        </h2>
        <p className="mb-7 text-sm text-ink-500 dark:text-ink-400">
          {dict.productFamiliesDesc}
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {selector.categories.map((cat) => (
            <Link
              key={cat.slug}
              href={localeHref(locale, `/guide/selector/${cat.slug}`)}
              className="hover-lift group flex items-center gap-3.5 rounded-2xl border border-ink-200 bg-white p-5 shadow-card transition hover:border-brand-200 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
            >
              <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-50 to-brand-100 text-brand-600 transition-transform group-hover:scale-105 dark:from-brand-950 dark:to-brand-900 dark:text-brand-300">
                <Zap size={19} />
              </span>
              <span
                className="min-w-0 flex-1 truncate font-medium text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300"
                title={cat.title}
              >
                {cat.title}
              </span>
              <ArrowRight
                size={16}
                className="shrink-0 text-ink-300 opacity-0 transition group-hover:translate-x-0.5 group-hover:opacity-100 group-hover:text-brand-500"
              />
            </Link>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-20 sm:pb-24">
        <h2 className="mb-1.5 text-xl font-semibold tracking-tight text-ink-900 dark:text-white">
          {dict.moreTools}
        </h2>
        <p className="mb-7 text-sm text-ink-500 dark:text-ink-400">
          {dict.moreToolsDesc}
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <Link
            href={localeHref(locale, "/xref")}
            className="hover-lift group flex items-start gap-4 rounded-2xl border border-ink-200 bg-white p-6 shadow-card transition hover:border-brand-200 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
          >
            <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-50 to-brand-100 text-brand-600 transition-transform group-hover:scale-105 dark:from-brand-950 dark:to-brand-900 dark:text-brand-300">
              <ArrowLeftRight size={20} />
            </span>
            <span className="min-w-0 flex-1">
              <span className="block font-semibold text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
                {dict.xrefCardTitle}
              </span>
              <span className="mt-0.5 block text-sm text-ink-500 dark:text-ink-400">
                {dict.xrefCardDesc}
              </span>
            </span>
          </Link>

          {locale !== "es" && (
            <Link
              href={localeHref(locale, "/spd-configurator")}
              className="hover-lift group flex items-start gap-4 rounded-2xl border border-ink-200 bg-white p-6 shadow-card transition hover:border-brand-200 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
            >
              <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-50 to-brand-100 text-brand-600 transition-transform group-hover:scale-105 dark:from-brand-950 dark:to-brand-900 dark:text-brand-300">
                <Sliders size={20} />
              </span>
              <span className="min-w-0 flex-1">
                <span className="block font-semibold text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
                  {dict.spdCardTitle}
                </span>
                <span className="mt-0.5 block text-sm text-ink-500 dark:text-ink-400">
                  {dict.spdCardDesc}
                </span>
              </span>
            </Link>
          )}

          <Link
            href={localeHref(locale, "/send-request")}
            className="hover-lift group flex items-start gap-4 rounded-2xl border border-ink-200 bg-white p-6 shadow-card transition hover:border-brand-200 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
          >
            <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-50 to-brand-100 text-brand-600 transition-transform group-hover:scale-105 dark:from-brand-950 dark:to-brand-900 dark:text-brand-300">
              <Mail size={20} />
            </span>
            <span className="min-w-0 flex-1">
              <span className="block font-semibold text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
                {dict.sendRequestCardTitle}
              </span>
              <span className="mt-0.5 block text-sm text-ink-500 dark:text-ink-400">
                {dict.sendRequestCardDesc}
              </span>
            </span>
          </Link>
        </div>
      </section>
    </div>
  );
}
