"use client";

import { useEffect, useMemo, useState } from "react";
import { Search, Loader2, ArrowLeftRight } from "lucide-react";
import type { XrefEntry } from "@/lib/types";

// Competitor -> Mersen only: the query is matched against competitor
// references exclusively, never against our own Part Number or the
// description, so looking up a Mersen reference here returns nothing.
function scoreEntry(entry: XrefEntry, q: string): { score: number; matched: string | null } {
  const query = q.toLowerCase();
  let score = 0;
  let matched: string | null = null;

  for (const r of entry.refs) {
    const ref = r.ref.toLowerCase();
    if (ref === query) {
      score += 190;
      matched = matched ?? r.brand;
    } else if (ref.startsWith(query)) {
      score += 120;
      matched = matched ?? r.brand;
    } else if (ref.includes(query)) {
      score += 50;
      matched = matched ?? r.brand;
    }
  }

  return { score, matched };
}

export default function XrefSearch() {
  const [query, setQuery] = useState("");
  const [entries, setEntries] = useState<XrefEntry[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/data/xref-index.json")
      .then((r) => r.json())
      .then((data) => {
        setEntries(data);
        setLoading(false);
      });
  }, []);

  const results = useMemo(() => {
    if (!entries || query.trim().length < 2) return [];
    const q = query.trim();
    return entries
      .map((e) => ({ e, ...scoreEntry(e, q) }))
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 50);
  }, [entries, query]);

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <div className="mb-2 flex items-center gap-2 text-brand-600 dark:text-brand-400">
        <ArrowLeftRight size={18} />
        <span className="text-xs font-semibold uppercase tracking-wide">
          Cross Reference Search
        </span>
      </div>
      <h1 className="mb-2 text-2xl font-bold text-ink-900 dark:text-white">
        Find a Mersen reference from a competitor part number
      </h1>
      <p className="mb-6 text-sm text-ink-500 dark:text-ink-400">
        Search by a competitor&apos;s reference (Citel, Dehn, Eaton, Siemens,
        Schneider Electric, and more) to find the equivalent Mersen part.
      </p>

      <div className="mb-8 flex items-center gap-2 rounded-lg border border-ink-200 bg-white px-3 py-2.5 shadow-sm focus-within:border-brand-500 dark:border-ink-700 dark:bg-ink-900">
        {loading ? (
          <Loader2 size={17} className="animate-spin text-ink-400" />
        ) : (
          <Search size={17} className="text-ink-400" />
        )}
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search a competitor reference..."
          autoFocus
          className="w-full bg-transparent text-sm outline-none placeholder:text-ink-400"
        />
      </div>

      {query.trim().length >= 2 && (
        <p className="mb-4 text-sm text-ink-500 dark:text-ink-400">
          {results.length} result{results.length !== 1 ? "s" : ""} for{" "}
          &ldquo;<strong>{query}</strong>&rdquo;
        </p>
      )}

      <ul className="space-y-3">
        {results.map((r) => (
          <li
            key={r.e.pn}
            className="rounded-lg border border-ink-200 bg-white p-4 dark:border-ink-800 dark:bg-ink-900"
          >
            <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1">
              <span className="font-mono text-sm font-semibold text-brand-600 dark:text-brand-400">
                {r.e.pn}
              </span>
              <span className="text-sm text-ink-600 dark:text-ink-300">
                {r.e.desc}
              </span>
              {r.matched && (
                <span className="ml-auto rounded bg-ink-100 px-1.5 py-0.5 text-xs text-ink-500 dark:bg-ink-800 dark:text-ink-400">
                  matched via {r.matched}
                </span>
              )}
            </div>
          </li>
        ))}
        {query.trim().length >= 2 && results.length === 0 && (
          <li className="rounded-lg border border-ink-200 bg-white px-4 py-8 text-center text-sm text-ink-400 dark:border-ink-800 dark:bg-ink-900">
            No results. Try a different reference.
          </li>
        )}
      </ul>
    </div>
  );
}
