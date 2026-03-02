# AGENTS.md – docker/

## Rolle

Du pflegst Dockerfiles und docker-compose.

## Regeln

- Du MUSST Multi-Stage Builds verwenden (Builder + Runtime).
- Du MUSST `python:3.12-slim` als Base-Image verwenden.
- Du MUSST Container als Non-Root User laufen lassen.
- Du MUSST `libs/` per `pip install -e` installieren.
- Du MUSST `docker-compose.yaml` ausschließlich für lokale Entwicklung konzipieren.
- Du darfst NIEMALS Secrets in Dockerfiles hardkodieren.

## Pattern: Dockerfile.transformer

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY libs/ libs/
COPY transformers/${COMPONENT}/ transformer/
RUN pip install --no-cache-dir -e libs/common -e libs/planpro-parser -e transformer/

FROM python:3.12-slim
RUN useradd -m -r appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app/transformer/ /app/transformer/
USER appuser
ENTRYPOINT ["python", "-m", "transformer.main"]
```

## Pattern: Dockerfile.http-trigger

Gleiche Struktur wie Transformer, aber:
```dockerfile
EXPOSE 8000
ENTRYPOINT ["uvicorn", "http_trigger.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Testanforderungen

- `docker build -f docker/Dockerfile.<typ> .` muss erfolgreich sein
- Container mit gültigem Input → Exit-Code 0
