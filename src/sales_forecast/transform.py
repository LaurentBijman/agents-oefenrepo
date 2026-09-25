"""Stap 2: losse verkoopregels omzetten naar een tijdreeks per periode.

Alle functies hier zijn puur: geen I/O en de invoer wordt nooit aangepast.
"""

from __future__ import annotations

import statistics
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from sales_forecast.ingest import SalesRecord
from sales_forecast.utils.dates import Period, iter_periods, period_start

SERIES_FIELDS: tuple[str, ...] = ("quantity", "revenue")


@dataclass(frozen=True)
class PeriodTotal:
    period_start: date
    quantity: int
    revenue: float


def filter_products(records: Iterable[SalesRecord], products: Iterable[str]) -> list[SalesRecord]:
    """Houd alleen regels over voor de opgegeven producten (hoofdletterongevoelig)."""
    wanted = {product.strip().lower() for product in products}
    return [record for record in records if record.product.lower() in wanted]


def aggregate_by_period(
    records: Iterable[SalesRecord], period: Period = "day"
) -> list[PeriodTotal]:
    """Tel aantallen en omzet op per periode, gesorteerd op periodestart."""
    quantities: dict[date, int] = defaultdict(int)
    revenues: dict[date, float] = defaultdict(float)
    for record in records:
        key = period_start(record.sale_date, period)
        quantities[key] += record.quantity
        revenues[key] += record.revenue
    return [
        PeriodTotal(key, quantities[key], round(revenues[key], 2)) for key in sorted(quantities)
    ]


def fill_missing_periods(totals: list[PeriodTotal], period: Period = "day") -> list[PeriodTotal]:
    """Vul gaten in de reeks op met perioden zonder verkoop (0 stuks, 0 omzet)."""
    if not totals:
        return []
    by_start = {total.period_start: total for total in totals}
    first = min(by_start)
    last = max(by_start)
    return [
        by_start.get(start, PeriodTotal(start, 0, 0.0))
        for start in iter_periods(first, last, period)
    ]


def remove_outliers(totals: list[PeriodTotal], z_threshold: float = 3.0) -> list[PeriodTotal]:
    """Verwijder perioden waarvan het aantal meer dan ``z_threshold`` standaarddeviaties afwijkt."""
    if len(totals) < 3:
        return list(totals)
    quantities = [total.quantity for total in totals]
    mean = statistics.fmean(quantities)
    stdev = statistics.pstdev(quantities)
    if stdev == 0:
        return list(totals)
    return [total for total in totals if abs(total.quantity - mean) / stdev <= z_threshold]


def to_series(totals: Iterable[PeriodTotal], field: str = "quantity") -> list[float]:
    """Haal één kolom uit de totalen als lijst getallen, klaar voor het model."""
    if field not in SERIES_FIELDS:
        raise ValueError(f"Onbekend veld: {field!r}, kies uit {SERIES_FIELDS}")
    return [float(getattr(total, field)) for total in totals]
