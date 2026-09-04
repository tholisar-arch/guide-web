import { Suspense } from "react";
import SearchInner from "@/app/search/SearchInner";

export const metadata = { title: "Keresés" };

export default function SearchPageHu() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-3xl px-4 py-10 text-ink-400">Betöltés...</div>}>
      <SearchInner locale="hu" />
    </Suspense>
  );
}
