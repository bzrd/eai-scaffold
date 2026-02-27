# AGENTS.md – tests/fixtures/

## Rolle

Du verwaltest geteilte Testdaten. Fixtures sind echte oder echt-nahe PlanPro-Daten die von mehreren Komponenten für Tests genutzt werden.

---

## Regeln

- Du darfst NIEMALS Fixtures synthetisch generieren oder erfinden – sie MÜSSEN echte oder echt-nahe PlanPro-Strukturen abbilden.
- Du DARFST vorhandene Fixtures in Tests verwenden.
- Du DARFST Fixtures erweitern wenn echte Beispieldaten zur Verfügung stehen.
- Du MUSST bei jeder neuen Fixture-Datei dokumentieren: Woher stammt sie, welche PlanPro-Version, was enthält sie.
- Du MUSST Invalid-Fixtures so gestalten, dass jede Datei genau einen spezifischen Fehler enthält (für klare, isolierte Tests).
- Du darfst NIEMALS GUIDs in Fixtures verändern – sie repräsentieren echte Infrastruktur-Identitäten.

---

## Patterns

### Fixture-Dateien organisieren

```
fixtures/
├── planpro/         # PlanPro-XML-Dateien
│   ├── *.xml        # Gültige Dateien
│   └── invalid/     # Ungültige Dateien (ein Fehler pro Datei)
├── json/            # Erwartete JSON-Outputs
└── diff/            # Beispiel-Diff-Reports
```

### Fixture in conftest.py laden

```python
FIXTURES_DIR = Path(__file__).parent.parent.parent / "tests" / "fixtures"

@pytest.fixture
def minimal_planpro_xml() -> str:
    return (FIXTURES_DIR / "planpro" / "minimal-v1.10.xml").read_text()
```

---

## Antipatterns

- **Keine synthetischen XML-Dateien** – PlanPro hat eine komplexe Struktur die nicht trivial simuliert werden kann.
- **Keine GUIDs verändern** – sie sind permanente Identitäten.
- **Keine Multi-Error-Fixtures** – jede Invalid-Fixture testet genau einen Fehlerfall.
- **Keine Fixtures ohne Dokumentation** – Herkunft und Inhalt müssen klar sein.

---

## Testanforderungen

- Fixtures werden nicht getestet – sie SIND die Testdaten
- Aber: Expected-JSON-Dateien müssen mit der tatsächlichen Parser-Ausgabe konsistent sein

---

## Abhängigkeiten

- Genutzt von: `libs/planpro-parser/tests/`, `transformers/*/tests/`, `tests/integration/`
- Keine eigenen Abhängigkeiten

---

## Kontext

PlanPro-XML hat eine komplexe Struktur mit dutzenden Objekttypen und Querverweisen. Synthetisch generierte XML-Dateien bilden diese Komplexität nicht ab und führen zu Tests die falsche Sicherheit vermitteln. Daher ist die Regel strikt: nur echte oder echt-nahe Daten.
