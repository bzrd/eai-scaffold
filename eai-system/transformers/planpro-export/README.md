# transformers/planpro-export – PlanPro XML Export-Transformer

## Zweck

Assembliert JSON-Objekte aus dem Datenspeicher zurück zu einer validen PlanPro-XML-Datei. Inverse Operation zum `planpro-ingest` Transformer.

---

## Struktur

```
planpro-export/
├── planpro_export/
│   ├── __init__.py
│   ├── main.py              # Standard-Entrypoint
│   └── transform.py         # Assemblierung: JSON-Objekte → PlanPro-XML
├── tests/
│   ├── conftest.py
│   ├── test_transform.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Konventionen

- Input: JSON-Datei unter `INPUT_PATH` mit Objektliste und Metadaten
- Output: PlanPro-XML-Datei unter `OUTPUT_PATH`
- Nutzt `libs/planpro-parser` für die XML-Erzeugung
- Git-Tag: `transformer-export/v<major>.<minor>.<patch>`

---

## Abhängigkeiten

- `libs/planpro-parser` – XML-Erzeugung, Objekttyp-Informationen
- `libs/common` – Logging, Config, Provenance

---

## Beispiel: Input/Output

**Input** (`INPUT_PATH`): JSON-Datei
```json
{
  "planpro_version": "1.10",
  "objects": [...],
  "scope": "projekt-abc",
  "phase": "planung"
}
```

**Output** (`OUTPUT_PATH`): Valide PlanPro-XML-Datei (Version 1.10)

---

## Checkliste

- [ ] `main.py` folgt Standard-Entrypoint-Pattern
- [ ] XML-Output ist valides PlanPro gemäß der angegebenen Version
- [ ] GUIDs im Output stimmen exakt mit Input überein
- [ ] Provenance-Fragment erzeugt
- [ ] Unit-Tests mit Roundtrip-Verifikation (Ingest → Export → Vergleich)
- [ ] Type Hints vollständig
