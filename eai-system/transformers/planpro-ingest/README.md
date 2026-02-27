# transformers/planpro-ingest – PlanPro XML Import-Transformer

## Zweck

Zerlegt eine PlanPro-XML-Datei in einzelne JSON-Objekte orientiert am PlanPro-Klassendiagramm. Erzeugt eine Adjazenzliste der Referenzstruktur als Metadatum. Validiert jedes Objekt gegen Mindestanforderungen (GUID, Objekttyp, PlanPro-Version).

---

## Struktur

```
planpro-ingest/
├── planpro_ingest/
│   ├── __init__.py
│   ├── main.py              # Standard-Entrypoint
│   └── transform.py         # Zerlegung: XML → JSON-Objekte + Adjazenzliste
├── tests/
│   ├── conftest.py
│   ├── test_transform.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- Input: PlanPro-XML-Datei unter `INPUT_PATH`
- Output: JSON-Datei unter `OUTPUT_PATH` mit Liste von Objekten + Adjazenzliste
- Nutzt `libs/planpro-parser` für die XML-Zerlegung
- Nutzt `libs/common` für Logging, Config, Provenance, Validierung
- Git-Tag: `transformer-ingest/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- `libs/planpro-parser` – XML-Zerlegung, GUID-Extraktion, Referenzerkennung
- `libs/common` – Logging, Config, Provenance, Validierung

---

## Beispiel: Input/Output

**Input** (`INPUT_PATH`): PlanPro-XML-Datei (Version 1.10)

**Output** (`OUTPUT_PATH`): JSON-Datei
```json
{
  "planpro_version": "1.10",
  "objects": [
    {
      "guid": "12345678-1234-1234-1234-123456789012",
      "object_type": "Signal",
      "data": { ... }
    }
  ],
  "adjacency_list": {
    "12345678-...": ["87654321-...", "abcdef01-..."]
  }
}
```

---

## Checkliste

- [ ] `main.py` folgt Standard-Entrypoint-Pattern
- [ ] Nutzt `planpro_parser.parse_xml()` für Zerlegung
- [ ] Adjazenzliste wird als Metadatum miterzeugt
- [ ] Mindest-Validierung für jedes Objekt (GUID, Objekttyp, Version)
- [ ] Ungültige Objekte werden abgewiesen und strukturiert geloggt
- [ ] Provenance-Fragment erzeugt
- [ ] Unit-Tests vorhanden
- [ ] Type Hints vollständig
