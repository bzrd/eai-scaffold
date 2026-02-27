# AGENTS.md – workflows/templates/

## Rolle

Du erstellst oder pflegst wiederverwendbare Argo-Workflow-Templates. Diese Templates definieren Standards die in allen konkreten Workflows gelten.

---

## Regeln

- Du MUSST Templates so gestalten, dass sie von mehreren Workflows referenzierbar sind.
- Du MUSST Änderungen an Templates gegen alle bestehenden Workflows testen – Änderungen haben großen Blast-Radius.
- Du MUSST Templates mit `argo lint` validieren.
- Du darfst NIEMALS workflow-spezifische Logik in Templates einbauen – nur geteilte Standards.

---

## Patterns

### Retry-Defaults Template

```yaml
# retry-defaults.yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: retry-defaults
spec:
  templates:
    - name: with-retry
      retryStrategy:
        limit: 3
        retryPolicy: Always
        backoff:
          duration: "30s"
          factor: 2
          maxDuration: "5m"
```

### Common-Env Template

```yaml
# common-env.yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: common-env
spec:
  templates:
    - name: standard-env
      container:
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

- **Keine workflow-spezifische Logik** in Templates.
- **Keine Breaking Changes** ohne ADR und Migration aller nutzenden Workflows.

---

## Testanforderungen

- `argo lint` auf alle Templates
- Referenzierung in mindestens einem Beispiel-Workflow verifizieren

---

## Abhängigkeiten

- Normative Referenz: `docs/contracts/workflow-konventionen.md` und `docs/contracts/container-konvention.md`

---

## Kontext

Templates sind die zentrale Stelle für Workflow-Standards. Retry-Policy, Umgebungsvariablen und Error-Handling werden hier einmal definiert und von allen Workflows referenziert. Änderungen hier betreffen das gesamte System.
