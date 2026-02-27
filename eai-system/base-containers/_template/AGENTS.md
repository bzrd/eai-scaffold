# AGENTS.md – base-containers/_template/

## Rolle

Du erzeugst einen neuen Base-Container auf Basis dieser Vorlage. Base-Container DÜRFEN I/O machen (HTTP, Dateisystem, Datenbank) – im Gegensatz zu Transformern.

---

## Regeln

- Du MUSST das Template-Verzeichnis kopieren, nicht direkt im `_template/` arbeiten.
- Du MUSST I/O-Logik in `handler.py` isolieren.
- Du MUSST `main.py` als Entrypoint beibehalten.
- Du MUSST Retry-Logik für transiente Netzwerkfehler implementieren.
- Du MUSST alle I/O in Tests mocken – keine echten HTTP-Calls in Unit-Tests.
- Du darfst NIEMALS das `_template/`-Verzeichnis selbst modifizieren.
- Du darfst NIEMALS Domänenlogik (PlanPro-Parsing, Diff-Berechnung) einbauen.
- Du darfst NIEMALS `planpro_parser` importieren.

---

## Patterns

### Schritt-für-Schritt

1. **Template kopieren und umbenennen**
2. **`handler.py` implementieren** – hier passiert das I/O:
   - HTTP-Calls an externe Systeme
   - Dateien von/nach `INPUT_PATH`/`OUTPUT_PATH`
   - REST-API-Calls über `ds_client` (wenn Datenspeicher-Container)
3. **`main.py` anpassen** – Container-Name, Import-Pfad
4. **Tests schreiben** – alle I/O gemockt
5. **`pyproject.toml` anpassen**
6. **`README.md` aktualisieren**

### Erlaubte I/O-Arten

| Container-Typ | Erlaubtes I/O |
|---|---|
| file-fetcher/file-pusher | HTTP-Calls, Dateisystem |
| ds-reader/ds-writer | Datenspeicher REST-API via `ds_client` |
| http-trigger | Eingehende HTTP-Requests (FastAPI) |
| Sonstige | HTTP-Calls, Dateisystem, externe APIs |

---

## Antipatterns

- **Kein Domänenlogik-Code** – kein PlanPro-Parsing, kein Diff, keine Validierung.
- **Kein `planpro_parser`-Import**.
- **Keine hartkodierten URLs, Tokens, Pfade**.
- **Keine echten HTTP-Calls in Unit-Tests**.

---

## Testanforderungen

- Framework: `pytest` + `responses`/`pytest-httpx`
- Alle I/O gemockt
- Mindestanforderungen: Happy Path, Netzwerkfehler, Auth-Fehler, Timeout

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `ds_client` (nur bei DS-Containern), `requests`, `httpx`
- Du darfst NICHT importieren: `planpro_parser`, andere Container, Transformer

---

## Kontext

Base-Container laufen als Argo-Workflow-Steps (Ausnahme: `http-trigger` als Long-Running-Service). Sie sind die Brücke zwischen der Außenwelt und den Transformern. Die Trennung I/O vs. Domänenlogik ist ein zentrales Architekturprinzip das die Testbarkeit und Wartbarkeit sicherstellt.
