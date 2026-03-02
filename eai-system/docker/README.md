# docker/ – Docker-Konfiguration

Dockerfiles für Transformer, Base-Container und HTTP-Trigger sowie docker-compose für lokale Entwicklung.

## Struktur

```
docker/
├── Dockerfile.transformer   # Shared Dockerfile für Transformer (ARG COMPONENT)
├── Dockerfile.base          # Shared Dockerfile für Base-Container
├── Dockerfile.http-trigger  # FastAPI Long-Running-Service
└── docker-compose.yaml      # NUR für lokale Entwicklung
```

## Konventionen

- Multi-Stage Builds: Builder + Runtime (`python:3.12-slim`)
- Non-Root User in Runtime-Stage
- `libs/` per `pip install -e` einbinden
- `docker-compose.yaml` ausschließlich für lokale Entwicklung

## Bauen

```bash
docker build -f docker/Dockerfile.transformer --build-arg COMPONENT=planpro-ingest .
# oder:
make build COMPONENT=transformer-ingest
```

## Checkliste

- [ ] Multi-Stage Build
- [ ] Non-Root User
- [ ] Keine Secrets in Dockerfiles
- [ ] Alle `libs/` korrekt installiert
