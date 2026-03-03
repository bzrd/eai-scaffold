# libs/ – Shared Libraries

Repo-interne Python-Libraries. Direkt per Import eingebunden (HEAD-Prinzip, kein Versions-Pinning).

## Struktur

```
libs/
├── ds-client/  # REST-Client für den Datenspeicher (FIN)
└── common/     # Logging, Provenance, Config, Validierung (Basis)
```

`planpro-parser` existiert nicht mehr. XML-Parsing lebt in `transformers/planpro-ingest/convert.py`.

## Abhängigkeitshierarchie

```
common  ←  ds-client
```

## Konventionen

- Ordner: `kebab-case`, Package: `snake_case`
- Git-Tag: `lib-<name>/v<major>.<minor>.<patch>`
- `pip install -e libs/<name>` muss funktionieren

## Checkliste für neue Libraries

- [ ] Eigene `pyproject.toml`
- [ ] Tests in `libs/<name>/tests/`
- [ ] `mypy --strict` grün
- [ ] Abhängigkeitshierarchie eingehalten
