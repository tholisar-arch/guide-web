"use client";

import { useEffect } from "react";
import { useSearchParams } from "next/navigation";

/** Cross Reference Search links to a product page with ?ref=<mersen part
 * number>; once there, find the table cell holding that exact reference
 * and highlight its row so the visitor can spot it immediately. */
export default function HighlightRefFromQuery() {
  const params = useSearchParams();
  const ref = params.get("ref");

  useEffect(() => {
    if (!ref) return;
    const target = ref.trim().toLowerCase();
    const cells = document.querySelectorAll<HTMLElement>("[data-ref-cell]");
    for (const cell of cells) {
      const value = (cell.dataset.refCell || "").trim().toLowerCase();
      if (value === target) {
        const row = cell.closest("tr");
        row?.classList.add("ref-highlight");
        row?.scrollIntoView({ behavior: "smooth", block: "center" });
        break;
      }
    }
  }, [ref]);

  return null;
}
