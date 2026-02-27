# AGENTS.md – workflows/examples/

## Rolle

Du erstellst oder pflegst Referenz-Workflows. Diese Beispiele sind die **normative Referenz** für neue Workflows. Jeder neue Workflow sollte sich an diesen Beispielen orientieren.

---

## Regeln

- Du MUSST jeden Step vollständig kommentieren: Warum dieser Step, welche Artifacts fließen, welche Env-Vars gesetzt werden.
- Du MUSST Templates aus `workflows/templates/` referenzieren (retry, env, error-handler).
- Du MUSST Annotation-Labels setzen: Team + Kategorie.
- Du MUSST Container-Images mit semantischem Tag referenzieren.
- Du darfst NIEMALS `latest` als Tag verwenden.
- Du MUSST Artifact Passing als Default für Datenübergabe verwenden.
- Du MUSST diese Beispiele lauffähig halten – sie sind keine Fragmente.

---

## Patterns

### Vollständig kommentierter Import-Workflow

```yaml
# import-planpro.yaml
# Zweck: Importiert eine PlanPro-XML-Datei in den Datenspeicher.
# Ablauf: Fetch → Transform → Store
# Team: eai-core | Kategorie: import
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: import-planpro
  labels:
    team: eai-core
    category: import
spec:
  entrypoint: main
  onExit: error-handler  # Bei Fehler: strukturiertes Logging
  arguments:
    parameters:
      # URL der PlanPro-Datei (von der aufrufenden Fachapplikation)
      - name: source-url
      # Ziel-Scope im Datenspeicher
      - name: scope
      # Ziel-Phase im Datenspeicher
      - name: phase
  templates:
    - name: main
      steps:
        # Step 1: PlanPro-XML von Fachapplikation holen
        - - name: fetch
            template: file-fetcher
        # Step 2: XML in JSON-Objekte zerlegen
        - - name: transform
            template: planpro-ingest
            arguments:
              artifacts:
                - name: input
                  from: "{{steps.fetch.outputs.artifacts.output}}"
        # Step 3: JSON-Objekte in Datenspeicher schreiben
        - - name: store
            template: ds-writer
            arguments:
              artifacts:
                - name: input
                  from: "{{steps.transform.outputs.artifacts.output}}"
```

---

## Antipatterns

- **Keine unkommentierten Steps** – jeder Step braucht eine Erklärung.
- **Keine fehlenden Labels** – Team und Kategorie sind Pflicht.
- **Keine Fragmente** – jedes Beispiel muss lauffähig sein.

---

## Testanforderungen

- `argo lint` auf alle Beispiele
- Beispiele werden in Integrationstests gegen die Dev-Umgebung getestet

---

## Abhängigkeiten

- Templates: `workflows/templates/`
- Container-Images: `transformers/` und `base-containers/`
- Normative Referenz: `docs/contracts/workflow-konventionen.md`

---

## Kontext

Diese Beispiele sind die normative Referenz für alle Workflows im System. Neue Workflows MÜSSEN sich an diesen Beispielen orientieren. Wenn ein neues Pattern benötigt wird, sollte zuerst ein neues Beispiel hier angelegt werden.
