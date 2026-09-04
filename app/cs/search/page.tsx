import { Suspense } from "react";
import SearchInner from "@/app/search/SearchInner";

export const metadata = { title: "Vyhledávání" };

export default function SearchPageCs() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-3xl px-4 py-10 text-ink-400">Načítání...</div>}>
      <SearchInner locale="cs" />
    </Suspense>
  );
}
