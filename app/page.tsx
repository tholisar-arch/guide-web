import Link from "next/link";
import { Layers, ArrowRight, ShieldCheck, Zap, Sun } from "lucide-react";
import SearchBox from "@/components/SearchBox";
import { nav, stats } from "@/lib/data";
import type { ChapterSelector } from "@/lib/types";

const CATEGORY_ICONS: Record<string, JSX.Element> = {
  "iec-fuses": <Zap size={18} />,
  "high-speed-fuses": <Zap size={18} />,
  "surge-protection": <ShieldCheck size={18} />,
  "medium-voltage-fuses": <Layers size={18} />,
  "photovoltaic-applications": <Sun size={18} />,
};

export default function HomePage() {
  const selector = nav.chapters.find(
    (c) => c.slug === "selector"
  ) as ChapterSelector;

  return (
    <div>
      <section className="relative overflow-hidden border-b border-ink-200 bg-gradient-to-b from-brand-50 via-white to-white dark:border-ink-800 dark:from-ink-900 dark:via-ink-950 dark:to-ink-950">
        <div className="mx-auto max-w-4xl px-4 py-16 text-center sm:py-24">
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
          <div className="mx-auto mt-10 grid max-w-xl grid-cols-3 gap-4">
            <Stat value={stats.totalPages} label="Guide pages" />
            <Stat value={stats.categories} label="Product families" />
            <Stat value={stats.productFamilies} label="References" />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-ink-900 dark:text-white">
            Product Families
          </h2>
          <Link
            href="/guide/selector"
            className="flex items-center gap-1 text-sm font-medium text-brand-600 hover:underline dark:text-brand-400"
          >
            View all <ArrowRight size={14} />
          </Link>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {selector.categories.map((cat) => (
            <Link
              key={cat.slug}
              href={`/guide/selector/${cat.slug}`}
              className="group flex items-start gap-3 rounded-xl border border-ink-200 bg-white p-4 shadow-card transition hover:border-brand-300 hover:shadow-md dark:border-ink-800 dark:bg-ink-900"
            >
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-300">
                {CATEGORY_ICONS[cat.slug] ?? <Layers size={18} />}
              </span>
              <span className="min-w-0">
                <span className="block truncate font-medium text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300">
                  {cat.title}
                </span>
                <span className="text-xs text-ink-400">
                  {cat.count} reference{cat.count > 1 ? "s" : ""}
                </span>
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}

function Stat({ value, label }: { value: number; label: string }) {
  return (
    <div className="rounded-lg border border-ink-200 bg-white/70 py-3 dark:border-ink-800 dark:bg-ink-900/50">
      <div className="text-2xl font-bold text-brand-600 dark:text-brand-400">
        {value.toLocaleString("en-US")}
      </div>
      <div className="text-xs text-ink-500 dark:text-ink-400">{label}</div>
    </div>
  );
}
