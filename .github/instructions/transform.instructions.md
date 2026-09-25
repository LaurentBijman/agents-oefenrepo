---
applyTo: "src/sales_forecast/transform.py"
description: Regels voor de transformatiestap van de pipeline.
---

# Regels voor transform.py

1. Functies blijven puur: geen I/O, geen `print`, geen globale state, en de invoerlijst
   wordt nooit aangepast. Geef altijd een nieuwe lijst terug.
2. Uitvoer is altijd gesorteerd op `period_start`, oplopend.
3. Omzet wordt pas afgerond (2 decimalen) bij het maken van een `PeriodTotal`, niet
   tussendoor, zodat afrondingsfouten zich niet opstapelen.
4. Periodegrenzen alleen via `period_start` en `iter_periods` uit `utils/dates.py`.
   Geen eigen `timedelta`-rekenwerk voor weken of maanden.
5. Een nieuwe transformatie is een nieuwe functie met een test in `tests/test_transform.py`;
   breid bestaande functies niet uit met extra vlaggen.
