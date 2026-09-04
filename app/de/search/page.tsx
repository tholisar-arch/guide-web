import { Suspense } from "react";
import SearchInner from "@/app/search/SearchInner";

export const metadata = { title: "Suche" };

export default function SearchPageDe() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-3xl px-4 py-10 text-ink-400">Wird geladen...</div>}>
      <SearchInner locale="de" />
    </Suspense>
  );
}
