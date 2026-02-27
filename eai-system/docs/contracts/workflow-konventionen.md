# Contract: Workflow-Konventionen

**Version:** 1.0
**Stand:** 2026-02-27
**Status:** Accepted

---

## Geltungsbereich

Gilt für **alle Argo-Workflow-Definitionen** in `workflows/`.

---

## Definitionen

- **Workflow:** Eine Argo-Workflow-Definition die einen vollständigen Datenfluss beschreibt.
- **Step:** Ein einzelner Container-Lauf innerhalb eines Workflows.
- **Artifact:** Eine Datei die zwischen Steps übergeben wird.
- **Parameter:** Metadaten oder Steuerungsinformation die zwischen Steps übergeben werden.

---

## Datenübergabe zwischen Steps

### Anforderungen

1. Artifact Passing MUSS als Default-Mechanismus für Datenübergabe zwischen Steps verwendet werden.
2. Shared Volumes DÜRFEN nur bei großen Payloads (>100MB) verwendet werden.
3. Bei Shared Volumes MUSS die Pfadkonvention dokumentiert werden.
4. Parameters MÜSSEN für Metadaten und Steuerungsinformation verwendet werden (IDs, Counts, Flags).
5. Parameters DÜRFEN NICHT für die Übergabe großer Datenmengen verwendet werden.

---

## Retry-Konfiguration

### Anforderungen

6. Jeder Step MUSS eine Retry-Konfiguration haben.
7. Die Standard-Retry-Policy MUSS sein: 3 Versuche, exponentielles Backoff ab 30 Sekunden.
8. Die maximale Retry-Dauer MUSS 5 Minuten sein.
9. Die Standard-Retry-Policy SOLL über das Template `workflows/templates/retry-defaults.yaml` referenziert werden.

### Standard-Konfiguration

```yaml
retryStrategy:
  limit: 3
  retryPolicy: Always
  backoff:
    duration: "30s"
    factor: 2
    maxDuration: "5m"
```

---

## Error-Handling

### Anforderungen

10. Jeder Workflow MUSS einen Exit-Handler definieren (`spec.onExit`).
11. Der Exit-Handler MUSS bei Fehler den Workflow-Status und den Fehler strukturiert loggen.
12. Der Exit-Handler SOLL das Template `workflows/templates/error-handler.yaml` referenzieren.

---

## Annotation-Labels

### Anforderungen

13. Jeder Workflow MUSS folgende Labels haben:

| Label | Beschreibung | Beispielwerte |
|---|---|---|
| `team` | Verantwortliches Team | `eai-core`, `integration-team` |
| `category` | Workflow-Kategorie | `import`, `export`, `diff`, `sync` |

---

## Container-Referenzierung

### Anforderungen

14. Container-Images MÜSSEN mit semantischem Tag referenziert werden (z.B. `v1.2.3`).
15. Container-Images DÜRFEN NICHT mit `latest` referenziert werden.
16. Container-Images MÜSSEN aus der internen Registry referenziert werden (`registry.intern/`).

---

## Umgebungsvariablen

### Anforderungen

17. Jeder Step MUSS die Standard-Umgebungsvariablen aus `container-konvention.md` setzen.
18. `CORRELATION_ID` MUSS auf die Workflow-UID gesetzt werden: `"{{workflow.uid}}"`.
19. Die Standard-Umgebungsvariablen SOLLEN über das Template `workflows/templates/common-env.yaml` gesetzt werden.

---

## Beispiele

### Korrekt: Vollständiger Workflow

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: import-planpro
  labels:
    team: eai-core
    category: import
spec:
  entrypoint: main
  onExit: error-handler
  templates:
    - name: main
      steps:
        - - name: fetch
            template: file-fetcher
        - - name: transform
            template: planpro-ingest
            arguments:
              artifacts:
                - name: input
                  from: "{{steps.fetch.outputs.artifacts.output}}"
    - name: file-fetcher
      container:
        image: registry.intern/base-file-fetcher:v1.0.0
        env:
          - name: CORRELATION_ID
            value: "{{workflow.uid}}"
      retryStrategy:
        limit: 3
        backoff:
          duration: "30s"
          factor: 2
```

### Inkorrekt: latest Tag

```yaml
container:
  image: registry.intern/base-file-fetcher:latest  # VERBOTEN
```

### Inkorrekt: Fehlende Labels

```yaml
metadata:
  name: import-planpro
  # FEHLT: labels mit team und category
```
