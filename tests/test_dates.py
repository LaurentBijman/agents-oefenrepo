from datetime import UTC, date, datetime

import pytest

from sales_forecast.utils.dates import (
    TIMEZONE,
    iter_periods,
    next_period_start,
    parse_date,
    parse_datetime,
    period_start,
    to_local_date,
)


def test_parse_date_iso_format():
    assert parse_date("2024-02-29") == date(2024, 2, 29)


def test_parse_date_strips_whitespace():
    assert parse_date("  2024-01-05 ") == date(2024, 1, 5)


@pytest.mark.parametrize("value", [None, "", "   "])
def test_parse_date_empty_input_returns_none(value):
    assert parse_date(value) is None


def test_parse_date_rejects_dutch_notation():
    with pytest.raises(ValueError, match="ISO 8601"):
        parse_date("29-02-2024")


def test_parse_datetime_naive_is_amsterdam_local_time():
    result = parse_datetime("2024-01-15T09:30:00")

    assert result.tzinfo == TIMEZONE
    assert result.hour == 9


def test_parse_datetime_converts_utc_to_summer_time():
    result = parse_datetime("2024-07-01T12:00:00Z")

    assert result.hour == 14
    assert result.utcoffset().total_seconds() == 2 * 3600


def test_parse_datetime_empty_input_returns_none():
    assert parse_datetime("") is None


def test_to_local_date_crosses_midnight():
    moment = datetime(2024, 1, 1, 23, 30, tzinfo=UTC)

    assert to_local_date(moment) == date(2024, 1, 2)


def test_to_local_date_rejects_naive_datetime():
    with pytest.raises(ValueError, match="tijdzone"):
        to_local_date(datetime(2024, 1, 1, 12, 0))


@pytest.mark.parametrize(
    ("period", "expected"),
    [("day", date(2024, 1, 10)), ("week", date(2024, 1, 8)), ("month", date(2024, 1, 1))],
)
def test_period_start(period, expected):
    assert period_start(date(2024, 1, 10), period) == expected


def test_period_start_unknown_period():
    with pytest.raises(ValueError, match="Onbekende periode"):
        period_start(date(2024, 1, 10), "year")


def test_next_period_start_month_rolls_over_year():
    assert next_period_start(date(2024, 12, 1), "month") == date(2025, 1, 1)


def test_iter_periods_months_includes_last():
    result = list(iter_periods(date(2024, 11, 15), date(2025, 2, 1), "month"))

    assert result == [date(2024, 11, 1), date(2024, 12, 1), date(2025, 1, 1), date(2025, 2, 1)]
