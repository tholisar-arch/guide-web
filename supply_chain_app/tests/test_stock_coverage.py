import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.stock_coverage import compute_coverage, service_level_z


def test_service_level_z_monotonic():
    assert service_level_z(0.95) > service_level_z(0.80)
    assert service_level_z(0.99) > service_level_z(0.95)


def test_stockout_risk_classification():
    products = pd.DataFrame(
        [{"sku": "S1", "name": "Item", "category": "Cat", "unit_cost": 1.0, "lead_time_days": 14}]
    )
    sales_monthly = pd.DataFrame(
        [
            {"sku": "S1", "period": "2024-01", "quantity": 300, "revenue": 300},
            {"sku": "S1", "period": "2024-02", "quantity": 300, "revenue": 300},
            {"sku": "S1", "period": "2024-03", "quantity": 300, "revenue": 300},
        ]
    )
    # avg daily demand ~= 300/30.44 ~= 9.85/day; 14 days of lead time needs ~138 units
    low_stock = pd.DataFrame([{"sku": "S1", "quantity_on_hand": 20}])
    df = compute_coverage(sales_monthly, low_stock, products, service_level=0.95,
                           default_lead_time_days=14, review_period_days=7)
    row = df.iloc[0]
    assert row["coverage_status"] == "Stockout Risk"
    assert row["needs_reorder"]


def test_excess_classification():
    products = pd.DataFrame(
        [{"sku": "S2", "name": "Item", "category": "Cat", "unit_cost": 1.0, "lead_time_days": 10}]
    )
    sales_monthly = pd.DataFrame(
        [{"sku": "S2", "period": "2024-01", "quantity": 30, "revenue": 30}]
    )
    high_stock = pd.DataFrame([{"sku": "S2", "quantity_on_hand": 5000}])
    df = compute_coverage(sales_monthly, high_stock, products, service_level=0.95,
                           default_lead_time_days=10, review_period_days=7)
    assert df.iloc[0]["coverage_status"] == "Excess"


def test_reorder_point_formula():
    products = pd.DataFrame(
        [{"sku": "S3", "name": "Item", "category": "Cat", "unit_cost": 2.0, "lead_time_days": 10}]
    )
    sales_monthly = pd.DataFrame(
        [
            {"sku": "S3", "period": "2024-01", "quantity": 304.4, "revenue": 100},
            {"sku": "S3", "period": "2024-02", "quantity": 304.4, "revenue": 100},
        ]
    )
    stock = pd.DataFrame([{"sku": "S3", "quantity_on_hand": 100}])
    df = compute_coverage(sales_monthly, stock, products, service_level=0.95,
                           default_lead_time_days=10, review_period_days=7)
    row = df.iloc[0]
    # avg_daily_demand should be ~10 units/day (304.4 / 30.44), std=0 -> safety stock = 0
    assert row["avg_daily_demand"] == pytest.approx(10.0)
    assert row["safety_stock"] == pytest.approx(0.0, abs=1e-6)
    assert row["reorder_point"] == pytest.approx(100.0, rel=0.01)
