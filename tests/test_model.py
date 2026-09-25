import pytest

from sales_forecast.model import (
    backtest,
    fit_linear_trend,
    forecast,
    linear_trend_forecast,
    mean_absolute_error,
    moving_average_forecast,
)


def test_moving_average_forecast_constant_series():
    assert moving_average_forecast([4, 4, 4, 4], horizon=2) == [4.0, 4.0]


def test_moving_average_forecast_uses_window():
    assert moving_average_forecast([1, 2, 3, 6], horizon=1, window=2) == [4.5]


def test_moving_average_forecast_too_short_series():
    with pytest.raises(ValueError, match="minimaal 3"):
        moving_average_forecast([1, 2], horizon=1)


def test_fit_linear_trend():
    slope, intercept = fit_linear_trend([1, 3, 5, 7])

    assert slope == pytest.approx(2.0)
    assert intercept == pytest.approx(1.0)


def test_linear_trend_forecast_extends_line():
    assert linear_trend_forecast([1, 3, 5, 7], horizon=2) == [9.0, 11.0]


def test_linear_trend_forecast_never_negative():
    assert linear_trend_forecast([6, 4, 2], horizon=3) == [0.0, 0.0, 0.0]


def test_forecast_unknown_method():
    with pytest.raises(ValueError, match="Onbekende methode"):
        forecast([1, 2, 3], horizon=1, method="magic")


def test_forecast_invalid_horizon():
    with pytest.raises(ValueError, match="horizon"):
        forecast([1, 2, 3], horizon=0)


def test_mean_absolute_error():
    assert mean_absolute_error([1, 2, 3], [2, 2, 5]) == pytest.approx(1.0)


def test_mean_absolute_error_length_mismatch():
    with pytest.raises(ValueError, match="even lang"):
        mean_absolute_error([1, 2], [1])


def test_backtest_perfect_trend():
    assert backtest([1, 3, 5, 7, 9, 11], holdout=2, method="linear_trend") == 0.0
