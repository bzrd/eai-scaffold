# AGENTS.md – libs/common/

## Rolle

Du pflegst die Basis-Utility-Library. Keine Abhängigkeiten auf `planpro-parser`, `ds-client` oder andere interne Libraries.

## Regeln

- Du darfst NIEMALS `planpro_parser`, `ds_client` oder andere interne Libraries importieren.
- Du darfst NIEMALS Netzwerk-Calls oder Datenbankzugriffe einbauen.
- Du MUSST das Logging-Format aus `docs/contracts/logging-format.md` einhalten.
- Du MUSST das Provenance-Format aus `docs/contracts/provenance-format.md` einhalten.
- Du MUSST alle Konstanten in `constants.py` definieren.
- Du MUSST `mypy --strict` einhalten.

## Pattern: StructuredLogger

```python
class StructuredLogger:
    def __init__(self, component: str) -> None:
        self.component = component

    def _log(self, level: str, message: str, **extra: object) -> None:
        print(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                          "level": level, "message": message,
                          "component": self.component, **extra}, default=str),
              file=sys.stdout, flush=True)
```

## Pattern: Config

```python
@dataclass(frozen=True)
class Config:
    input_path: str
    output_path: str
    correlation_id: str
    log_level: str
    ds_api_url: str
    ds_api_token: str
```

## Pattern: ProvenanceFragment

```python
@dataclass(frozen=True)
class ProvenanceFragment:
    transformer_name: str
    transformer_version: str
    timestamp: str
    correlation_id: str
    input_refs: list[str]
    output_refs: list[str]
    error_info: str | None = None

    def write_to(self, path: str) -> None:
        Path(path).write_text(json.dumps(asdict(self), indent=2))
```

## Testanforderungen

- `@pytest.mark.unit`, Testort: `common/tests/`
- Logging: alle Pflichtfelder vorhanden, kein Multi-Line
- Config: Env-Vars + Defaults korrekt
- Provenance: Pflichtfelder vorhanden, `write_to` erzeugt gültiges JSON
- Validation: GUID-Format, Objekttyp gegen Liste

## Abhängigkeiten

- DARFST: Python-Standardbibliothek
- NICHT: `planpro_parser`, `ds_client`, andere interne Libraries
