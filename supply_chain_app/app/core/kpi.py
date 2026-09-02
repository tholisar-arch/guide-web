"""Dashboard KPI computations.

All functions are pure: they take the DataFrames already loaded from the
database and return either a scalar, a small dict of scalars, or a
DataFrame ready to be charted / tabulated by the UI layer.
"""
from __future__ import annotations

import pandas as pd


def compute_headline_kpis(sales: pd.DataFrame, latest_stock: pd.DataFrame, products: pd.DataFrame) -> dict:
    """Top-line numbers shown as KPI cards on the Dashboard screen."""
    kpis = {
        "total_revenue": float(sales["revenue"].sum()) if not sales.empty else 0.0,
        "total_units_sold": float(sales["quantity"].sum()) if not sales.empty else 0.0,
        "num_active_skus": int(sales["sku"].nunique()) if not sales.empty else 0,
        "num_transactions": int(len(sales)),
        "num_products_master": int(len(products)),
    }

    if not latest_stock.empty and not products.empty:
        merged = latest_stock.merge(products[["sku", "unit_cost"]], on="sku", how="left")
        merged["unit_cost"] = merged["unit_cost"].fillna(0.0)
        kpis["total_stock_value"] = float((merged["quantity_on_hand"] * merged["unit_cost"]).sum())
        kpis["total_units_in_stock"] = float(merged["quantity_on_hand"].sum())
    else:
        kpis["total_stock_value"] = 0.0
        kpis["total_units_in_stock"] = 0.0

    if not sales.empty:
        kpis["average_selling_price"] = (
            kpis["total_revenue"] / kpis["total_units_sold"] if kpis["total_units_sold"] else 0.0
        )
    else:
        kpis["average_selling_price"] = 0.0

    return kpis


def revenue_trend(sales_monthly: pd.DataFrame) -> pd.DataFrame:
    """Total revenue and units per calendar month, across all SKUs."""
    if sales_monthly.empty:
        return pd.DataFrame(columns=["period", "revenue", "quantity"])
    return (
        sales_monthly.groupby("period", as_index=False)
        .agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
        .sort_values("period")
    )


def top_products_by_revenue(sales: pd.DataFrame, products: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    if sales.empty:
        return pd.DataFrame(columns=["sku", "name", "revenue", "quantity"])
    agg = sales.groupby("sku", as_index=False).agg(revenue=("revenue", "sum"), quantity=("quantity", "sum"))
    agg = agg.merge(products[["sku", "name"]], on="sku", how="left")
    agg["name"] = agg["name"].fillna(agg["sku"])
    return agg.sort_values("revenue", ascending=False).head(top_n)[["sku", "name", "revenue", "quantity"]]


def revenue_by_category(sales: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    if sales.empty:
        return pd.DataFrame(columns=["category", "revenue"])
    merged = sales.merge(products[["sku", "category"]], on="sku", how="left")
    merged["category"] = merged["category"].fillna("Uncategorized")
    return (
        merged.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    )
