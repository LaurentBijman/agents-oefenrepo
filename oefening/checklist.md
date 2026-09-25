# Checklist: een goed agent-bestand

Loop deze lijst langs voordat je je agent test. Elke "nee" is een reden om je bestand aan
te passen.

## 1. Eén duidelijke rol

- [ ] Kun je in één zin zeggen wat de agent doet? Staat die zin in `description`?
- [ ] Doet de agent **één** ding? "Reviewt en fixt en schrijft tests" zijn drie agents.
- [ ] Is `name` kort, in kleine letters met koppeltekens, en gelijk aan de bestandsnaam
      (`review-agent` → `review-agent.agent.md`)?
- [ ] Beschrijft `description` ook *wanneer* je de agent kiest? Copilot gebruikt die tekst
      om te bepalen of de agent bij een vraag past.

## 2. Beperkte tools

- [ ] Staat in `tools` alleen wat de rol echt nodig heeft?
- [ ] Heeft een agent die niets mag wijzigen ook geen `edit`?
- [ ] Heeft de agent `execute` (terminal) of `web` alleen als je kunt uitleggen waarom?
- [ ] Is `tools` een YAML-lijst, bijvoorbeeld `["read", "search"]`?

> Een regel in de instructies ("wijzig nooit code") is een verzoek. Een tool die ontbreekt
> is een garantie. Gebruik allebei.

## 3. Een vast outputformaat

- [ ] Staat er een concreet voorbeeld van het antwoord in het bestand?
- [ ] Is er een maximum (bijvoorbeeld 5 punten), zodat het antwoord leesbaar blijft?
- [ ] Moet elk punt naar een plek wijzen (`bestand:regel`)?
- [ ] Is duidelijk wat de agent zegt als er **niets** te melden is?

## 4. Wat de agent nooit doet

- [ ] Staan de harde grenzen in een eigen kopje, bovenaan of onderaan goed zichtbaar?
- [ ] Staat erbij wat de agent in plaats daarvan doet (bijvoorbeeld doorverwijzen)?
- [ ] Zijn het er weinig genoeg (3 tot 5) dat ze allemaal serieus genomen worden?

## 5. Past in de lagen

- [ ] Herhaal je niet wat al in `AGENTS.md` of `.github/instructions/` staat? Verwijs ernaar.
- [ ] Staat er niets in dat eigenlijk voor het hele team geldt? Dat hoort in `AGENTS.md`.
- [ ] Is specialistische kennis die maar soms nodig is een skill in plaats van agent-tekst?

## 6. Getest

- [ ] `make check-agents` is groen.
- [ ] Je hebt de agent geprobeerd op `practice/report_export.py`.
- [ ] Je hebt de grens getest: *"Los het maar meteen op."* Weigerde hij?
- [ ] Je hebt minstens één keer je instructies aangepast op basis van wat je zag.
