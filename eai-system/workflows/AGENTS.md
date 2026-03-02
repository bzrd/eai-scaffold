# AGENTS.md – workflows/

## Rolle

Du erstellst oder pflegst Argo-Workflow-Definitionen.

## Regeln

- Du MUSST Artifact Passing für Datenübergabe verwenden.
- Du MUSST Parameters nur für Metadaten (IDs, Counts, Flags) verwenden.
- Du MUSST Retry: 3 Versuche, exponentiell ab 30s, max 5min.
- Du MUSST einen Exit-Handler für jeden Workflow definieren.
- Du MUSST Labels `team` und `category` setzen.
- Du darfst NIEMALS `latest` als Container-Tag verwenden.
- Normativ: `docs/contracts/workflow-konventionen.md`.

## Pattern: Artifact Passing

```yaml
steps:
  - - name: fetch
      template: file-fetcher
  - - name: transform
      template: planpro-ingest
      arguments:
        artifacts:
          - name: input
            from: "{{steps.fetch.outputs.artifacts.output}}"
```

## Pattern: Retry

```yaml
retryStrategy:
  limit: 3
  retryPolicy: Always
  backoff:
    duration: "30s"
    factor: 2
    maxDuration: "5m"
```

## Pattern: Env-Vars

```yaml
env:
  - name: CORRELATION_ID
    value: "{{workflow.uid}}"
  - name: INPUT_PATH
    value: "/tmp/input"
  - name: OUTPUT_PATH
    value: "/tmp/output"
```

## Abhängigkeiten

- Container-Images aus `transformers/` und `base-containers/`
- Templates aus `workflows/templates/`
- Normativ: `docs/contracts/workflow-konventionen.md`
