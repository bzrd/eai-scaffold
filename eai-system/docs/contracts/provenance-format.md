# Contract: Provenance-Fragment-Format

**Version:** 1.0
**Stand:** 2026-02-27
**Status:** Accepted

---

## Geltungsbereich

Gilt für **alle Container** (Transformer und Base-Container). Jeder Container MUSS ein Provenance-Fragment erzeugen.

---

## Definitionen

- **Provenance-Fragment:** Ein JSON-Dokument das dokumentiert wer, wann, mit welchen Inputs welche Outputs erzeugt hat.
- **Data Provenance:** Die vollständige Nachvollziehbarkeit der Herkunft und Verarbeitung von Daten – regulatorische Anforderung im Bereich kritischer Bahninfrastruktur.

---

## JSON-Schema

### Pflichtfelder

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| `transformer_name` | string | Name des Containers (auch für Base-Container) | `"transformer-ingest"` |
| `transformer_version` | string | Semantische Version des Containers | `"v1.2.3"` |
| `timestamp` | string (ISO 8601) | Zeitpunkt der Verarbeitung in UTC | `"2026-02-27T14:30:00.123Z"` |
| `correlation_id` | string | Workflow-Korrelations-ID | `"wf-abc-123"` |
| `input_refs` | array[string] | Liste von Objekt-GUIDs die als Input verwendet wurden | `["guid-1", "guid-2"]` |
| `output_refs` | array[string] | Liste von Objekt-GUIDs die als Output erzeugt wurden | `["guid-1", "guid-2", "guid-3"]` |

### Optionale Felder

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| `planpro_version` | string | PlanPro-Version der verarbeiteten Daten | `"1.10"` |
| `scope` | string | Datenspeicher-Scope | `"projekt-abc"` |
| `phase` | string | Datenspeicher-Phase | `"planung"` |
| `error_info` | string | Fehlerbeschreibung (bei Exit-Code 1 oder 2) | `"GUIDValidationError: ..."` |

---

## Anforderungen

1. Jeder Container MUSS ein Provenance-Fragment als JSON-Datei unter `/tmp/provenance.json` erzeugen.
2. Alle Pflichtfelder MÜSSEN vorhanden sein.
3. `timestamp` MUSS in UTC sein (ISO 8601 Format).
4. `input_refs` und `output_refs` MÜSSEN gültige GUIDs im UUID-Format enthalten.
5. `transformer_version` MUSS die semantische Version des Container-Images sein (Format: `v<major>.<minor>.<patch>`).
6. Bei Fehlern (Exit-Code 1 oder 2) MUSS `error_info` befüllt werden.
7. Bei Fehlern MÜSSEN `input_refs` und `output_refs` so weit wie möglich befüllt werden (auch wenn unvollständig).
8. Das Provenance-Fragment MUSS auch dann geschrieben werden, wenn die Verarbeitung fehlschlägt.
9. Alle Container MÜSSEN `common.provenance` verwenden – keine eigene Provenance-Implementierung.

---

## Beispiele

### Korrekt: Erfolgreiche Verarbeitung

```json
{
  "transformer_name": "transformer-ingest",
  "transformer_version": "v1.2.3",
  "timestamp": "2026-02-27T14:30:00.123Z",
  "correlation_id": "wf-abc-123",
  "input_refs": [
    "12345678-1234-1234-1234-123456789012"
  ],
  "output_refs": [
    "12345678-1234-1234-1234-123456789012",
    "87654321-4321-4321-4321-210987654321"
  ],
  "planpro_version": "1.10",
  "scope": "projekt-abc",
  "phase": "planung"
}
```

### Korrekt: Fehlerfall

```json
{
  "transformer_name": "transformer-ingest",
  "transformer_version": "v1.2.3",
  "timestamp": "2026-02-27T14:30:00.123Z",
  "correlation_id": "wf-abc-123",
  "input_refs": [],
  "output_refs": [],
  "error_info": "PlanProParseError: XML-Struktur ungültig, Root-Element fehlt"
}
```

### Inkorrekt: Fehlende Pflichtfelder

```json
{
  "transformer_name": "transformer-ingest",
  "timestamp": "2026-02-27T14:30:00.123Z"
}
```
*Fehlt: `transformer_version`, `correlation_id`, `input_refs`, `output_refs`*
