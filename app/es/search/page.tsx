import { Suspense } from "react";
import SearchInner from "@/app/search/SearchInner";

export const metadata = { title: "Buscar" };

export default function SearchPageEs() {
  return (
    <Suspense fallback={<div className="mx-auto max-w-3xl px-4 py-10 text-ink-400">Cargando...</div>}>
      <SearchInner locale="es" />
    </Suspense>
  );
}
