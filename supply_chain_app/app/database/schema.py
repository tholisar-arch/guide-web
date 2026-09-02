"""SQLite schema definition for the application's local database.

The schema is intentionally simple (star-like): a ``products`` master table,
and time-series fact tables (``sales``, ``stock_levels``) that reference it.
Everything runs 100% locally; no network access is required or performed.
"""

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    sku             TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    category        TEXT DEFAULT 'Uncategorized',
    supplier        TEXT DEFAULT '',
    unit_cost       REAL DEFAULT 0,
    unit_price      REAL DEFAULT 0,
    lead_time_days  REAL DEFAULT 14,
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sales (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    sku         TEXT NOT NULL,
    sale_date   TEXT NOT NULL,          -- ISO date 'YYYY-MM-DD'
    quantity    REAL NOT NULL DEFAULT 0,
    revenue     REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (sku) REFERENCES products (sku) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sales_sku_date ON sales (sku, sale_date);

CREATE TABLE IF NOT EXISTS stock_levels (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sku                 TEXT NOT NULL,
    snapshot_date       TEXT NOT NULL,   -- ISO date 'YYYY-MM-DD'
    quantity_on_hand    REAL NOT NULL DEFAULT 0,
    warehouse           TEXT DEFAULT 'Main',
    FOREIGN KEY (sku) REFERENCES products (sku) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_stock_sku_date ON stock_levels (sku, snapshot_date);

CREATE TABLE IF NOT EXISTS import_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name       TEXT NOT NULL,
    import_type     TEXT NOT NULL,      -- 'products' | 'sales' | 'stock'
    rows_imported   INTEGER NOT NULL,
    rows_rejected   INTEGER NOT NULL DEFAULT 0,
    imported_at     TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS simulation_params (
    id                      INTEGER PRIMARY KEY CHECK (id = 1),
    service_level           REAL DEFAULT 0.95,
    lead_time_days          REAL DEFAULT 14,
    review_period_days      REAL DEFAULT 7,
    demand_growth_pct       REAL DEFAULT 0.0
);

INSERT OR IGNORE INTO simulation_params (id, service_level, lead_time_days, review_period_days, demand_growth_pct)
VALUES (1, 0.95, 14, 7, 0.0);
"""
