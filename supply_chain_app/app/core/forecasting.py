"""Sales forecasting engine.

Implements a small set of classical, transparent forecasting methods with no
heavy ML dependency, on purpose: a Distribution Manager needs to be able to
trust *and explain* a forecast, which is much easier for methods with a
closed-form formula than for a black-box model.

Methods implemented:
    - Moving Average          (flat forecast, smooths noise)
    - Simple Exponential Smoothing (SES)   (flat forecast, reacts to level shifts)
    - Holt's Linear Trend      (extrapolates a trend)
    - Naive Seasonal           (repeats last year's same period)

``auto_forecast`` backtests the applicable methods on the tail of the
history and picks the one with the lowest MAPE, so the user gets a good
default while still being able to override the method manually.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from app.config import FORECAST_HORIZON_MONTHS, MIN_HISTORY_POINTS


@dataclass
class ForecastResult:
    method: str
    history: pd.Series                 # original observed series (index = period 'YYYY-MM')
    fitted: pd.Series                  # in-sample one-step-ahead fitted values
    forecast: pd.Series                # out-of-sample forecast (index = future periods)
    accuracy: dict                     # {"mae":..., "rmse":..., "mape":...}
    explanation: str
    params: dict = field(default_factory=dict)


def build_series(sales_monthly: pd.DataFrame, sku: str) -> pd.Series:
    """Return the monthly quantity series for one SKU, indexed by period string."""
    sub = sales_monthly[sales_monthly["sku"] == sku].sort_values("period")
    return pd.Series(sub["quantity"].values, index=sub["period"].values, dtype=float)


def _next_periods(last_period: str, horizon: int) -> list[str]:
    ts = pd.Period(last_period, freq="M")
    return [str(ts + i) for i in range(1, horizon + 1)]


def _accuracy(actual: np.ndarray, fitted: np.ndarray) -> dict:
    mask = ~np.isnan(fitted) & ~np.isnan(actual)
    if mask.sum() == 0:
        return {"mae": float("nan"), "rmse": float("nan"), "mape": float("nan")}
    err = actual[mask] - fitted[mask]
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err ** 2)))
    nonzero = actual[mask] != 0
    mape = float(np.mean(np.abs(err[nonzero] / actual[mask][nonzero])) * 100) if nonzero.any() else float("nan")
    return {"mae": mae, "rmse": rmse, "mape": mape}


# ---------------------------------------------------------------------------
# Individual methods
# ---------------------------------------------------------------------------
def moving_average(series: pd.Series, horizon: int, window: int = 3) -> ForecastResult:
    values = series.values.astype(float)
    n = len(values)
    window = max(1, min(window, n))
    fitted = np.full(n, np.nan)
    for t in range(window, n):
        fitted[t] = values[t - window:t].mean()
    last_avg = values[-window:].mean() if n else 0.0
    future_idx = _next_periods(series.index[-1], horizon)
    forecast = pd.Series([last_avg] * horizon, index=future_idx)

    explanation = (
        f"Moving Average (window={window}): each forecast point is the flat "
        f"average of the last {window} observed month(s) ({last_avg:,.1f} units/month). "
        "Best suited to stable demand with little trend or seasonality."
    )
    return ForecastResult(
        method="Moving Average", history=series, fitted=pd.Series(fitted, index=series.index),
        forecast=forecast, accuracy=_accuracy(values, fitted), explanation=explanation,
        params={"window": window},
    )


def simple_exponential_smoothing(series: pd.Series, horizon: int, alpha: float = 0.3) -> ForecastResult:
    values = series.values.astype(float)
    n = len(values)
    level = values[0] if n else 0.0
    fitted = np.full(n, np.nan)
    for t in range(1, n):
        fitted[t] = level
        level = alpha * values[t] + (1 - alpha) * level
    future_idx = _next_periods(series.index[-1], horizon)
    forecast = pd.Series([level] * horizon, index=future_idx)

    explanation = (
        f"Simple Exponential Smoothing (alpha={alpha}): the forecast is a flat "
        f"level of {level:,.1f} units/month, an exponentially-weighted average that "
        "reacts to recent months more than old ones. No trend is projected."
    )
    return ForecastResult(
        method="Simple Exponential Smoothing", history=series, fitted=pd.Series(fitted, index=series.index),
        forecast=forecast, accuracy=_accuracy(values, fitted), explanation=explanation,
        params={"alpha": alpha},
    )


def holt_linear(series: pd.Series, horizon: int, alpha: float = 0.3, beta: float = 0.2) -> ForecastResult:
    values = series.values.astype(float)
    n = len(values)
    if n < 2:
        return simple_exponential_smoothing(series, horizon, alpha)

    level = values[0]
    trend = values[1] - values[0]
    fitted = np.full(n, np.nan)
    for t in range(1, n):
        fitted[t] = level + trend
        new_level = alpha * values[t] + (1 - alpha) * (level + trend)
        trend = beta * (new_level - level) + (1 - beta) * trend
        level = new_level

    future_idx = _next_periods(series.index[-1], horizon)
    forecast_values = [level + (h + 1) * trend for h in range(horizon)]
    forecast_values = [max(0.0, v) for v in forecast_values]  # demand can't be negative
    forecast = pd.Series(forecast_values, index=future_idx)

    trend_word = "growing" if trend > 0 else ("declining" if trend < 0 else "flat")
    explanation = (
        f"Holt's Linear Trend (alpha={alpha}, beta={beta}): projects a {trend_word} "
        f"trend of {trend:+,.1f} units/month on top of a current level of {level:,.1f} "
        "units/month. Best suited when demand shows a sustained up/down trend."
    )
    return ForecastResult(
        method="Holt Linear Trend", history=series, fitted=pd.Series(fitted, index=series.index),
        forecast=forecast, accuracy=_accuracy(values, fitted), explanation=explanation,
        params={"alpha": alpha, "beta": beta},
    )


def naive_seasonal(series: pd.Series, horizon: int, season_length: int = 12) -> ForecastResult:
    values = series.values.astype(float)
    n = len(values)
    fitted = np.full(n, np.nan)
    for t in range(season_length, n):
        fitted[t] = values[t - season_length]

    future_idx = _next_periods(series.index[-1], horizon)
    if n >= season_length:
        forecast_values = [values[n - season_length + (h % season_length)] for h in range(horizon)]
    else:
        forecast_values = [values[-1]] * horizon
    forecast = pd.Series(forecast_values, index=future_idx)

    explanation = (
        f"Naive Seasonal (season={season_length} months): repeats the demand observed "
        "in the same period one year earlier. Captures recurring seasonal patterns "
        "without smoothing trend or noise."
    )
    return ForecastResult(
        method="Naive Seasonal", history=series, fitted=pd.Series(fitted, index=series.index),
        forecast=forecast, accuracy=_accuracy(values, fitted), explanation=explanation,
        params={"season_length": season_length},
    )


METHODS = {
    "Moving Average": moving_average,
    "Simple Exponential Smoothing": simple_exponential_smoothing,
    "Holt Linear Trend": holt_linear,
    "Naive Seasonal": naive_seasonal,
}


def auto_forecast(series: pd.Series, horizon: int = FORECAST_HORIZON_MONTHS) -> ForecastResult:
    """Backtest the applicable methods and return the one with the lowest MAPE.

    Falls back to a flat "last value" forecast when history is too short for
    any method to be fitted reliably.
    """
    n = len(series)
    if n == 0:
        empty = pd.Series(dtype=float)
        return ForecastResult(
            method="No Data", history=empty, fitted=empty, forecast=empty,
            accuracy={"mae": float("nan"), "rmse": float("nan"), "mape": float("nan")},
            explanation="No sales history available for this SKU.",
        )
    if n < MIN_HISTORY_POINTS:
        last_val = float(series.iloc[-1])
        future_idx = _next_periods(series.index[-1], horizon)
        forecast = pd.Series([last_val] * horizon, index=future_idx)
        return ForecastResult(
            method="Naive (insufficient history)", history=series, fitted=series * np.nan,
            forecast=forecast, accuracy={"mae": float("nan"), "rmse": float("nan"), "mape": float("nan")},
            explanation=(
                f"Only {n} month(s) of history available (minimum {MIN_HISTORY_POINTS} recommended). "
                f"Using the last observed value ({last_val:,.1f} units) as a flat forecast."
            ),
        )

    candidates = [moving_average, simple_exponential_smoothing, holt_linear]
    if n >= 24:
        candidates.append(naive_seasonal)

    best_result = None
    best_score = float("inf")
    for fn in candidates:
        result = fn(series, horizon)
        score = result.accuracy["mape"]
        if np.isnan(score):
            score = result.accuracy["mae"] if not np.isnan(result.accuracy["mae"]) else float("inf")
        if score < best_score:
            best_score = score
            best_result = result
    best_result.explanation = "[Auto-selected: lowest backtested error] " + best_result.explanation
    return best_result
