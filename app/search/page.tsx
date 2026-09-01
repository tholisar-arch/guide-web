import { Suspense } from "react";
import SearchInner from "./SearchInner";

export const metadata = { title: "Recherche" };

export default function SearchPage() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-3xl px-4 py-10 text-ink-400">Chargement...</div>}>
      <SearchInner />
    </Suspense>
  );
}
