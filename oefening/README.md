# Oefening: bouw je eigen review-agent

**Doel:** je schrijft een custom agent, `review-agent`, die Python-code reviewt volgens de
afspraken van dit team. Je test hem op een bewust slecht bestand en laat hem daarna een
pull request beoordelen.

**Tijd:** ongeveer 45 minuten.

**Wat je nodig hebt:** je fork van deze repo, geopend in VS Code of een Codespace, met
GitHub Copilot Chat aan. Zie de [README in de root](../README.md) voor de setup.

**Materiaal in deze map:**

| Bestand                                                        | Wat                                           |
| -------------------------------------------------------------- | --------------------------------------------- |
| [`review-agent.template.agent.md`](review-agent.template.agent.md) | Skelet om mee te beginnen                  |
| [`checklist.md`](checklist.md)                                 | Waar een goed agent-bestand aan voldoet       |
| [`oplossing/review-agent.agent.md`](oplossing/review-agent.agent.md) | Voorbeeldoplossing. Pas kijken als je klaar bent! |

---

## Stap 1: maak een branch

```bash
git checkout -b mijn-agent
```

Werk nooit direct op `main`: in stap 5 open je een pull request vanaf deze branch.

## Stap 2: maak de map voor agents

De map `.github/agents/` bestaat al, want de voorbeeldagent `test-writer.agent.md` staat
erin. Kijk er even naar: jouw agent krijgt dezelfde opbouw.

```bash
ls .github/agents/
```

Werk je in een andere repo zonder deze map? Maak hem dan aan met `mkdir -p .github/agents`.
Copilot zoekt custom agents precies op deze plek, met de extensie `.agent.md`.

## Stap 3: schrijf `review-agent.agent.md`

Kopieer het skelet en vul alle TODO's in:

```bash
cp oefening/review-agent.template.agent.md .github/agents/review-agent.agent.md
```

Een agent-bestand heeft twee delen:

1. **Frontmatter** (het YAML-blok tussen `---`):
   - `name`: `review-agent`
   - `description`: één zin; wat doet hij en wanneer kies je hem?
   - `tools`: alleen wat een reviewer nodig heeft. Moet een reviewer bestanden kunnen wijzigen?
2. **Instructies** (de Markdown eronder), minstens:
   - de rol, in één of twee zinnen
   - waar hij op let (tip: `AGENTS.md` heeft een lijst met regels)
   - het outputformaat: **maximaal 5 punten, elk met regelnummer**
   - wat hij nooit doet: **nooit zelf code wijzigen**

Loop daarna [`checklist.md`](checklist.md) langs. Controleer ook of je frontmatter geldig is:

```bash
make check-agents
```

## Stap 4: kies je agent met `/agents`

1. Open `src/sales_forecast/practice/report_export.py`. Dit bestand is bewust slecht.
2. Open Copilot Chat (`Ctrl+Alt+I` / `Cmd+Ctrl+I`), typ `/agents` en kies
   **review-agent** in de lijst. (De agent-dropdown onder het invoerveld werkt ook.)
   Zie je hem niet? Herlaad het venster (`Developer: Reload Window`) en controleer de
   bestandsnaam en de frontmatter. In de Copilot CLI kies je hem met `/agent`.
3. Vraag: *"Review dit bestand."*

Controleer het antwoord:

- Zijn het er maximaal 5, met regelnummers?
- Vond hij het hardcoded token, de SQL-injectie en de kale `except:`?
- Test de grens: vraag *"Fix het eerste punt maar meteen."* Weigert hij netjes?

Niet tevreden? Pas je instructies aan en probeer opnieuw. Juist dat itereren is de
oefening. Schrijf op wat je veranderde en waarom.

## Stap 5: commit, push, PR en laat de agent reviewen

```bash
git add .github/agents/review-agent.agent.md
git commit -m "Voeg review-agent toe"
git push -u origin mijn-agent
```

1. Zorg dat de PR iets te reviewen heeft: los in dezelfde branch **één** bevinding uit
   stap 4 op in `report_export.py` (bijvoorbeeld het token naar een omgevingsvariabele),
   commit en push.
2. Open een pull request van `mijn-agent` naar `main` **van je eigen fork** (niet naar de
   originele repo). Let op de dropdown "base repository" op GitHub.
3. De workflow `tests` draait: lint, tests en `make check-agents` op je nieuwe agent.
   Draait er niets? In een fork staan Actions standaard uit: zet ze aan via het tabblad
   *Actions* (zie de setup in de [README](../README.md#setup)) en push opnieuw.
4. Laat de agent de PR reviewen. Installeer de extensie *GitHub Pull Requests* (zit al in de
   Codespace), check de PR uit, kies **review-agent** via `/agents` en vraag:
   *"Review de wijzigingen in deze PR ten opzichte van main."*
5. Zet de bevindingen als reviewcommentaar in de PR.

> **Waarom niet direct op GitHub.com?** Copilot op GitHub.com gebruikt de custom agents
> van de standaardbranch. Je agent staat nog op `mijn-agent`, dus daar is hij pas na de
> merge beschikbaar. Merge je PR en probeer het daarna nog eens via de Agents-tab.

---

## Klaar? Extra uitdagingen

- Laat `test-writer` tests schrijven voor `iter_periods` in `utils/dates.py`. Past hij de
  regels uit `tests.instructions.md` toe? Vraag hem ook iets in `src/` te wijzigen.
- Voeg een pad-instructie toe voor `src/sales_forecast/model.py`.
- Vergelijk je agent met [`oplossing/review-agent.agent.md`](oplossing/review-agent.agent.md).
  Wat deed jij beter?
- Geef je review-agent de skill `datum-parsing` als extra kennisbron. Vindt hij dan meer?

## Problemen?

| Probleem                            | Oplossing                                                          |
| ----------------------------------- | ------------------------------------------------------------------ |
| Agent staat niet in `/agents`       | Bestand moet in `.github/agents/` staan en eindigen op `.agent.md` |
| `make check-agents` geeft een FOUT  | Lees de melding; vaak een lege `description` of `tools` zonder lijst |
| Agent wijzigt tóch code             | Haal `edit` uit `tools` en maak de regel in "Wat je nooit doet" harder |
| Agent geeft 12 punten               | Maak het outputformaat concreet, met een voorbeeld                 |
