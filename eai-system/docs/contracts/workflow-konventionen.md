# Contract: Workflow-Konventionen

**Version:** 1.0 | **Status:** Accepted

Gilt für alle Argo-Workflow-Definitionen in `workflows/`.

## Datenübergabe

1. Artifact Passing MUSS der Default-Mechanismus sein.
2. Shared Volumes NUR bei >100MB, Pfadkonvention dokumentieren.
3. Parameters NUR für Metadaten (IDs, Counts, Flags).
4. Parameters NICHT für große Daten.

## Retry

5. Jeder Step MUSS eine Retry-Konfiguration haben.
6. Standard: 3 Versuche, exponentiell ab 30s.
7. Max. Retry-Dauer: 5 Minuten.

```yaml
retryStrategy:
  limit: 3
  retryPolicy: Always
  backoff:
    duration: "30s"
    factor: 2
    maxDuration: "5m"
```

## Error-Handling

8. Jeder Workflow MUSS einen Exit-Handler haben (`spec.onExit`).
9. Exit-Handler MUSS Fehler strukturiert loggen.

## Labels

10. Jeder Workflow MUSS Labels haben:
    - `team`: verantwortliches Team
    - `category`: `import`/`export`/`diff`/`sync`

## Container-Referenzierung

11. Images MÜSSEN mit semantischem Tag referenziert werden.
12. `latest` ist VERBOTEN.
13. Images MÜSSEN aus `registry.intern/` kommen.

## Umgebungsvariablen

14. Jeder Step MUSS Standard-Env-Vars aus `container-konvention.md` setzen.
15. `CORRELATION_ID` MUSS `"{{workflow.uid}}"` sein.
