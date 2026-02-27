# base-containers/ds-writer – Datenspeicher-Schreiber

## Zweck

Schreibt JSON-Objekte in den Datenspeicher (FIN) über die REST-API. Nutzt `libs/ds-client` für die API-Kommunikation. Liest die zu schreibenden Objekte von `INPUT_PATH`.

---

## Struktur

```
ds-writer/
├── ds_writer/
│   ├── __init__.py
│   ├── main.py          # Standard-Entrypoint
│   └── handler.py       # Schreib-Logik mit ds-client
├── tests/
│   ├── conftest.py
│   ├── test_handler.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- Input: JSON-Datei unter `INPUT_PATH` mit Objektliste
- Output: Keine lokale Datei – Objekte werden in den Datenspeicher geschrieben
- Nutzt ausschließlich `libs/ds-client` für API-Zugriff
- Scope und Phase über Umgebungsvariablen konfiguriert
- Git-Tag: `base-ds-writer/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- `libs/common` – Logging, Config, Provenance
- `libs/ds-client` – REST-API-Client

---

## Checkliste

- [ ] Nutzt `ds_client` für alle API-Zugriffe
- [ ] Scope und Phase korrekt übergeben
- [ ] Provenance-Fragment mit geschriebenen GUIDs
- [ ] Fehlerbehandlung für API-Fehler
- [ ] Unit-Tests mit gemocktem `ds_client`
