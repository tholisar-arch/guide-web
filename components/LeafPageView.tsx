import Link from "next/link";
import Image from "next/image";
import { ChevronLeft, ChevronRight, FileText } from "lucide-react";
import type { PageEntry } from "@/lib/types";
import { getAdjacentPages } from "@/lib/data";
import Breadcrumbs, { type Crumb } from "@/components/Breadcrumbs";

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
  const textLines = entry.text
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean);

  return (
    <article className="mx-auto max-w-4xl px-4 py-8">
      <Breadcrumbs items={crumbs} />
      <h1 className="mb-1 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
        {entry.title}
      </h1>
      <p className="mb-6 text-sm text-ink-400">
        Page {entry.page} du guide
        {parentHref && (
          <>
            {" · "}
            <Link href={parentHref} className="text-brand-600 hover:underline dark:text-brand-400">
              retour à la liste
            </Link>
          </>
        )}
      </p>

      <div className="overflow-hidden rounded-xl border border-ink-200 bg-ink-50 shadow-card dark:border-ink-800 dark:bg-ink-900">
        <Image
          src={entry.image}
          alt={entry.title}
          width={1400}
          height={788}
          className="h-auto w-full"
          priority
        />
      </div>

      {textLines.length > 0 && (
        <details className="group mt-6 rounded-xl border border-ink-200 bg-white dark:border-ink-800 dark:bg-ink-900">
          <summary className="flex cursor-pointer list-none items-center gap-2 px-4 py-3 text-sm font-medium text-ink-600 [&::-webkit-details-marker]:hidden dark:text-ink-300">
            <FileText size={15} />
            Contenu extrait de cette page (texte, recherche, accessibilité)
          </summary>
          <div className="prose-guide border-t border-ink-100 px-4 py-4 text-sm leading-relaxed text-ink-600 dark:border-ink-800 dark:text-ink-300">
            {textLines.map((l, i) => (
              <p key={i}>{l}</p>
            ))}
          </div>
        </details>
      )}

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
