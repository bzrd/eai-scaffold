# AGENTS.md – base-containers/

## Rolle

Du entwickelst oder pflegst einen Base-Container. Base-Container sind die I/O-Schicht – keine Domänenlogik.

## Regeln

- Du MUSST I/O in `handler.py` isolieren.
- Du MUSST `common.logging` und `common.provenance` verwenden.
- Du MUSST Exit-Codes 0/1/2 verwenden.
- Du MUSST Retry mit exponentiellem Backoff für Netzwerkfehler implementieren.
- Du darfst NIEMALS Domänenlogik (PlanPro-Parsing, Diff) einbauen.
- Du darfst NIEMALS `planpro_parser` importieren.
- Du MUSST `mypy --strict` einhalten.

## Pattern: main.py

```python
def main() -> int:
    config = get_config()
    logger = get_logger("<name>")
    try:
        result = handle(config)
        create_provenance_fragment(...).write_to("/tmp/provenance.json")
        return ExitCode.SUCCESS
    except BusinessError as e:
        logger.error("Fachlicher Fehler", error=str(e))
        return ExitCode.BUSINESS_ERROR
    except Exception as e:
        logger.error("Technischer Fehler", error=str(e))
        return ExitCode.TECHNICAL_ERROR
```

## Pattern: Retry

```python
def handle_with_retry(operation: Callable[[], T], max_retries: int = 3) -> T:
    for attempt in range(max_retries):
        try:
            return operation()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2.0 * (2 ** attempt))
    raise RuntimeError("Unreachable")
```

## Testanforderungen

- `pytest` + `responses`/`pytest-httpx` für HTTP-Mocking
- Happy Path, Netzwerkfehler → Retry, Auth-Fehler, Provenance korrekt

## Abhängigkeiten

- DARFST: `common`, `ds_client` (nur DS-Container), `requests`/`httpx`
- NICHT: `planpro_parser`, andere Base-Container, Transformer
