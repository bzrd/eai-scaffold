# AGENTS.md – base-containers/file-fetcher/

## Rolle

Du entwickelst oder pflegst den File-Fetcher. Er holt Dateien von externen Systemen und stellt sie dem nachfolgenden Workflow-Step zur Verfügung.

---

## Regeln

- Du MUSST Retry-Logik für transiente Netzwerkfehler implementieren (3 Versuche, exponentielles Backoff ab 2s).
- Du MUSST Auth-Credentials ausschließlich aus Umgebungsvariablen lesen.
- Du MUSST die abgerufene Datei unter `OUTPUT_PATH` ablegen.
- Du MUSST ein Provenance-Fragment erzeugen mit der Quell-URL als Metadatum.
- Du darfst NIEMALS Domänenlogik (PlanPro-Parsing etc.) einbauen.
- Du darfst NIEMALS `planpro_parser` importieren.

---

## Patterns

```python
# handler.py
import requests
from common.config import get_config
from common.logging import get_logger
from pathlib import Path

def fetch_file(source_url: str, output_path: str, token: str) -> Path:
    response = requests.get(source_url, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    out = Path(output_path)
    out.write_bytes(response.content)
    return out
```

---

## Antipatterns

- **Keine Dateiverarbeitung** – nur herunterladen und ablegen.
- **Keine hartkodierten URLs** – alles über Umgebungsvariablen.
- **Kein `planpro_parser`** – keine Domänenlogik.

---

## Testanforderungen

- HTTP-Calls mocken mit `responses` oder `pytest-httpx`
- Test: Erfolgreicher Download → Datei unter `OUTPUT_PATH`
- Test: HTTP 500 → Retry → Erfolg beim 2. Versuch
- Test: HTTP 401 → Auth-Fehler, kein Retry

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `requests`, `httpx`
- Du darfst NICHT importieren: `planpro_parser`, `ds_client`, andere Container

---

## Kontext

Der File-Fetcher ist typischerweise der erste Step in einem Import-Workflow. Er holt eine PlanPro-XML-Datei von einer Fachapplikation und stellt sie dem `planpro-ingest` Transformer zur Verfügung.
