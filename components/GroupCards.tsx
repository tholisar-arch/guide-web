import Link from "next/link";
import { Folder, ArrowRight } from "lucide-react";

export default function GroupCards({
  items,
}: {
  items: { title: string; href: string }[];
}) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((it) => (
        <Link
          key={it.href}
          href={it.href}
          className="hover-lift group flex items-center gap-3 rounded-2xl border border-ink-200 bg-white p-4 shadow-card transition hover:border-brand-200 hover:shadow-card-hover dark:border-ink-800 dark:bg-ink-900"
        >
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-50 to-brand-100 text-brand-600 transition-transform group-hover:scale-105 dark:from-brand-950 dark:to-brand-900 dark:text-brand-300">
            <Folder size={17} />
          </span>
          <span
            className="min-w-0 flex-1 truncate font-medium text-ink-800 group-hover:text-brand-700 dark:text-ink-100 dark:group-hover:text-brand-300"
            title={it.title}
          >
            {it.title}
          </span>
          <ArrowRight
            size={15}
            className="shrink-0 text-ink-300 transition group-hover:translate-x-0.5 group-hover:text-brand-500"
          />
        </Link>
      ))}
    </div>
  );
}
