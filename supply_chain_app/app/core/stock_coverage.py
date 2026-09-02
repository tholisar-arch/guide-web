"""Stock coverage, safety stock and reorder point computations.

Formulas used (classic inventory-theory, and intentionally standard so the
results are explainable and auditable by a Distribution Manager):

    avg_daily_demand   = average monthly demand / 30.44
    daily_demand_std   = std of monthly demand / sqrt(30.44)      (variance scales linearly with time)
    safety_stock       = z(service_level) * daily_demand_std * sqrt(lead_time_days)
    reorder_point (ROP)= avg_daily_demand * lead_time_days + safety_stock
    days_of_coverage   = current_stock / avg_daily_demand
    order_up_to_level  = ROP + avg_daily_demand * review_period_days

``z(service_level)`` is the inverse standard-normal CDF, computed with the
Python standard library (``statistics.NormalDist``) so no extra dependency
(e.g. SciPy) is required.
"""
from __future__ import annotations

from statistics import NormalDist

import numpy as np
import pandas as pd

from app.config import (
    COVERAGE_EXCESS_DAYS,
    DEFAULT_LEAD_TIME_DAYS,
    DEFAULT_REVIEW_PERIOD_DAYS,
    DEFAULT_SERVICE_LEVEL,
)

DAYS_PER_MONTH = 30.44


def service_level_z(service_level: float) -> float:
    """Inverse normal CDF (z-score) for a given target service level (0-1)."""
    service_level = min(max(service_level, 0.5), 0.9999)
    return NormalDist().inv_cdf(service_level)


def compute_coverage(
    sales_monthly: pd.DataFrame,
    latest_stock: pd.DataFrame,
    products: pd.DataFrame,
    service_level: float = DEFAULT_SERVICE_LEVEL,
    default_lead_time_days: float = DEFAULT_LEAD_TIME_DAYS,
    review_period_days: float = DEFAULT_REVIEW_PERIOD_DAYS,
    demand_growth_pct: float = 0.0,
) -> pd.DataFrame:
    """Return one row per SKU with demand statistics, safety stock, reorder
    point and a coverage-risk classification."""
    all_skus = products[["sku", "name", "category", "unit_cost", "lead_time_days"]].copy()
    if all_skus.empty:
        return pd.DataFrame()

    if not sales_monthly.empty:
        demand_stats = sales_monthly.groupby("sku")["quantity"].agg(["mean", "std"]).reset_index()
        demand_stats.columns = ["sku", "mean_monthly_demand", "std_monthly_demand"]
    else:
        demand_stats = pd.DataFrame(columns=["sku", "mean_monthly_demand", "std_monthly_demand"])

    df = all_skus.merge(demand_stats, on="sku", how="left")
    df["mean_monthly_demand"] = df["mean_monthly_demand"].fillna(0.0)
    df["std_monthly_demand"] = df["std_monthly_demand"].fillna(0.0)

    growth_factor = 1.0 + (demand_growth_pct / 100.0)
    df["avg_daily_demand"] = (df["mean_monthly_demand"] * growth_factor) / DAYS_PER_MONTH
    df["daily_demand_std"] = (df["std_monthly_demand"] * growth_factor) / np.sqrt(DAYS_PER_MONTH)

    df["lead_time_days"] = df["lead_time_days"].where(df["lead_time_days"] > 0, default_lead_time_days)

    z = service_level_z(service_level)
    df["safety_stock"] = z * df["daily_demand_std"] * np.sqrt(df["lead_time_days"])
    df["safety_stock"] = df["safety_stock"].clip(lower=0)
    df["reorder_point"] = df["avg_daily_demand"] * df["lead_time_days"] + df["safety_stock"]
    df["order_up_to_level"] = df["reorder_point"] + df["avg_daily_demand"] * review_period_days

    stock = latest_stock[["sku", "quantity_on_hand"]] if not latest_stock.empty else pd.DataFrame(
        columns=["sku", "quantity_on_hand"]
    )
    df = df.merge(stock, on="sku", how="left")
    df["quantity_on_hand"] = df["quantity_on_hand"].fillna(0.0)
    df["stock_value"] = df["quantity_on_hand"] * df["unit_cost"]

    df["days_of_coverage"] = np.where(
        df["avg_daily_demand"] > 0, df["quantity_on_hand"] / df["avg_daily_demand"], np.inf
    )

    def classify(row):
        if row["avg_daily_demand"] <= 0:
            return "No Demand Data" if row["quantity_on_hand"] == 0 else "Excess (No Demand)"
        if row["days_of_coverage"] < row["lead_time_days"]:
            return "Stockout Risk"
        if row["days_of_coverage"] < 2 * row["lead_time_days"]:
            return "Low"
        if row["days_of_coverage"] > COVERAGE_EXCESS_DAYS:
            return "Excess"
        return "Adequate"

    df["coverage_status"] = df.apply(classify, axis=1)
    df["needs_reorder"] = df["quantity_on_hand"] < df["reorder_point"]
    df["service_level_used"] = service_level
    df["z_score"] = z

    cols = [
        "sku", "name", "category", "unit_cost", "quantity_on_hand", "stock_value",
        "avg_daily_demand", "daily_demand_std", "lead_time_days", "safety_stock",
        "reorder_point", "order_up_to_level", "days_of_coverage", "coverage_status",
        "needs_reorder", "service_level_used", "z_score",
    ]
    return df[cols].sort_values("days_of_coverage")


def explain_row(row: pd.Series) -> str:
    """Human-readable explanation of how one SKU's numbers were derived."""
    return (
        f"SKU {row['sku']} — average demand {row['avg_daily_demand']:.2f} units/day "
        f"(std {row['daily_demand_std']:.2f}). With a lead time of {row['lead_time_days']:.0f} days "
        f"and a target service level of {row['service_level_used'] * 100:.0f}% (z={row['z_score']:.2f}), "
        f"safety stock = {row['z_score']:.2f} x {row['daily_demand_std']:.2f} x sqrt({row['lead_time_days']:.0f}) "
        f"= {row['safety_stock']:.1f} units. Reorder point = ({row['avg_daily_demand']:.2f} x "
        f"{row['lead_time_days']:.0f}) + {row['safety_stock']:.1f} = {row['reorder_point']:.1f} units. "
        f"Current stock of {row['quantity_on_hand']:.0f} units gives "
        f"{row['days_of_coverage']:.1f} days of coverage -> classified as '{row['coverage_status']}'."
    )
