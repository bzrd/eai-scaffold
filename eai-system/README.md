# EAI System – PlanPro Integrationsplattform

Monorepo für den nachvollziehbaren Austausch von PlanPro-Infrastrukturdaten zwischen Fachapplikationen. Alle Flows gehen über den Logistics Layer (Argo Workflows).

## Architektur

```
Fachapplikationen → HTTP-Trigger → Argo Workflows → Datenspeicher (FIN / MSSQL+REST)
                                    Base-Container (I/O) ↔ Transformer (Domäne)
```

## Struktur

```
eai-system/
├── libs/            # planpro-parser, ds-client, common
├── transformers/    # Domänenlogik-Container (kein I/O)
├── base-containers/ # I/O-Container (HTTP, Datei, DB)
├── workflows/       # Argo Workflow-Definitionen
├── docker/          # Dockerfiles
├── ci/              # GitLab CI/CD
├── docs/            # Contracts (normativ), ADRs, Runbooks
└── tests/           # Integrationstests + Fixtures
```

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e "libs/common[dev]" -e "libs/planpro-parser[dev]" -e "libs/ds-client[dev]"
pre-commit install && make test-unit
```

## Normative Priorität

`docs/contracts/` > ordnerspezifische `AGENTS.md` > Root-`AGENTS.md`
