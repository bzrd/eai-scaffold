# AGENTS.md – transformers/planpro-export/

## Rolle

Du entwickelst oder pflegst den PlanPro-Export-Transformer. Dieser Transformer assembliert JSON-Objekte zu einer validen PlanPro-XML-Datei. Er ist die Inverse zum `planpro-ingest`.

---

## Regeln

- Du MUSST `planpro_parser` für die XML-Erzeugung verwenden.
- Du MUSST sicherstellen, dass die erzeugte XML-Datei valides PlanPro der angegebenen Version ist.
- Du MUSST GUIDs exakt aus dem Input übernehmen – niemals verändern.
- Du MUSST die Referenzstruktur (Adjazenzliste) korrekt in XML-Referenzen zurückübersetzen.
- Du darfst NIEMALS HTTP-Calls oder Datenbankzugriffe machen.
- Du darfst NIEMALS `ds_client` importieren.

---

## Patterns

### Transform-Logik

```python
# transform.py
from planpro_parser import build_xml
from planpro_parser.types import PlanProObject

def transform(objects: list[PlanProObject], planpro_version: str) -> str:
    """Assembliert JSON-Objekte zu PlanPro-XML."""
    return build_xml(objects, version=planpro_version)
```

---

## Antipatterns

- **Keine manuelle XML-String-Konkatenation** – immer `planpro_parser` für XML-Erzeugung.
- **Keine GUIDs verändern** – sie müssen exakt übernommen werden.
- **Kein HTTP/DB-Zugriff** – reiner Transformer.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `planpro-export/tests/`
- **Roundtrip-Test ist Pflicht:** XML → Ingest → JSON → Export → XML → Vergleich
- Fixtures: PlanPro-Beispieldateien aus `tests/fixtures/`

**Mindestanforderungen:**
1. Gültige Objektliste → valides PlanPro-XML
2. GUIDs im Output exakt wie im Input
3. PlanPro-Version korrekt im XML-Header
4. Roundtrip: Ingest → Export ergibt semantisch äquivalentes XML
5. Leere Objektliste → minimales gültiges PlanPro-XML

---

## Abhängigkeiten

- Du DARFST importieren: `planpro_parser`, `common`
- Du darfst NICHT importieren: `ds_client`, andere Transformer, Base-Container

---

## Kontext

Der Export-Transformer wird in Export-Workflows eingesetzt, wo JSON-Objekte aus dem Datenspeicher (gelesen durch `ds-reader`) zurück in PlanPro-XML umgewandelt und über `file-pusher` an Fachapplikationen geliefert werden. Korrektes PlanPro-XML ist kritisch – die empfangenden Fachapplikationen validieren das XML streng.
