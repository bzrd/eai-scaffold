# ci/ – GitLab CI/CD

Selektive Pipeline: baut nur geänderte Komponenten basierend auf Git-Tags und Path-Filtern.

## Struktur

```
ci/
├── .gitlab-ci.yml           # Haupt-Pipeline
├── build-transformer.yml    # Template: Transformer-Builds
├── build-base.yml           # Template: Base-Container-Builds
├── build-lib.yml            # Template: Library-Tests
└── path-filters.yml         # Pfad → Build-Trigger Mapping
```

## Stages

```
lint → test → build → push → deploy-dev (auto) → deploy-int (manuell) → deploy-prod (manuell)
```

## Tag-Konvention

| Tag-Pattern | Trigger |
|---|---|
| `transformer-*` | Transformer-Build |
| `base-*` | Base-Container-Build |
| `lib-*` | Library-Tests + abhängige Builds |

## Checkliste

- [ ] Path-Filter bei neuer Komponente aktualisiert
- [ ] `deploy-int` und `deploy-prod` manuell
- [ ] Images mit sem. Tag + Git-SHA getaggt
- [ ] Keine Secrets in Pipeline-Dateien
