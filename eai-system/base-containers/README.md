# base-containers/ – I/O-Container

Base-Container sind die einzige I/O-Schicht: HTTP-Calls, Datenbankzugriffe, externe Dateioperationen.

## Struktur

```
base-containers/
├── file-fetcher/   # Holt Dateien von externen Systemen
├── file-pusher/    # Liefert Dateien an externe Systeme
├── http-trigger/   # Long-Running FastAPI-Service für Webhooks → Argo
├── ds-writer/      # Schreibt JSON-Objekte in den Datenspeicher (FIN)
├── ds-reader/      # Liest JSON-Objekte aus dem Datenspeicher (FIN)
└── _template/      # Kopiervorlage
```

## Konventionen

- Ordner: `kebab-case`, Package: `snake_case`
- I/O-Logik in `handler.py`, Entrypoint in `main.py`
- Git-Tag: `base-<name>/v<major>.<minor>.<patch>`
- Provenance-Fragment Pflicht

## Abhängigkeiten

- DARFST: `common`, `ds_client` (nur ds-writer/ds-reader), `requests`/`httpx`
- NICHT: `planpro_parser`, andere Base-Container, Transformer

## Checkliste

- [ ] I/O in `handler.py` isoliert
- [ ] Retry für transiente Fehler
- [ ] `common.logging`, Provenance-Fragment
- [ ] Unit-Tests mit gemocktem I/O
