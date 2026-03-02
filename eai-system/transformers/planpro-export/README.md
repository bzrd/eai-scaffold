# transformers/planpro-export – PlanPro XML Export-Transformer

Assembliert JSON-Objekte zurück zu einer validen PlanPro-XML-Datei. Inverse Operation zum `planpro-ingest`.

## I/O

- Input: `{"planpro_version": ..., "objects": [...]}` unter `INPUT_PATH`
- Output: PlanPro-XML-Datei unter `OUTPUT_PATH`
- Git-Tag: `transformer-export/v<major>.<minor>.<patch>`

## Checkliste

- [ ] XML-Output valides PlanPro der angegebenen Version
- [ ] GUIDs exakt aus Input übernommen
- [ ] Roundtrip-Test (Ingest → Export → Vergleich)
- [ ] Provenance-Fragment erzeugt
