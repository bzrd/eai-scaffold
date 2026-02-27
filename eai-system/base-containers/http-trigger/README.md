# base-containers/http-trigger – Webhook-Service (Long-Running)

## Zweck

Ein dauerlaufender FastAPI-Service, der Webhooks von Fachapplikationen entgegennimmt und Argo-Workflows triggert. **Anders als alle anderen Container ist dieser KEIN Run-to-Completion-Container, sondern ein Long-Running-Service.**

---

## Struktur

```
http-trigger/
├── http_trigger/
│   ├── __init__.py
│   ├── main.py          # FastAPI-App Entrypoint (uvicorn)
│   ├── routes.py        # Webhook-Endpoints
│   ├── workflow.py       # Argo-Workflow-Auslösung
│   └── models.py        # Request/Response-Modelle
├── tests/
│   ├── conftest.py
│   ├── test_routes.py
│   └── test_workflow.py
├── pyproject.toml
└── README.md
```

---

## Konventionen

- **Deployment:** Kubernetes Deployment (nicht Argo-Step!) mit Service und Ingress
- **Dockerfile:** Eigenes `docker/Dockerfile.http-trigger` (nicht das Standard-Base-Dockerfile)
- **Entrypoint:** `uvicorn http_trigger.main:app`
- **Health-Check:** `/health` Endpoint
- **Git-Tag:** `base-http-trigger/v<major>.<minor>.<patch>`

**WICHTIG:** Dieser Container hat ein fundamental anderes Deployment-Modell als alle anderen Container:
- Läuft dauerhaft (nicht einmalig wie Argo-Steps)
- Braucht ein Kubernetes Deployment, Service und ggf. Ingress
- Hat keinen `INPUT_PATH`/`OUTPUT_PATH` – er empfängt HTTP-Requests

---

## Abhängigkeiten

- `libs/common` – Logging, Config
- `fastapi` – Web-Framework
- `uvicorn` – ASGI-Server
- Argo-API-Client (für Workflow-Auslösung)

---

## Beispiel: Webhook-Endpoint

```python
# routes.py
@app.post("/webhook/import")
async def trigger_import(request: ImportRequest) -> TriggerResponse:
    workflow_name = submit_workflow(
        template="import-planpro",
        parameters={"source_url": request.source_url},
    )
    return TriggerResponse(workflow_name=workflow_name, status="submitted")
```

---

## Checkliste

- [ ] FastAPI-App mit `/health` Endpoint
- [ ] Webhook-Endpoints dokumentiert
- [ ] Argo-Workflow-Auslösung implementiert
- [ ] Request-Validierung (Pydantic-Modelle)
- [ ] Structured JSON Logging
- [ ] Eigenes Dockerfile (`Dockerfile.http-trigger`)
- [ ] Kubernetes Deployment-Manifest (oder Verweis auf ArgoCD)
- [ ] Unit-Tests mit TestClient
- [ ] Auth-Prüfung auf eingehende Webhooks
