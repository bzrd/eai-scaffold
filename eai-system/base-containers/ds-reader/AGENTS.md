# AGENTS.md – base-containers/ds-reader/

## Rolle

Du entwickelst den DS-Reader. Er liest JSON-Objekte aus dem Datenspeicher über `ds_client` und legt sie unter `OUTPUT_PATH` ab.

## Regeln

- Du MUSST `ds_client` für alle API-Zugriffe verwenden.
- Du MUSST gelesene Objekte als JSON unter `OUTPUT_PATH` ablegen.
- Du MUSST Provenance mit gelesenen GUIDs erzeugen.
- Du darfst NIEMALS `planpro_parser` importieren.

## Testanforderungen

1. Erfolgreicher Read → JSON unter `OUTPUT_PATH`
2. API 404 → DsNotFoundError
3. Leere Ergebnisliste → leere JSON-Datei

## Abhängigkeiten

- DARFST: `common`, `ds_client`
- NICHT: `planpro_parser`, andere Container
