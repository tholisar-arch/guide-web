import { Suspense } from "react";
import SearchInner from "@/app/search/SearchInner";

export const metadata = { title: "Căutare" };

export default function SearchPageRo() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-3xl px-4 py-10 text-ink-400">Se încarcă...</div>}>
      <SearchInner locale="ro" />
    </Suspense>
  );
}
