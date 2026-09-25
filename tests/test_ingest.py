from datetime import date

import pytest

from sales_forecast.ingest import IngestError, SalesRecord, parse_row, read_sales_csv


def test_read_sales_csv_parses_rows(write_csv):
    path = write_csv('2024-01-01,koffie,2,3.50\n2024-01-02,thee,1,"2,25"\n')

    result = read_sales_csv(path)

    assert result == [
        SalesRecord(date(2024, 1, 1), "koffie", 2, 3.50),
        SalesRecord(date(2024, 1, 2), "thee", 1, 2.25),
    ]


def test_read_sales_csv_missing_column(write_csv):
    path = write_csv("2024-01-01,koffie,2\n", header="date,product,quantity\n")

    with pytest.raises(IngestError, match="unit_price"):
        read_sales_csv(path)


def test_read_sales_csv_reports_line_number(write_csv):
    path = write_csv("2024-01-01,koffie,2,3.50\n2024-01-02,thee,veel,2.25\n")

    with pytest.raises(IngestError, match="Regel 3"):
        read_sales_csv(path)


def test_read_sales_csv_skip_invalid(write_csv):
    path = write_csv("2024-01-01,koffie,2,3.50\n,thee,1,2.25\n")

    result = read_sales_csv(path, skip_invalid=True)

    assert [record.product for record in result] == ["koffie"]


def test_parse_row_empty_date():
    row = {"date": "", "product": "koffie", "quantity": "1", "unit_price": "1"}

    with pytest.raises(IngestError, match="datum ontbreekt"):
        parse_row(row, line_number=2)


def test_parse_row_negative_quantity():
    row = {"date": "2024-01-01", "product": "koffie", "quantity": "-1", "unit_price": "1"}

    with pytest.raises(IngestError, match="negatieve"):
        parse_row(row, line_number=2)


def test_sales_record_revenue():
    record = SalesRecord(date(2024, 1, 1), "koffie", 3, 2.5)

    assert record.revenue == pytest.approx(7.5)
