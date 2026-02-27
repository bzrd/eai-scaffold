# tests/ – Geteilte Tests und Fixtures

## Zweck

Dieser Ordner enthält Integrationstests die mehrere Komponenten zusammen testen und geteilte Fixtures die von mehreren Komponenten genutzt werden.

---

## Struktur

```
tests/
├── integration/       # Integrationstests gegen die echte REST-API
├── fixtures/          # Geteilte Testdaten (PlanPro-Dateien, JSON-Outputs, Diff-Reports)
├── README.md
└── AGENTS.md
```

---

## Konventionen

- **Integrationstests** laufen nicht bei jedem Commit, sondern manuell oder als Nightly-Job
- **Unit-Tests** liegen in den jeweiligen Komponenten-Ordnern (`libs/<name>/tests/`, `transformers/<name>/tests/`)
- **Fixtures** werden geteilt und niemals synthetisch generiert
- pytest Marker: `@pytest.mark.unit`, `@pytest.mark.integration`

---

## Abhängigkeiten

- Integrationstests benötigen eine laufende Dev-Umgebung
- Fixtures werden von Komponenten-Tests referenziert

---

## Checkliste

- [ ] Tests mit korrektem Marker (`unit` oder `integration`)
- [ ] Integrationstests räumen Testdaten auf
- [ ] Fixtures sind echte oder echt-nahe PlanPro-Daten
