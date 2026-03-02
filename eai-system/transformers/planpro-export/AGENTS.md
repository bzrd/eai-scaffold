# AGENTS.md – transformers/planpro-export/

## Rolle

Du entwickelst den PlanPro-Export-Transformer. Er assembliert JSON-Objekte zu validem PlanPro-XML.

## Regeln

- Du MUSST `planpro_parser` für XML-Erzeugung verwenden – keine manuelle XML-Konkatenation.
- Du MUSST GUIDs exakt aus dem Input übernehmen.
- Du MUSST valides PlanPro der angegebenen Version erzeugen.
- Du darfst NIEMALS `ds_client` importieren.

## Testanforderungen

1. Gültige Objektliste → valides PlanPro-XML
2. GUIDs im Output exakt wie im Input
3. PlanPro-Version korrekt im XML-Header
4. **Roundtrip-Test Pflicht:** Ingest → Export → semantisch äquivalentes XML
5. Leere Objektliste → minimales gültiges PlanPro-XML

## Abhängigkeiten

- DARFST: `planpro_parser`, `common`
- NICHT: `ds_client`, andere Transformer, Base-Container
