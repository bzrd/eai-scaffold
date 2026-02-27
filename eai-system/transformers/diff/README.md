# transformers/diff – Differenz-Transformer

## Zweck

Vergleicht zwei Stände von PlanPro-Objekten und erzeugt einen strukturierten Diff-Report. Identifiziert hinzugefügte, entfernte und geänderte Objekte anhand ihrer GUIDs.

---

## Struktur

```
diff/
├── diff_transformer/
│   ├── __init__.py
│   ├── main.py              # Standard-Entrypoint
│   └── transform.py         # Diff-Berechnung zwischen zwei Ständen
├── tests/
│   ├── conftest.py
│   ├── test_transform.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- Input: Zwei JSON-Dateien unter `INPUT_PATH` (Stand 1 und Stand 2)
- Output: Diff-Report als JSON unter `OUTPUT_PATH`
- GUIDs sind der Schlüssel für den Vergleich (nicht Array-Positionen)
- Git-Tag: `transformer-diff/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- `libs/planpro-parser` – Objekttyp-Informationen
- `libs/common` – Logging, Config, Provenance

---

## Beispiel: Output (Diff-Report)

```json
{
  "planpro_version_from": "1.10",
  "planpro_version_to": "1.10",
  "added": [{"guid": "...", "object_type": "Signal"}],
  "removed": [{"guid": "...", "object_type": "Weiche"}],
  "modified": [
    {
      "guid": "...",
      "object_type": "Signal",
      "changes": [
        {"field": "bezeichnung", "from": "S1", "to": "S1a"}
      ]
    }
  ],
  "unchanged_count": 142
}
```

---

## Checkliste

- [ ] `main.py` folgt Standard-Entrypoint-Pattern
- [ ] Diff basiert auf GUIDs (nicht auf Array-Reihenfolge)
- [ ] Added, Removed, Modified korrekt klassifiziert
- [ ] Modified enthält feldweise Änderungen
- [ ] Provenance-Fragment erzeugt
- [ ] Unit-Tests vorhanden
- [ ] Type Hints vollständig
