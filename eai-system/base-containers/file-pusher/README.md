# base-containers/file-pusher – Datei-Versand

## Zweck

Liefert Dateien an externe Systeme (HTTP-Upload, SFTP, Netzlaufwerke). Liest die zu versendende Datei von `INPUT_PATH` und überträgt sie an das Zielsystem.

---

## Struktur

```
file-pusher/
├── file_pusher/
│   ├── __init__.py
│   ├── main.py          # Standard-Entrypoint
│   └── handler.py       # Datei-Versand-Logik
├── tests/
│   ├── conftest.py
│   ├── test_handler.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- Input: Datei unter `INPUT_PATH` + Konfiguration über Umgebungsvariablen (Ziel-URL, Auth)
- Output: Keine lokale Datei – I/O geht an externes System
- Git-Tag: `base-file-pusher/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- `libs/common` – Logging, Config, Provenance
- `requests` oder `httpx` – HTTP-Client

---

## Checkliste

- [ ] Retry bei Netzwerkfehlern
- [ ] Auth über Umgebungsvariable
- [ ] Provenance-Fragment mit Ziel-URL
- [ ] Unit-Tests mit gemocktem HTTP
