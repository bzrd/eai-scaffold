# AGENTS.md – libs/common/

## Rolle

Du erweiterst oder pflegst die Shared-Utility-Library. Diese Library ist die unterste Schicht im Dependency-Graph und darf KEINE Abhängigkeiten auf `planpro-parser`, `ds-client` oder andere repo-interne Libraries haben.

---

## Regeln

- Du darfst NIEMALS `planpro_parser`, `ds_client` oder andere repo-interne Libraries importieren.
- Du darfst NIEMALS Netzwerk-Calls, HTTP-Requests oder Datenbankzugriffe einbauen.
- Du MUSST das Logging-Format aus `docs/contracts/logging-format.md` einhalten – es ist die normative Referenz.
- Du MUSST das Provenance-Format aus `docs/contracts/provenance-format.md` einhalten – es ist die normative Referenz.
- Du MUSST alle Konstanten (Env-Var-Namen, Objekttypen, Exit-Codes) in `constants.py` zentral definieren.
- Du MUSST alle Funktionen zustandslos implementieren (pure functions) oder mit explizitem Context-Objekt.
- Du MUSST `mypy --strict` einhalten.
- Du MUSST alle öffentlichen Funktionen in `__init__.py` explizit exportieren.

---

## Patterns

### Logging (JSON, eine Zeile pro Eintrag, nach stdout)

```python
# common/logging.py
import json
import sys
from datetime import datetime, timezone

def get_logger(component: str) -> "StructuredLogger":
    return StructuredLogger(component)

class StructuredLogger:
    def __init__(self, component: str) -> None:
        self.component = component

    def _log(self, level: str, message: str, **extra: object) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message,
            "component": self.component,
            **extra,
        }
        print(json.dumps(entry, default=str), file=sys.stdout, flush=True)

    def info(self, message: str, **extra: object) -> None:
        self._log("INFO", message, **extra)

    def error(self, message: str, **extra: object) -> None:
        self._log("ERROR", message, **extra)

    def warning(self, message: str, **extra: object) -> None:
        self._log("WARNING", message, **extra)

    def debug(self, message: str, **extra: object) -> None:
        self._log("DEBUG", message, **extra)
```

### Config (Umgebungsvariablen typisiert laden)

```python
# common/config.py
import os
from dataclasses import dataclass
from common.constants import EnvVars

@dataclass(frozen=True)
class Config:
    input_path: str
    output_path: str
    correlation_id: str
    log_level: str
    ds_api_url: str
    ds_api_token: str

def get_config() -> Config:
    return Config(
        input_path=os.environ.get(EnvVars.INPUT_PATH, "/tmp/input"),
        output_path=os.environ.get(EnvVars.OUTPUT_PATH, "/tmp/output"),
        correlation_id=os.environ.get(EnvVars.CORRELATION_ID, ""),
        log_level=os.environ.get(EnvVars.LOG_LEVEL, "INFO"),
        ds_api_url=os.environ.get(EnvVars.DS_API_URL, ""),
        ds_api_token=os.environ.get(EnvVars.DS_API_TOKEN, ""),
    )
```

### Provenance-Fragment

```python
# common/provenance.py
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass(frozen=True)
class ProvenanceFragment:
    transformer_name: str
    transformer_version: str
    timestamp: str
    correlation_id: str
    input_refs: list[str]
    output_refs: list[str]
    planpro_version: str | None = None
    scope: str | None = None
    phase: str | None = None
    error_info: str | None = None

    def write_to(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

def create_provenance_fragment(
    transformer_name: str,
    transformer_version: str,
    correlation_id: str,
    input_refs: list[str],
    output_refs: list[str],
    **kwargs: object,
) -> ProvenanceFragment:
    return ProvenanceFragment(
        transformer_name=transformer_name,
        transformer_version=transformer_version,
        timestamp=datetime.now(timezone.utc).isoformat(),
        correlation_id=correlation_id,
        input_refs=input_refs,
        output_refs=output_refs,
        **kwargs,
    )
```

### Konstanten

```python
# common/constants.py
from enum import StrEnum

class EnvVars:
    CORRELATION_ID = "CORRELATION_ID"
    LOG_LEVEL = "LOG_LEVEL"
    INPUT_PATH = "INPUT_PATH"
    OUTPUT_PATH = "OUTPUT_PATH"
    DS_API_URL = "DS_API_URL"
    DS_API_TOKEN = "DS_API_TOKEN"

class ExitCode:
    SUCCESS = 0
    BUSINESS_ERROR = 1
    TECHNICAL_ERROR = 2
```

---

## Antipatterns

- **Kein Import von `planpro_parser` oder `ds_client`** – `common` ist die Basis, nicht umgekehrt.
- **Kein `print()`** für Logging – nur `StructuredLogger`.
- **Kein Multi-Line-Logging** – jede Zeile ist ein vollständiges JSON-Objekt.
- **Keine Logs in Dateien** – nur `stdout`.
- **Keine globalen Variablen** für Konfiguration oder Zustand.
- **Keine hartkodierten Env-Var-Namen** in aufrufendem Code – immer `common.constants.EnvVars` nutzen.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `common/tests/`
- Alle Tests mit `@pytest.mark.unit` markieren

**Mindestanforderungen:**
1. **Logging:** JSON-Output validieren, alle Pflichtfelder prüfen, kein Multi-Line
2. **Config:** Env-Vars korrekt geladen, Defaults greifen wenn Var fehlt
3. **Provenance:** Fragment enthält alle Pflichtfelder, `write_to` erzeugt gültiges JSON
4. **Validation:** GUID-Validierung erkennt gültige und ungültige UUIDs, Objekttyp gegen Liste geprüft

---

## Abhängigkeiten

- Du DARFST importieren: Python-Standardbibliothek
- Du darfst NICHT importieren: `planpro_parser`, `ds_client`, jede andere repo-interne Library

---

## Kontext

`common` wird von **jeder** Komponente importiert. Änderungen hier haben den größten Blast-Radius im gesamten Repo. Vor jeder Änderung prüfen: Ist sie rückwärtskompatibel? Wenn nicht: ADR schreiben, alle Konsumenten updaten, Major-Version-Bump.
