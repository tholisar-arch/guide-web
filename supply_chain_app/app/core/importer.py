"""Excel / CSV import pipeline.

The import flow is: read the raw file into a DataFrame -> auto-guess a
column mapping (field name -> source column) -> let the user confirm/adjust
the mapping in the UI -> apply the mapping, coerce types and drop invalid
rows -> hand the clean, normalized DataFrame to the database layer.

Supported formats: .csv, .xlsx, .xlsm, .xls.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from app.utils.logger import get_logger

logger = get_logger(__name__)

# Field definitions per import type: field_name -> (required, keyword hints for auto-mapping)
FIELD_SPECS: dict[str, dict[str, tuple[bool, list[str]]]] = {
    "products": {
        "sku": (True, ["sku", "item", "code", "reference", "part number", "product id"]),
        "name": (True, ["name", "description", "designation", "label"]),
        "category": (False, ["category", "family", "segment", "group"]),
        "supplier": (False, ["supplier", "vendor", "manufacturer"]),
        "unit_cost": (False, ["cost", "unit cost", "purchase price"]),
        "unit_price": (False, ["price", "unit price", "sales price", "list price"]),
        "lead_time_days": (False, ["lead time", "leadtime", "lead_time"]),
    },
    "sales": {
        "sku": (True, ["sku", "item", "code", "reference", "product id"]),
        "sale_date": (True, ["date", "sale date", "order date", "period"]),
        "quantity": (True, ["quantity", "qty", "units", "volume"]),
        "revenue": (False, ["revenue", "sales", "amount", "turnover", "value"]),
    },
    "stock": {
        "sku": (True, ["sku", "item", "code", "reference", "product id"]),
        "snapshot_date": (True, ["date", "snapshot date", "as of", "stock date"]),
        "quantity_on_hand": (True, ["quantity", "qty", "on hand", "stock", "units in stock"]),
        "warehouse": (False, ["warehouse", "location", "site", "dc"]),
    },
}


@dataclass
class ImportResult:
    dataframe: pd.DataFrame
    rows_imported: int
    rows_rejected: int
    warnings: list[str] = field(default_factory=list)


def read_tabular_file(path: str | Path) -> pd.DataFrame:
    """Load a CSV or Excel file into a DataFrame of raw strings/objects."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        # Try a couple of common separators/encodings transparently.
        for sep in (",", ";", "\t"):
            try:
                df = pd.read_csv(path, sep=sep, engine="python")
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
        return pd.read_csv(path)
    elif suffix in (".xlsx", ".xlsm", ".xls"):
        return pd.read_excel(path, sheet_name=0)
    raise ValueError(f"Unsupported file type: {suffix}")


def guess_mapping(columns: list[str], import_type: str) -> dict[str, str | None]:
    """Best-effort automatic mapping from expected fields to source columns."""
    specs = FIELD_SPECS[import_type]
    lowered = {c: str(c).strip().lower() for c in columns}
    mapping: dict[str, str | None] = {}
    for field_name, (_, hints) in specs.items():
        match = None
        for col, low in lowered.items():
            if low == field_name.replace("_", " ") or low == field_name:
                match = col
                break
        if match is None:
            for col, low in lowered.items():
                if any(hint in low for hint in hints):
                    match = col
                    break
        mapping[field_name] = match
    return mapping


def _coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(r"[^\d\.\-eE]", "", regex=True), errors="coerce"
    )


def apply_mapping(df: pd.DataFrame, mapping: dict[str, str | None], import_type: str) -> ImportResult:
    """Rename mapped columns to canonical field names, coerce types, validate."""
    specs = FIELD_SPECS[import_type]
    warnings: list[str] = []

    out = pd.DataFrame()
    for field_name, source_col in mapping.items():
        if source_col and source_col in df.columns:
            out[field_name] = df[source_col]
        else:
            out[field_name] = np.nan

    required = [f for f, (req, _) in specs.items() if req]
    missing_required = [f for f in required if mapping.get(f) is None]
    if missing_required:
        raise ValueError(f"Missing required column mapping for: {', '.join(missing_required)}")

    total_rows = len(out)

    if import_type == "products":
        out["sku"] = out["sku"].astype(str).str.strip()
        out["name"] = out["name"].fillna(out["sku"]).astype(str).str.strip()
        out["category"] = out["category"].fillna("Uncategorized").astype(str).str.strip()
        out["supplier"] = out["supplier"].fillna("").astype(str).str.strip()
        for numcol, default in (("unit_cost", 0.0), ("unit_price", 0.0), ("lead_time_days", 14.0)):
            out[numcol] = _coerce_numeric(out[numcol]).fillna(default)
        out = out[out["sku"].str.len() > 0]
        out = out.drop_duplicates(subset="sku", keep="last")

    elif import_type == "sales":
        out["sku"] = out["sku"].astype(str).str.strip()
        out["sale_date"] = pd.to_datetime(out["sale_date"], errors="coerce", dayfirst=False)
        out["quantity"] = _coerce_numeric(out["quantity"])
        out["revenue"] = _coerce_numeric(out["revenue"]) if mapping.get("revenue") else np.nan
        before = len(out)
        out = out[out["sku"].str.len() > 0]
        out = out.dropna(subset=["sale_date", "quantity"])
        if len(out) < before:
            warnings.append(f"{before - len(out)} row(s) dropped: missing/invalid SKU, date or quantity.")
        out["revenue"] = out["revenue"].fillna(0.0)
        out["sale_date"] = out["sale_date"].dt.strftime("%Y-%m-%d")

    elif import_type == "stock":
        out["sku"] = out["sku"].astype(str).str.strip()
        out["snapshot_date"] = pd.to_datetime(out["snapshot_date"], errors="coerce", dayfirst=False)
        out["quantity_on_hand"] = _coerce_numeric(out["quantity_on_hand"])
        out["warehouse"] = out["warehouse"].fillna("Main").astype(str).str.strip()
        out.loc[out["warehouse"] == "", "warehouse"] = "Main"
        before = len(out)
        out = out[out["sku"].str.len() > 0]
        out = out.dropna(subset=["snapshot_date", "quantity_on_hand"])
        if len(out) < before:
            warnings.append(f"{before - len(out)} row(s) dropped: missing/invalid SKU, date or quantity.")
        out["snapshot_date"] = out["snapshot_date"].dt.strftime("%Y-%m-%d")

    rows_imported = len(out)
    rows_rejected = total_rows - rows_imported
    logger.info("Import %s: %d imported, %d rejected", import_type, rows_imported, rows_rejected)
    return ImportResult(dataframe=out.reset_index(drop=True), rows_imported=rows_imported,
                         rows_rejected=rows_rejected, warnings=warnings)
