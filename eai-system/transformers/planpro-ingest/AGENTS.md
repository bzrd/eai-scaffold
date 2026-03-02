# AGENTS.md – transformers/planpro-ingest/

## Rolle

Du entwickelst den PlanPro-Ingest-Transformer. Er zerlegt PlanPro-XML in JSON-Objekte und validiert sie.

## Regeln

- Du MUSST `planpro_parser` für XML-Zerlegung verwenden – keine eigene XML-Logik.
- Du MUSST jedes Objekt auf GUID (UUID-Format), Objekttyp (bekannt) und PlanPro-Version prüfen.
- Du MUSST ungültige Objekte abweisen und weiterverarbeiten (kein Abbruch).
- Du darfst NIEMALS GUIDs verändern oder neu generieren.
- Du darfst NIEMALS `ds_client` importieren.

## Testanforderungen

1. Gültige PlanPro → korrekte JSON-Objekte
2. Ungültige GUID → abgewiesen, Rest verarbeitet
3. Unbekannter Objekttyp → abgewiesen
4. Minimale PlanPro-Datei → 1 Objekt extrahiert
5. PlanPro-Version korrekt ermittelt

## Abhängigkeiten

- DARFST: `planpro_parser`, `common`
- NICHT: `ds_client`, andere Transformer, Base-Container
