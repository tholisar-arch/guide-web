import { Suspense } from "react";
import SearchInner from "@/app/search/SearchInner";

export const metadata = { title: "Pesquisa" };

export default function SearchPagePt() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-3xl px-4 py-10 text-ink-400">A carregar...</div>}>
      <SearchInner locale="pt" />
    </Suspense>
  );
}
