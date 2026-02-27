# workflows/templates/ – Wiederverwendbare Argo Workflow Templates

## Zweck

Wiederverwendbare Argo-Workflow-Templates die in konkreten Workflows referenziert werden. Sie definieren Standards für Retry-Policies, Umgebungsvariablen und Error-Handling.

---

## Struktur

```
templates/
├── retry-defaults.yaml    # Standard Retry-Policy
├── common-env.yaml        # Standard-Umgebungsvariablen für alle Container
├── error-handler.yaml     # Standard Exit-Handler für fehlgeschlagene Steps
└── README.md
```

---

## Konventionen

- Templates werden von konkreten Workflows per `templateRef` referenziert
- Änderungen an Templates betreffen **alle Workflows** die sie nutzen
- Templates folgen der gleichen Tag-Konvention wie Workflows

---

## Erwartete Templates

### `retry-defaults.yaml`
Standard Retry-Policy: 3 Versuche, exponentielles Backoff ab 30s, Maximum 5 Minuten.

### `common-env.yaml`
Standard-Umgebungsvariablen die jeder Container bekommt: `CORRELATION_ID`, `LOG_LEVEL`, `INPUT_PATH`, `OUTPUT_PATH`, `DS_API_URL`, `DS_API_TOKEN`.

### `error-handler.yaml`
Standard Exit-Handler für fehlgeschlagene Steps: Strukturiertes Logging des Fehlers, Benachrichtigung (optional), Workflow-Status aktualisieren.

---

## Checkliste

- [ ] Template ist syntaktisch korrekt (`argo lint`)
- [ ] Template ist von mindestens einem Beispiel-Workflow referenziert
- [ ] Änderungsauswirkungen auf bestehende Workflows geprüft
