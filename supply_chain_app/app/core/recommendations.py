"""Rule-based automatic recommendation engine.

Combines the ABC/XYZ classification with the stock-coverage analysis to
produce a prioritized, explained action list — the kind of triage a
Distribution Manager would otherwise build by hand in a spreadsheet.

Each rule is intentionally simple and auditable: given the same inputs, the
same recommendation is always produced, and the explanation states exactly
which numbers triggered it.
"""
from __future__ import annotations

import pandas as pd

PRIORITY_RANK = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


def _add(rows, sku, name, priority, category, message, explanation):
    rows.append(
        {
            "sku": sku,
            "name": name,
            "priority": priority,
            "priority_rank": PRIORITY_RANK[priority],
            "category": category,
            "recommendation": message,
            "explanation": explanation,
        }
    )


def generate_recommendations(abc_xyz_df: pd.DataFrame, coverage_df: pd.DataFrame) -> pd.DataFrame:
    if coverage_df.empty:
        return pd.DataFrame(
            columns=["sku", "name", "priority", "priority_rank", "category", "recommendation", "explanation"]
        )

    merged = coverage_df.merge(
        abc_xyz_df[["sku", "abc_class", "xyz_class", "combined_class"]], on="sku", how="left"
    )
    merged["abc_class"] = merged["abc_class"].fillna("C")
    merged["xyz_class"] = merged["xyz_class"].fillna("Z")
    merged["combined_class"] = merged["combined_class"].fillna("CZ")

    rows: list[dict] = []
    for _, r in merged.iterrows():
        sku, name = r["sku"], r["name"]
        status = r["coverage_status"]
        abc, xyz = r["abc_class"], r["xyz_class"]
        gap_units = max(0.0, r["reorder_point"] - r["quantity_on_hand"])

        # --- Stockout / reorder rules --------------------------------------
        if status == "Stockout Risk":
            priority = "Critical" if abc == "A" else ("High" if abc == "B" else "Medium")
            _add(
                rows, sku, name, priority, "Replenishment",
                f"Reorder now: place a purchase order for at least {gap_units:.0f} units.",
                f"Coverage is {r['days_of_coverage']:.1f} days, below the {r['lead_time_days']:.0f}-day "
                f"supplier lead time. This is a class '{r['combined_class']}' item "
                f"({'high' if abc == 'A' else 'medium/low'} revenue contribution), so a stockout "
                "would directly affect service level.",
            )
        elif status == "Low":
            priority = "Medium" if abc in ("A", "B") else "Low"
            _add(
                rows, sku, name, priority, "Replenishment",
                f"Plan a reorder within the next review cycle ({gap_units:.0f} units short of target).",
                f"Coverage is {r['days_of_coverage']:.1f} days — above the lead time but below the "
                f"recommended {2 * r['lead_time_days']:.0f}-day buffer, so it should enter the next "
                "planned purchase order.",
            )

        # --- Excess stock rules ---------------------------------------------
        if status == "Excess":
            priority = "Medium" if abc == "A" else "Low"
            _add(
                rows, sku, name, priority, "Excess Stock",
                "Pause replenishment and consider a promotion/clearance to reduce holding cost.",
                f"Coverage is {r['days_of_coverage']:.1f} days, well above the {r['lead_time_days']:.0f}-day "
                f"lead time, tying up {r['stock_value']:,.0f} in inventory value for a "
                f"class '{r['combined_class']}' item.",
            )
        elif status == "Excess (No Demand)":
            _add(
                rows, sku, name, "Low", "Obsolescence Risk",
                "Investigate: stock on hand with no recent sales history.",
                f"{r['quantity_on_hand']:.0f} units in stock (value {r['stock_value']:,.0f}) but no "
                "measurable demand in the imported sales history — potential obsolete or slow-moving stock.",
            )

        # --- Forecastability / variability rules ----------------------------
        if xyz == "Z" and abc in ("A", "B") and status not in ("No Demand Data",):
            _add(
                rows, sku, name, "Medium", "Forecast Risk",
                "Increase monitoring frequency and safety stock buffer; demand is erratic.",
                f"Class '{r['combined_class']}': significant revenue contribution ('{abc}') combined with "
                "highly variable, hard-to-forecast demand ('Z'). Standard reorder-point formulas are less "
                "reliable here — consider more frequent reviews or a higher service-level target.",
            )

        # --- Strategic priority for top performers ---------------------------
        if r["combined_class"] == "AX" and status == "Adequate":
            _add(
                rows, sku, name, "Low", "Strategic",
                "Maintain: top-performing, predictable item with healthy coverage.",
                "Class 'AX' (high revenue, stable demand) with adequate coverage — a candidate for a "
                "tighter (s,S) automated replenishment policy given its predictability.",
            )

    result = pd.DataFrame(rows)
    if result.empty:
        return result
    return result.sort_values(["priority_rank", "sku"]).reset_index(drop=True)


def summarize(recommendations_df: pd.DataFrame) -> dict:
    if recommendations_df.empty:
        return {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0}
    counts = recommendations_df["priority"].value_counts()
    return {
        "total": int(len(recommendations_df)),
        "critical": int(counts.get("Critical", 0)),
        "high": int(counts.get("High", 0)),
        "medium": int(counts.get("Medium", 0)),
        "low": int(counts.get("Low", 0)),
    }
