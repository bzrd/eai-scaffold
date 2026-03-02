# Contract: Provenance-Fragment-Format

**Version:** 1.0 | **Status:** Accepted

Gilt für alle Container. Data Provenance ist regulatorische Anforderung.

## JSON-Schema

### Pflichtfelder

| Feld | Typ | Beispiel |
|---|---|---|
| `transformer_name` | string | `"transformer-ingest"` |
| `transformer_version` | string | `"v1.2.3"` |
| `timestamp` | ISO 8601 UTC | `"2026-02-27T14:30:00.123Z"` |
| `correlation_id` | string | `"wf-abc-123"` |
| `input_refs` | array[string] | `["guid-1"]` |
| `output_refs` | array[string] | `["guid-1", "guid-2"]` |

### Optionale Felder

`planpro_version`, `scope`, `phase`, `error_info`

## Anforderungen

1. Jeder Container MUSS `/tmp/provenance.json` erzeugen.
2. Alle Pflichtfelder MÜSSEN vorhanden sein.
3. `timestamp` MUSS in UTC sein.
4. `input_refs` und `output_refs` MÜSSEN gültige UUIDs enthalten.
5. `transformer_version` MUSS `v<major>.<minor>.<patch>` sein.
6. Bei Fehlern (Exit-Code 1/2) MUSS `error_info` befüllt werden.
7. Provenance MUSS auch bei Fehlern geschrieben werden.
8. Alle Container MÜSSEN `common.provenance` verwenden.
