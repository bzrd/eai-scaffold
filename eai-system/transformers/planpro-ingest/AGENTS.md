# AGENTS.md – transformers/planpro-ingest/

## Rolle

Du entwickelst oder pflegst den PlanPro-Ingest-Transformer. Dieser Transformer zerlegt PlanPro-XML in JSON-Objekte, validiert sie und erzeugt eine Adjazenzliste der Referenzstruktur.

---

## Regeln

- Du MUSST `planpro_parser` für die XML-Zerlegung verwenden – keine eigene XML-Parsing-Logik.
- Du MUSST für jedes extrahierte Objekt die Mindest-Validierung durchführen: GUID vorhanden + UUID-Format, Objekttyp vorhanden + bekannt, PlanPro-Version vorhanden.
- Du MUSST ungültige Objekte abweisen und den Fehler strukturiert loggen (nicht den gesamten Import abbrechen).
- Du MUSST eine Adjazenzliste als Metadatum erzeugen, die die Referenzstruktur zwischen den importierten Objekten abbildet.
- Du darfst NIEMALS GUIDs verändern oder neu generieren.
- Du darfst NIEMALS HTTP-Calls oder Datenbankzugriffe machen.
- Du darfst NIEMALS `ds_client` importieren.

---

## Patterns

### Transform-Logik

```python
# transform.py
from planpro_parser import parse_xml, ParseResult
from common.validation import validate_guid, validate_object_type

def transform(xml_content: str) -> IngestResult:
    parse_result: ParseResult = parse_xml(xml_content)

    valid_objects = []
    rejected_objects = []

    for obj in parse_result.objects:
        try:
            validate_guid(obj.guid)
            validate_object_type(obj.object_type)
            valid_objects.append(obj)
        except ValidationError as e:
            rejected_objects.append((obj, str(e)))

    return IngestResult(
        objects=valid_objects,
        rejected=rejected_objects,
        adjacency_list=parse_result.adjacency_list,
        planpro_version=parse_result.planpro_version,
    )
```

---

## Antipatterns

- **Kein eigenes XML-Parsing** – immer `planpro_parser` verwenden.
- **Kein Abbruch bei einzelnem ungültigem Objekt** – abweisen und weiterverarbeiten.
- **Keine GUIDs transformieren** – sie kommen aus dem XML und bleiben exakt so.
- **Kein `requests`-Import** – kein Netzwerk in Transformern.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `planpro-ingest/tests/`
- Fixtures: PlanPro-XML-Dateien aus `tests/fixtures/` (Repo-Root)

**Mindestanforderungen:**
1. Gültige PlanPro-Datei → korrekte JSON-Objekte mit allen Feldern
2. Adjazenzliste korrekt aufgebaut
3. Ungültige GUID → Objekt abgewiesen, Rest verarbeitet
4. Unbekannter Objekttyp → Objekt abgewiesen
5. Minimale PlanPro-Datei → 1 Objekt korrekt extrahiert
6. PlanPro-Version korrekt ermittelt

---

## Abhängigkeiten

- Du DARFST importieren: `planpro_parser`, `common`
- Du darfst NICHT importieren: `ds_client`, andere Transformer, Base-Container

---

## Kontext

Dieser Transformer ist der Haupteingangspunkt für PlanPro-Daten ins System. Er wird in Import-Workflows zwischen einem `file-fetcher` (Base-Container, holt die XML-Datei) und einem `ds-writer` (Base-Container, schreibt JSON in den Datenspeicher) eingesetzt. Die GUIDs aus dem Import werden als permanente Identität der Infrastrukturelemente im gesamten System genutzt.
