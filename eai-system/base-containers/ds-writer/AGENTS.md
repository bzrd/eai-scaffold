# AGENTS.md – base-containers/ds-writer/

## Rolle

Du entwickelst den DS-Writer. Er schreibt JSON-Objekte aus `INPUT_PATH` über `ds_client` in den Datenspeicher.

## Regeln

- Du MUSST `ds_client` verwenden – keine direkten HTTP-Calls gegen die FIN-API.
- Du MUSST Scope und Phase aus Umgebungsvariablen lesen.
- Du MUSST Provenance mit geschriebenen GUIDs erzeugen.
- Du darfst NIEMALS `planpro_parser` importieren.

## Testanforderungen

1. Erfolgreicher Write → GUIDs im Provenance
2. API-Fehler → korrekte Exception und Exit-Code

## Abhängigkeiten

- DARFST: `common`, `ds_client`
- NICHT: `planpro_parser`, andere Container
