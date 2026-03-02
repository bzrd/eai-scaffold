# AGENTS.md – transformers/diff/

## Rolle

Du entwickelst den Diff-Transformer. Er vergleicht zwei Stände per GUID und erzeugt einen strukturierten Diff-Report.

## Regeln

- Du MUSST GUIDs als Vergleichsschlüssel verwenden – keine Array-Positionen.
- Du MUSST feldweise Änderungen für modifizierte Objekte identifizieren.
- Du MUSST zwischen Added, Removed und Modified unterscheiden.
- Du darfst NIEMALS GUIDs verändern.
- Du darfst NIEMALS `ds_client` importieren.

## Pattern: Diff-Logik

```python
def compute_diff(stand_1: list[dict], stand_2: list[dict]) -> DiffResult:
    index_1 = {obj["guid"]: obj for obj in stand_1}
    index_2 = {obj["guid"]: obj for obj in stand_2}
    guids_1, guids_2 = set(index_1), set(index_2)
    added = [index_2[g] for g in guids_2 - guids_1]
    removed = [index_1[g] for g in guids_1 - guids_2]
    modified = [compute_field_diff(index_1[g], index_2[g])
                for g in guids_1 & guids_2 if index_1[g] != index_2[g]]
    return DiffResult(added, removed, modified, len(guids_1 & guids_2) - len(modified))
```

## Testanforderungen

1. Identische Stände → leerer Diff
2. Nur Hinzufügungen / nur Entfernungen / Feldänderung / gemischt
3. GUIDs bleiben unverändert

## Abhängigkeiten

- DARFST: `common`, `planpro_parser`
- NICHT: `ds_client`, andere Transformer, Base-Container
