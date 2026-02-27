# AGENTS.md – base-containers/ds-reader/

## Rolle

Du entwickelst oder pflegst den DS-Reader. Er liest JSON-Objekte aus dem Datenspeicher (FIN) über `libs/ds-client` und legt sie als Datei ab.

---

## Regeln

- Du MUSST `ds_client` für alle API-Zugriffe verwenden.
- Du MUSST gelesene Objekte als JSON unter `OUTPUT_PATH` ablegen.
- Du MUSST ein Provenance-Fragment erzeugen mit den GUIDs der gelesenen Objekte.
- Du darfst NIEMALS Domänenlogik einbauen.
- Du darfst NIEMALS `planpro_parser` importieren.

---

## Patterns

```python
# handler.py
from ds_client import DsClient
from common.config import get_config
import json
from pathlib import Path

def handle(config: Config) -> HandlerResult:
    client = DsClient(base_url=config.ds_api_url, token=config.ds_api_token)
    result = client.read_objects(guids=config.guids, scope=config.scope, phase=config.phase)

    output = {"objects": [obj.to_dict() for obj in result.objects]}
    Path(config.output_path).write_text(json.dumps(output, indent=2))

    return HandlerResult(
        input_refs=config.guids,
        output_refs=[obj.guid for obj in result.objects],
    )
```

---

## Antipatterns

- **Keine direkten HTTP-Calls** – immer `ds_client`.
- **Kein PlanPro-Parsing** – nur lesen und als JSON ablegen.

---

## Testanforderungen

- `ds_client` mocken
- Test: Erfolgreicher Read → JSON unter `OUTPUT_PATH`
- Test: API 404 → korrekte Exception
- Test: Leere Ergebnisliste → leere JSON-Datei

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `ds_client`
- Du darfst NICHT importieren: `planpro_parser`, andere Container

---

## Kontext

Der DS-Reader ist einer von nur zwei Containern die mit dem Datenspeicher kommunizieren. Er ist typischerweise der erste Step in Export- und Diff-Workflows.
