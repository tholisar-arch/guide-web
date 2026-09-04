"use client";

import { useEffect } from "react";
import { useSearchParams } from "next/navigation";

/** Cross Reference Search and the site search both link to a product page
 * with one or more ?ref=<mersen part number> params; once there, find every
 * table cell holding one of those exact references and highlight its row
 * so the visitor can spot all of them, not just the first, immediately. */
export default function HighlightRefFromQuery() {
  const params = useSearchParams();
  const refs = params.getAll("ref");

  useEffect(() => {
    if (refs.length === 0) return;
    const targets = new Set(refs.map((r) => r.trim().toLowerCase()));
    const cells = document.querySelectorAll<HTMLElement>("[data-ref-cell]");
    let scrolled = false;
    for (const cell of cells) {
      const value = (cell.dataset.refCell || "").trim().toLowerCase();
      if (targets.has(value)) {
        const row = cell.closest("tr");
        row?.classList.add("ref-highlight");
        if (!scrolled) {
          row?.scrollIntoView({ behavior: "smooth", block: "center" });
          scrolled = true;
        }
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refs.join("|")]);

  return null;
}
