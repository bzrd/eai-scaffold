# workflows/ – Argo Workflow-Definitionen

Orchestriert Datenflüsse zwischen Base-Containern und Transformern.

## Struktur

```
workflows/
├── templates/   # retry-defaults.yaml, common-env.yaml, error-handler.yaml
├── examples/    # import-planpro.yaml, export-planpro.yaml, diff-report.yaml
└── AGENTS.md
```

## Konventionen

- Container-Tags: immer semantische Version, **niemals `latest`**
- Datenübergabe: Artifact Passing (Default), Shared Volumes nur bei >100MB
- Retry: 3 Versuche, exponentiell ab 30s, max 5min
- Exit-Handler: Pflicht für jeden Workflow
- Labels: `team` + `category` (import/export/diff/sync)
- Git-Tag: `workflow-<name>/v<major>.<minor>.<patch>`

## Checkliste

- [ ] Kein `latest`-Tag
- [ ] Artifact Passing für Daten
- [ ] Retry-Defaults angewandt
- [ ] Exit-Handler definiert
- [ ] Labels gesetzt
