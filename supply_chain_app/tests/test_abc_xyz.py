import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.abc_xyz import compute_abc_xyz, matrix_summary


def _sample_data():
    sales_monthly = pd.DataFrame(
        [
            # A-class, stable demand -> AX
            {"sku": "A1", "period": "2024-01", "quantity": 100, "revenue": 10000},
            {"sku": "A1", "period": "2024-02", "quantity": 102, "revenue": 10200},
            {"sku": "A1", "period": "2024-03", "quantity": 98, "revenue": 9800},
            # C-class, erratic demand -> CZ
            {"sku": "C1", "period": "2024-01", "quantity": 5, "revenue": 50},
            {"sku": "C1", "period": "2024-02", "quantity": 40, "revenue": 400},
            {"sku": "C1", "period": "2024-03", "quantity": 1, "revenue": 10},
        ]
    )
    products = pd.DataFrame(
        [{"sku": "A1", "name": "Item A1"}, {"sku": "C1", "name": "Item C1"}]
    )
    return sales_monthly, products


def test_abc_ranks_by_revenue_descending():
    sales_monthly, products = _sample_data()
    df = compute_abc_xyz(sales_monthly, products)
    assert df.iloc[0]["sku"] == "A1"
    assert df.iloc[0]["abc_class"] == "A"


def test_xyz_flags_erratic_demand_as_z():
    sales_monthly, products = _sample_data()
    df = compute_abc_xyz(sales_monthly, products)
    c1 = df[df["sku"] == "C1"].iloc[0]
    assert c1["xyz_class"] == "Z"
    assert c1["cv"] > 1.0


def test_matrix_summary_shape_and_totals():
    sales_monthly, products = _sample_data()
    df = compute_abc_xyz(sales_monthly, products)
    matrix = matrix_summary(df)
    assert list(matrix.index) == ["A", "B", "C"]
    assert list(matrix.columns) == ["X", "Y", "Z"]
    assert matrix.values.sum() == len(df)


def test_empty_input_returns_empty_frame():
    df = compute_abc_xyz(pd.DataFrame(), pd.DataFrame())
    assert df.empty
