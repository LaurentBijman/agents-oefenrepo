---
name: datum-parsing
description: Teamconventies voor datums en tijden in sales_forecast (ISO 8601, Europe/Amsterdam, lege invoer wordt None). Gebruik deze skill bij het parsen, formatteren of vergelijken van datums, bij tijdzones of zomertijd, en bij het indelen in dagen, weken of maanden.
---

# Datum-parsing: de teamconventies

## De vier afspraken

1. **Formaat is ISO 8601.** Datum: `2024-03-31`. Tijdstip: `2024-03-31T14:05:00+02:00`.
   Nooit `31-03-2024`, `03/31/2024` of een eigen `strptime`-formaat, ook niet "even snel".
2. **Tijdzone is `Europe/Amsterdam`.** Een tijdstip zonder tijdzone is lokale Amsterdamse
   tijd; een tijdstip met tijdzone wordt naar Amsterdam omgerekend. Gebruik nooit een vaste
   offset als `+01:00`: die klopt in de zomer niet.
3. **Lege invoer wordt `None`.** `None`, `""` en `"   "` geven `None`, geen exceptie.
   Ongeldige invoer geeft een `ValueError` met een Nederlandse melding. De aanroeper beslist
   of `None` mag: in `ingest.py` is een datum verplicht, dus daar wordt het een `IngestError`.
4. **Weken beginnen op maandag, maanden op dag 1.** Dat volgt ISO 8601 en is wat de
   rapportages van het team verwachten.

## Gebruik de bestaande helpers

Alles staat in `src/sales_forecast/utils/dates.py`. Schrijf geen eigen varianten.

| Nodig                                  | Functie                                  |
| -------------------------------------- | ---------------------------------------- |
| Tekst → `date` (of `None`)             | `parse_date(value)`                      |
| Tekst → `datetime` in Amsterdam        | `parse_datetime(value)`                  |
| `datetime` → Amsterdamse kalenderdag   | `to_local_date(moment)`                  |
| Begin van dag/week/maand               | `period_start(day, period)`              |
| Alle periodes tussen twee datums       | `iter_periods(first, last, period)`      |
| De tijdzone zelf                       | `TIMEZONE`                               |

## Voorbeelden

```python
from datetime import date

from sales_forecast.utils.dates import parse_date, parse_datetime, period_start

parse_date("2024-02-29")  # date(2024, 2, 29)
parse_date("  ")  # None
parse_date("29-02-2024")  # ValueError: Geen geldige ISO 8601-datum
parse_datetime("2024-07-01T12:00:00Z")  # 14:00 in Amsterdam (+02:00, zomertijd)
period_start(date(2024, 1, 10), "week")  # date(2024, 1, 8), een maandag
```

## Valkuilen

- `datetime.now()` zonder tijdzone: gebruik `datetime.now(TIMEZONE)`.
- Een UTC-tijdstip rond middernacht valt in Amsterdam vaak op de *volgende* dag. Gebruik
  `to_local_date` in plaats van `.date()`.
- Op de nacht van de zomertijdwissel (laatste zondag van maart) bestaat 02:00-03:00 lokaal
  niet. Rekenen met `timedelta(hours=...)` op lokale tijden gaat daar fout; reken in UTC.
- Op Windows is het pakket `tzdata` nodig voor `ZoneInfo`. Dat staat al in `pyproject.toml`.
