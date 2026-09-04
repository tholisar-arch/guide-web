import Link from "next/link";
import { Suspense } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { PageEntry } from "@/lib/types";
import { getData, getProductImage } from "@/lib/data";
import Breadcrumbs, { type Crumb } from "@/components/Breadcrumbs";
import ContentBlocks from "@/components/ContentBlocks";
import ResourceLinks from "@/components/ResourceLinks";
import SelectorFrame from "@/components/SelectorFrame";
import HighlightRefFromQuery from "@/components/HighlightRefFromQuery";
import { localeHref, type Locale } from "@/lib/i18n";

export default function LeafPageView({
  entry,
  crumbs,
  parentHref,
  locale,
}: {
  entry: PageEntry;
  crumbs: Crumb[];
  parentHref?: string;
  locale: Locale;
}) {
  const { prev, next } = getData(locale).getAdjacentPages(entry.page);
  const productImage = getProductImage(entry.page);

  return (
    <SelectorFrame
      backHref={parentHref}
      locale={locale}
      topLeft={
        productImage && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={productImage} alt="" className="h-16 w-auto object-contain" />
        )
      }
    >
      <article>
        <Breadcrumbs items={crumbs} />
        <h1 className="mb-6 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
          {entry.title}
        </h1>

        <Suspense fallback={null}>
          <HighlightRefFromQuery />
        </Suspense>
        <ContentBlocks blocks={entry.blocks} />

        <ResourceLinks links={entry.resourceLinks ?? []} locale={locale} />

        <div className="mt-8 flex items-center justify-between gap-3 border-t border-ink-200 pt-6 dark:border-ink-800">
          {prev ? (
            <Link
              href={localeHref(locale, `/guide/${prev.slug}`)}
              className="flex min-w-0 flex-1 items-center gap-2 rounded-lg border border-ink-200 px-3 py-2 text-sm hover:border-brand-300 hover:bg-brand-50 dark:border-ink-800 dark:hover:bg-brand-950"
            >
              <ChevronLeft size={16} className="shrink-0 text-ink-400" />
              <span className="min-w-0 truncate text-ink-600 dark:text-ink-300" title={prev.title}>
                {prev.title}
              </span>
            </Link>
          ) : (
            <span className="flex-1" />
          )}
          {next ? (
            <Link
              href={localeHref(locale, `/guide/${next.slug}`)}
              className="flex min-w-0 flex-1 items-center justify-end gap-2 rounded-lg border border-ink-200 px-3 py-2 text-right text-sm hover:border-brand-300 hover:bg-brand-50 dark:border-ink-800 dark:hover:bg-brand-950"
            >
              <span className="min-w-0 truncate text-ink-600 dark:text-ink-300" title={next.title}>
                {next.title}
              </span>
              <ChevronRight size={16} className="shrink-0 text-ink-400" />
            </Link>
          ) : (
            <span className="flex-1" />
          )}
        </div>
      </article>
    </SelectorFrame>
  );
}
