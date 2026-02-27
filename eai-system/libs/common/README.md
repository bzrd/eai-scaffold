# libs/common – Shared Utilities

## Zweck

Shared Utilities die von allen Komponenten im Repo genutzt werden. `common` ist die unterste Schicht des Dependency-Graphen – sie hat keine Abhängigkeiten auf andere repo-interne Libraries.

---

## Struktur

```
common/
├── common/
│   ├── __init__.py          # Öffentliche API
│   ├── logging.py           # Strukturiertes JSON-Logging mit Correlation-ID
│   ├── config.py            # Umgebungsvariablen laden, validieren, typisiert bereitstellen
│   ├── provenance.py        # Provenance-Fragment-Erzeugung
│   ├── validation.py        # Mindest-Validierung (GUID-Format, Objekttyp, Version)
│   ├── constants.py         # Standard-Env-Var-Namen, Objekttyp-Enums, Exit-Codes
│   └── types.py             # Geteilte Typdefinitionen
├── tests/
│   ├── conftest.py
│   ├── test_logging.py
│   ├── test_config.py
│   ├── test_provenance.py
│   └── test_validation.py
└── pyproject.toml
```

---

## Konventionen

- **Keine Abhängigkeiten auf andere repo-interne Libraries** – `common` ist die Basis, von der alles andere abhängt
- **Keine Netzwerk-Calls oder Datenbankzugriffe** – reine Utilities
- **Alle Funktionen zustandslos** (pure functions) oder mit explizitem Context-Objekt
- **Log-Format folgt `docs/contracts/logging-format.md`** (normativ)
- **Provenance-Format folgt `docs/contracts/provenance-format.md`** (normativ)
- Python-Package-Name: `common`

---

## Abhängigkeiten

- Nur Python-Standardbibliothek
- **Keine anderen repo-internen Libraries**

---

## Beispiel: Logging

```python
from common.logging import get_logger

logger = get_logger("transformer-ingest")
logger.info("Verarbeitung gestartet", extra={
    "correlation_id": "abc-123",
    "object_count": 42,
    "planpro_version": "1.10",
})
```

## Beispiel: Config

```python
from common.config import get_config

config = get_config()
print(config.input_path)    # /tmp/input (aus INPUT_PATH)
print(config.output_path)   # /tmp/output (aus OUTPUT_PATH)
print(config.log_level)     # INFO (aus LOG_LEVEL)
```

## Beispiel: Provenance

```python
from common.provenance import create_provenance_fragment

fragment = create_provenance_fragment(
    transformer_name="planpro-ingest",
    transformer_version="v1.2.3",
    correlation_id="abc-123",
    input_refs=["guid-1", "guid-2"],
    output_refs=["guid-1", "guid-2", "guid-3"],
)
fragment.write_to("/tmp/provenance.json")
```

---

## Checkliste

- [ ] Keine Imports aus anderen repo-internen Libraries
- [ ] Alle Funktionen mit Type Hints
- [ ] Unit-Tests vorhanden
- [ ] `mypy --strict` grün
- [ ] Logging-Format entspricht `docs/contracts/logging-format.md`
- [ ] Provenance-Format entspricht `docs/contracts/provenance-format.md`
