# AGENTS.md – ci/

## Rolle

Du erstellst oder pflegst die GitLab CI/CD Pipeline-Konfiguration. Die Pipeline baut selektiv, testet und deployed Container-Images basierend auf Git Tags und Path-Filtern.

---

## Regeln

- Du MUSST die Pipeline so gestalten, dass sie selektiv baut – nicht alles bei jedem Commit.
- Du MUSST die Tag-Konvention respektieren: `transformer-*`, `base-*`, `lib-*` triggern jeweils den passenden Build.
- Du MUSST Path-Filter pflegen: Wenn eine neue Komponente hinzukommt, muss `path-filters.yml` aktualisiert werden.
- Du MUSST die Stage-Reihenfolge einhalten: `lint → test → build → push → deploy-dev → deploy-int → deploy-prod`.
- Du MUSST `deploy-int` und `deploy-prod` als manuelle Jobs konfigurieren.
- Du MUSST Images mit semantischem Tag UND Git-SHA taggen.
- Du darfst NIEMALS Secrets in Pipeline-Dateien hardkodieren – GitLab CI/CD Variables verwenden.
- Du darfst NIEMALS `deploy-prod` automatisch triggern.
- Du MUSST bei Änderungen an `libs/` alle abhängigen Builds berücksichtigen.

---

## Patterns

### Haupt-Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - push
  - deploy-dev
  - deploy-int
  - deploy-prod

include:
  - local: ci/build-transformer.yml
  - local: ci/build-base.yml
  - local: ci/build-lib.yml
  - local: ci/path-filters.yml
```

### Transformer-Build Template

```yaml
# build-transformer.yml
.build-transformer:
  stage: build
  script:
    - docker build -f docker/Dockerfile.transformer
        --build-arg COMPONENT=$COMPONENT_NAME
        -t $REGISTRY/transformer-$COMPONENT_NAME:$CI_COMMIT_TAG
        -t $REGISTRY/transformer-$COMPONENT_NAME:$CI_COMMIT_SHORT_SHA
        .
  rules:
    - if: '$CI_COMMIT_TAG =~ /^transformer-.*/'
```

### Path-Filter

```yaml
# path-filters.yml
.changes-planpro-parser:
  rules:
    - changes:
        - libs/planpro-parser/**/*
        - libs/common/**/*  # common ist Abhängigkeit von planpro-parser

.changes-transformer-ingest:
  rules:
    - changes:
        - transformers/planpro-ingest/**/*
        - libs/planpro-parser/**/*
        - libs/common/**/*
```

### Library-Build mit Abhängigkeitskaskade

```yaml
# build-lib.yml
.build-lib:
  stage: test
  script:
    - pip install -e libs/$LIB_NAME[dev]
    - pytest libs/$LIB_NAME/tests/
    - mypy libs/$LIB_NAME/
  rules:
    - if: '$CI_COMMIT_TAG =~ /^lib-.*/'
    - changes:
        - libs/$LIB_NAME/**/*
```

---

## Antipatterns

- **Keine hartkodierten Secrets** – GitLab CI/CD Variables verwenden.
- **Keine automatischen Prod-Deployments** – immer manuell.
- **Kein `docker push latest`** – immer semantische Tags + Git-SHA.
- **Keine Build-All-bei-jedem-Commit-Strategie** – selektiv bauen.
- **Kein `allow_failure: true`** auf Test-Jobs – Tests müssen grün sein.

---

## Testanforderungen

- Pipeline-YAML-Syntax validieren
- `path-filters.yml` muss alle Komponenten und ihre Abhängigkeiten abbilden
- Selektives Bauen manuell verifizieren bei neuen Komponenten

---

## Abhängigkeiten

- `docker/` (Dockerfiles)
- Alle Komponenten-Ordner (für Path-Filter)
- ArgoCD (für Deployment – nicht in CI konfiguriert, aber referenziert)

---

## Kontext

Die CI-Pipeline ist der zentrale Qualitätstor des Systems. Kein Code kommt ohne Lint, Tests und Build in die Registry. Deployment auf die Cluster übernimmt ArgoCD – die Pipeline pusht nur Images. Die Tag-basierte selektive Build-Strategie ist kritisch für die Entwicklungsgeschwindigkeit, da das Repo viele Komponenten enthält.
