# EAI System – Enterprise Application Integration für Bahninfrastruktur-Planung

Dieses Monorepo enthält alle Komponenten der zentralen Integrationsplattform für den Austausch von PlanPro-Daten zwischen heterogenen Fachapplikationen in der Bahninfrastruktur-Planung.

---

## Was ist dieses System?

Das EAI-System ermöglicht den strukturierten, nachvollziehbaren und asynchronen Austausch von PlanPro-Infrastrukturdaten (Weichen, Signale, Gleise, etc.) zwischen verschiedenen Fachapplikationen. Es bildet die technische Grundlage für die gemeinsame Planung kritischer Bahninfrastruktur.

Jede Datenveränderung ist auditierbar: Woher kamen die Daten, wann, durch welchen Transformer in welcher Version – das ist die normative Anforderung an jede Komponente.

---

## Architekturüberblick

```
Fachapplikation A          Fachapplikation B
       │                          │
       │  HTTP-Trigger             │
       ▼                          ▼
┌─────────────────────────────────────────┐
│          Logistics Layer                │
│     (Argo Workflows auf Kubernetes)     │
│                                         │
│  ┌──────────┐  ┌───────────┐           │
│  │  Base-   │  │Transformer│           │
│  │Container │──│(Domäne)   │           │
│  │  (I/O)   │  │           │           │
│  └──────────┘  └───────────┘           │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│ Datenspeicher│
│    (FIN)    │
│  MSSQL +    │
│  REST-API   │
└─────────────┘
```

**Datenspeicher (FIN):** MSSQL-Datenbank mit REST-API. Speichert JSON-Objekte (aus PlanPro-XML zerlegt), bietet Versionierung, Scopes, Phasen und Referenzierung.

**Logistics Layer:** Alle Datenflüsse laufen über Argo Workflows. Kein direkter API-Zugriff durch Fachapplikationen. Alle Flows sind asynchron.

**Transformer:** Eigenständige Container mit ausschließlich Domänenlogik. Kein I/O, kein HTTP, kein Datenbankzugriff. Lesen von `INPUT_PATH`, schreiben nach `OUTPUT_PATH`.

**Base-Container:** Die I/O-Schicht. Holen Dateien, machen REST-API-Calls, schreiben in den Datenspeicher. Nutzen `libs/ds-client` und `libs/common`.

**Libraries:** Repo-intern, direkt per Import eingebunden (HEAD-Prinzip, keine Versionspins).

---

## Repository-Struktur

```
eai-system/
├── libs/                    # Shared Libraries (planpro-parser, ds-client, common)
├── transformers/            # Domänenlogik-Container
├── base-containers/         # I/O-Container (Dateisystem, HTTP, Datenbank)
├── workflows/               # Argo Workflow Definitionen
├── docker/                  # Dockerfiles und docker-compose
├── ci/                      # GitLab CI/CD Konfiguration
├── docs/                    # ADRs, Runbooks, Contracts (normative Referenz)
└── tests/                   # Integrationstests und geteilte Fixtures
```

---

## Setup für neue Entwickler

### 1. Repository klonen
```bash
git clone <repo-url>
cd eai-system
```

### 2. Python-Umgebung einrichten
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e "libs/common[dev]"
pip install -e "libs/planpro-parser[dev]"
pip install -e "libs/ds-client[dev]"
```

### 3. Pre-commit Hooks installieren
```bash
pip install pre-commit
pre-commit install
```

### 4. Ersten Test ausführen
```bash
make test-unit
```

### 5. Linting prüfen
```bash
make lint
```

---

## Neuen Transformer anlegen

1. `transformers/_template/` nach `transformers/<name>/` kopieren
2. `transform.py` mit der Domänenlogik implementieren
3. Tests in `tests/` schreiben (Fixtures nutzen, keine synthetischen Daten)
4. `README.md` im neuen Ordner aktualisieren
5. Git-Tag nach Konvention setzen: `transformer-<name>/v1.0.0`

Detaillierte Anleitung: `transformers/_template/README.md` und `docs/runbooks/neuen-transformer-anlegen.md`

---

## Wichtigste Dokumentation

| Dokument | Inhalt |
|---|---|
| `docs/contracts/container-konvention.md` | **Normativ:** Umgebungsvariablen, I/O-Konventionen, Exit-Codes |
| `docs/contracts/logging-format.md` | **Normativ:** JSON-Log-Schema |
| `docs/contracts/provenance-format.md` | **Normativ:** Provenance-Fragment-Schema |
| `docs/contracts/workflow-konventionen.md` | **Normativ:** Argo-Workflow-Struktur |
| `docs/contracts/namenskonventionen.md` | **Normativ:** Naming für Images, Tags, Ordner |
| `docs/adr/` | Architecture Decision Records |
| `docs/runbooks/` | Operative Anleitungen |

---

## AI-gestützte Entwicklung

Dieses Repo ist für AI-Agenten-gestützte Entwicklung konzipiert. Lies `AGENTS.md` in diesem Ordner als erstes Dokument, bevor du Änderungen vornimmst. Jeder Ordner enthält eine eigene `AGENTS.md` mit spezifischen Anweisungen für den Kontext dieses Ordners.

**Goldene Regel:** Contracts in `docs/contracts/` sind normativ. Bei Widerspruch zwischen einer `AGENTS.md` und einem Contract gilt der Contract.
