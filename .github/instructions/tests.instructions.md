---
applyTo: "tests/**"
description: Regels voor het schrijven van pytest-tests in deze repo.
---

# Regels voor tests

1. Eén testbestand per module: `tests/test_<module>.py`. Testnamen volgen
   `test_<functie>_<situatie>`, bijvoorbeeld `test_parse_date_empty_input_returns_none`.
2. Alleen pytest-stijl: kale `assert`, `pytest.raises(..., match=...)` met een stukje van de
   Nederlandse foutmelding, en `pytest.approx` voor floats. Geen `unittest.TestCase`.
3. Geen netwerk en geen bestanden buiten `tmp_path`. Gebruik de fixture `write_csv` uit
   `tests/conftest.py` om een CSV te maken.
4. Eén gedrag per test, opgebouwd als Arrange / Act / Assert met een lege regel ertussen.
5. Test naast het normale pad altijd de randgevallen: lege invoer, ongeldige invoer en
   grenswaarden (bijvoorbeeld de jaarwisseling of een week die op maandag begint).
