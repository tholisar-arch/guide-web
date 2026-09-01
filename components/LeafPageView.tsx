import Link from "next/link";
import Image from "next/image";
import { ChevronLeft, ChevronRight, ImageIcon } from "lucide-react";
import type { PageEntry } from "@/lib/types";
import { getAdjacentPages } from "@/lib/data";
import Breadcrumbs, { type Crumb } from "@/components/Breadcrumbs";
import ContentBlocks from "@/components/ContentBlocks";
import OriginalPageToggle from "@/components/OriginalPageToggle";

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
    <article className="mx-auto max-w-4xl px-4 py-8">
      <Breadcrumbs items={crumbs} />
      <h1 className="mb-1 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
        {entry.title}
      </h1>
      <p className="mb-6 text-sm text-ink-400">
        Page {entry.page} of the guide
        {parentHref && (
          <>
            {" · "}
            <Link href={parentHref} className="text-brand-600 hover:underline dark:text-brand-400">
              back to the list
            </Link>
          </>
        )}
      </p>

      {entry.images.length > 0 && (
        <div className="mb-6 flex flex-wrap items-start gap-4 rounded-xl border border-ink-200 bg-ink-50 p-4 dark:border-ink-800 dark:bg-ink-900">
          {entry.images.map((img, i) => (
            <div
              key={i}
              className="relative flex items-center justify-center overflow-hidden rounded-lg bg-white dark:bg-ink-950"
              style={{
                width: Math.min(img.w, 220),
                height: (Math.min(img.w, 220) * img.h) / img.w,
                maxHeight: 220,
              }}
            >
              <Image
                src={img.file}
                alt={entry.title}
                fill
                sizes="220px"
                className="object-contain"
              />
            </div>
          ))}
        </div>
      )}

      <ContentBlocks blocks={entry.blocks} />

      {entry.blocks.length === 0 && entry.images.length === 0 && (
        <p className="flex items-center gap-2 rounded-lg border border-dashed border-ink-200 px-4 py-6 text-sm text-ink-400 dark:border-ink-800">
          <ImageIcon size={16} />
          This page is mostly visual &mdash; see the original page
          below.
        </p>
      )}

      <OriginalPageToggle screenshot={entry.screenshot} title={entry.title} />

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
  );
}
