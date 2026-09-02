"""What-if simulation engine backing the Simulator screen's sliders.

Wraps :func:`app.core.stock_coverage.compute_coverage` so the UI only needs
to pass slider values and get back both the "before" (persisted parameters)
and "after" (simulated parameters) coverage tables plus a portfolio-level
delta summary, without duplicating any formula.
"""
from __future__ import annotations

import pandas as pd

from app.core.stock_coverage import compute_coverage


def run_simulation(
    sales_monthly: pd.DataFrame,
    latest_stock: pd.DataFrame,
    products: pd.DataFrame,
    baseline_params: dict,
    simulated_params: dict,
) -> dict:
    """Return {'baseline': df, 'simulated': df, 'delta': dict} for the given parameter sets."""
    baseline = compute_coverage(
        sales_monthly, latest_stock, products,
        service_level=baseline_params["service_level"],
        default_lead_time_days=baseline_params["lead_time_days"],
        review_period_days=baseline_params["review_period_days"],
        demand_growth_pct=baseline_params.get("demand_growth_pct", 0.0),
    )
    simulated = compute_coverage(
        sales_monthly, latest_stock, products,
        service_level=simulated_params["service_level"],
        default_lead_time_days=simulated_params["lead_time_days"],
        review_period_days=simulated_params["review_period_days"],
        demand_growth_pct=simulated_params.get("demand_growth_pct", 0.0),
    )

    delta = {
        "total_safety_stock_before": float(baseline["safety_stock"].sum()) if not baseline.empty else 0.0,
        "total_safety_stock_after": float(simulated["safety_stock"].sum()) if not simulated.empty else 0.0,
        "total_reorder_value_before": float(
            (baseline["reorder_point"] * baseline["unit_cost"]).sum()
        ) if not baseline.empty else 0.0,
        "total_reorder_value_after": float(
            (simulated["reorder_point"] * simulated["unit_cost"]).sum()
        ) if not simulated.empty else 0.0,
        "stockout_risk_count_before": int((baseline["coverage_status"] == "Stockout Risk").sum())
        if not baseline.empty else 0,
        "stockout_risk_count_after": int((simulated["coverage_status"] == "Stockout Risk").sum())
        if not simulated.empty else 0,
        "excess_count_before": int((baseline["coverage_status"] == "Excess").sum()) if not baseline.empty else 0,
        "excess_count_after": int((simulated["coverage_status"] == "Excess").sum()) if not simulated.empty else 0,
    }

    return {"baseline": baseline, "simulated": simulated, "delta": delta}
