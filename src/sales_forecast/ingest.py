"""Stap 1: verkoopregels inlezen uit een CSV-bestand."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from sales_forecast.utils.dates import parse_date

REQUIRED_COLUMNS: tuple[str, ...] = ("date", "product", "quantity", "unit_price")


class IngestError(ValueError):
    """Een regel of bestand voldoet niet aan het verwachte formaat."""


@dataclass(frozen=True)
class SalesRecord:
    sale_date: date
    product: str
    quantity: int
    unit_price: float

    @property
    def revenue(self) -> float:
        return self.quantity * self.unit_price


def _parse_price(raw: str) -> float:
    # Sommige exports gebruiken een decimale komma ("2,50").
    return float(raw.strip().replace(",", "."))


def parse_row(row: dict[str, str | None], line_number: int) -> SalesRecord:
    """Zet één CSV-regel om naar een SalesRecord, of gooi een IngestError."""
    try:
        sale_date = parse_date(row.get("date"))
    except ValueError as exc:
        raise IngestError(f"Regel {line_number}: {exc}") from exc
    if sale_date is None:
        raise IngestError(f"Regel {line_number}: datum ontbreekt")

    product = (row.get("product") or "").strip()
    if not product:
        raise IngestError(f"Regel {line_number}: product ontbreekt")

    try:
        quantity = int((row.get("quantity") or "").strip())
        unit_price = _parse_price(row.get("unit_price") or "")
    except ValueError as exc:
        raise IngestError(f"Regel {line_number}: ongeldig getal ({exc})") from exc

    if quantity < 0 or unit_price < 0:
        raise IngestError(f"Regel {line_number}: negatieve waarden zijn niet toegestaan")

    return SalesRecord(sale_date, product, quantity, unit_price)


def read_sales_csv(path: str | Path, *, skip_invalid: bool = False) -> list[SalesRecord]:
    """Lees een CSV-bestand met verkoopregels.

    Met ``skip_invalid=True`` worden foute regels overgeslagen in plaats van
    dat er een IngestError wordt gegooid.
    """
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise IngestError(f"Ontbrekende kolommen: {', '.join(missing)}")

        records: list[SalesRecord] = []
        # Regel 1 is de header, dus de eerste dataregel is regel 2.
        for line_number, row in enumerate(reader, start=2):
            try:
                records.append(parse_row(row, line_number))
            except IngestError:
                if not skip_invalid:
                    raise
        return records
