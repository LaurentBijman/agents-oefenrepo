"""Stap 3: eenvoudige voorspelmodellen voor een tijdreeks van verkopen."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

Method = Literal["moving_average", "linear_trend"]
METHODS: tuple[str, ...] = ("moving_average", "linear_trend")


@dataclass(frozen=True)
class Forecast:
    method: str
    values: list[float]


def _check_horizon(horizon: int) -> None:
    if horizon < 1:
        raise ValueError("horizon moet minimaal 1 zijn")


def moving_average_forecast(series: Sequence[float], horizon: int, window: int = 3) -> list[float]:
    """Voorspel recursief: elke stap is het gemiddelde van de laatste ``window`` waarden."""
    _check_horizon(horizon)
    if window < 1:
        raise ValueError("window moet minimaal 1 zijn")
    if len(series) < window:
        raise ValueError(f"minimaal {window} waarnemingen nodig, kreeg {len(series)}")
    history = list(series)
    predictions: list[float] = []
    for _ in range(horizon):
        value = sum(history[-window:]) / window
        predictions.append(round(value, 2))
        history.append(value)
    return predictions


def fit_linear_trend(series: Sequence[float]) -> tuple[float, float]:
    """Bereken de kleinste-kwadratenlijn door de reeks; geeft ``(helling, snijpunt)``."""
    n = len(series)
    if n < 2:
        raise ValueError("minimaal 2 waarnemingen nodig voor een trend")
    mean_x = (n - 1) / 2
    mean_y = sum(series) / n
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in enumerate(series))
    denominator = sum((x - mean_x) ** 2 for x in range(n))
    slope = numerator / denominator
    return slope, mean_y - slope * mean_x


def linear_trend_forecast(series: Sequence[float], horizon: int) -> list[float]:
    """Trek de trendlijn door; negatieve verkopen bestaan niet, dus minimaal 0."""
    _check_horizon(horizon)
    slope, intercept = fit_linear_trend(series)
    n = len(series)
    return [round(max(0.0, intercept + slope * (n + step)), 2) for step in range(horizon)]


def forecast(
    series: Sequence[float], horizon: int, method: Method = "moving_average", window: int = 3
) -> Forecast:
    """Maak een voorspelling met de gekozen methode."""
    if method == "moving_average":
        values = moving_average_forecast(series, horizon, window)
    elif method == "linear_trend":
        values = linear_trend_forecast(series, horizon)
    else:
        raise ValueError(f"Onbekende methode: {method!r}, kies uit {METHODS}")
    return Forecast(method, values)


def mean_absolute_error(actual: Sequence[float], predicted: Sequence[float]) -> float:
    """Gemiddelde absolute afwijking tussen werkelijkheid en voorspelling."""
    if not actual:
        raise ValueError("lege reeks")
    if len(actual) != len(predicted):
        raise ValueError("reeksen moeten even lang zijn")
    return sum(abs(a - p) for a, p in zip(actual, predicted, strict=True)) / len(actual)


def backtest(
    series: Sequence[float], holdout: int, method: Method = "moving_average", window: int = 3
) -> float:
    """Houd de laatste ``holdout`` waarden achter, voorspel ze en geef de MAE terug."""
    if not 1 <= holdout < len(series):
        raise ValueError("holdout moet tussen 1 en de lengte van de reeks liggen")
    train, actual = series[:-holdout], series[-holdout:]
    result = forecast(train, holdout, method, window)
    return round(mean_absolute_error(actual, result.values), 2)
