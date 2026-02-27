# Contract: Container-Konvention

**Version:** 1.0
**Stand:** 2026-02-27
**Status:** Accepted

---

## Geltungsbereich

Gilt für **alle Container** im System: Transformer, Base-Container und den HTTP-Trigger (soweit anwendbar). Jeder Container MUSS diesen Vertrag einhalten.

---

## Definitionen

- **Container:** Ein Docker-Image das als Argo-Workflow-Step oder als Kubernetes Deployment ausgeführt wird.
- **Transformer:** Container mit ausschließlich Domänenlogik. Kein I/O außer INPUT_PATH/OUTPUT_PATH.
- **Base-Container:** Container mit I/O-Verantwortung (HTTP, Dateisystem, Datenbank).
- **Run-to-Completion:** Container startet, verarbeitet, beendet sich mit Exit-Code.
- **Long-Running:** Container läuft dauerhaft (nur http-trigger).

---

## Standard-Umgebungsvariablen

Jeder Container MUSS die folgenden Umgebungsvariablen akzeptieren:

| Variable | Beschreibung | Default | Pflicht |
|---|---|---|---|
| `CORRELATION_ID` | Eindeutige ID für den gesamten Workflow-Durchlauf | `""` | MUSS |
| `LOG_LEVEL` | Logging-Verbosity: DEBUG, INFO, WARNING, ERROR | `"INFO"` | MUSS |
| `INPUT_PATH` | Pfad zur Input-Datei/zum Input-Verzeichnis | `"/tmp/input"` | MUSS |
| `OUTPUT_PATH` | Pfad zur Output-Datei/zum Output-Verzeichnis | `"/tmp/output"` | MUSS |
| `DS_API_URL` | URL der Datenspeicher REST-API | `""` | NUR Base-Container |
| `DS_API_TOKEN` | Auth-Token für die Datenspeicher REST-API | `""` | NUR Base-Container |

### Anforderungen

1. Jeder Container MUSS `CORRELATION_ID` in allen Log-Einträgen mitführen.
2. Jeder Container MUSS `LOG_LEVEL` respektieren und die Logging-Verbosity entsprechend setzen.
3. Transformer DÜRFEN NICHT `DS_API_URL` oder `DS_API_TOKEN` verwenden.
4. Container DÜRFEN NICHT auf andere Umgebungsvariablen angewiesen sein, die nicht hier dokumentiert sind, ohne diese in der eigenen README.md zu dokumentieren.

---

## Input/Output-Konvention

### Anforderungen

5. Transformer MÜSSEN Input von `INPUT_PATH` lesen (Default: `/tmp/input`).
6. Transformer MÜSSEN Output nach `OUTPUT_PATH` schreiben (Default: `/tmp/output`).
7. Container DÜRFEN NICHT an andere Dateisystempfade schreiben, außer `/tmp/provenance.json` (siehe Provenance).
8. Base-Container DÜRFEN zusätzlich Netzwerk-I/O machen (HTTP, Datenbank).
9. Transformer DÜRFEN NICHT Netzwerk-I/O machen.

### Format

10. Input- und Output-Dateien MÜSSEN im JSON-Format sein, es sei denn die Domäne erfordert ein anderes Format (z.B. PlanPro-XML).
11. JSON-Dateien MÜSSEN UTF-8 kodiert sein.

---

## Exit-Codes

### Anforderungen

12. Jeder Run-to-Completion-Container MUSS einen der folgenden Exit-Codes verwenden:

| Exit-Code | Bedeutung | Beschreibung |
|---|---|---|
| `0` | Erfolg | Verarbeitung erfolgreich abgeschlossen |
| `1` | Fachlicher Fehler | Domänenfehler (z.B. ungültige GUID, unbekannter Objekttyp). Retry ist sinnlos. |
| `2` | Technischer Fehler | Infrastrukturfehler (z.B. Netzwerk-Timeout, Dateisystem-Fehler). Retry kann helfen. |

13. Container DÜRFEN NICHT andere Exit-Codes verwenden.
14. Bei Exit-Code 1 MUSS der Fehler strukturiert geloggt werden (siehe `logging-format.md`).
15. Bei Exit-Code 2 MUSS der Fehler strukturiert geloggt werden.

---

## Provenance

### Anforderungen

16. Jeder Container MUSS ein Provenance-Fragment als JSON-Datei unter `/tmp/provenance.json` ausgeben.
17. Das Provenance-Fragment MUSS dem Schema in `provenance-format.md` entsprechen.
18. Das Provenance-Fragment MUSS auch bei Fehlern (Exit-Code 1 oder 2) geschrieben werden, mit `error_info` befüllt.

---

## Beispiele

### Korrekt: Transformer

```bash
# Container startet mit:
CORRELATION_ID=workflow-123 LOG_LEVEL=INFO INPUT_PATH=/tmp/input OUTPUT_PATH=/tmp/output

# Container liest /tmp/input, verarbeitet, schreibt /tmp/output und /tmp/provenance.json
# Exit-Code: 0
```

### Inkorrekt: Transformer mit HTTP-Call

```python
# FALSCH: Transformer darf kein HTTP machen
import requests
data = requests.get("https://api.example.com/data")  # VERBOTEN in Transformern
```

### Inkorrekt: Falscher Exit-Code

```python
# FALSCH: Exit-Code 42 ist nicht definiert
sys.exit(42)  # VERBOTEN – nur 0, 1 oder 2
```
