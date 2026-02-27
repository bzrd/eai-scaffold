# tests/fixtures/ – Geteilte Testdaten

## Zweck

Geteilte Testdaten die von mehreren Komponenten genutzt werden. Enthält echte oder echt-nahe PlanPro-Beispieldateien, erwartete JSON-Outputs und Beispiel-Diff-Reports.

---

## Struktur

```
fixtures/
├── planpro/
│   ├── minimal-v1.9.xml         # Minimale PlanPro-Datei (wenige Objekte, Version 1.9)
│   ├── minimal-v1.10.xml        # Minimale PlanPro-Datei (wenige Objekte, Version 1.10)
│   ├── realistic-v1.10.xml      # Realistische PlanPro-Datei (komplexe Referenzen)
│   └── invalid/
│       ├── missing-guid.xml     # PlanPro mit fehlender GUID
│       ├── invalid-guid.xml     # PlanPro mit ungültigem UUID-Format
│       └── unknown-type.xml     # PlanPro mit unbekanntem Objekttyp
├── json/
│   ├── expected-minimal.json    # Erwarteter JSON-Output für minimal XML
│   └── expected-realistic.json  # Erwarteter JSON-Output für realistisches XML
├── diff/
│   ├── sample-diff-report.json  # Beispiel-Diff-Report
│   └── empty-diff-report.json   # Diff-Report bei identischen Ständen
├── README.md
└── AGENTS.md
```

---

## Konventionen

- **Fixtures werden NIEMALS generiert oder synthetisch erzeugt** – sie müssen echte oder echt-nahe PlanPro-Strukturen abbilden
- Minimale Fixtures: wenige Objekte (3-5) für schnelle Tests
- Realistische Fixtures: komplexe Referenzstrukturen, dutzende Objekte
- Verschiedene PlanPro-Versionen: mindestens 1.9 und 1.10
- Invalid-Fixtures: für Fehlerfall-Tests

---

## Abhängigkeiten

- Werden von `libs/planpro-parser/tests/`, `transformers/*/tests/`, `tests/integration/` genutzt

---

## Beispiel: Fixture in Test verwenden

```python
# conftest.py
import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent.parent / "tests" / "fixtures"

@pytest.fixture
def minimal_planpro_xml() -> str:
    return (FIXTURES_DIR / "planpro" / "minimal-v1.10.xml").read_text()

@pytest.fixture
def expected_json() -> dict:
    return json.loads((FIXTURES_DIR / "json" / "expected-minimal.json").read_text())
```

---

## Checkliste für neue Fixtures

- [ ] Echte oder echt-nahe PlanPro-Struktur (nicht synthetisch)
- [ ] GUIDs im gültigen UUID-Format
- [ ] PlanPro-Version angegeben
- [ ] Dateiname beschreibt den Inhalt
- [ ] Bei Invalid-Fixtures: genau ein Fehler pro Datei (für klare Tests)
