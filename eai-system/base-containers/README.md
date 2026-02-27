# base-containers/ – I/O-Container

## Zweck

Dieser Ordner enthält alle Base-Container. Base-Container sind die einzige Schicht die I/O macht: HTTP-Calls gegen externe Systeme, REST-API-Zugriffe auf den Datenspeicher (FIN), Dateisystem-Operationen gegen externe Quellen. Sie sind die Brücke zwischen der Außenwelt und den Transformern.

---

## Struktur

```
base-containers/
├── file-fetcher/      # Holt Dateien von externen Systemen
├── file-pusher/       # Liefert Dateien an externe Systeme
├── http-trigger/      # Long-Running FastAPI-Service für Webhooks → Argo-Workflows
├── ds-writer/         # Schreibt JSON-Objekte in den Datenspeicher (FIN)
├── ds-reader/         # Liest JSON-Objekte aus dem Datenspeicher (FIN)
├── _template/         # Kopiervorlage für neue Base-Container
├── README.md          # Diese Datei
└── AGENTS.md          # Anweisungen für AI-Agenten
```

Jeder Base-Container hat folgende innere Struktur:

```
<container-name>/
├── <container_name>/
│   ├── __init__.py
│   ├── main.py          # Entrypoint
│   └── handler.py       # I/O-Logik
├── tests/
│   ├── conftest.py
│   ├── test_handler.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- **Ordnername:** `kebab-case` (z.B. `file-fetcher`)
- **Python-Package:** `snake_case` (z.B. `file_fetcher`)
- **Git-Tag:** `base-<name>/v<major>.<minor>.<patch>` (z.B. `base-file-fetcher/v1.0.0`)
- **Container-Image:** `registry.intern/base-<name>:<version>`
- **I/O ist erlaubt und erwartet** – anders als Transformer
- **Provenance-Fragment ist Pflicht** auch für Base-Container

---

## Abhängigkeiten

Base-Container dürfen importieren:
- `libs/common` (Logging, Config, Provenance)
- `libs/ds-client` (nur `ds-writer` und `ds-reader`)
- `requests`, `httpx`, `aiohttp` (für HTTP-I/O)

Base-Container dürfen **NICHT** importieren:
- `libs/planpro-parser` (Domänenlogik gehört in Transformer)
- Andere Base-Container
- Transformer

---

## Beispiel: Neuen Base-Container anlegen

1. `cp -r base-containers/_template base-containers/mein-container`
2. Package umbenennen
3. `handler.py` mit I/O-Logik implementieren
4. Tests schreiben (mit HTTP-Mocking)
5. README anpassen

---

## Checkliste für neue Base-Container

- [ ] `main.py` folgt Standard-Entrypoint-Pattern
- [ ] I/O-Logik in `handler.py` isoliert
- [ ] Structured JSON Logging über `common.logging`
- [ ] Provenance-Fragment wird erzeugt
- [ ] Fehlerbehandlung mit korrekten Exit-Codes (0/1/2)
- [ ] Unit-Tests mit gemocktem I/O
- [ ] Alle Type Hints vollständig
- [ ] `mypy --strict` grün
- [ ] README beschreibt Input/Output und Konfiguration
