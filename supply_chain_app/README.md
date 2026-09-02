# Supply Chain & Sales Decision Assistant

A professional, 100% local Windows desktop application built with **Python
and PySide6**, designed for an **EMEA Distribution Manager** who needs to
pilot sales, stock, forecasting and operational performance from a single
tool — no server, no browser, no cloud.

## Features

1. **Excel / CSV import** — flexible column mapping (auto-guessed, user
   confirmable) for product master data, sales history and stock snapshots.
2. **Local SQLite database** — all data stays on the machine, stored under
   `%APPDATA%/SupplyChainAssistant` on Windows.
3. **KPI dashboard** — revenue, units sold, stock value, active SKUs,
   average selling price, monthly trend, top products, revenue by category.
4. **Sales forecasting** — Moving Average, Simple Exponential Smoothing,
   Holt's Linear Trend and Naive Seasonal methods, with an "Auto" mode that
   backtests and picks the lowest-error method, plus MAE/RMSE/MAPE metrics.
5. **ABC / XYZ analysis** — Pareto revenue classification crossed with
   demand-variability classification, 3x3 matrix and Pareto chart.
6. **Stock coverage** — days of coverage, safety stock and reorder point
   using the classic `z(service level) x sigma x sqrt(lead time)` formula.
7. **Automatic recommendations** — rule-based, prioritized, and explained
   action list combining ABC/XYZ and coverage analysis (reorder now, reduce
   excess stock, review forecast, obsolescence risk, etc.).
8. **What-if simulator** — sliders for service level, lead time, review
   period and demand growth, recomputing safety stock / reorder points /
   coverage live, with a saved-baseline comparison.
9. **Explanations everywhere** — every screen carries an explanation panel
   stating exactly which formula and inputs produced the numbers shown.
10. **PDF & Excel report generation** — one-click executive PDF report
    (reportlab) and multi-sheet Excel workbook (openpyxl), saved locally.

## Constraints honored

- **No web components**: the UI is built entirely with native Qt widgets
  (PySide6) and charts are rendered natively via matplotlib's Qt backend —
  no browser, no HTML/JS, no embedded web view anywhere.
- **100% local / offline**: SQLite database, local file import/export, no
  network calls.
- **Modular architecture**: `app/database` (persistence), `app/core`
  (pure-Python business logic, unit-testable independently of the UI),
  `app/ui` (PySide6 screens), `app/reports` (PDF/Excel export).
- **Documented code**: module- and function-level docstrings explain the
  *why*, not just the *what* — formulas are spelled out where they matter.
- **Windows 11 compatible**, with a **PyInstaller** spec ready to build a
  standalone `.exe`.

## Project layout

```
supply_chain_app/
├── main.py                     # entry point
├── build.spec                  # PyInstaller build spec (-> .exe)
├── requirements.txt
├── app/
│   ├── config.py                # paths & default business parameters
│   ├── database/
│   │   ├── schema.py            # SQLite DDL
│   │   └── db_manager.py        # all SQL goes through here
│   ├── core/                    # pure business logic, no Qt dependency
│   │   ├── importer.py          # Excel/CSV -> normalized DataFrame
│   │   ├── kpi.py
│   │   ├── forecasting.py
│   │   ├── abc_xyz.py
│   │   ├── stock_coverage.py
│   │   ├── recommendations.py
│   │   └── simulator.py
│   ├── reports/
│   │   ├── pdf_report.py
│   │   └── excel_report.py
│   └── ui/
│       ├── theme.py             # Qt stylesheet
│       ├── main_window.py       # sidebar navigation + page stack
│       └── widgets/             # one module per screen
├── sample_data/                 # demo CSVs (products/sales/stock) + generator
└── tests/                       # pytest unit tests for app/core
```

## Running from source

Requires Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux (for development)
pip install -r requirements.txt
python main.py
```

On first launch, use **Import Data** to load the sample CSVs in
`sample_data/` (or your own Excel/CSV exports) to see the dashboard,
forecasts, ABC/XYZ analysis, stock coverage and recommendations populate.

## Running the tests

```bash
pip install pytest
pytest tests/ -q
```

## Building a Windows executable

```bash
pip install pyinstaller
pyinstaller build.spec
```

The standalone application is produced under `dist/SupplyChainAssistant/`,
including `SupplyChainAssistant.exe`. Copy the whole folder to deploy —
PyInstaller's one-folder mode starts faster than a single-file `.exe` and is
the recommended distribution shape for this app. Drop a `.ico` file at
`resources/app_icon.ico` before building to brand the executable.

## Data model

- `products` — SKU master data (name, category, supplier, unit cost/price,
  lead time).
- `sales` — one row per sales transaction (SKU, date, quantity, revenue).
- `stock_levels` — periodic stock snapshots (SKU, date, quantity on hand,
  warehouse).
- `simulation_params` — the currently saved what-if baseline (service
  level, lead time, review period, demand growth) used across the app.
- `import_log` — audit trail of every file imported.

All formulas (safety stock, reorder point, ABC/XYZ thresholds, forecast
methods) are implemented in `app/core/` with references to their
definitions in each module's docstring, so results can be audited and
explained to stakeholders.
