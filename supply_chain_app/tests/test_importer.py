import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.importer import apply_mapping, guess_mapping


def test_guess_mapping_matches_common_headers():
    columns = ["Item Code", "Sale Date", "Quantity", "Revenue"]
    mapping = guess_mapping(columns, "sales")
    assert mapping["sku"] == "Item Code"
    assert mapping["sale_date"] == "Sale Date"
    assert mapping["quantity"] == "Quantity"
    assert mapping["revenue"] == "Revenue"


def test_apply_mapping_drops_invalid_rows():
    raw = pd.DataFrame(
        {
            "Item Code": ["SKU1", "SKU2", ""],
            "Sale Date": ["2024-01-01", "not-a-date", "2024-01-03"],
            "Quantity": [10, 5, 3],
        }
    )
    mapping = {"sku": "Item Code", "sale_date": "Sale Date", "quantity": "Quantity", "revenue": None}
    result = apply_mapping(raw, mapping, "sales")
    assert result.rows_imported == 1
    assert result.rows_rejected == 2
    assert result.dataframe.iloc[0]["sku"] == "SKU1"


def test_apply_mapping_raises_on_missing_required_field():
    raw = pd.DataFrame({"Item Code": ["SKU1"]})
    mapping = {"sku": "Item Code", "sale_date": None, "quantity": None, "revenue": None}
    try:
        apply_mapping(raw, mapping, "sales")
        assert False, "expected ValueError"
    except ValueError:
        pass
