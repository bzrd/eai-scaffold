# Contract: Logging-Format

**Version:** 1.0 | **Status:** Accepted

Gilt für alle Komponenten. Jede Log-Ausgabe MUSS diesem Format entsprechen.

## JSON-Log-Schema

### Pflichtfelder

| Feld | Typ | Beispiel |
|---|---|---|
| `timestamp` | ISO 8601 UTC | `"2026-02-27T14:30:00.123Z"` |
| `level` | `DEBUG`/`INFO`/`WARNING`/`ERROR` | `"INFO"` |
| `message` | string | `"Verarbeitung gestartet"` |
| `correlation_id` | string | `"wf-abc-123"` |
| `component` | string | `"transformer-ingest"` |

### Optionale Felder

`object_id`, `planpro_version`, `error_type`, `duration_ms`, `object_count`, `scope`, `phase`

## Anforderungen

1. Jeder Log-Eintrag MUSS ein vollständiges JSON-Objekt auf einer Zeile sein.
2. Kein Multi-Line-Logging.
3. Alle Logs nach `stdout`.
4. Alle Pflichtfelder MÜSSEN vorhanden sein.
5. `timestamp` in UTC (ISO 8601).
6. Alle Komponenten MÜSSEN `common.logging` verwenden.
7. Kein `print()`, kein `logging.basicConfig()`.
8. Stack-Traces als Single-String kodieren (Newlines escaped).
