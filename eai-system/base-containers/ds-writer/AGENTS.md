# AGENTS.md – base-containers/ds-writer/

## Rolle

Du entwickelst oder pflegst den DS-Writer. Er schreibt JSON-Objekte in den Datenspeicher (FIN) über `libs/ds-client`.

---

## Regeln

- Du MUSST `ds_client` für alle API-Zugriffe verwenden – keine direkten `requests`-Calls gegen die FIN-API.
- Du MUSST Scope und Phase aus Umgebungsvariablen lesen.
- Du MUSST ein Provenance-Fragment erzeugen mit den GUIDs der geschriebenen Objekte.
- Du darfst NIEMALS Domänenlogik einbauen (kein PlanPro-Parsing, keine Validierung über Mindestvalidierung hinaus).
- Du darfst NIEMALS `planpro_parser` importieren.

---

## Patterns

```python
# handler.py
from ds_client import DsClient
from ds_client.models import DsObject
from common.config import get_config
from common.logging import get_logger
import json
from pathlib import Path

def handle(config: Config) -> HandlerResult:
    client = DsClient(base_url=config.ds_api_url, token=config.ds_api_token)
    input_data = json.loads(Path(config.input_path).read_text())

    objects = [DsObject(**obj) for obj in input_data["objects"]]
    result = client.write_objects(objects, scope=config.scope, phase=config.phase)

    return HandlerResult(
        input_refs=[obj.guid for obj in objects],
        output_refs=[obj.guid for obj in result.written],
    )
```

---

## Antipatterns

- **Keine direkten `requests.post`-Calls** gegen die FIN-API – immer `ds_client`.
- **Kein PlanPro-Parsing** – nur JSON-Objekte lesen und an die API weiterreichen.

---

## Testanforderungen

- `ds_client` mocken (nicht die HTTP-Schicht)
- Test: Erfolgreicher Write → GUIDs im Provenance
- Test: API-Fehler → korrekte Exception und Exit-Code

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `ds_client`
- Du darfst NICHT importieren: `planpro_parser`, andere Container

---

## Kontext

Der DS-Writer ist einer von nur zwei Containern (`ds-writer`, `ds-reader`) die mit dem Datenspeicher kommunizieren. Er ist typischerweise der letzte Step in einem Import-Workflow, nachdem der Transformer die Daten transformiert hat.
