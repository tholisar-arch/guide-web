"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { Search, FileText } from "lucide-react";
import type { NavLeafItem } from "@/lib/types";

export default function LeafFilterList({ items }: { items: NavLeafItem[] }) {
  const [q, setQ] = useState("");

  const filtered = useMemo(() => {
    if (!q.trim()) return items;
    const query = q.trim().toLowerCase();
    return items.filter((it) => it.title.toLowerCase().includes(query));
  }, [items, q]);

  return (
    <div>
      {items.length > 8 && (
        <div className="mb-4 flex items-center gap-2 rounded-lg border border-ink-200 bg-white px-3 py-2 dark:border-ink-800 dark:bg-ink-900">
          <Search size={15} className="text-ink-400" />
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Filter references..."
            className="w-full bg-transparent text-sm outline-none placeholder:text-ink-400"
          />
        </div>
      )}
      <ul className="divide-y divide-ink-100 overflow-hidden rounded-lg border border-ink-200 dark:divide-ink-800 dark:border-ink-800">
        {filtered.map((it) => (
          <li key={it.slug}>
            <Link
              href={`/guide/${it.slug}`}
              className="flex items-center gap-3 bg-white px-3 py-2.5 text-sm text-ink-700 transition hover:bg-brand-50 hover:text-brand-700 dark:bg-ink-900 dark:text-ink-200 dark:hover:bg-brand-950 dark:hover:text-brand-300"
            >
              <FileText size={14} className="shrink-0 text-ink-300" />
              <span className="min-w-0 flex-1 truncate">{it.title}</span>
              <span className="shrink-0 text-xs text-ink-400">
                p.{it.page}
              </span>
            </Link>
          </li>
        ))}
        {filtered.length === 0 && (
          <li className="bg-white px-3 py-4 text-center text-sm text-ink-400 dark:bg-ink-900">
            No references found.
          </li>
        )}
      </ul>
    </div>
  );
}
