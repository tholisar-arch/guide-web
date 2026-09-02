"""Central configuration: paths, defaults and tunable business parameters.

All values here are defaults only; the Simulator screen lets the user
override the business parameters (service level, lead time, growth, ...)
at runtime without touching this file.
"""
from __future__ import annotations

import sys
from pathlib import Path


def _app_data_dir() -> Path:
    """Return a writable per-user directory, valid both frozen (.exe) and as script.

    On Windows this resolves to %APPDATA%/SupplyChainAssistant. When the app is
    packaged with PyInstaller (``sys.frozen``), the executable's own folder is
    read-only in many corporate deployments, so we never write next to it.
    """
    if sys.platform.startswith("win"):
        base = Path(
            __import__("os").environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
        )
    else:
        base = Path.home() / ".local" / "share"
    path = base / "SupplyChainAssistant"
    path.mkdir(parents=True, exist_ok=True)
    return path


APP_NAME = "Supply Chain & Sales Decision Assistant"
APP_ORG = "EMEA Distribution Analytics"
APP_VERSION = "1.0.0"

DATA_DIR = _app_data_dir()
DATABASE_PATH = DATA_DIR / "supply_chain.db"
REPORTS_DIR = DATA_DIR / "reports"
LOG_DIR = DATA_DIR / "logs"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Default business parameters (all editable live in the Simulator screen)
# ---------------------------------------------------------------------------
DEFAULT_SERVICE_LEVEL = 0.95          # target probability of not stocking out
DEFAULT_LEAD_TIME_DAYS = 14           # supplier replenishment lead time
DEFAULT_REVIEW_PERIOD_DAYS = 7        # how often stock is reviewed / reordered
DEFAULT_DEMAND_GROWTH_PCT = 0.0       # simulated demand growth applied to forecast

# ABC classification cumulative-revenue thresholds
ABC_THRESHOLD_A = 0.80
ABC_THRESHOLD_B = 0.95

# XYZ classification coefficient-of-variation thresholds
XYZ_THRESHOLD_X = 0.5
XYZ_THRESHOLD_Y = 1.0

# Stock coverage classification (in days of forward coverage)
COVERAGE_CRITICAL_DAYS = DEFAULT_LEAD_TIME_DAYS       # below lead time => stockout risk
COVERAGE_EXCESS_DAYS = 120                            # above this => overstock

# Forecasting
FORECAST_HORIZON_MONTHS = 3
MIN_HISTORY_POINTS = 4

APP_ICON = str(Path(__file__).resolve().parent.parent / "resources" / "app_icon.ico")
