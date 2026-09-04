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
      <section className="relative border-b border-ink-200 bg-ink-50 dark:border-ink-800 dark:bg-ink-900/40">
        <div className="flex flex-col items-end gap-2 px-4 pt-6 sm:pt-8">
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
            className="flex items-center gap-1 text-xs font-medium text-ink-500 hover:text-brand-600 dark:text-ink-400 dark:hover:text-brand-400"
          >
            {dict.mersenWebsiteLabel}
            <ExternalLink size={12} />
          </a>
        </div>
        <div className="mx-auto max-w-4xl px-4 pb-14 pt-6 text-center sm:pb-20">
          <span className="mb-4 inline-block rounded border border-brand-200 bg-white px-2.5 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700 dark:border-brand-900 dark:bg-transparent dark:text-brand-400">
            {dict.heroBadge}
          </span>
          <h1 className="text-3xl font-bold tracking-tight text-ink-900 sm:text-5xl dark:text-white">
            {dict.heroTitle1}
            <span className="block text-brand-600 dark:text-brand-400">
              {dict.heroTitle2}
            </span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-base text-ink-600 sm:text-lg dark:text-ink-300">
            {dict.heroDescription}
          </p>
          <div className="mx-auto mt-8 max-w-xl">
            <SearchBox variant="hero" />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14">
        <h2 className="mb-1 text-lg font-semibold text-ink-900 dark:text-white">
          {dict.productFamilies}
        </h2>
        <p className="mb-6 text-sm text-ink-500 dark:text-ink-400">
          {dict.productFamiliesDesc}
        </p>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {selector.categories.map((cat) => (
            <Link
              key={cat.slug}
              href={localeHref(locale, `/guide/selector/${cat.slug}`)}
              className="group flex items-center gap-3 rounded-lg border border-ink-200 bg-white p-4 transition hover:border-brand-300 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
            >
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
                <Zap size={18} />
              </span>
              <span
                className="min-w-0 flex-1 truncate font-medium text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300"
                title={cat.title}
              >
                {cat.title}
              </span>
              <ArrowRight
                size={15}
                className="shrink-0 text-ink-300 opacity-0 transition group-hover:translate-x-0.5 group-hover:opacity-100 group-hover:text-brand-500"
              />
            </Link>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-16">
        <h2 className="mb-1 text-lg font-semibold text-ink-900 dark:text-white">
          {dict.moreTools}
        </h2>
        <p className="mb-6 text-sm text-ink-500 dark:text-ink-400">
          {dict.moreToolsDesc}
        </p>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <Link
            href={localeHref(locale, "/xref")}
            className="group flex items-start gap-4 rounded-lg border border-ink-200 bg-white p-5 transition hover:border-brand-300 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
          >
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
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
              className="group flex items-start gap-4 rounded-lg border border-ink-200 bg-white p-5 transition hover:border-brand-300 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
            >
              <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
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
            className="group flex items-start gap-4 rounded-lg border border-ink-200 bg-white p-5 transition hover:border-brand-300 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
          >
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
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
