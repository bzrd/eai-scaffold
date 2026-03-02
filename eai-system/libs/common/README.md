# libs/common – Shared Utilities

Basis-Library. Keine Abhängigkeiten auf andere repo-interne Libraries.

## Struktur

```
common/
├── common/
│   ├── logging.py     # StructuredLogger → JSON nach stdout
│   ├── config.py      # Config-Dataclass aus Umgebungsvariablen
│   ├── provenance.py  # ProvenanceFragment → /tmp/provenance.json
│   ├── validation.py  # GUID-Format, Objekttyp, Version prüfen
│   └── constants.py   # EnvVars, ExitCode
└── tests/
```

## Konventionen

- Keine anderen repo-internen Abhängigkeiten
- Alle Funktionen zustandslos
- Normativ: `docs/contracts/logging-format.md` und `provenance-format.md`

## Checkliste

- [ ] Keine internen Imports
- [ ] Type Hints vollständig, `mypy --strict` grün
- [ ] Tests in `common/tests/`
