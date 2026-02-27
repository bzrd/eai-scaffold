# docker/ – Docker-Konfiguration

## Zweck

Enthält alle Docker-relevanten Dateien: Shared Dockerfiles für Transformer und Base-Container, ein eigenes Dockerfile für den HTTP-Trigger und docker-compose für die lokale Entwicklung.

---

## Struktur

```
docker/
├── Dockerfile.transformer     # Shared Dockerfile für alle Transformer
├── Dockerfile.base            # Shared Dockerfile für Base-Container
├── Dockerfile.http-trigger    # Eigenes Dockerfile für den dauerlaufenden HTTP-Trigger
├── docker-compose.yaml        # Lokaler Dev-Stack
├── README.md
└── AGENTS.md
```

---

## Konventionen

### Dockerfiles
- **Multi-Stage Builds:** Builder-Stage für Dependencies, Runtime-Stage minimal
- **Minimale Images:** `python:3.12-slim` als Base
- **Non-Root User:** Container laufen als non-root User
- **Libs aus dem Repo installiert:** `libs/common`, `libs/planpro-parser`, etc. werden per `pip install -e` eingebunden
- **Build-Argument `COMPONENT`:** Wählt welcher Transformer/Base-Container gebaut wird

### Transformer-Entwicklung ohne Docker
Transformer MÜSSEN auch ohne Docker entwickelbar sein:
```bash
INPUT_PATH=./testdata/input.xml OUTPUT_PATH=./testdata/output.json python -m planpro_ingest.main
```

### docker-compose.yaml
- **NUR für lokale Entwicklung** – nicht für Produktion
- Services: Mock-Datenspeicher, Transformer, Base-Container
- Shared Volume für Artifact-Passing zwischen Containern

---

## Abhängigkeiten

- `transformers/` und `base-containers/` (Code der in Container gebaut wird)
- `libs/` (installiert in die Container)

---

## Beispiel: Transformer bauen

```bash
# Einzelnen Transformer bauen
docker build -f docker/Dockerfile.transformer \
    --build-arg COMPONENT=planpro-ingest \
    -t registry.intern/transformer-ingest:dev .

# Über Makefile
make build COMPONENT=transformer-ingest
```

---

## Checkliste für Dockerfile-Änderungen

- [ ] Multi-Stage Build beibehalten
- [ ] Non-Root User beibehalten
- [ ] `python:3.12-slim` als Base
- [ ] Alle `libs/` korrekt installiert
- [ ] Image baut erfolgreich für alle Transformer/Base-Container
- [ ] Container startet und gibt Exit-Code 0 bei gültigem Input
