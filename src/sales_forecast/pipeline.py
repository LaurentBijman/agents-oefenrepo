"""Koppelt de drie stappen: ingest → transform → model."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from sales_forecast.ingest import read_sales_csv
from sales_forecast.model import METHODS, Forecast, Method, forecast
from sales_forecast.transform import (
    aggregate_by_period,
    fill_missing_periods,
    filter_products,
    to_series,
)
from sales_forecast.utils.dates import PERIODS, Period


def run(
    path: str | Path,
    period: Period = "week",
    horizon: int = 4,
    method: Method = "moving_average",
    products: Sequence[str] | None = None,
) -> Forecast:
    """Lees een CSV, maak er een reeks van en voorspel ``horizon`` perioden vooruit."""
    records = read_sales_csv(path, skip_invalid=True)
    if products:
        records = filter_products(records, products)
    totals = fill_missing_periods(aggregate_by_period(records, period), period)
    return forecast(to_series(totals), horizon, method)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Maak een eenvoudige verkoopvoorspelling.")
    parser.add_argument("csv", type=Path, help="CSV met kolommen date,product,quantity,unit_price")
    parser.add_argument("--period", choices=PERIODS, default="week")
    parser.add_argument("--horizon", type=int, default=4)
    parser.add_argument("--method", choices=METHODS, default="moving_average")
    parser.add_argument("--product", action="append", dest="products")
    args = parser.parse_args(argv)

    result = run(args.csv, args.period, args.horizon, args.method, args.products)
    print(f"Methode: {result.method}")
    for step, value in enumerate(result.values, start=1):
        print(f"  +{step} {args.period}: {value}")
    return 0
