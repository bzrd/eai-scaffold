# Contract: Logging-Format

**Version:** 1.0
**Stand:** 2026-02-27
**Status:** Accepted

---

## Geltungsbereich

Gilt für **alle Komponenten** im System: Transformer, Base-Container, Libraries. Jede Log-Ausgabe MUSS diesem Format entsprechen.

---

## Definitionen

- **Log-Eintrag:** Eine einzelne Zeile auf stdout die ein JSON-Objekt enthält.
- **Pflichtfeld:** MUSS in jedem Log-Eintrag vorhanden sein.
- **Optionales Feld:** KANN vorhanden sein wenn die Information verfügbar ist.

---

## JSON-Log-Schema

### Pflichtfelder

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| `timestamp` | string (ISO 8601) | Zeitpunkt des Log-Eintrags in UTC | `"2026-02-27T14:30:00.123Z"` |
| `level` | string (Enum) | Log-Level | `"INFO"`, `"ERROR"`, `"WARNING"`, `"DEBUG"` |
| `message` | string | Menschenlesbare Nachricht | `"Verarbeitung gestartet"` |
| `correlation_id` | string | Workflow-Korrelations-ID | `"workflow-abc-123"` |
| `component` | string | Name der Komponente | `"transformer-ingest"` |

### Optionale Felder

| Feld | Typ | Beschreibung | Beispiel |
|---|---|---|---|
| `object_id` | string | GUID des betroffenen Objekts | `"12345678-1234-..."` |
| `planpro_version` | string | PlanPro-Version | `"1.10"` |
| `error_type` | string | Fehlerklasse | `"GUIDValidationError"` |
| `duration_ms` | number | Dauer der Operation in Millisekunden | `1234` |
| `object_count` | number | Anzahl verarbeiteter Objekte | `42` |
| `scope` | string | Datenspeicher-Scope | `"projekt-abc"` |
| `phase` | string | Datenspeicher-Phase | `"planung"` |

---

## Anforderungen

1. Jeder Log-Eintrag MUSS ein vollständiges JSON-Objekt auf einer einzigen Zeile sein.
2. Log-Einträge DÜRFEN NICHT über mehrere Zeilen gehen (kein Multi-Line-Logging).
3. Alle Logs MÜSSEN nach `stdout` geschrieben werden, NIEMALS in Dateien.
4. Alle Pflichtfelder MÜSSEN in jedem Log-Eintrag vorhanden sein.
5. `timestamp` MUSS in UTC sein (ISO 8601 Format mit Zeitzone).
6. `level` MUSS einer der Werte `DEBUG`, `INFO`, `WARNING`, `ERROR` sein.
7. Alle Komponenten MÜSSEN `common.logging` verwenden – keine eigenen Logging-Implementierungen.
8. `print()` DARF NICHT für Logging verwendet werden.
9. Python `logging.basicConfig()` DARF NICHT verwendet werden.
10. Stack-Traces MÜSSEN als einzelner String im `message`- oder `error_type`-Feld kodiert werden (Newlines escaped), NICHT als separate Zeilen.

---

## Beispiele

### Korrekt: Standard-Log-Eintrag

```json
{"timestamp": "2026-02-27T14:30:00.123Z", "level": "INFO", "message": "Verarbeitung gestartet", "correlation_id": "wf-abc-123", "component": "transformer-ingest"}
```

### Korrekt: Fehler-Log-Eintrag

```json
{"timestamp": "2026-02-27T14:30:01.456Z", "level": "ERROR", "message": "Ungültige GUID gefunden", "correlation_id": "wf-abc-123", "component": "transformer-ingest", "object_id": "not-a-valid-guid", "error_type": "GUIDValidationError"}
```

### Korrekt: Performance-Log

```json
{"timestamp": "2026-02-27T14:30:05.789Z", "level": "INFO", "message": "Transformation abgeschlossen", "correlation_id": "wf-abc-123", "component": "transformer-ingest", "object_count": 42, "duration_ms": 1234}
```

### Inkorrekt: Multi-Line

```
ERROR: Something went wrong
Traceback (most recent call last):
  File "main.py", line 10, in <module>
    ...
```

### Inkorrekt: print()

```python
print("Verarbeitung gestartet")  # VERBOTEN
```
