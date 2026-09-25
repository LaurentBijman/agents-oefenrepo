# agents-oefenrepo

Oefenrepository voor de workshop **"Je eigen Copilot-agent"**. Je schrijft een custom agent
(`.agent.md`) en ziet hoe gelaagde instructies samenwerken in een echt, klein Python-project.

Het project zelf is een eenvoudige verkoopvoorspelling: **ingest → transform → model**.
De code is niet het onderwerp; het is het speelveld.

## Chat in de IDE vs. een custom agent

- **Rol:** gewone chat begint elke vraag blanco en jij zet de rol in je prompt. Een custom
  agent heeft een vaste rol die in de repo staat, onder versiebeheer en voor iedereen gelijk.
- **Tools:** chat in agent-modus mag alles wat jij toestaat. Een custom agent krijgt alleen
  de tools uit zijn frontmatter, bijvoorbeeld alleen lezen en zoeken.
- **Output:** chat antwoordt zoals het uitkomt. Een agent heeft een afgesproken
  outputformaat, zoals "maximaal 5 punten, met regelnummer".
- **Grenzen:** in chat moet je elke keer zeggen wat niet mag. Een agent heeft harde regels
  ("wijzig nooit zelf code") die bij elke vraag gelden.

## De 4 instructielagen

```text
agents-oefenrepo/
├── AGENTS.md ─────────────────────────────┐  LAAG 1 · repo-breed
├── .github/                               │  altijd actief, bij elke vraag
│   ├── copilot-instructions.md ───────────┘  (verwijst naar AGENTS.md)
│   │
│   ├── instructions/ ─────────────────────┐  LAAG 2 · per pad
│   │   ├── tests.instructions.md          │  actief als het bestand waar je
│   │   └── transform.instructions.md ─────┘  aan werkt matcht met applyTo
│   │
│   ├── agents/ ───────────────────────────┐  LAAG 3 · per rol
│   │   ├── test-writer.agent.md           │  actief als je de agent kiest
│   │   └── review-agent.agent.md ─────────┘  ◄── die schrijf jij!
│   │
│   └── skills/ ───────────────────────────┐  LAAG 4 · op aanvraag
│       └── datum-parsing/SKILL.md ────────┘  geladen als de taak erom vraagt
│
├── src/sales_forecast/   ingest.py → transform.py → model.py (+ utils/dates.py)
│   └── practice/report_export.py   ◄── bewust slecht, reviewmateriaal
├── tests/
└── oefening/             de opdracht, het skelet, de checklist en de oplossing
```

Hoe de lagen stapelen als je de test-writer vraagt tests te schrijven in `tests/test_dates.py`:

```text
  AGENTS.md                       laag 1  (altijd)
+ tests.instructions.md           laag 2  (want tests/** matcht)
+ test-writer.agent.md            laag 3  (want die agent heb je gekozen)
+ datum-parsing/SKILL.md          laag 4  (want de taak gaat over datums)
= de context waarmee Copilot aan de slag gaat
```

| Laag         | Bestand                               | Wanneer actief                      | Hier voor                    |
| ------------ | ------------------------------------- | ----------------------------------- | ---------------------------- |
| 1. Repo-breed | `AGENTS.md`, `.github/copilot-instructions.md` | Altijd                     | Stack, commando's, regels    |
| 2. Per pad   | `.github/instructions/*.instructions.md` | Bestand matcht `applyTo`          | Regels voor tests, transform |
| 3. Per rol   | `.github/agents/*.agent.md`           | Als je de agent kiest               | Test-writer, review-agent    |
| 4. Op aanvraag | `.github/skills/*/SKILL.md`         | Als de `description` bij de taak past | Datumconventies            |

Vuistregel: hoe lager de laag, hoe specifieker en hoe minder vaak geladen. Zet iets zo laag
mogelijk, dan kost het alleen context als het nodig is.

## Setup

1. **Fork** deze repository naar je eigen GitHub-account (knop *Fork* rechtsboven).
2. **Zet Actions aan in je fork.** GitHub schakelt workflows in een fork standaard uit.
   Ga naar het tabblad *Actions* en klik op *I understand my workflows, go ahead and enable
   them*. Anders draait de CI niet op je pull request in stap 5.
3. **Open** je fork op één van twee manieren:
   - **Codespace (aanbevolen):** *Code* → *Codespaces* → *Create codespace on main*. Python,
     de extensies en `make install` worden automatisch ingericht.
   - **Lokaal in VS Code:** clone je fork, zorg voor Python 3.12 en draai `make install`.
     Geen `make` (standaard op Windows)? Gebruik de commando's uit de tabel hieronder.
4. **Controleer** dat alles werkt:
   ```bash
   make test          # alle tests groen
   make check-agents  # frontmatter van agents, skills en instructies geldig
   ```
5. **Open Copilot Chat** (`Ctrl+Alt+I` / `Cmd+Ctrl+I`) en typ `/agents`. Daar staat
   **test-writer** tussen de ingebouwde agents. Kies hem en vraag:
   *"Schrijf tests voor `iter_periods` in utils/dates.py."*

Je hebt nodig: een GitHub-account met Copilot en een recente VS Code met de Copilot
Chat-extensie. `.vscode/settings.json` zet `AGENTS.md`, instructiebestanden en skills aan.

## Aan de slag

➡️ **[Naar de oefening: oefening/README.md](oefening/README.md)**

## Commando's

| Commando            | Zonder `make` (bv. Windows)                          | Wat                                     |
| ------------------- | ---------------------------------------------------- | --------------------------------------- |
| `make install`      | `python -m pip install -e ".[dev]"`                  | Installeer het project en de dev-tools  |
| `make test`         | `python -m pytest`                                   | Draai de tests                          |
| `make lint`         | `python -m ruff check .` en `python -m ruff format --check .` | Lint en formatcheck            |
| `make check-agents` | `python scripts/check_frontmatter.py`                | Valideer de frontmatter van agents, skills en instructies |

Voorspelling draaien: `python -m sales_forecast data/sample_sales.csv --period week`.

De workflow [`tests.yml`](.github/workflows/tests.yml) draait lint, tests en
`check-agents` bij elke pull request.
