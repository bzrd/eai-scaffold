# AGENTS.md – base-containers/file-pusher/

## Rolle

Du entwickelst oder pflegst den File-Pusher. Er liefert Dateien an externe Systeme – typischerweise der letzte Step in einem Export-Workflow.

---

## Regeln

- Du MUSST Retry-Logik für transiente Netzwerkfehler implementieren.
- Du MUSST Auth-Credentials aus Umgebungsvariablen lesen.
- Du MUSST die Datei von `INPUT_PATH` lesen und an das Zielsystem senden.
- Du MUSST ein Provenance-Fragment erzeugen mit der Ziel-URL als Metadatum.
- Du darfst NIEMALS Domänenlogik einbauen.

---

## Patterns

```python
# handler.py
def push_file(input_path: str, target_url: str, token: str) -> None:
    data = Path(input_path).read_bytes()
    response = requests.post(target_url, data=data, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
```

---

## Antipatterns

- **Keine Dateiverarbeitung** – nur lesen und senden.
- **Keine hartkodierten Ziel-URLs**.
- **Kein `planpro_parser`** – keine Domänenlogik.

---

## Testanforderungen

- HTTP-Calls mocken
- Test: Erfolgreicher Upload
- Test: Netzwerkfehler → Retry
- Test: Auth-Fehler

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `requests`, `httpx`
- Du darfst NICHT importieren: `planpro_parser`, `ds_client`, andere Container

---

## Kontext

Der File-Pusher ist typischerweise der letzte Step in einem Export-Workflow. Er nimmt eine vom `planpro-export` Transformer erzeugte PlanPro-XML-Datei und liefert sie an die Ziel-Fachapplikation.
