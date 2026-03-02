# AGENTS.md – libs/

## Rolle

Du erweiterst oder pflegst eine repo-interne Shared Library.

## Regeln

- Du MUSST die Abhängigkeitshierarchie einhalten: `common` hat keine internen Abhängigkeiten; `planpro-parser` und `ds-client` importieren nur `common`.
- Du MUSST vollständige Type Hints verwenden. `mypy --strict` grün.
- Du MUSST Tests für jede neue Funktion schreiben.
- Du darfst NIEMALS Netzwerk-Calls oder Datenbankzugriffe in `common` oder `planpro-parser` einbauen.
- Du MUSST `common.logging` verwenden, kein `print()`.
- Du MUSST bei Breaking Changes einen ADR schreiben und alle Stellen im Repo updaten.

## Pattern: Library-Struktur

```
libs/<name>/
├── <name_snake>/
│   ├── __init__.py  # öffentliche API explizit exportieren
│   └── core.py
├── tests/
│   └── test_core.py
└── pyproject.toml
```

## Testanforderungen

- `@pytest.mark.unit`, Testort: `libs/<name>/tests/`
- Happy Path, Edge Cases (leer, None), Error Cases

## Abhängigkeiten

| Library | Darf importieren | Nicht erlaubt |
|---|---|---|
| `common` | Python-stdlib | alle internen |
| `planpro-parser` | `common`, `lxml`/`xml.etree` | `ds_client` |
| `ds-client` | `common`, `requests`/`httpx` | `planpro_parser` |
