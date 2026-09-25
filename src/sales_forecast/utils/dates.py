"""Datumhulpjes volgens de teamconventies.

De conventies staan uitgeschreven in .github/skills/datum-parsing/SKILL.md:
ISO 8601 als formaat, Europe/Amsterdam als tijdzone en lege invoer wordt None.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo("Europe/Amsterdam")

Period = Literal["day", "week", "month"]
PERIODS: tuple[str, ...] = ("day", "week", "month")


def parse_date(value: str | None) -> date | None:
    """Parse een ISO 8601-datum (``YYYY-MM-DD``); lege invoer geeft ``None``."""
    if value is None or not value.strip():
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError as exc:
        raise ValueError(f"Geen geldige ISO 8601-datum: {value!r}") from exc


def parse_datetime(value: str | None) -> datetime | None:
    """Parse een ISO 8601-tijdstip en geef het terug in Europe/Amsterdam.

    Een tijdstip zonder tijdzone wordt gelezen als lokale tijd in Amsterdam;
    een tijdstip met tijdzone wordt naar Amsterdam omgerekend.
    """
    if value is None or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip())
    except ValueError as exc:
        raise ValueError(f"Geen geldig ISO 8601-tijdstip: {value!r}") from exc
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=TIMEZONE)
    return parsed.astimezone(TIMEZONE)


def to_local_date(moment: datetime) -> date:
    """Geef de kalenderdatum van een tijdstip zoals die in Amsterdam geldt."""
    if moment.tzinfo is None:
        raise ValueError("Tijdstip zonder tijdzone; gebruik parse_datetime")
    return moment.astimezone(TIMEZONE).date()


def period_start(day: date, period: Period) -> date:
    """Geef het begin van de periode waarin ``day`` valt (week begint op maandag)."""
    if period == "day":
        return day
    if period == "week":
        return day - timedelta(days=day.weekday())
    if period == "month":
        return day.replace(day=1)
    raise ValueError(f"Onbekende periode: {period!r}, kies uit {PERIODS}")


def next_period_start(start: date, period: Period) -> date:
    """Geef het begin van de periode direct na de periode die op ``start`` begint."""
    if period == "day":
        return start + timedelta(days=1)
    if period == "week":
        return start + timedelta(weeks=1)
    if period == "month":
        if start.month == 12:
            return date(start.year + 1, 1, 1)
        return date(start.year, start.month + 1, 1)
    raise ValueError(f"Onbekende periode: {period!r}, kies uit {PERIODS}")


def iter_periods(first: date, last: date, period: Period) -> Iterator[date]:
    """Loop over alle periodestarts van ``first`` tot en met ``last``."""
    current = period_start(first, period)
    while current <= last:
        yield current
        current = next_period_start(current, period)
