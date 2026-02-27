# AGENTS.md – docker/

## Rolle

Du erstellst oder pflegst Dockerfiles und die docker-compose-Konfiguration. Du stellst sicher, dass alle Container korrekt gebaut und lokal getestet werden können.

---

## Regeln

- Du MUSST Multi-Stage Builds verwenden: Builder-Stage für Dependencies, Runtime-Stage minimal.
- Du MUSST `python:3.12-slim` als Base-Image verwenden.
- Du MUSST Container als Non-Root User laufen lassen.
- Du MUSST `libs/` aus dem Repo per `pip install -e` in die Container installieren.
- Du MUSST sicherstellen, dass Transformer auch OHNE Docker entwickelbar sind (`python main.py` mit lokaler Input-Datei reicht für die tägliche Arbeit).
- Du MUSST `docker-compose.yaml` NUR für lokale Entwicklung konzipieren – nicht für Produktion.
- Du darfst NIEMALS Secrets (Tokens, Passwörter) in Dockerfiles hardkodieren.
- Du darfst NIEMALS `RUN pip install` mit externen Packages ohne explizite Version ausführen.

---

## Patterns

### Dockerfile.transformer (Multi-Stage)

```dockerfile
# Builder Stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY libs/ libs/
COPY transformers/${COMPONENT}/ transformer/
RUN pip install --no-cache-dir \
    -e libs/common \
    -e libs/planpro-parser \
    -e transformer/

# Runtime Stage
FROM python:3.12-slim
RUN useradd -m -r appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app/transformer/ /app/transformer/
USER appuser
ENTRYPOINT ["python", "-m", "transformer.main"]
```

### Dockerfile.base (Multi-Stage)

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY libs/ libs/
COPY base-containers/${COMPONENT}/ container/
RUN pip install --no-cache-dir \
    -e libs/common \
    -e libs/ds-client \
    -e container/

FROM python:3.12-slim
RUN useradd -m -r appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app/container/ /app/container/
USER appuser
ENTRYPOINT ["python", "-m", "container.main"]
```

### Dockerfile.http-trigger

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY libs/common libs/common
COPY base-containers/http-trigger/ service/
RUN pip install --no-cache-dir \
    -e libs/common \
    -e service/

FROM python:3.12-slim
RUN useradd -m -r appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app/service/ /app/service/
USER appuser
EXPOSE 8000
ENTRYPOINT ["uvicorn", "http_trigger.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yaml Struktur

```yaml
# NUR FÜR LOKALE ENTWICKLUNG
services:
  # Mock-Datenspeicher (optional, für lokale Tests)
  ds-mock:
    image: ...
    ports: ["8080:8080"]

  # Beispiel: Transformer lokal ausführen
  transformer-ingest:
    build:
      context: ..
      dockerfile: docker/Dockerfile.transformer
      args:
        COMPONENT: planpro-ingest
    volumes:
      - ./testdata:/tmp/input:ro
      - ./output:/tmp/output
    environment:
      - CORRELATION_ID=local-test
      - LOG_LEVEL=DEBUG
```

---

## Antipatterns

- **Keine Secrets in Dockerfiles** – immer über Umgebungsvariablen oder Secrets-Management.
- **Keine `latest` Tags** in `FROM`-Statements – immer explizite Version.
- **Kein `docker-compose` für Produktion** – nur lokal.
- **Keine `RUN pip install` ohne Version-Pin** für externe Packages.
- **Kein Root-User** in Runtime-Stage.

---

## Testanforderungen

- Alle Dockerfiles müssen erfolgreich bauen: `docker build -f docker/Dockerfile.<typ> .`
- Container muss mit gültigem Test-Input starten und Exit-Code 0 geben
- `docker-compose up` muss den lokalen Dev-Stack starten können

---

## Abhängigkeiten

- `libs/` – installiert in Container
- `transformers/` und `base-containers/` – Code der gebaut wird

---

## Kontext

Container-Images werden über Prefixed Git Tags versioniert und in die interne Registry gepusht. CI reagiert auf Tags und baut selektiv. Images werden mit semantischem Tag UND Git-SHA getaggt. In Workflows wird immer der semantische Tag referenziert.
