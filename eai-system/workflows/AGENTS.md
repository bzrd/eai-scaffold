# AGENTS.md – workflows/

## Rolle

Du erstellst oder pflegst Argo-Workflow-Definitionen. Workflows orchestrieren die Datenflüsse zwischen Base-Containern und Transformern im Logistics Layer.

---

## Regeln

- Du MUSST Artifact Passing als Default-Mechanismus für Datenübergabe zwischen Steps verwenden.
- Du MUSST Shared Volumes nur bei großen Payloads (>100MB) verwenden und die Pfadkonvention dokumentieren.
- Du MUSST Parameters für Metadaten und Steuerungsinformation verwenden (IDs, Counts, Flags).
- Du MUSST Retry-Defaults anwenden: 3 Versuche, exponentielles Backoff ab 30s.
- Du MUSST einen Exit-Handler für jeden Workflow definieren.
- Du MUSST Annotation-Labels setzen: Verantwortliches Team + Kategorie.
- Du darfst NIEMALS `latest` als Container-Tag verwenden – immer semantische Version.
- Du darfst NIEMALS Container-Images referenzieren die nicht im Repo definiert sind.
- Du MUSST jeden Workflow vollständig kommentieren: Warum dieser Step, welche Artifacts fließen, welche Env-Vars.
- Du MUSST `docs/contracts/workflow-konventionen.md` als normative Referenz beachten.

---

## Patterns

### Artifact Passing zwischen Steps

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

### Retry-Konfiguration

```yaml
retryStrategy:
  limit: 3
  retryPolicy: Always
  backoff:
    duration: "30s"
    factor: 2
    maxDuration: "5m"
```

### Exit-Handler

```yaml
spec:
  onExit: exit-handler
  templates:
    - name: exit-handler
      steps:
        - - name: log-result
            template: error-logger
            when: "{{workflow.status}} != Succeeded"
```

### Standard-Umgebungsvariablen

```yaml
env:
  - name: CORRELATION_ID
    value: "{{workflow.uid}}"
  - name: LOG_LEVEL
    value: "INFO"
  - name: INPUT_PATH
    value: "/tmp/input"
  - name: OUTPUT_PATH
    value: "/tmp/output"
```

---

## Antipatterns

- **Kein `latest` Tag** – immer semantische Version.
- **Keine Parameters für große Daten** – Artifacts verwenden.
- **Keine hartkodierten Container-Registry-URLs** – über Template-Parameter oder ConfigMaps.
- **Keine Workflows ohne Exit-Handler** – Fehler müssen immer geloggt werden.
- **Keine Workflows ohne Annotation-Labels** – Team-Zuordnung ist Pflicht.

---

## Testanforderungen

- Workflow-YAML auf syntaktische Korrektheit prüfen (`argo lint`)
- Beispiel-Workflows in `workflows/examples/` als normative Referenz verwenden
- Integrationstests in `tests/integration/` gegen eine Dev-Umgebung

---

## Abhängigkeiten

- Container-Images aus `transformers/` und `base-containers/` (als Referenz, nicht als Import)
- Templates aus `workflows/templates/`
- Normative Referenz: `docs/contracts/workflow-konventionen.md`

---

## Kontext

Argo Workflows ist der Logistics Layer des Systems. Alle Datenflüsse zwischen Fachapplikationen und dem Datenspeicher laufen über Argo-Workflows. Ein typischer Workflow besteht aus: Base-Container (I/O) → Transformer (Domänenlogik) → Base-Container (I/O). Die Workflows sind die einzige Stelle wo die verschiedenen Container zusammengeführt werden.
