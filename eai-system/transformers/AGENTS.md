# AGENTS.md – transformers/

## Rolle

Du entwickelst oder pflegst einen Transformer. Transformer enthalten ausschließlich Domänenlogik. Sie lesen Input von einem lokalen Dateipfad, transformieren die Daten und schreiben Output auf einen lokalen Dateipfad. Kein I/O, kein HTTP, kein Datenbankzugriff.

---

## Regeln

- Du MUSST jeden Transformer mit einem `main.py` Entrypoint versehen der dem Standard-Ablauf folgt.
- Du darfst NIEMALS HTTP-Calls, Datenbankzugriffe oder Dateisystem-Operationen außerhalb von `INPUT_PATH` und `OUTPUT_PATH` in einen Transformer einbauen.
- Du MUSST die Domänenlogik in `transform.py` isolieren – getrennt von Config, Logging und I/O im `main.py`.
- Du MUSST structured JSON Logging über `common.logging` verwenden.
- Du MUSST ein Provenance-Fragment über `common.provenance` erzeugen.
- Du MUSST Exit-Code 0 bei Erfolg, 1 bei fachlichem Fehler, 2 bei technischem Fehler verwenden.
- Du darfst NICHT `libs/ds-client` importieren – das ist eine I/O-Library für Base-Container.
- Du darfst NICHT andere Transformer oder Base-Container importieren.
- Du MUSST alle Funktionen mit vollständigen Python Type Hints versehen.

---

## Patterns

### Standard-Entrypoint (`main.py`)

Jeder Transformer folgt diesem Ablauf:

```python
# main.py
import sys
from common.config import get_config
from common.logging import get_logger
from common.provenance import create_provenance_fragment
from common.constants import ExitCode

from <transformer_name>.transform import transform

def main() -> int:
    config = get_config()                       # 1. Config laden
    logger = get_logger("<transformer-name>")    # 2. Logger initialisieren

    try:
        logger.info("Transformation gestartet", correlation_id=config.correlation_id)

        input_data = load_input(config.input_path)   # 3. Input lesen
        result = transform(input_data)                # 4. Transformation
        write_output(result, config.output_path)      # 5. Output schreiben

        provenance = create_provenance_fragment(      # 6. Provenance
            transformer_name="<transformer-name>",
            transformer_version="<version>",
            correlation_id=config.correlation_id,
            input_refs=result.input_refs,
            output_refs=result.output_refs,
        )
        provenance.write_to("/tmp/provenance.json")

        logger.info("Transformation abgeschlossen", correlation_id=config.correlation_id)
        return ExitCode.SUCCESS                       # 7. Exit 0

    except BusinessError as e:
        logger.error("Fachlicher Fehler", error=str(e), correlation_id=config.correlation_id)
        return ExitCode.BUSINESS_ERROR

    except Exception as e:
        logger.error("Technischer Fehler", error=str(e), correlation_id=config.correlation_id)
        return ExitCode.TECHNICAL_ERROR

if __name__ == "__main__":
    sys.exit(main())
```

### Domänenlogik (`transform.py`)

```python
# transform.py – reine Domänenlogik, keine Seiteneffekte
from dataclasses import dataclass

@dataclass
class TransformResult:
    objects: list[dict]
    input_refs: list[str]
    output_refs: list[str]

def transform(input_data: InputData) -> TransformResult:
    """Reine Transformationslogik. Kein I/O, kein Logging, kein State."""
    ...
```

---

## Antipatterns

- **Kein `requests.get/post`** in Transformern – I/O gehört in Base-Container.
- **Keine globalen Variablen für Zustand** – Container sind stateless.
- **Keine eigenen Logging-Formate** – immer `common.logging` verwenden.
- **Keine hartkodierten Pfade** – immer über Umgebungsvariablen (`INPUT_PATH`, `OUTPUT_PATH`).
- **Kein `ds_client`-Import** – Transformer haben keinen Netzwerkzugriff.
- **Kein `os.environ` direkt lesen** – immer über `common.config.get_config()`.
- **Keine Business-Logik in `main.py`** – `main.py` ist nur Orchestrierung, `transform.py` ist die Logik.
- **Kein `print()`** – immer `common.logging`.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `<transformer>/tests/`
- Tests für `transform.py` – die reine Domänenlogik, ohne `main.py`
- Fixtures in `tests/fixtures/` oder aus `tests/fixtures/` (Repo-Root)

**Mindestanforderungen:**
1. Happy Path: gültige Eingabe → korrekte Ausgabe
2. Edge Case: minimale Eingabe (z.B. 1 Objekt)
3. Edge Case: leere Eingabe
4. Error Case: ungültige Eingabe → fachlicher Fehler
5. GUID-Integrität: GUIDs im Output stimmen mit Input überein
6. Provenance: Input-Refs und Output-Refs korrekt

**Assertion-Pattern:**
```python
def test_transform_preserves_guids(sample_input: InputData) -> None:
    result = transform(sample_input)
    input_guids = {obj.guid for obj in sample_input.objects}
    output_guids = {obj["guid"] for obj in result.objects}
    assert input_guids == output_guids
```

---

## Abhängigkeiten

- Du DARFST importieren: `libs/common`, `libs/planpro-parser`, Python-Standardbibliothek
- Du darfst NICHT importieren: `libs/ds-client`, andere Transformer, Base-Container, `requests`, `httpx`

---

## Kontext

Transformer sind die Domänenkern-Schicht des Systems. Sie verarbeiten PlanPro-Daten (XML → JSON, JSON → XML, Diff-Berechnung). PlanPro-GUIDs sind permanente Infrastruktur-Identitäten und dürfen niemals verändert werden. Mehrere PlanPro-Versionen koexistieren – ein Transformer muss alle unterstützten Versionen verarbeiten können. Der regulatorische Kontext erfordert vollständige Nachvollziehbarkeit (Provenance).
