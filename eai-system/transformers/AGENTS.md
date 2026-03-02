# AGENTS.md – transformers/

## Rolle

Du entwickelst oder pflegst einen Transformer. Lesen von `INPUT_PATH`, transformieren, schreiben nach `OUTPUT_PATH`. Kein I/O, kein HTTP, kein DB.

## Regeln

- Du MUSST `main.py` dem Standard-Ablauf folgen lassen.
- Du darfst NIEMALS HTTP-Calls, DB-Zugriffe oder I/O außerhalb von `INPUT_PATH`/`OUTPUT_PATH` einbauen.
- Du MUSST Domänenlogik in `transform.py` isolieren.
- Du MUSST `common.logging` und `common.provenance` verwenden.
- Du MUSST Exit-Codes 0/1/2 verwenden.
- Du darfst NICHT `ds_client`, andere Transformer oder Base-Container importieren.

## Pattern: main.py

```python
def main() -> int:
    config = get_config()
    logger = get_logger("<name>")
    try:
        input_data = load_input(config.input_path)
        result = transform(input_data)
        write_output(result, config.output_path)
        create_provenance_fragment(...).write_to("/tmp/provenance.json")
        return ExitCode.SUCCESS
    except BusinessError as e:
        logger.error("Fachlicher Fehler", error=str(e))
        return ExitCode.BUSINESS_ERROR
    except Exception as e:
        logger.error("Technischer Fehler", error=str(e))
        return ExitCode.TECHNICAL_ERROR
```

## Pattern: transform.py

```python
@dataclass
class TransformResult:
    objects: list[dict]
    input_refs: list[str]
    output_refs: list[str]

def transform(input_data: InputData) -> TransformResult: ...
```

## Testanforderungen

- `@pytest.mark.unit`, Testort: `<transformer>/tests/`
- Happy Path, Edge Cases (leer, minimal), Error Case, GUID-Integrität

## Abhängigkeiten

- DARFST: `common`, `planpro_parser`, Python-stdlib
- NICHT: `ds_client`, andere Transformer, Base-Container
