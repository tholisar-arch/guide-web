import Link from "next/link";
import {
  BookOpen,
  Layers,
  Globe2,
  Lightbulb,
  ArrowRight,
  ShieldCheck,
  Zap,
  Sun,
} from "lucide-react";
import SearchBox from "@/components/SearchBox";
import { nav, stats } from "@/lib/data";
import type { ChapterSelector, ChapterMarkets } from "@/lib/types";

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
  const markets = nav.chapters.find(
    (c) => c.slug === "markets"
  ) as ChapterMarkets;

  return (
    <div>
      <section className="relative overflow-hidden border-b border-ink-200 bg-gradient-to-b from-brand-50 via-white to-white dark:border-ink-800 dark:from-ink-900 dark:via-ink-950 dark:to-ink-950">
        <div className="mx-auto max-w-4xl px-4 py-16 text-center sm:py-24">
          <span className="mb-4 inline-block rounded-full bg-brand-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700 dark:bg-brand-950 dark:text-brand-300">
            Interactive Guide · 2026 Europe Edition
          </span>
          <h1 className="text-3xl font-bold tracking-tight text-ink-900 sm:text-5xl dark:text-white">
            Selection Guide
            <span className="block text-brand-600 dark:text-brand-400">
              Electrical Protection
            </span>
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-base text-ink-600 sm:text-lg dark:text-ink-300">
            The full print guide, transformed into a website: fuses, surge
            protection devices, photovoltaic solutions, and selection
            tools, organized by product family and fully browsable on
            mobile, tablet, and desktop.
          </p>
          <div className="mx-auto mt-8 max-w-xl">
            <SearchBox variant="hero" />
          </div>
          <div className="mx-auto mt-10 grid max-w-2xl grid-cols-2 gap-4 sm:grid-cols-4">
            <Stat value={stats.totalPages} label="Guide pages" />
            <Stat value={stats.categories} label="Product families" />
            <Stat value={stats.productFamilies} label="References" />
            <Stat value={stats.markets} label="Markets covered" />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-14">
        <h2 className="mb-6 text-xl font-semibold text-ink-900 dark:text-white">
          Browse the guide
        </h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <ChapterCard
            href="/guide/about"
            icon={<BookOpen size={20} />}
            title="About Us"
            desc="Expertise, key figures, and the group's commitment to sustainability."
          />
          <ChapterCard
            href="/guide/selector"
            icon={<Layers size={20} />}
            title="Product Selector"
            desc={`${stats.productFamilies} references across ${stats.categories} product families.`}
          />
          <ChapterCard
            href="/guide/markets"
            icon={<Globe2 size={20} />}
            title="Markets"
            desc="Solutions by sector: industrial, distribution, solar, lighting..."
          />
          <ChapterCard
            href="/guide/knowledge"
            icon={<Lightbulb size={20} />}
            title="Knowledge Centre"
            desc="Selection guides, technical FAQs, and best practices."
          />
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-16">
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

      <section className="border-t border-ink-200 bg-ink-50 dark:border-ink-800 dark:bg-ink-900/40">
        <div className="mx-auto max-w-6xl px-4 py-14">
          <h2 className="mb-6 text-xl font-semibold text-ink-900 dark:text-white">
            Markets Served
          </h2>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
            {markets.items.map((m) => (
              <Link
                key={m.slug}
                href={`/guide/${m.slug}`}
                className="rounded-xl border border-ink-200 bg-white p-4 text-center shadow-card transition hover:border-brand-300 hover:shadow-md dark:border-ink-800 dark:bg-ink-950"
              >
                <span className="text-sm font-medium text-ink-800 dark:text-ink-100">
                  {m.title}
                </span>
              </Link>
            ))}
          </div>
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

function ChapterCard({
  href,
  icon,
  title,
  desc,
}: {
  href: string;
  icon: React.ReactNode;
  title: string;
  desc: string;
}) {
  return (
    <Link
      href={href}
      className="group flex flex-col rounded-xl border border-ink-200 bg-white p-5 shadow-card transition hover:-translate-y-0.5 hover:border-brand-300 hover:shadow-md dark:border-ink-800 dark:bg-ink-900"
    >
      <span className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-brand-600 text-white">
        {icon}
      </span>
      <span className="font-semibold text-ink-800 dark:text-ink-100">
        {title}
      </span>
      <span className="mt-1 text-sm text-ink-500 dark:text-ink-400">
        {desc}
      </span>
      <span className="mt-3 flex items-center gap-1 text-sm font-medium text-brand-600 group-hover:gap-2 dark:text-brand-400">
        Explore <ArrowRight size={14} className="transition-all" />
      </span>
    </Link>
  );
}
