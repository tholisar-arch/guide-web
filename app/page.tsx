import Image from "next/image";
import Link from "next/link";
import { ArrowLeftRight, Sliders, Zap } from "lucide-react";
import SearchBox from "@/components/SearchBox";
import { nav } from "@/lib/data";
import type { ChapterSelector } from "@/lib/types";

export default function HomePage() {
  const selector = nav.chapters.find(
    (c) => c.slug === "selector"
  ) as ChapterSelector;

  return (
    <div>
      <section className="relative border-b border-ink-200 bg-gradient-to-b from-brand-50 via-white to-white dark:border-ink-800 dark:from-ink-900 dark:via-ink-950 dark:to-ink-950">
        <div className="mx-auto max-w-4xl px-4 pt-6 sm:pt-8">
          <div className="inline-flex rounded-xl bg-white px-5 py-3 shadow-sm">
            <Image
              src="/brand/mersen-logo.png"
              alt="Mersen"
              width={140}
              height={53}
              priority
            />
          </div>
        </div>
        <div className="mx-auto max-w-4xl px-4 pb-16 pt-6 text-center sm:pb-24">
          <span className="mb-4 inline-block rounded-full bg-brand-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700 dark:bg-brand-950 dark:text-brand-300">
            Interactive Product Selector · 2026 Europe Edition
          </span>
          <h1 className="text-3xl font-bold tracking-tight text-ink-900 sm:text-5xl dark:text-white">
            Selection Guide
            <span className="block text-brand-600 dark:text-brand-400">
              Electrical Protection
            </span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-base text-ink-600 sm:text-lg dark:text-ink-300">
            The full product selector, transformed into a website: fuses,
            surge protection devices, and photovoltaic solutions, organized
            by product family and fully browsable on mobile, tablet, and
            desktop.
          </p>
          <div className="mx-auto mt-8 max-w-xl">
            <SearchBox variant="hero" />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pt-10">
        <Link
          href="/xref"
          className="group flex items-center gap-4 rounded-xl border border-ink-200 bg-white p-4 shadow-card transition hover:border-brand-300 hover:shadow-md dark:border-ink-800 dark:bg-ink-900"
        >
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
            <ArrowLeftRight size={20} />
          </span>
          <span className="min-w-0 flex-1">
            <span className="block font-semibold text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
              Cross Reference Search
            </span>
            <span className="block text-sm text-ink-500 dark:text-ink-400">
              Find the equivalent Mersen reference for a competitor part
              number (Citel, Dehn, Eaton, Siemens, and more).
            </span>
          </span>
        </Link>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14">
        <h2 className="mb-6 text-xl font-semibold text-ink-900 dark:text-white">
          Product Families
        </h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {selector.categories.map((cat) => (
            <Link
              key={cat.slug}
              href={`/guide/selector/${cat.slug}`}
              className="group flex items-center gap-3 rounded-xl border border-ink-200 bg-white p-4 shadow-card transition hover:border-brand-300 hover:shadow-md dark:border-ink-800 dark:bg-ink-900"
            >
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
                <Zap size={18} />
              </span>
              <span className="min-w-0 flex-1 truncate font-medium text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
                {cat.title}
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-14">
        <Link
          href="/spd-configurator"
          className="group flex items-center gap-4 rounded-xl border border-ink-200 bg-white p-4 shadow-card transition hover:border-brand-300 hover:shadow-md dark:border-ink-800 dark:bg-ink-900"
        >
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
            <Sliders size={20} />
          </span>
          <span className="min-w-0 flex-1">
            <span className="block font-semibold text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
              SPD Configurator
            </span>
            <span className="block text-sm text-ink-500 dark:text-ink-400">
              Answer a few questions about your installation to find the
              right Surge Protection Device family.
            </span>
          </span>
        </Link>
      </section>
    </div>
  );
}
