# base-containers/file-fetcher – Datei-Abruf

## Zweck

Holt Dateien von externen Systemen (HTTP-Endpoints, SFTP, Netzlaufwerke) und legt sie unter `OUTPUT_PATH` ab, damit der nachfolgende Transformer sie verarbeiten kann.

---

## Struktur

```
file-fetcher/
├── file_fetcher/
│   ├── __init__.py
│   ├── main.py          # Standard-Entrypoint
│   └── handler.py       # Datei-Abruf-Logik (HTTP, SFTP, etc.)
├── tests/
│   ├── conftest.py
│   ├── test_handler.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- Input: Konfiguration über Umgebungsvariablen (Quell-URL, Auth-Token, Protokoll)
- Output: Abgerufene Datei unter `OUTPUT_PATH`
- Retry bei Netzwerkfehlern (3 Versuche, exponentielles Backoff)
- Git-Tag: `base-file-fetcher/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- `libs/common` – Logging, Config, Provenance
- `requests` oder `httpx` – HTTP-Client

---

## Checkliste

- [ ] Netzwerkfehler mit Retry behandelt
- [ ] Auth-Token über Umgebungsvariable
- [ ] Provenance-Fragment erzeugt
- [ ] Unit-Tests mit gemocktem HTTP
