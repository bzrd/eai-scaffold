# base-containers/ds-reader – Datenspeicher-Leser

## Zweck

Liest JSON-Objekte aus dem Datenspeicher (FIN) über die REST-API und legt sie unter `OUTPUT_PATH` ab. Nutzt `libs/ds-client` für die API-Kommunikation.

---

## Struktur

```
ds-reader/
├── ds_reader/
│   ├── __init__.py
│   ├── main.py          # Standard-Entrypoint
│   └── handler.py       # Lese-Logik mit ds-client
├── tests/
│   ├── conftest.py
│   ├── test_handler.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- Input: Konfiguration über Umgebungsvariablen (GUIDs, Scope, Phase)
- Output: JSON-Datei mit gelesenen Objekten unter `OUTPUT_PATH`
- Nutzt ausschließlich `libs/ds-client` für API-Zugriff
- Git-Tag: `base-ds-reader/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- `libs/common` – Logging, Config, Provenance
- `libs/ds-client` – REST-API-Client

---

## Checkliste

- [ ] Nutzt `ds_client` für alle API-Zugriffe
- [ ] GUIDs, Scope und Phase korrekt übergeben
- [ ] Gelesene Objekte als JSON unter `OUTPUT_PATH`
- [ ] Provenance-Fragment mit gelesenen GUIDs
- [ ] Fehlerbehandlung für API-Fehler (Not Found, Auth)
- [ ] Unit-Tests mit gemocktem `ds_client`
