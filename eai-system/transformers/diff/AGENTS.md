# AGENTS.md – transformers/diff/

## Rolle

Du entwickelst oder pflegst den Diff-Transformer. Dieser Transformer vergleicht zwei Stände von PlanPro-Objekten und erzeugt einen strukturierten Diff-Report.

---

## Regeln

- Du MUSST GUIDs als Schlüssel für den Vergleich verwenden – nicht Array-Positionen oder Indizes.
- Du MUSST feldweise Änderungen für modifizierte Objekte identifizieren.
- Du MUSST zwischen Added (nur in Stand 2), Removed (nur in Stand 1) und Modified (in beiden, aber unterschiedlich) unterscheiden.
- Du darfst NIEMALS GUIDs verändern.
- Du darfst NIEMALS HTTP-Calls oder Datenbankzugriffe machen.
- Du MUSST `common.logging` und `common.provenance` verwenden.

---

## Patterns

### Diff-Logik

```python
# transform.py
from dataclasses import dataclass

@dataclass
class DiffResult:
    added: list[dict]
    removed: list[dict]
    modified: list[ModifiedObject]
    unchanged_count: int

def compute_diff(stand_1: list[dict], stand_2: list[dict]) -> DiffResult:
    index_1 = {obj["guid"]: obj for obj in stand_1}
    index_2 = {obj["guid"]: obj for obj in stand_2}

    guids_1 = set(index_1.keys())
    guids_2 = set(index_2.keys())

    added = [index_2[g] for g in guids_2 - guids_1]
    removed = [index_1[g] for g in guids_1 - guids_2]
    modified = [
        compute_field_diff(index_1[g], index_2[g])
        for g in guids_1 & guids_2
        if index_1[g] != index_2[g]
    ]
    unchanged_count = len(guids_1 & guids_2) - len(modified)

    return DiffResult(added, removed, modified, unchanged_count)
```

---

## Antipatterns

- **Kein Index-basierter Vergleich** – immer GUID-basiert.
- **Kein HTTP-Zugriff** – reiner Transformer.
- **Kein einfacher `==`-Vergleich ohne Feldaufschlüsselung** – der Report muss zeigen WAS sich geändert hat.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `diff/tests/`

**Mindestanforderungen:**
1. Identische Stände → leerer Diff
2. Nur Hinzufügungen → `added` korrekt befüllt
3. Nur Entfernungen → `removed` korrekt befüllt
4. Feldänderung → `modified` mit korrekten `changes`
5. Gemischter Fall → alle drei Listen korrekt
6. GUIDs bleiben unverändert im Report

---

## Abhängigkeiten

- Du DARFST importieren: `planpro_parser`, `common`
- Du darfst NICHT importieren: `ds_client`, andere Transformer, Base-Container

---

## Kontext

Der Diff-Transformer wird in Diff-Workflows eingesetzt: `ds-reader` liest Stand 1, `ds-reader` liest Stand 2, der Diff-Transformer vergleicht und der Report wird über `ds-writer` gespeichert. Die Diff-Reports sind Teil der Auditierbarkeit – sie dokumentieren was sich zwischen Planungsphasen geändert hat.
