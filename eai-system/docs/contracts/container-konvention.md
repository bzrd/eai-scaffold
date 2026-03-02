# Contract: Container-Konvention

**Version:** 1.0 | **Status:** Accepted

Gilt für alle Container. Jeder Container MUSS diesen Vertrag einhalten.

## Umgebungsvariablen

| Variable | Default | Pflicht |
|---|---|---|
| `CORRELATION_ID` | `""` | alle |
| `LOG_LEVEL` | `"INFO"` | alle |
| `INPUT_PATH` | `"/tmp/input"` | alle |
| `OUTPUT_PATH` | `"/tmp/output"` | alle |
| `DS_API_URL` | `""` | nur Base-Container |
| `DS_API_TOKEN` | `""` | nur Base-Container |

## Anforderungen

1. Jeder Container MUSS `CORRELATION_ID` in allen Log-Einträgen mitführen.
2. Jeder Container MUSS `LOG_LEVEL` respektieren.
3. Transformer DÜRFEN NICHT `DS_API_URL`/`DS_API_TOKEN` verwenden.
4. Zusätzliche Env-Vars MÜSSEN in der Komponenten-README dokumentiert werden.

## I/O

5. Transformer MÜSSEN Input von `INPUT_PATH` lesen.
6. Transformer MÜSSEN Output nach `OUTPUT_PATH` schreiben.
7. Container DÜRFEN NICHT an andere Pfade schreiben außer `/tmp/provenance.json`.
8. Base-Container DÜRFEN zusätzlich Netzwerk-I/O machen.
9. Transformer DÜRFEN NICHT Netzwerk-I/O machen.
10. JSON-Dateien MÜSSEN UTF-8 sein.

## Exit-Codes

| Code | Bedeutung |
|---|---|
| `0` | Erfolg |
| `1` | Fachlicher Fehler (kein Retry sinnvoll) |
| `2` | Technischer Fehler (Retry kann helfen) |

11. Nur Exit-Codes 0, 1, 2 erlaubt.
12. Bei Exit-Code 1 und 2 MUSS strukturiert geloggt werden.

## Provenance

13. Jeder Container MUSS `/tmp/provenance.json` schreiben (Schema: `provenance-format.md`).
14. Provenance MUSS auch bei Fehlern geschrieben werden.
