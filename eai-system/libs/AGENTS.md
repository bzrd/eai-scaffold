# AGENTS.md – libs/

## Rolle

Du erweiterst oder pflegst eine der repo-internen Shared Libraries. Libraries liefern wiederverwendbare Domänenlogik und Infrastruktur-Utilities für Transformer und Base-Container.

---

## Regeln

- Du MUSST die Abhängigkeitshierarchie einhalten: `common` hat keine internen Abhängigkeiten, `planpro-parser` und `ds-client` dürfen nur `common` importieren, aber nie sich gegenseitig.
- Du MUSST alle Funktionen, Klassen und Methoden mit vollständigen Python Type Hints versehen. `mypy --strict` muss grün sein.
- Du MUSST Tests für jede neue Funktion schreiben. Testabdeckung ist kein optionales Feature.
- Du darfst NIEMALS Netzwerk-Calls, Datenbankzugriffe oder Dateisystem-Operationen (außer `INPUT_PATH`/`OUTPUT_PATH`) in Libraries einbauen – außer in `ds-client`, wo REST-Calls die Kernfunktionalität sind.
- Du MUSST strukturiertes JSON-Logging über `common.logging` verwenden, auch in Libraries.
- Du darfst NICHT externe Libraries ohne explizite Abstimmung und Dokumentation in einer `pyproject.toml` hinzufügen.
- Du MUSST bei Breaking Changes (geänderte Signaturen, entfernte Funktionen) einen ADR schreiben und alle Stellen im Repo updaten.

---

## Patterns

### Library-Struktur

```
libs/<name>/
├── <name_snake>/
│   ├── __init__.py      # Öffentliche API explizit exportieren
│   ├── core.py          # Hauptlogik
│   └── types.py         # Typdefinitionen (dataclasses, TypedDicts)
├── tests/
│   ├── conftest.py      # Pytest Fixtures
│   └── test_core.py
└── pyproject.toml
```

### Öffentliche API in `__init__.py` definieren

```python
# libs/planpro_parser/__init__.py
from planpro_parser.core import parse_xml, extract_adjacency_list
from planpro_parser.types import PlanProObject, AdjacencyList

__all__ = ["parse_xml", "extract_adjacency_list", "PlanProObject", "AdjacencyList"]
```

### Tests mit pytest

```python
# libs/<name>/tests/test_core.py
import pytest
from <name> import <function>

@pytest.mark.unit
def test_<function>_with_valid_input() -> None:
    result = <function>(valid_input)
    assert result == expected

@pytest.mark.unit
def test_<function>_raises_on_invalid_input() -> None:
    with pytest.raises(ValueError, match="erwartet"):
        <function>(invalid_input)
```

---

## Antipatterns

- **Kein `requests.get/post`** in `planpro-parser` oder `common` – I/O gehört ausschließlich in `ds-client` (und nur wenn es die REST-API betrifft) oder Base-Container.
- **Kein `print()`** – immer `common.logging` verwenden.
- **Keine globalen Variablen für Zustand** – Libraries sind zustandslos. Konfiguration wird übergeben, nicht global gespeichert.
- **Keine zirkulären Imports** – niemals `planpro-parser` von `ds-client` importieren oder umgekehrt.
- **Keine hartkodierten Strings** für Objekttypen, Versionen oder Pfade – Konstanten in `common.constants` definieren.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `libs/<name>/tests/`
- Alle Tests mit `@pytest.mark.unit` markieren
- Fixtures in `conftest.py` definieren
- Mindestanforderungen:
  - Happy Path: Funktion mit gültigem Input getestet
  - Edge Cases: leere Inputs, None-Werte, Grenzwerte
  - Error Cases: ungültige Inputs lösen die richtigen Exceptions aus
  - Typen: Return-Werte haben erwarteten Typ

---

## Abhängigkeiten

**`libs/common`:**
- Du DARFST importieren: Python-Standardbibliothek, explizit genehmigte externe Packages
- Du darfst NICHT importieren: `planpro_parser`, `ds_client`, alle anderen internen Libraries

**`libs/planpro-parser`:**
- Du DARFST importieren: `common`, Python-Standardbibliothek, `lxml` oder `xml.etree`
- Du darfst NICHT importieren: `ds_client`, Base-Container, Transformer

**`libs/ds-client`:**
- Du DARFST importieren: `common`, Python-Standardbibliothek, `requests` oder `httpx`
- Du darfst NICHT importieren: `planpro_parser`, Base-Container, Transformer

---

## Kontext

Libraries sind die unterste Code-Schicht. Änderungen hier können viele Konsumenten betreffen. Vor Breaking Changes immer prüfen:
1. Welche Transformer importieren diese Library?
2. Welche Base-Container importieren diese Library?
3. Gibt es Tests die das bisherige Verhalten dokumentieren?

Bei Breaking Changes: ADR schreiben, alle Stellen updaten, CI-Tag mit Major-Version-Bump setzen.
