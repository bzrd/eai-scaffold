# ci/ – CI/CD Konfiguration

## Zweck

Enthält alle GitLab CI/CD Konfigurationsdateien. Die Pipeline baut selektiv basierend auf Prefixed Git Tags und Path-Filtern.

---

## Struktur

```
ci/
├── .gitlab-ci.yml             # Haupt-Pipeline-Definition
├── build-transformer.yml      # Wiederverwendbares Template für Transformer-Builds
├── build-base.yml             # Wiederverwendbares Template für Base-Container-Builds
├── build-lib.yml              # Template für Library-Tests
├── path-filters.yml           # Mapping welcher Pfad welchen Build triggert
├── README.md
└── AGENTS.md
```

---

## Konventionen

### Pipeline Stages

```
lint → test → build → push → deploy-dev (auto) → deploy-int (manuell) → deploy-prod (manuell)
```

### Tag-basierte Builds

| Tag-Pattern | Trigger |
|---|---|
| `transformer-*` | Transformer-Build |
| `base-*` | Base-Container-Build |
| `lib-*` | Library-Tests + alle abhängigen Container-Builds |

### Path-Filter

Änderungen an `libs/planpro-parser/` triggern alle Builds die `planpro-parser` nutzen (alle Transformer, indirekt).

### Selektives Bauen

Die Pipeline baut **nicht** alles bei jedem Commit. Nur geänderte Komponenten oder deren Abhängige werden gebaut.

### Image-Tagging

```
registry.intern/transformer-ingest:v1.2.3
registry.intern/transformer-ingest:abc123f
```

### Deployment

ArgoCD ist für das Deployment auf den Cluster zuständig. Die CI-Pipeline pusht Images in die Registry, ArgoCD erkennt neue Tags und deployed automatisch (dev) oder manuell (int, prod).

---

## Abhängigkeiten

- `docker/` – Dockerfiles
- Alle Komponenten-Ordner (für Path-Filter)

---

## Checkliste für Pipeline-Änderungen

- [ ] `argo lint` / YAML-Validierung
- [ ] Selektives Bauen weiterhin korrekt
- [ ] Path-Filter aktualisiert bei neuen Komponenten
- [ ] Stages-Reihenfolge eingehalten
- [ ] Keine Secrets in der Pipeline-Definition
- [ ] Deploy-Stages manuell für int/prod
