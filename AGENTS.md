# AGENTS.md

Repo-brede instructies voor AI-agents (laag 1). Copilot en andere agents die
`AGENTS.md` lezen, krijgen dit bij elke vraag in deze repository mee. Houd het
kort en concreet: alles hier kost context bij *elke* vraag.

## Stack

- Python 3.12, src-layout (`src/sales_forecast/`)
- Alleen de standaardbibliotheek in `src/` (plus `tzdata` voor tijdzones op Windows)
- pytest voor tests, ruff voor linting en formatting
- Configuratie staat in `pyproject.toml`; er is geen `setup.py` of `requirements.txt`

## Commando's

| Doel                         | Commando                                                               |
| ---------------------------- | ---------------------------------------------------------------------- |
| Installeren                  | `make install` (= `pip install -e ".[dev]"`)                           |
| Tests                        | `make test`                                                            |
| Lint + formatcheck           | `make lint`                                                            |
| Automatisch formatteren      | `make format`                                                          |
| Frontmatter van agents check | `make check-agents`                                                    |
| Voorspelling draaien         | `python -m sales_forecast data/sample_sales.csv --period week --horizon 4` |

## Architectuur

De pipeline loopt in één richting; een module importeert alleen van links naar rechts.

```text
ingest.py  ──►  transform.py  ──►  model.py
(CSV → SalesRecord)  (→ PeriodTotal per dag/week/maand)  (→ Forecast)
        \              |              /
         └──── utils/dates.py ───────┘   (datums en tijdzones)

pipeline.py   koppelt de drie stappen en bevat de CLI
practice/     OEFENMATERIAAL, geen onderdeel van de pipeline
```

- `ingest` is de enige module die bestanden leest.
- `transform` en `model` zijn puur: geen I/O, geen print, invoer wordt niet aangepast.
- Alle datumlogica gaat via `sales_forecast.utils.dates` (zie skill `datum-parsing`).

## Regels

- Code-identifiers in het Engels; commentaar, docstrings en foutmeldingen in het Nederlands.
- Type hints op alle publieke functies; `from __future__ import annotations` bovenaan.
- Geen nieuwe runtime-afhankelijkheden zonder overleg.
- Geen geheimen in code. Tokens en wachtwoorden komen uit omgevingsvariabelen.
- SQL altijd met parameters (`?`), nooit via string-concatenatie of f-strings.
- Nooit een kale `except:`; vang een specifieke exceptie en log of herhaal hem.
- Functies kort houden (richtlijn: onder de 30 regels); splits anders op.
- `src/sales_forecast/practice/` is bewust slecht oefenmateriaal. Niet repareren of
  refactoren tenzij de gebruiker daar expliciet om vraagt.

## Klaar betekent

- [ ] `make test` is groen
- [ ] `make lint` is groen
- [ ] Nieuwe of gewijzigde logica heeft een test in `tests/`
- [ ] Publieke functies hebben een docstring
- [ ] Geen losse `print`-debugging, uitgecommentarieerde code of TODO zonder uitleg
