# AGENTS.md – ci/

## Rolle

Du pflegst die GitLab CI/CD Pipeline-Konfiguration.

## Regeln

- Du MUSST selektiv bauen – nicht alles bei jedem Commit.
- Du MUSST Tag-Konvention respektieren: `transformer-*`, `base-*`, `lib-*`.
- Du MUSST `path-filters.yml` bei neuen Komponenten aktualisieren.
- Du MUSST Stages: `lint → test → build → push → deploy-dev → deploy-int → deploy-prod`.
- Du MUSST `deploy-int` und `deploy-prod` als manuelle Jobs konfigurieren.
- Du MUSST Images mit semantischem Tag + Git-SHA taggen.
- Du darfst NIEMALS Secrets hardkodieren – GitLab CI/CD Variables.
- Du darfst NIEMALS `deploy-prod` automatisch triggern.

## Pattern: Transformer-Build

```yaml
.build-transformer:
  stage: build
  script:
    - docker build -f docker/Dockerfile.transformer
        --build-arg COMPONENT=$COMPONENT_NAME
        -t $REGISTRY/transformer-$COMPONENT_NAME:$CI_COMMIT_TAG
        -t $REGISTRY/transformer-$COMPONENT_NAME:$CI_COMMIT_SHORT_SHA .
  rules:
    - if: '$CI_COMMIT_TAG =~ /^transformer-.*/'
```

## Pattern: Path-Filter

```yaml
.changes-planpro-parser:
  rules:
    - changes:
        - libs/planpro-parser/**/*
        - libs/common/**/*
```

## Abhängigkeiten

- `docker/` (Dockerfiles)
- Alle Komponenten-Ordner (für Path-Filter)
