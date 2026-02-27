# AGENTS.md – base-containers/

## Rolle

Du entwickelst oder pflegst einen Base-Container. Base-Container sind die I/O-Schicht des Systems. Sie holen Dateien, machen REST-API-Calls, schreiben in den Datenspeicher. Sie enthalten **keine Domänenlogik** – die gehört in Transformer.

---

## Regeln

- Du MUSST I/O (HTTP, Dateisystem, REST-API) in `handler.py` isolieren – getrennt vom Entrypoint `main.py`.
- Du MUSST structured JSON Logging über `common.logging` verwenden.
- Du MUSST ein Provenance-Fragment über `common.provenance` erzeugen.
- Du MUSST Exit-Code 0 bei Erfolg, 1 bei fachlichem Fehler, 2 bei technischem Fehler verwenden.
- Du MUSST Fehlerbehandlung für Netzwerkfehler implementieren (Retry mit exponentiellem Backoff).
- Du darfst NIEMALS Domänenlogik (PlanPro-Parsing, Diff-Berechnung, Validierung) in Base-Container einbauen – das gehört in Transformer oder Libraries.
- Du darfst NIEMALS `planpro_parser` importieren.
- Du darfst NIEMALS andere Base-Container oder Transformer importieren.
- Du MUSST `mypy --strict` einhalten.

---

## Patterns

### Standard-Entrypoint (`main.py`)

```python
# main.py
import sys
from common.config import get_config
from common.logging import get_logger
from common.provenance import create_provenance_fragment
from common.constants import ExitCode

from <container_name>.handler import handle

def main() -> int:
    config = get_config()
    logger = get_logger("<container-name>")

    try:
        logger.info("Handler gestartet", correlation_id=config.correlation_id)
        result = handle(config)
        provenance = create_provenance_fragment(
            transformer_name="<container-name>",
            transformer_version="<version>",
            correlation_id=config.correlation_id,
            input_refs=result.input_refs,
            output_refs=result.output_refs,
        )
        provenance.write_to("/tmp/provenance.json")
        logger.info("Handler abgeschlossen", correlation_id=config.correlation_id)
        return ExitCode.SUCCESS
    except BusinessError as e:
        logger.error("Fachlicher Fehler", error=str(e))
        return ExitCode.BUSINESS_ERROR
    except Exception as e:
        logger.error("Technischer Fehler", error=str(e))
        return ExitCode.TECHNICAL_ERROR

if __name__ == "__main__":
    sys.exit(main())
```

### I/O-Handler mit Retry

```python
# handler.py
import time
from common.logging import get_logger

logger = get_logger(__name__)

def handle_with_retry(
    operation: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 2.0,
) -> T:
    for attempt in range(max_retries):
        try:
            return operation()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            logger.warning(f"Retry {attempt + 1}/{max_retries} nach {delay}s")
            time.sleep(delay)
    raise RuntimeError("Unreachable")
```

---

## Antipatterns

- **Keine Domänenlogik** in Base-Containern – kein PlanPro-Parsing, kein Diff, keine Validierung über Mindestvalidierung hinaus.
- **Kein `planpro_parser`-Import** – Domäne gehört in Transformer.
- **Keine eigenen Logging-Formate** – immer `common.logging`.
- **Keine hartkodierten URLs, Tokens oder Pfade** – alles über Umgebungsvariablen.
- **Kein `print()`** – immer `common.logging`.
- **Keine Imports von anderen Base-Containern oder Transformern**.

---

## Testanforderungen

- Framework: `pytest` + `responses` oder `pytest-httpx` für HTTP-Mocking
- Testort: `<container>/tests/`
- **Alle I/O muss gemockt werden** – Unit-Tests machen keine echten HTTP-Calls
- Integrationstests mit echter API in `tests/integration/`

**Mindestanforderungen:**
1. Happy Path: erfolgreiches I/O → korrekte Ausgabe
2. Netzwerkfehler → Retry greift
3. Auth-Fehler → korrekte Exception
4. Timeout → korrekte Exception
5. Provenance-Fragment korrekt erzeugt

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `ds_client` (nur ds-writer/ds-reader), `requests`, `httpx`, Python-Standardbibliothek
- Du darfst NICHT importieren: `planpro_parser`, andere Base-Container, Transformer

---

## Kontext

Base-Container laufen als Argo-Workflow-Steps. Sie sind die einzigen Komponenten die mit der Außenwelt kommunizieren: Dateien holen/ablegen, REST-API-Calls gegen den Datenspeicher, HTTP-Anfragen an externe Systeme. Der `http-trigger` ist eine Ausnahme: er ist ein Long-Running-Service (nicht Run-to-Completion).
