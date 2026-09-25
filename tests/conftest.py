from datetime import date
from pathlib import Path

import pytest

from sales_forecast.ingest import SalesRecord

CSV_HEADER = "date,product,quantity,unit_price\n"


@pytest.fixture
def write_csv(tmp_path: Path):
    """Schrijf een CSV met header naar tmp_path en geef het pad terug."""

    def _write(body: str, header: str = CSV_HEADER) -> Path:
        path = tmp_path / "sales.csv"
        path.write_text(header + body, encoding="utf-8")
        return path

    return _write


@pytest.fixture
def records() -> list[SalesRecord]:
    return [
        SalesRecord(date(2024, 1, 1), "koffie", 2, 3.50),
        SalesRecord(date(2024, 1, 1), "thee", 1, 2.25),
        SalesRecord(date(2024, 1, 3), "koffie", 4, 3.50),
        SalesRecord(date(2024, 1, 9), "Koffie", 3, 3.50),
    ]
