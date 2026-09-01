import Link from "next/link";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { PageEntry } from "@/lib/types";
import { getAdjacentPages } from "@/lib/data";
import Breadcrumbs, { type Crumb } from "@/components/Breadcrumbs";
import ContentBlocks from "@/components/ContentBlocks";
import ResourceLinks from "@/components/ResourceLinks";
import SelectorFrame from "@/components/SelectorFrame";

export default function LeafPageView({
  entry,
  crumbs,
  parentHref,
}: {
  entry: PageEntry;
  crumbs: Crumb[];
  parentHref?: string;
}) {
  const { prev, next } = getAdjacentPages(entry.page);

  return (
    <SelectorFrame title="Product Selector" backHref={parentHref}>
      <article>
        <Breadcrumbs items={crumbs} />
        <h1 className="mb-1 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
          {entry.title}
        </h1>
        <p className="mb-6 text-sm text-ink-400">
          Page {entry.page} of the guide
        </p>

        <ContentBlocks blocks={entry.blocks} />

        <ResourceLinks links={entry.resourceLinks ?? []} />

        <div className="mt-8 flex items-center justify-between gap-3 border-t border-ink-200 pt-6 dark:border-ink-800">
          {prev ? (
            <Link
              href={`/guide/${prev.slug}`}
              className="flex min-w-0 flex-1 items-center gap-2 rounded-lg border border-ink-200 px-3 py-2 text-sm hover:border-brand-300 hover:bg-brand-50 dark:border-ink-800 dark:hover:bg-brand-950"
            >
              <ChevronLeft size={16} className="shrink-0 text-ink-400" />
              <span className="min-w-0 truncate text-ink-600 dark:text-ink-300">
                {prev.title}
              </span>
            </Link>
          ) : (
            <span className="flex-1" />
          )}
          {next ? (
            <Link
              href={`/guide/${next.slug}`}
              className="flex min-w-0 flex-1 items-center justify-end gap-2 rounded-lg border border-ink-200 px-3 py-2 text-right text-sm hover:border-brand-300 hover:bg-brand-50 dark:border-ink-800 dark:hover:bg-brand-950"
            >
              <span className="min-w-0 truncate text-ink-600 dark:text-ink-300">
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
