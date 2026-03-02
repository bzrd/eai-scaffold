# base-containers/http-trigger – Webhook-Service (Long-Running)

Dauerlaufender FastAPI-Service der Webhooks entgegennimmt und Argo-Workflows triggert. **Kein Run-to-Completion-Container.**

## Struktur

```
http-trigger/
├── http_trigger/
│   ├── main.py     # FastAPI-App (uvicorn)
│   ├── routes.py   # Webhook-Endpoints
│   ├── workflow.py # Argo-Workflow-Auslösung
│   └── models.py   # Pydantic-Modelle
└── tests/
```

## Besonderheiten

- Deployment: Kubernetes Deployment (nicht Argo-Step)
- Dockerfile: `docker/Dockerfile.http-trigger`
- Entrypoint: `uvicorn http_trigger.main:app`
- Git-Tag: `base-http-trigger/v<major>.<minor>.<patch>`

## Checkliste

- [ ] `/health` Endpoint implementiert
- [ ] Webhooks mit Pydantic validiert
- [ ] Auth auf eingehende Requests
- [ ] Argo-Workflow-Auslösung implementiert
- [ ] Unit-Tests mit TestClient
