# tests/integration/ – Integrationstests

## Zweck

Integrationstests die mehrere Komponenten zusammen testen. Laufen gegen die echte REST-API in der Dev-Umgebung, nicht gegen Mocks.

---

## Struktur

```
integration/
├── conftest.py                    # Shared Fixtures (API-Client, Test-Scope, Cleanup)
├── test_import_workflow.py        # End-to-End Import: XML → Ingest → Store → Read
├── test_export_workflow.py        # End-to-End Export: Read → Export → XML
├── test_diff_workflow.py          # End-to-End Diff: Read → Read → Diff → Verify
├── test_roundtrip.py             # Roundtrip: Import → Export → Vergleich
├── README.md
└── AGENTS.md
```

---

## Konventionen

- **Laufen NICHT in der CI bei jedem Commit** – manuell oder als Nightly-Job
- **Benötigen eine laufende Dev-Umgebung** mit Datenspeicher-API
- **Testen die echte API** – keine Mocks
- **Testdaten vor dem Test anlegen, nach dem Test aufräumen**
- **Eigener Test-Scope** im Datenspeicher (nicht den Hauptdatenbestand anfassen)
- Umgebungsvariablen: `DS_API_URL`, `DS_API_TOKEN` müssen gesetzt sein

---

## Abhängigkeiten

- Laufende Dev-Umgebung mit Datenspeicher-API
- `libs/ds-client` für API-Zugriff
- Fixtures aus `tests/fixtures/`

---

## Ausführung

```bash
# Voraussetzung: Dev-Umgebung läuft, Env-Vars gesetzt
export DS_API_URL=https://dev.ds.intern/api
export DS_API_TOKEN=dev-token

make test-integration
# oder direkt:
pytest -m integration tests/integration/ -v
```

---

## Checkliste

- [ ] `@pytest.mark.integration` auf allen Tests
- [ ] Testdaten werden vor dem Test angelegt
- [ ] Testdaten werden nach dem Test aufgeräumt (auch bei Fehler)
- [ ] Eigener Test-Scope verwendet
- [ ] Keine Mocks – echte API
