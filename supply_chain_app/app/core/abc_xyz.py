"""ABC (revenue-based Pareto) and XYZ (demand-variability) classification.

- ABC ranks SKUs by revenue contribution: class A = the top ~80% of
  cumulative revenue, B = the next ~15%, C = the long tail.
- XYZ ranks SKUs by the coefficient of variation (CV = std / mean) of their
  monthly demand: X = stable/predictable, Y = moderately variable,
  Z = erratic/hard to forecast.
- The combined 3x3 matrix (AX...CZ) is the classic input to differentiated
  inventory policies (e.g. tight control + low safety stock on AX, loose
  control + high safety stock on CZ).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from app.config import ABC_THRESHOLD_A, ABC_THRESHOLD_B, XYZ_THRESHOLD_X, XYZ_THRESHOLD_Y


def _abc_class(cum_share: float) -> str:
    if cum_share <= ABC_THRESHOLD_A:
        return "A"
    if cum_share <= ABC_THRESHOLD_B:
        return "B"
    return "C"


def _xyz_class(cv: float) -> str:
    if np.isnan(cv):
        return "Z"
    if cv <= XYZ_THRESHOLD_X:
        return "X"
    if cv <= XYZ_THRESHOLD_Y:
        return "Y"
    return "Z"


def compute_abc_xyz(sales_monthly: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Return one row per SKU with revenue share, CV, and combined ABC/XYZ class."""
    if sales_monthly.empty:
        return pd.DataFrame(
            columns=["sku", "name", "total_revenue", "revenue_share", "cum_revenue_share",
                     "abc_class", "mean_monthly_demand", "std_monthly_demand", "cv",
                     "xyz_class", "combined_class"]
        )

    revenue_by_sku = sales_monthly.groupby("sku", as_index=False)["revenue"].sum()
    revenue_by_sku = revenue_by_sku.sort_values("revenue", ascending=False).reset_index(drop=True)
    total_revenue = revenue_by_sku["revenue"].sum()
    revenue_by_sku["revenue_share"] = (
        revenue_by_sku["revenue"] / total_revenue if total_revenue else 0.0
    )
    revenue_by_sku["cum_revenue_share"] = revenue_by_sku["revenue_share"].cumsum()
    # Classify using the cumulative share *before* this SKU is added, so the
    # SKU(s) needed to reach the threshold are still counted in that class
    # (otherwise a single dominant SKU whose own share exceeds 80% would be
    # misclassified as 'C' instead of 'A').
    prior_cum_share = revenue_by_sku["cum_revenue_share"] - revenue_by_sku["revenue_share"]
    revenue_by_sku["abc_class"] = prior_cum_share.apply(_abc_class)

    demand_stats = sales_monthly.groupby("sku")["quantity"].agg(["mean", "std"]).reset_index()
    demand_stats.columns = ["sku", "mean_monthly_demand", "std_monthly_demand"]
    demand_stats["std_monthly_demand"] = demand_stats["std_monthly_demand"].fillna(0.0)
    demand_stats["cv"] = np.where(
        demand_stats["mean_monthly_demand"] > 0,
        demand_stats["std_monthly_demand"] / demand_stats["mean_monthly_demand"],
        np.nan,
    )
    demand_stats["xyz_class"] = demand_stats["cv"].apply(_xyz_class)

    result = revenue_by_sku.merge(demand_stats, on="sku", how="left")
    result = result.merge(products[["sku", "name"]], on="sku", how="left")
    result["name"] = result["name"].fillna(result["sku"])
    result["combined_class"] = result["abc_class"] + result["xyz_class"]
    result = result.rename(columns={"revenue": "total_revenue"})

    cols = ["sku", "name", "total_revenue", "revenue_share", "cum_revenue_share", "abc_class",
            "mean_monthly_demand", "std_monthly_demand", "cv", "xyz_class", "combined_class"]
    return result[cols].sort_values("total_revenue", ascending=False).reset_index(drop=True)


def matrix_summary(abc_xyz_df: pd.DataFrame) -> pd.DataFrame:
    """Pivot: count of SKUs and total revenue for each of the 9 ABC/XYZ cells."""
    if abc_xyz_df.empty:
        return pd.DataFrame()
    pivot = abc_xyz_df.pivot_table(
        index="abc_class", columns="xyz_class", values="sku", aggfunc="count", fill_value=0,
        observed=False,
    )
    for cls in ("A", "B", "C"):
        if cls not in pivot.index:
            pivot.loc[cls] = 0
    for cls in ("X", "Y", "Z"):
        if cls not in pivot.columns:
            pivot[cls] = 0
    return pivot.reindex(index=["A", "B", "C"], columns=["X", "Y", "Z"])


EXPLANATION = (
    "ABC classification ranks products by their share of total revenue: "
    "'A' items are the vital few that make up the first {a:.0f}% of cumulative "
    "revenue, 'B' items the next {b:.0f}%, and 'C' items the long tail. "
    "XYZ classification measures demand predictability using the coefficient "
    "of variation (CV = standard deviation / mean of monthly demand): 'X' "
    "items are stable (CV <= {x}), 'Y' items moderately variable, and 'Z' "
    "items erratic (CV > {y}), and therefore hardest to forecast accurately."
).format(a=ABC_THRESHOLD_A * 100, b=ABC_THRESHOLD_B * 100, x=XYZ_THRESHOLD_X, y=XYZ_THRESHOLD_Y)
