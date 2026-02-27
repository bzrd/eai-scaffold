# libs/ – Shared Libraries

Dieser Ordner enthält alle repo-internen Python-Libraries, die von Transformern und Base-Containern gemeinsam genutzt werden.

## Zweck

Libraries kapseln geteilte Domänenlogik und Infrastruktur-Utilities. Sie werden **nicht** über PyPI oder einen internen Package-Server veröffentlicht, sondern direkt per Python-Import eingebunden (HEAD-Prinzip: kein Versions-Pinning, immer der aktuelle Stand).

## Struktur

```
libs/
├── planpro-parser/    # PlanPro XML → JSON Zerlegung + Referenzextraktion
├── ds-client/         # Typisierter REST-Client für den Datenspeicher (FIN)
└── common/            # Logging, Provenance, Config, Validierung (Basis-Schicht)
```

## Konventionen

- Jede Library ist ein eigenständiges Python-Package mit eigener `pyproject.toml`
- Python-Packagename: `snake_case` (z.B. `planpro_parser`, `ds_client`, `common`)
- Ordnername: `kebab-case` (z.B. `planpro-parser`, `ds-client`)
- Jede Library muss eine `tests/`-Unterordner haben
- Jede Library muss mit `pip install -e libs/<name>` installierbar sein
- CI-Tag-Format: `lib-<name>/v<major>.<minor>.<patch>`

## Abhängigkeiten zwischen Libraries

```
common          (keine Abhängigkeiten auf andere repo-interne Libraries)
    ▲
    │
planpro-parser  (darf nur common importieren)
    │
ds-client       (darf nur common importieren)
```

`common` ist die unterste Schicht. `planpro-parser` und `ds-client` sind unabhängig voneinander und dürfen sich **nicht** gegenseitig importieren.

## Beispiel: Neue Library anlegen

```
libs/
└── neue-library/
    ├── neue_library/
    │   ├── __init__.py
    │   └── core.py
    ├── tests/
    │   └── test_core.py
    ├── pyproject.toml
    └── README.md
```

`pyproject.toml` Minimalstruktur:
```toml
[project]
name = "neue-library"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["common"]  # falls benötigt

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Checkliste für neue Libraries

- [ ] Eigene `pyproject.toml` vorhanden
- [ ] `pip install -e libs/<name>` funktioniert
- [ ] Tests in `tests/` vorhanden
- [ ] Alle Funktionen mit Type Hints annotiert
- [ ] `mypy --strict` läuft ohne Fehler
- [ ] `README.md` beschreibt Zweck, API und Beispiele
- [ ] `AGENTS.md` beschreibt erlaubte Imports und Antipatterns
- [ ] Abhängigkeitshierarchie eingehalten (`common` importiert nichts intern)
