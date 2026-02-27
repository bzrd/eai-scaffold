# AGENTS.md – base-containers/http-trigger/

## Rolle

Du entwickelst oder pflegst den HTTP-Trigger-Service. Dieser Service ist ein dauerlaufender FastAPI-Service der Webhooks entgegennimmt und Argo-Workflows auslöst. Er ist **KEIN Run-to-Completion-Container** wie alle anderen.

---

## Regeln

- Du MUSST FastAPI als Web-Framework verwenden.
- Du MUSST einen `/health` Endpoint implementieren (für Kubernetes Liveness-/Readiness-Probes).
- Du MUSST eingehende Webhooks mit Pydantic-Modellen validieren.
- Du MUSST Auth-Prüfung auf eingehende Requests implementieren (Token oder API-Key).
- Du MUSST structured JSON Logging über `common.logging` verwenden.
- Du MUSST Fehler als strukturierte JSON-Responses zurückgeben (nicht als HTML).
- Du darfst NIEMALS Domänenlogik (PlanPro-Parsing etc.) einbauen.
- Du darfst NIEMALS `planpro_parser` importieren.
- Du MUSST beachten: Dieses Dockerfile ist `docker/Dockerfile.http-trigger`, nicht das Standard-Base-Dockerfile.
- Du MUSST beachten: Deployment via Kubernetes Deployment, nicht Argo-Step.

---

## Patterns

### FastAPI-App

```python
# main.py
from fastapi import FastAPI
from common.logging import get_logger
from http_trigger.routes import router

logger = get_logger("http-trigger")
app = FastAPI(title="EAI HTTP Trigger")
app.include_router(router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

### Webhook-Route

```python
# routes.py
from fastapi import APIRouter, Depends
from http_trigger.models import ImportRequest, TriggerResponse
from http_trigger.workflow import submit_workflow

router = APIRouter()

@router.post("/webhook/import", response_model=TriggerResponse)
async def trigger_import(request: ImportRequest) -> TriggerResponse:
    workflow_name = await submit_workflow(
        template="import-planpro",
        parameters={"source_url": request.source_url},
        correlation_id=request.correlation_id,
    )
    return TriggerResponse(workflow_name=workflow_name, status="submitted")
```

---

## Antipatterns

- **Kein Synchronous Blocking** – FastAPI ist async, I/O-Calls async oder in Thread-Executor.
- **Keine Domänenlogik** – nur Webhook empfangen und Workflow triggern.
- **Kein `INPUT_PATH`/`OUTPUT_PATH`** – dieser Container nutzt HTTP, nicht Dateisystem.
- **Keine hartkodierten Workflow-Namen** – über Config oder Request-Parameter.

---

## Testanforderungen

- Framework: `pytest` + `httpx` (mit FastAPI TestClient)
- Testort: `http-trigger/tests/`
- Argo-API mocken

**Mindestanforderungen:**
1. `/health` gibt 200 zurück
2. Gültiger Webhook → Workflow wird submitted
3. Ungültiger Request Body → 422 mit strukturierter Fehlermeldung
4. Auth-Fehler → 401/403
5. Argo-API nicht erreichbar → 502 mit strukturiertem Fehler

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `fastapi`, `uvicorn`, `httpx`, Python-Standardbibliothek
- Du darfst NICHT importieren: `planpro_parser`, `ds_client`, andere Container

---

## Kontext

Der HTTP-Trigger ist der Einstiegspunkt für externe Fachapplikationen, die einen Datenfluss auslösen wollen. Er nimmt einen HTTP-Request entgegen, validiert ihn und submitted einen Argo-Workflow. Er hat ein anderes Deployment-Modell als alle anderen Container: Kubernetes Deployment statt Argo-Step, dauerlaufend statt Run-to-Completion.
