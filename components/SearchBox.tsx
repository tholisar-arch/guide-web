"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { Search, X, Loader2 } from "lucide-react";
import { localeFromPathname, localeHref, t } from "@/lib/i18n";

type SearchItem = {
  title: string;
  slug: string;
  chapter: string;
  category: string | null;
  page: number;
  text: string;
  codes: string;
};

const cache: Record<string, SearchItem[]> = {};

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

/** Every reference on this page whose code contains the query, deduped and
 * in table order - a page can hold several matching Part/Catalog numbers
 * (e.g. a whole "MI6SF..." series), and all of them should be surfaced,
 * not just the first one. */
export function matchedCodes(item: SearchItem, q: string): string[] {
  const query = q.toLowerCase();
  if (!item.codes) return [];
  const tokens = item.codes.split(/\s+/);
  const seen = new Set<string>();
  const hits: string[] = [];
  for (const c of tokens) {
    if (c.toLowerCase().includes(query) && !seen.has(c)) {
      seen.add(c);
      hits.push(c);
    }
  }
  return hits;
}

export default function SearchBox({ variant = "header" }: { variant?: "header" | "hero" }) {
  const pathname = usePathname() ?? "/";
  const locale = localeFromPathname(pathname);
  const dict = t(locale);
  const indexUrl =
    locale === "en" ? "/data/search-index.json" : `/data/search-index.${locale}.json`;

  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [items, setItems] = useState<SearchItem[] | null>(cache[indexUrl] ?? null);
  const [loading, setLoading] = useState(false);
  const boxRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  useEffect(() => {
    setItems(cache[indexUrl] ?? null);
  }, [indexUrl]);

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
    if (cache[indexUrl]) {
      setItems(cache[indexUrl]);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(indexUrl);
      const data = (await res.json()) as SearchItem[];
      cache[indexUrl] = data;
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

  function goToItem(slug: string, refs: string[]) {
    setOpen(false);
    setQuery("");
    const suffix = refs.length
      ? `?${refs.map((r) => `ref=${encodeURIComponent(r)}`).join("&")}`
      : "";
    router.push(localeHref(locale, `/guide/${slug}${suffix}`));
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim().length > 0) {
      setOpen(false);
      router.push(localeHref(locale, `/search?q=${encodeURIComponent(query.trim())}`));
    }
  }

  const wide = variant === "hero";

  return (
    <div ref={boxRef} className={`relative min-w-0 ${wide ? "w-full" : "w-full max-w-xs"}`}>
      <form onSubmit={onSubmit} className="min-w-0">
        <div
          className={`flex min-w-0 items-center gap-2 rounded-full border border-ink-200 bg-white px-4 shadow-sm transition focus-within:border-brand-400 focus-within:shadow-card-hover focus-within:ring-4 focus-within:ring-brand-100/70 dark:border-ink-700 dark:bg-ink-900 dark:focus-within:ring-brand-950/70 ${
            wide ? "h-14 text-base" : "h-9 text-sm"
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
            placeholder={wide ? dict.searchPlaceholderHero : dict.searchPlaceholderHeader}
            className="min-w-0 w-full bg-transparent text-ink-800 outline-none placeholder:text-ink-400 dark:text-ink-100"
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
        <div className="absolute left-0 right-0 top-full z-30 mt-2 max-h-96 overflow-y-auto rounded-2xl border border-ink-200/80 bg-white/95 p-1.5 shadow-elevated backdrop-blur-md dark:border-ink-700/80 dark:bg-ink-900/95">
          {results.length === 0 ? (
            <p className="px-3 py-3 text-sm text-ink-400">
              {dict.noResultsFor(query)}
            </p>
          ) : (
            <>
              {results.map((r) => {
                const refs = matchedCodes(r, query);
                const shown = refs.slice(0, 6);
                return (
                <button
                  key={r.slug}
                  onClick={() => goToItem(r.slug, refs)}
                  className="flex w-full flex-col items-start gap-0.5 rounded-xl px-3 py-2.5 text-left transition-colors hover:bg-brand-50 dark:hover:bg-brand-950/60"
                >
                  <span className="text-xs font-medium uppercase tracking-wide text-brand-600 dark:text-brand-400">
                    {r.category ?? dict.productSelectorFallback}
                  </span>
                  <span className="text-sm text-ink-800 dark:text-ink-100">
                    {r.title}
                  </span>
                  {shown.length > 0 && (
                    <span className="flex flex-wrap gap-1">
                      {shown.map((code) => (
                        <span
                          key={code}
                          className="rounded bg-ink-100 px-1.5 py-0.5 font-mono text-xs text-ink-600 dark:bg-ink-800 dark:text-ink-300"
                        >
                          {code}
                        </span>
                      ))}
                      {refs.length > shown.length && (
                        <span className="rounded px-1.5 py-0.5 font-mono text-xs text-ink-400">
                          +{refs.length - shown.length}
                        </span>
                      )}
                    </span>
                  )}
                </button>
                );
              })}
              <button
                onClick={(e) => onSubmit(e)}
                className="mt-1 w-full rounded-xl px-3 py-2.5 text-left text-sm font-medium text-brand-600 transition-colors hover:bg-brand-50 dark:text-brand-400 dark:hover:bg-brand-950/60"
              >
                {dict.viewAllResultsFor(query)}
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export type { SearchItem };
