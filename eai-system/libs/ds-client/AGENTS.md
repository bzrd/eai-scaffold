# AGENTS.md – libs/ds-client/

## Rolle

Du pflegst den typisierten REST-Client für den Datenspeicher (FIN). Wird AUSSCHLIESSLICH von Base-Containern importiert.

## Regeln

- Du MUSST alle Operationen synchron implementieren (kein `async/await`).
- Du MUSST für jeden Fehlerfall eine eigene Exception-Klasse verwenden.
- Du MUSST alle Modelle typisieren (`dataclass` oder `TypedDict`).
- Du MUSST Retry-Logik implementieren (3 Versuche, exponentielles Backoff).
- Du darfst NIEMALS `planpro_parser` importieren.
- Du MUSST Auth-Tokens aus `common.config` lesen, niemals hardkodiert.
- Du MUSST `mypy --strict` einhalten.

## Pattern: Exception-Hierarchie

```python
class DsError(Exception): ...
class DsApiError(DsError):
    def __init__(self, status_code: int, message: str) -> None: ...
class DsAuthError(DsError): ...
class DsNotFoundError(DsError): ...
class DsValidationError(DsError): ...
```

## Pattern: Retry

```python
def _with_retry(self, operation: Callable[[], T]) -> T:
    for attempt in range(self.max_retries):
        try:
            return operation()
        except DsApiError as e:
            if e.status_code < 500 or attempt == self.max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("Unreachable")
```

## Testanforderungen

- `@pytest.mark.unit`, HTTP mocken mit `responses`/`pytest-httpx`
- Erfolg (200), 404 → DsNotFoundError, 401 → DsAuthError, 503 → Retry

## Abhängigkeiten

- DARFST: `common`, `requests`/`httpx`, Python-stdlib
- NICHT: `planpro_parser`, Transformer, Base-Container
