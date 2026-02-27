# workflows/examples/ – Referenz-Workflows

## Zweck

Vollständig kommentierte Beispiel-Workflows als normative Referenz für neue Workflows. Jedes Beispiel dokumentiert in Kommentaren: Warum dieser Schritt, welche Artifacts fließen, welche Env-Vars gesetzt werden.

---

## Struktur

```
examples/
├── import-planpro.yaml    # Fetch → Ingest-Transform → Store
├── export-planpro.yaml    # Read → Export-Transform → Push
├── diff-report.yaml       # Read Stand 1 → Read Stand 2 → Diff → Store
└── README.md
```

---

## Erwartete Beispiele

### `import-planpro.yaml`
Einfacher Import-Workflow:
1. `file-fetcher` holt PlanPro-XML von Fachapplikation
2. `planpro-ingest` zerlegt XML in JSON-Objekte
3. `ds-writer` speichert Objekte im Datenspeicher

### `export-planpro.yaml`
Export-Workflow:
1. `ds-reader` liest Objekte aus dem Datenspeicher
2. `planpro-export` assembliert JSON zu PlanPro-XML
3. `file-pusher` liefert XML an Fachapplikation

### `diff-report.yaml`
Diff-Workflow:
1. `ds-reader` liest Stand 1 (z.B. Phase "Entwurf")
2. `ds-reader` liest Stand 2 (z.B. Phase "Genehmigung")
3. `diff` vergleicht die Stände
4. `ds-writer` speichert den Diff-Report

---

## Konventionen

- Jede YAML-Datei ist vollständig lauffähig (nicht nur Fragment)
- Inline-Kommentare erklären jeden Step
- Container-Tags sind semantisch (niemals `latest`)
- Templates aus `workflows/templates/` werden referenziert
- Annotation-Labels sind gesetzt

---

## Checkliste

- [ ] Workflow ist syntaktisch korrekt (`argo lint`)
- [ ] Jeder Step ist kommentiert (Zweck, Artifacts, Env-Vars)
- [ ] Templates referenziert (retry, env, error-handler)
- [ ] Annotation-Labels gesetzt
- [ ] Container-Tags semantisch
