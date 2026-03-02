# transformers/ – Domänenlogik-Container

Transformer enthalten ausschließlich Domänenlogik. Kein I/O, kein HTTP, kein DB außer `INPUT_PATH`/`OUTPUT_PATH`.

## Struktur

```
transformers/
├── planpro-ingest/  # PlanPro-XML → JSON-Objekte
├── planpro-export/  # JSON-Objekte → PlanPro-XML
├── diff/            # Zwei Stände → Diff-Report
└── _template/       # Kopiervorlage
```

Jeder Transformer:
```
<name>/
├── <name_snake>/
│   ├── main.py      # Entrypoint (Config, I/O, Provenance)
│   └── transform.py # Reine Domänenlogik
├── tests/
├── pyproject.toml
└── README.md
```

## Konventionen

- Ordner: `kebab-case`, Package: `snake_case`
- Git-Tag: `transformer-<name>/v<major>.<minor>.<patch>`
- Exit-Codes: 0 = OK, 1 = Fachfehler, 2 = Technikfehler

## Checkliste

- [ ] Domänenlogik nur in `transform.py`
- [ ] `main.py` folgt Standard-Entrypoint
- [ ] Kein I/O in `transform.py`
- [ ] Provenance-Fragment erzeugt
- [ ] `mypy --strict` grün
