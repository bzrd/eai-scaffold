# AGENTS.md – libs/ds-client/

## Rolle

Du erweiterst oder pflegst den typisierten Python-Client für den Datenspeicher (FIN REST-API). Dieser Client wird AUSSCHLIESSLICH von Base-Containern (`ds-writer`, `ds-reader`) importiert – niemals von Transformern.

---

## Regeln

- Du MUSST alle API-Operationen synchron implementieren (kein `async/await`).
- Du MUSST für jeden Fehlerfall eine eigene Exception-Klasse definieren statt generische Exceptions zu verwenden.
- Du MUSST alle Request- und Response-Modelle typisieren (`dataclass` oder `TypedDict`).
- Du MUSST Retry-Logik für transiente Netzwerkfehler einbauen (mindestens 3 Versuche, exponentielles Backoff).
- Du darfst NIEMALS `planpro_parser` oder andere Transformer/Base-Container importieren.
- Du MUSST Auth-Tokens ausschließlich aus Umgebungsvariablen lesen (über `common.config`), niemals hardkodiert.
- Du MUSST alle API-Calls über `common.logging` loggen (Request-URL, Response-Status, Duration).
- Du MUSST `mypy --strict` einhalten.

---

## Patterns

### Client-Struktur

```python
# ds_client/client.py
from dataclasses import dataclass
from ds_client.models import DsObject, WriteResult, ReadResult
from ds_client.exceptions import DsApiError, DsNotFoundError
from common.logging import get_logger

logger = get_logger(__name__)

@dataclass
class DsClient:
    base_url: str
    token: str
    timeout: int = 30
    max_retries: int = 3

    def write_objects(
        self,
        objects: list[DsObject],
        scope: str,
        phase: str,
    ) -> WriteResult:
        """Schreibt Objekte in den Datenspeicher."""
        ...

    def read_objects(
        self,
        guids: list[str],
        scope: str,
        phase: str,
    ) -> ReadResult:
        """Liest Objekte aus dem Datenspeicher."""
        ...

    def get_version_diff(
        self,
        scope: str,
        phase_from: str,
        phase_to: str,
    ) -> list[str]:
        """Gibt GUIDs zurück die zwischen zwei Phasen verändert wurden."""
        ...
```

### Exception-Hierarchie

```python
# ds_client/exceptions.py
class DsError(Exception):
    """Basis-Exception für alle Datenspeicher-Fehler."""

class DsApiError(DsError):
    """HTTP-Fehler von der API (4xx, 5xx)."""
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"API-Fehler {status_code}: {message}")

class DsAuthError(DsError):
    """Authentifizierungsfehler (401, 403)."""

class DsNotFoundError(DsError):
    """Objekt nicht gefunden (404)."""

class DsValidationError(DsError):
    """Validierungsfehler vom Server (422)."""
```

### Retry-Pattern

```python
import time

def _with_retry(self, operation: Callable[[], T]) -> T:
    """Führt eine Operation mit exponentiellem Backoff durch."""
    for attempt in range(self.max_retries):
        try:
            return operation()
        except DsApiError as e:
            if e.status_code < 500 or attempt == self.max_retries - 1:
                raise
            wait = 2 ** attempt
            logger.warning(f"Retry {attempt + 1}/{self.max_retries} nach {wait}s")
            time.sleep(wait)
    raise RuntimeError("Unreachable")
```

---

## Antipatterns

- **Kein `planpro_parser`-Import** – dieser Client kennt keine PlanPro-Strukturen.
- **Keine hartkodierten URLs oder Tokens** – immer über `common.config`.
- **Keine generischen `Exception`-Catches** ohne Re-Raise oder strukturiertes Logging.
- **Kein Multi-Line-Logging** – jeder Log-Aufruf ein vollständiges JSON-Objekt.
- **Kein direkter Zugriff auf MSSQL** – immer über die REST-API.
- **Kein Caching** von API-Antworten ohne explizite Anforderung (Datenkonsistenz ist kritisch).

---

## Testanforderungen

- Framework: `pytest` + `responses` oder `pytest-httpx` für HTTP-Mocking
- Testort: `ds-client/tests/`
- Alle Tests mit `@pytest.mark.unit` markieren
- **Keine echten HTTP-Calls in Unit-Tests** – immer mocken

**Mindestanforderungen:**
1. Erfolgreiches Schreiben: API antwortet 200, Objekte werden korrekt serialisiert
2. Fehlerfall 404: `DsNotFoundError` wird ausgelöst
3. Fehlerfall 401: `DsAuthError` wird ausgelöst
4. Retry: Bei 503-Antwort wird dreimal versucht
5. Timeout: Wenn API nicht antwortet, wird Exception ausgelöst

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `requests`, `httpx`, Python-Standardbibliothek
- Du darfst NICHT importieren: `planpro_parser`, Transformer, Base-Container

---

## Kontext

Der Datenspeicher (FIN) ist schemalos auf Datenbankebene, aber die API erzwingt Mindestvalidierung: Jedes Objekt muss eine gültige GUID, einen bekannten Objekttyp und eine PlanPro-Version haben. Fehler werden als strukturierte JSON-Fehler zurückgegeben. Die API bietet Versionierung (Stände), Scopes (Projekte) und Phasen (Planungsphasen) als erste Klasse.
