# workflows/ – Argo Workflow Definitionen

## Zweck

Dieser Ordner enthält alle Argo-Workflow-Definitionen. Workflows orchestrieren die Datenflüsse zwischen Base-Containern und Transformern. Sie werden als YAML oder über Hera (Python SDK) definiert.

---

## Struktur

```
workflows/
├── templates/         # Wiederverwendbare Workflow-Templates
│   ├── retry-defaults.yaml
│   ├── common-env.yaml
│   └── error-handler.yaml
├── examples/          # Vollständig kommentierte Beispiel-Workflows
│   ├── import-planpro.yaml
│   ├── export-planpro.yaml
│   └── diff-report.yaml
├── README.md
└── AGENTS.md
```

---

## Konventionen

- **Workflow-Namen:** `<kategorie>-<beschreibung>` (z.B. `import-planpro`, `export-system-a`)
- **Container-Tags:** Immer semantische Version, **niemals `latest`**
- **Artifact Passing** als Default-Mechanismus für Datenübergabe zwischen Steps
- **Parameters** für Metadaten und Steuerungsinformation (IDs, Counts, Flags)
- **Retry-Defaults:** 3 Versuche, exponentielles Backoff ab 30s
- **Exit-Handler** für jeden Workflow
- **Annotation-Labels:** Verantwortliches Team + Kategorie (import/export/diff/sync)
- Git-Tag: `workflow-<name>/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- Container-Images aus `transformers/` und `base-containers/`
- Templates aus `workflows/templates/`
- Konventionen aus `docs/contracts/workflow-konventionen.md`

---

## Beispiel: Workflow-Struktur

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
        - - name: store
            template: ds-writer
```

---

## Checkliste für neue Workflows

- [ ] Alle Container-Referenzen mit semantischem Tag (kein `latest`)
- [ ] Artifact Passing für Daten zwischen Steps
- [ ] Retry-Defaults angewandt
- [ ] Exit-Handler definiert
- [ ] Annotation-Labels gesetzt (Team, Kategorie)
- [ ] Vollständig kommentiert
- [ ] Konform mit `docs/contracts/workflow-konventionen.md`
