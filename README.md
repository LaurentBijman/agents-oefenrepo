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
     Loopt er iets vast of gebruik je `uv`? Zie [Debug](#debug).
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

## Debug

Problemen die deelnemers bij een lokale installatie tegenkwamen, met de oplossing.

### `make` niet gevonden

| Systeem       | Installeren                                                        |
| ------------- | ------------------------------------------------------------------ |
| Windows       | `winget install ezwinports.make` en open daarna een nieuwe terminal |
| macOS         | `xcode-select --install` (Command Line Tools, bevat `make`)        |
| Linux (Debian/Ubuntu) | `sudo apt install make`                                    |

Wil je geen `make` installeren? Gebruik dan de commando's uit de tabel bij
[Commando's](#commandos).

### Python 3.12 met een gewone venv (pip)

Heb je zelf Python 3.12 geïnstalleerd, dan werkt alles zoals beschreven:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (PowerShell)
source .venv/bin/activate     # macOS / Linux
make install
make test
make check-agents
```

Controleer met `python --version` dat je echt 3.12 (of hoger) gebruikt.

### Python 3.12 met `uv`

[`uv`](https://docs.astral.sh/uv/) kan Python 3.12 zelf voor je installeren, maar let op:
**een venv van `uv` bevat standaard geen `pip`**. `make install` draait
`python -m pip install ...` en faalt dan met `No module named pip`. Kies één van twee routes.

Route A: laat `uv` pip in de venv zetten, dan werkt de Makefile ongewijzigd:

```bash
uv python install 3.12
uv venv --python 3.12 --seed   # --seed installeert pip in de venv
.venv\Scripts\activate          # Windows; macOS/Linux: source .venv/bin/activate
make install
make test
make check-agents
```

Route B: installeer met `uv` zelf en sla `make install` over:

```bash
uv python install 3.12
uv venv --python 3.12
.venv\Scripts\activate          # Windows; macOS/Linux: source .venv/bin/activate
uv pip install -e ".[dev]"
make test
make check-agents
```

Wil je de venv niet activeren? Geef dan de Python van de venv mee aan `make`:
`make test PYTHON=.venv/Scripts/python.exe` (Windows) of
`make test PYTHON=.venv/bin/python` (macOS/Linux).

### `uv`: `failed to hardlink file` (os error 396)

`uv` koppelt bestanden standaard via hardlinks vanuit zijn cache. In een map die door
OneDrive wordt gesynchroniseerd (vaak `Downloads`, `Documenten` of `Bureaublad` op Windows)
mag dat niet. Laat `uv` de bestanden kopiëren:

```powershell
$env:UV_LINK_MODE = 'copy'   # alleen deze terminal
setx UV_LINK_MODE copy       # permanent; open daarna een nieuwe terminal
```

Of clone de repo naar een map buiten OneDrive, bijvoorbeeld `C:\dev\`.

### `python` opent de Microsoft Store of doet niets (Windows)

Zonder actieve venv wijst `python` op Windows vaak naar een placeholder in
`...\WindowsApps\python.exe`. Controleer het met `Get-Command python` (PowerShell).
Activeer je venv, of zet de aliassen uit via *Instellingen* → *Apps* →
*Geavanceerde app-instellingen* → *App-uitvoeringsaliassen* (`python.exe` en `python3.exe`).

### Activeren van de venv wordt geblokkeerd (PowerShell)

Krijg je `running scripts is disabled on this system`? Sta lokale scripts toe voor je eigen
gebruiker:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### `ModuleNotFoundError: No module named 'pytest'` (of `ruff`, `yaml`)

De dev-afhankelijkheden zitten niet in de Python die je gebruikt. Meestal is de venv niet
geactiveerd, of is de installatie zonder `[dev]` gedaan. Activeer de venv en draai opnieuw
`make install` (of `uv pip install -e ".[dev]"`).

### VS Code gebruikt de verkeerde Python

Kies de interpreter van de venv: `Ctrl+Shift+P` → *Python: Select Interpreter* →
`.venv`. Open daarna een nieuwe terminal in VS Code, zodat die de venv automatisch activeert.

### `make lint` faalt lokaal maar niet in de CI (of andersom)

`ruff` is vastgepind op `>=0.16,<0.17`, omdat nieuwe versies de formatting veranderen.
Een globaal geïnstalleerde `ruff` kan een andere versie zijn. Gebruik de `ruff` uit de
venv (`python -m ruff --version`) en draai `make format` om automatisch te herstellen.
