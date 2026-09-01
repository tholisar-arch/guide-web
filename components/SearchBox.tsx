"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Search, X, Loader2 } from "lucide-react";

type SearchItem = {
  title: string;
  slug: string;
  chapter: string;
  category: string | null;
  page: number;
  text: string;
  codes: string;
};

let cache: SearchItem[] | null = null;

export function scoreItem(item: SearchItem, q: string): number {
  const query = q.toLowerCase();
  const title = item.title.toLowerCase();
  let score = 0;

  // reference codes (Part Number, Catalog Number, ...) take priority: this
  // site is a product-reference lookup, so an exact/prefix code match
  // should always outrank a generic title/category/text match
  if (item.codes) {
    const codesLower = item.codes.toLowerCase();
    const codeTokens = codesLower.split(/\s+/);
    if (codeTokens.includes(query)) score += 200;
    else if (codeTokens.some((c) => c.startsWith(query))) score += 130;
    else if (codesLower.includes(query)) score += 70;
  }

  if (title === query) score += 100;
  else if (title.startsWith(query)) score += 60;
  else if (title.includes(query)) score += 35;
  if (item.category && item.category.toLowerCase().includes(query))
    score += 15;
  if (item.text.toLowerCase().includes(query)) score += 8;
  return score;
}

export function matchedCode(item: SearchItem, q: string): string | null {
  const query = q.toLowerCase();
  if (!item.codes) return null;
  const tokens = item.codes.split(/\s+/);
  const hit = tokens.find((c) => c.toLowerCase().includes(query));
  return hit ?? null;
}

export default function SearchBox({ variant = "header" }: { variant?: "header" | "hero" }) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [items, setItems] = useState<SearchItem[] | null>(cache);
  const [loading, setLoading] = useState(false);
  const boxRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    function onKey(e: KeyboardEvent) {
      if (e.key === "/" && document.activeElement?.tagName !== "INPUT") {
        e.preventDefault();
        boxRef.current?.querySelector("input")?.focus();
      }
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", onClick);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onClick);
      document.removeEventListener("keydown", onKey);
    };
  }, []);

  async function ensureLoaded() {
    if (cache) {
      setItems(cache);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch("/data/search-index.json");
      const data = (await res.json()) as SearchItem[];
      cache = data;
      setItems(data);
    } finally {
      setLoading(false);
    }
  }

  const results = useMemo(() => {
    if (!items || query.trim().length < 2) return [];
    return items
      .map((it) => ({ it, score: scoreItem(it, query.trim()) }))
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 8)
      .map((r) => r.it);
  }, [items, query]);

  function goToItem(slug: string) {
    setOpen(false);
    setQuery("");
    router.push(`/guide/${slug}`);
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim().length > 0) {
      setOpen(false);
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  }

  const wide = variant === "hero";

  return (
    <div ref={boxRef} className={`relative ${wide ? "w-full" : "w-full max-w-xs"}`}>
      <form onSubmit={onSubmit}>
        <div
          className={`flex items-center gap-2 rounded-lg border border-ink-200 bg-white px-3 shadow-sm transition focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-100 dark:border-ink-700 dark:bg-ink-900 dark:focus-within:ring-brand-950 ${
            wide ? "h-12 text-base" : "h-9 text-sm"
          }`}
        >
          {loading ? (
            <Loader2 size={16} className="animate-spin text-ink-400" />
          ) : (
            <Search size={16} className="shrink-0 text-ink-400" />
          )}
          <input
            value={query}
            onFocus={() => {
              setOpen(true);
              ensureLoaded();
            }}
            onChange={(e) => {
              setQuery(e.target.value);
              setOpen(true);
            }}
            placeholder="Search the guide... (fuses, SPD, voltage...)"
            className="w-full bg-transparent text-ink-800 outline-none placeholder:text-ink-400 dark:text-ink-100"
          />
          {query && (
            <button
              type="button"
              onClick={() => setQuery("")}
              className="text-ink-400 hover:text-ink-600"
              aria-label="Clear"
            >
              <X size={14} />
            </button>
          )}
          {!wide && (
            <kbd className="hidden shrink-0 rounded border border-ink-200 px-1 text-[10px] text-ink-400 sm:block dark:border-ink-700">
              /
            </kbd>
          )}
        </div>
      </form>

      {open && query.trim().length >= 2 && (
        <div className="absolute left-0 right-0 top-full z-30 mt-2 max-h-96 overflow-y-auto rounded-lg border border-ink-200 bg-white p-1 shadow-lg dark:border-ink-700 dark:bg-ink-900">
          {results.length === 0 ? (
            <p className="px-3 py-3 text-sm text-ink-400">
              No results for &ldquo;{query}&rdquo;
            </p>
          ) : (
            <>
              {results.map((r) => (
                <button
                  key={r.slug}
                  onClick={() => goToItem(r.slug)}
                  className="flex w-full flex-col items-start gap-0.5 rounded-md px-3 py-2 text-left hover:bg-ink-100 dark:hover:bg-ink-800"
                >
                  <span className="text-xs font-medium uppercase tracking-wide text-brand-600 dark:text-brand-400">
                    {r.category ?? "Product Selector"}
                  </span>
                  <span className="text-sm text-ink-800 dark:text-ink-100">
                    {r.title}
                  </span>
                  {matchedCode(r, query) && (
                    <span className="rounded bg-ink-100 px-1.5 py-0.5 font-mono text-xs text-ink-600 dark:bg-ink-800 dark:text-ink-300">
                      {matchedCode(r, query)}
                    </span>
                  )}
                </button>
              ))}
              <button
                onClick={(e) => onSubmit(e)}
                className="mt-1 w-full rounded-md px-3 py-2 text-left text-sm text-brand-600 hover:bg-ink-100 dark:hover:bg-ink-800"
              >
                View all results for &ldquo;{query}&rdquo; &rarr;
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export type { SearchItem };
