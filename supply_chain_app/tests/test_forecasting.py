import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core import forecasting


def _series(values, start="2024-01"):
    idx = [str(p) for p in pd.period_range(start=start, periods=len(values), freq="M")]
    return pd.Series(values, index=idx, dtype=float)


def test_moving_average_flat_forecast():
    series = _series([10, 12, 11, 13, 12, 14])
    result = forecasting.moving_average(series, horizon=3, window=3)
    assert len(result.forecast) == 3
    assert np.allclose(result.forecast.values, result.forecast.values[0])
    expected_last_avg = series.values[-3:].mean()
    assert result.forecast.iloc[0] == pytest.approx(expected_last_avg)


def test_holt_linear_projects_positive_trend():
    series = _series([10, 20, 30, 40, 50, 60])
    result = forecasting.holt_linear(series, horizon=2, alpha=0.8, beta=0.8)
    assert result.forecast.iloc[1] > result.forecast.iloc[0]
    assert result.forecast.iloc[0] > series.iloc[-1] * 0.9


def test_forecast_never_negative():
    series = _series([5, 3, 1, 0, 0, 1])
    result = forecasting.holt_linear(series, horizon=6)
    assert (result.forecast.values >= 0).all()


def test_auto_forecast_short_history_uses_naive():
    series = _series([10, 12])
    result = forecasting.auto_forecast(series, horizon=1)
    assert "insufficient history" in result.method.lower()
    assert result.forecast.iloc[0] == pytest.approx(12)


def test_auto_forecast_picks_a_valid_method():
    series = _series([10, 11, 9, 12, 13, 14, 15, 16])
    result = forecasting.auto_forecast(series, horizon=3)
    assert len(result.forecast) == 3
    assert result.method  # non-empty
