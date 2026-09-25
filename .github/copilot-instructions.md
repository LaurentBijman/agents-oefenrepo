# Copilot-instructies

De repo-brede instructies staan in [`AGENTS.md`](../AGENTS.md) in de root van deze
repository. Lees en volg die: Stack, Commando's, Architectuur, Regels en Klaar betekent.

Dit bestand bestaat zodat ook Copilot-omgevingen die `AGENTS.md` niet automatisch
inlezen (bijvoorbeeld Copilot code review op GitHub) dezelfde basis krijgen. De
belangrijkste afspraken nog één keer in het kort:

- Antwoord in het Nederlands; code-identifiers blijven Engels.
- Tests draaien met `make test`, linten met `make lint`.
- Datums altijd via `sales_forecast.utils.dates` (ISO 8601, Europe/Amsterdam).
- Geen geheimen in code, SQL alleen met parameters, geen kale `except:`.
- `src/sales_forecast/practice/` is oefenmateriaal: niet repareren tenzij gevraagd.

Meer specifieke regels staan in `.github/instructions/` (per pad), `.github/agents/`
(per rol) en `.github/skills/` (op aanvraag).
