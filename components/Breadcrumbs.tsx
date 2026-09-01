import Link from "next/link";
import { ChevronRight } from "lucide-react";

export type Crumb = { title: string; href?: string };

export default function Breadcrumbs({ items }: { items: Crumb[] }) {
  return (
    <nav
      aria-label="Breadcrumb"
      className="flex flex-wrap items-center gap-1 text-xs text-ink-500 dark:text-ink-400"
    >
      {items.map((c, i) => (
        <span key={i} className="flex items-center gap-1">
          {i > 0 && <ChevronRight size={12} className="shrink-0" />}
          {c.href ? (
            <Link
              href={c.href}
              className="max-w-[220px] truncate hover:text-brand-600 dark:hover:text-brand-400"
            >
              {c.title}
            </Link>
          ) : (
            <span className="max-w-[280px] truncate text-ink-700 dark:text-ink-200">
              {c.title}
            </span>
          )}
        </span>
      ))}
    </nav>
  );
}
