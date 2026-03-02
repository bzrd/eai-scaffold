# AGENTS.md – base-containers/file-fetcher/

## Rolle

Du entwickelst den File-Fetcher. Er holt Dateien von externen Systemen und legt sie unter `OUTPUT_PATH` ab.

## Regeln

- Du MUSST Retry (3 Versuche, exponentiell ab 2s) implementieren.
- Du MUSST Auth aus Umgebungsvariablen lesen.
- Du MUSST die Datei unter `OUTPUT_PATH` ablegen.
- Du darfst NIEMALS Domänenlogik oder `planpro_parser` einbauen.

## Testanforderungen

1. Erfolgreicher Download → Datei unter `OUTPUT_PATH`
2. HTTP 500 → Retry → Erfolg
3. HTTP 401 → Auth-Fehler, kein Retry

## Abhängigkeiten

- DARFST: `common`, `requests`/`httpx`
- NICHT: `planpro_parser`, `ds_client`, andere Container
