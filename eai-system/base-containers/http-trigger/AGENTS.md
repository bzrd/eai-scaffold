# AGENTS.md – base-containers/http-trigger/

## Rolle

Du entwickelst den HTTP-Trigger-Service. Dauerlaufender FastAPI-Service, der Webhooks entgegennimmt und Argo-Workflows auslöst.

## Regeln

- Du MUSST FastAPI verwenden.
- Du MUSST `/health` Endpoint implementieren.
- Du MUSST Webhooks mit Pydantic validieren.
- Du MUSST Auth-Prüfung auf eingehende Requests implementieren.
- Du MUSST `common.logging` verwenden.
- Du darfst NIEMALS Domänenlogik einbauen.
- Dockerfile: `docker/Dockerfile.http-trigger`, Deployment: Kubernetes Deployment.

## Pattern

```python
app = FastAPI(title="EAI HTTP Trigger")

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/webhook/import", response_model=TriggerResponse)
async def trigger_import(request: ImportRequest) -> TriggerResponse:
    workflow_name = await submit_workflow(
        template="import-planpro",
        parameters={"source_url": request.source_url},
    )
    return TriggerResponse(workflow_name=workflow_name, status="submitted")
```

## Testanforderungen

1. `/health` → 200
2. Gültiger Webhook → Workflow submitted
3. Ungültiger Body → 422
4. Auth-Fehler → 401/403
5. Argo nicht erreichbar → 502

## Abhängigkeiten

- DARFST: `common`, `fastapi`, `uvicorn`, `httpx`
- NICHT: `planpro_parser`, `ds_client`, andere Container
