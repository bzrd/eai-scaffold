# transformers/planpro-ingest – PlanPro XML Import-Transformer

Zerlegt PlanPro-XML in plain-dict JSON-Objekte. Validiert GUID, Objekttyp und PlanPro-Version. Abgewiesene Objekte werden geloggt, Import läuft weiter.

## Struktur

```
planpro-ingest/
├── main.py          # Entrypoint (Config, Logging, I/O-Pfade, Provenance)
├── convert.py       # XML→JSON Konvertierung (reine Funktion, kein I/O)
├── tests/
│   ├── test_convert.py
│   └── fixtures/
│       ├── sample_1.9.xml
│       ├── sample_1.10.xml
│       └── expected_output.json
├── pyproject.toml
└── README.md
```

## I/O

- Input: PlanPro-XML unter `INPUT_PATH`
- Output: `{"planpro_version": "1.10", "objects": [{...}, ...]}` unter `OUTPUT_PATH`
- Objekte sind plain dicts – keine Dataclasses, keine TypedDicts
- Git-Tag: `transformer-ingest/v<major>.<minor>.<patch>`

## Checkliste

- [ ] XML-Logik ausschließlich in `convert.py`
- [ ] Objekte als plain dicts (keine Dataclasses)
- [ ] Mindest-Validierung (GUID, Objekttyp, Version) pro Objekt
- [ ] Ungültige Objekte abweisen, nicht abbrechen
- [ ] Provenance-Fragment erzeugt
- [ ] Fixtures aus echten/echt-nahen PlanPro-Daten
