from datetime import date

import pytest

from sales_forecast.transform import (
    PeriodTotal,
    aggregate_by_period,
    fill_missing_periods,
    filter_products,
    remove_outliers,
    to_series,
)


def test_aggregate_by_period_day(records):
    result = aggregate_by_period(records, "day")

    assert result == [
        PeriodTotal(date(2024, 1, 1), 3, 9.25),
        PeriodTotal(date(2024, 1, 3), 4, 14.0),
        PeriodTotal(date(2024, 1, 9), 3, 10.5),
    ]


def test_aggregate_by_period_week(records):
    result = aggregate_by_period(records, "week")

    assert [(t.period_start, t.quantity) for t in result] == [
        (date(2024, 1, 1), 7),
        (date(2024, 1, 8), 3),
    ]


def test_fill_missing_periods_adds_zero_days():
    totals = [PeriodTotal(date(2024, 1, 1), 2, 5.0), PeriodTotal(date(2024, 1, 3), 1, 2.5)]

    result = fill_missing_periods(totals, "day")

    assert result[1] == PeriodTotal(date(2024, 1, 2), 0, 0.0)
    assert len(result) == 3


def test_fill_missing_periods_empty_input():
    assert fill_missing_periods([], "day") == []


def test_remove_outliers_drops_spike():
    totals = [PeriodTotal(date(2024, 1, day), 10, 10.0) for day in range(1, 10)]
    totals.append(PeriodTotal(date(2024, 1, 10), 100, 100.0))

    result = remove_outliers(totals, z_threshold=2.5)

    assert len(result) == 9
    assert all(total.quantity == 10 for total in result)


def test_remove_outliers_constant_series_unchanged():
    totals = [PeriodTotal(date(2024, 1, day), 5, 5.0) for day in range(1, 5)]

    assert remove_outliers(totals) == totals


def test_filter_products_is_case_insensitive(records):
    result = filter_products(records, ["KOFFIE"])

    assert len(result) == 3


def test_to_series_revenue():
    totals = [PeriodTotal(date(2024, 1, 1), 2, 5.0)]

    assert to_series(totals, "revenue") == [5.0]


def test_to_series_unknown_field():
    with pytest.raises(ValueError, match="Onbekend veld"):
        to_series([], "price")
