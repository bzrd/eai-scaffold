# transformers/planpro-ingest – PlanPro XML Import-Transformer

Zerlegt PlanPro-XML in typisierte JSON-Objekte. Validiert GUID, Objekttyp und PlanPro-Version. Abgewiesene Objekte werden geloggt, Import läuft weiter.

## I/O

- Input: PlanPro-XML unter `INPUT_PATH`
- Output: `{"planpro_version": ..., "objects": [...]}` unter `OUTPUT_PATH`
- Git-Tag: `transformer-ingest/v<major>.<minor>.<patch>`

## Checkliste

- [ ] Nutzt `planpro_parser.parse_xml()`
- [ ] Mindest-Validierung (GUID, Objekttyp, Version) pro Objekt
- [ ] Ungültige Objekte abweisen, nicht abbrechen
- [ ] Provenance-Fragment erzeugt
