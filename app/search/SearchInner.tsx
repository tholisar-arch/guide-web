"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Search as SearchIcon, FileText } from "lucide-react";
import { scoreItem, type SearchItem } from "@/components/SearchBox";

const CHAPTER_LABELS: Record<string, string> = {
  about: "About us",
  selector: "Product Selector",
  markets: "Markets",
  knowledge: "Knowledge Centre",
  cover: "Guide",
};

export default function SearchPage() {
  const params = useSearchParams();
  const router = useRouter();
  const q = params.get("q") ?? "";
  const [input, setInput] = useState(q);
  const [items, setItems] = useState<SearchItem[]>([]);

  useEffect(() => {
    fetch("/data/search-index.json")
      .then((r) => r.json())
      .then(setItems);
  }, []);

  useEffect(() => setInput(q), [q]);

  const results = useMemo(() => {
    if (!q.trim()) return [];
    return items
      .map((it) => ({ it, score: scoreItem(it, q.trim()) }))
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((r) => r.it);
  }, [items, q]);

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    router.push(`/search?q=${encodeURIComponent(input.trim())}`);
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="mb-4 text-2xl font-bold text-ink-900 dark:text-white">
        Search
      </h1>
      <form onSubmit={onSubmit} className="mb-8">
        <div className="flex items-center gap-2 rounded-lg border border-ink-200 bg-white px-3 py-2.5 shadow-sm focus-within:border-brand-500 dark:border-ink-700 dark:bg-ink-900">
          <SearchIcon size={17} className="text-ink-400" />
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Search the guide..."
            autoFocus
            className="w-full bg-transparent text-sm outline-none placeholder:text-ink-400"
          />
        </div>
      </form>

      {q.trim() && (
        <p className="mb-4 text-sm text-ink-500 dark:text-ink-400">
          {results.length} result{results.length !== 1 ? "s" : ""} for{" "}
          &ldquo;<strong>{q}</strong>&rdquo;
        </p>
      )}

      <ul className="divide-y divide-ink-100 overflow-hidden rounded-lg border border-ink-200 dark:divide-ink-800 dark:border-ink-800">
        {results.map((r) => (
          <li key={r.slug}>
            <Link
              href={`/guide/${r.slug}`}
              className="flex items-start gap-3 bg-white px-4 py-3 hover:bg-brand-50 dark:bg-ink-900 dark:hover:bg-brand-950"
            >
              <FileText size={16} className="mt-0.5 shrink-0 text-ink-300" />
              <span className="min-w-0">
                <span className="mb-0.5 block text-xs font-medium uppercase tracking-wide text-brand-600 dark:text-brand-400">
                  {CHAPTER_LABELS[r.chapter] ?? r.chapter}
                  {r.category ? ` · ${r.category}` : ""}
                </span>
                <span className="block text-sm font-medium text-ink-800 dark:text-ink-100">
                  {r.title}
                </span>
                {r.text && (
                  <span className="mt-0.5 block line-clamp-1 text-xs text-ink-400">
                    {r.text}
                  </span>
                )}
              </span>
            </Link>
          </li>
        ))}
        {q.trim() && results.length === 0 && (
          <li className="bg-white px-4 py-8 text-center text-sm text-ink-400 dark:bg-ink-900">
            No results. Try a different search term.
          </li>
        )}
      </ul>
    </div>
  );
}
