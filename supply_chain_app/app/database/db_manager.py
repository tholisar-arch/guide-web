"""Thin, dependency-free wrapper around the local SQLite database.

Every query in the application goes through :class:`DatabaseManager`, which
keeps a single long-lived connection (SQLite handles concurrent readers from
one process fine) and exposes small, purpose-specific helper methods rather
than leaking raw SQL through the rest of the codebase.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from app.config import DATABASE_PATH
from app.database.schema import SCHEMA_SQL
from app.utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Owns the single SQLite connection used across the application."""

    def __init__(self, db_path: Path | str = DATABASE_PATH):
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def _initialize_schema(self) -> None:
        self._conn.executescript(SCHEMA_SQL)
        self._conn.commit()
        logger.info("Database ready at %s", self.db_path)

    @property
    def connection(self) -> sqlite3.Connection:
        return self._conn

    def close(self) -> None:
        self._conn.close()

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------
    def execute(self, sql: str, params: Iterable[Any] = ()) -> sqlite3.Cursor:
        cur = self._conn.execute(sql, params)
        self._conn.commit()
        return cur

    def query_df(self, sql: str, params: Iterable[Any] = ()) -> pd.DataFrame:
        return pd.read_sql_query(sql, self._conn, params=params)

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------
    def upsert_products(self, df: pd.DataFrame) -> int:
        """Insert or update product master data. Returns the number of rows written."""
        rows = df.to_dict("records")
        self._conn.executemany(
            """
            INSERT INTO products (sku, name, category, supplier, unit_cost, unit_price, lead_time_days, updated_at)
            VALUES (:sku, :name, :category, :supplier, :unit_cost, :unit_price, :lead_time_days, datetime('now'))
            ON CONFLICT(sku) DO UPDATE SET
                name=excluded.name,
                category=excluded.category,
                supplier=excluded.supplier,
                unit_cost=excluded.unit_cost,
                unit_price=excluded.unit_price,
                lead_time_days=excluded.lead_time_days,
                updated_at=datetime('now')
            """,
            rows,
        )
        self._conn.commit()
        return len(rows)

    def ensure_products_exist(self, skus: Iterable[str]) -> None:
        """Create a bare product row for any SKU referenced by a fact table but
        not yet present in the master data, so foreign keys never fail on import."""
        unique_skus = sorted(set(skus))
        self._conn.executemany(
            "INSERT OR IGNORE INTO products (sku, name) VALUES (?, ?)",
            [(sku, sku) for sku in unique_skus],
        )
        self._conn.commit()

    def get_products(self) -> pd.DataFrame:
        return self.query_df("SELECT * FROM products ORDER BY sku")

    # ------------------------------------------------------------------
    # Sales
    # ------------------------------------------------------------------
    def insert_sales(self, df: pd.DataFrame) -> int:
        self.ensure_products_exist(df["sku"].tolist())
        rows = df.to_dict("records")
        self._conn.executemany(
            "INSERT INTO sales (sku, sale_date, quantity, revenue) VALUES (:sku, :sale_date, :quantity, :revenue)",
            rows,
        )
        self._conn.commit()
        return len(rows)

    def get_sales(self) -> pd.DataFrame:
        return self.query_df("SELECT * FROM sales ORDER BY sale_date")

    def get_sales_monthly(self) -> pd.DataFrame:
        """Sales aggregated to (sku, year-month) buckets — the base series for
        forecasting, ABC/XYZ, and coverage calculations."""
        df = self.get_sales()
        if df.empty:
            return df
        df["sale_date"] = pd.to_datetime(df["sale_date"])
        df["period"] = df["sale_date"].dt.to_period("M").astype(str)
        grouped = (
            df.groupby(["sku", "period"], as_index=False)
            .agg(quantity=("quantity", "sum"), revenue=("revenue", "sum"))
            .sort_values(["sku", "period"])
        )
        return grouped

    # ------------------------------------------------------------------
    # Stock
    # ------------------------------------------------------------------
    def insert_stock(self, df: pd.DataFrame) -> int:
        self.ensure_products_exist(df["sku"].tolist())
        rows = df.to_dict("records")
        self._conn.executemany(
            "INSERT INTO stock_levels (sku, snapshot_date, quantity_on_hand, warehouse) "
            "VALUES (:sku, :snapshot_date, :quantity_on_hand, :warehouse)",
            rows,
        )
        self._conn.commit()
        return len(rows)

    def get_latest_stock(self) -> pd.DataFrame:
        """Most recent stock snapshot per SKU (summed across warehouses)."""
        sql = """
            SELECT sku, snapshot_date, SUM(quantity_on_hand) AS quantity_on_hand
            FROM stock_levels
            WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM stock_levels s2 WHERE s2.sku = stock_levels.sku)
            GROUP BY sku
        """
        return self.query_df(sql)

    # ------------------------------------------------------------------
    # Import log
    # ------------------------------------------------------------------
    def log_import(self, file_name: str, import_type: str, rows_imported: int, rows_rejected: int = 0) -> None:
        self.execute(
            "INSERT INTO import_log (file_name, import_type, rows_imported, rows_rejected) VALUES (?, ?, ?, ?)",
            (file_name, import_type, rows_imported, rows_rejected),
        )

    def get_import_log(self) -> pd.DataFrame:
        return self.query_df("SELECT * FROM import_log ORDER BY imported_at DESC")

    # ------------------------------------------------------------------
    # Simulation parameters (persisted so the Simulator remembers its state)
    # ------------------------------------------------------------------
    def get_simulation_params(self) -> dict:
        row = self.query_df("SELECT * FROM simulation_params WHERE id = 1").iloc[0]
        return row.to_dict()

    def save_simulation_params(self, service_level: float, lead_time_days: float,
                                review_period_days: float, demand_growth_pct: float) -> None:
        self.execute(
            """
            UPDATE simulation_params
            SET service_level = ?, lead_time_days = ?, review_period_days = ?, demand_growth_pct = ?
            WHERE id = 1
            """,
            (service_level, lead_time_days, review_period_days, demand_growth_pct),
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------
    def clear_all_data(self) -> None:
        for table in ("sales", "stock_levels", "products", "import_log"):
            self._conn.execute(f"DELETE FROM {table}")
        self._conn.commit()
        logger.info("All application data cleared by user request")
