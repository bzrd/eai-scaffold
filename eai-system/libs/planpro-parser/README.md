# libs/planpro-parser – PlanPro XML Parser

## Zweck

Die zentrale Library für die Verarbeitung von PlanPro-XML-Dateien. Sie zerlegt PlanPro-Dateien in JSON-Objekte orientiert am PlanPro-Klassendiagramm, extrahiert GUIDs, erkennt Referenzen und erzeugt Adjazenzlisten.

Diese Library ist die **meistgenutzte Library im Repo**. Sie wird von `transformer-planpro-ingest`, `transformer-planpro-export`, `transformer-diff` und potenziell Validierungslogik verwendet.

---

## Struktur

```
planpro-parser/
├── planpro_parser/
│   ├── __init__.py          # Öffentliche API
│   ├── parser.py            # XML-Zerlegung (parse_xml, parse_file)
│   ├── extractor.py         # GUID- und Referenz-Extraktion
│   ├── adjacency.py         # Adjazenzlisten-Erzeugung
│   ├── validator.py         # Mindest-Validierung (GUID-Format, Objekttyp, Version)
│   ├── types.py             # Typdefinitionen (PlanProObject, AdjacencyList, etc.)
│   └── constants.py         # Bekannte Objekttypen, PlanPro-Versionen, XML-Namespaces
├── tests/
│   ├── conftest.py          # Fixtures (lädt PlanPro-Beispieldateien)
│   ├── test_parser.py
│   ├── test_extractor.py
│   ├── test_adjacency.py
│   └── test_validator.py
└── pyproject.toml
```

---

## Konventionen

- **Keine Netzwerk-Calls**, keine Dateisystem-Annahmen außer dem übergebenen XML-String oder Dateipfad
- **Kein Wissen über den Datenspeicher (FIN)** – die Library liefert Python-Datenstrukturen, nicht API-kompatible Formate
- **GUIDs werden niemals verändert** – sie sind permanente Infrastruktur-Identitäten
- **Mehrere PlanPro-Versionen** (1.9, 1.10, ...) müssen transparent verarbeitet werden
- Fehlerbehandlung: ungültige XML löst `PlanProParseError`, ungültige GUIDs lösen `GUIDValidationError`
- Python-Package-Name: `planpro_parser`

---

## Abhängigkeiten

- Python-Standardbibliothek (`xml.etree.ElementTree` oder `lxml`)
- `libs/common` (für `GUIDValidationError` und Logging)
- **Keine anderen repo-internen Libraries**

---

## Beispiel: Neue Komponente

**Neuen Objekttyp hinzufügen:**
1. Objekttyp-Konstante in `constants.py` registrieren
2. Extraktionslogik in `extractor.py` erweitern
3. Test mit Fixture-Datei aus `tests/fixtures/` schreiben

**Neue PlanPro-Version unterstützen:**
1. XML-Namespace in `constants.py` eintragen
2. Versionserkennungslogik in `parser.py` anpassen
3. Regressionstests gegen alle bekannten Versionen sicherstellen

---

## Checkliste

- [ ] Neue Funktion mit vollständigen Type Hints
- [ ] Unit-Test mit gültigem PlanPro-Input (Fixture aus `tests/fixtures/`)
- [ ] Unit-Test mit ungültigem Input (prüft Exception)
- [ ] Keine HTTP/DB-Calls eingebaut
- [ ] `mypy --strict` grün
- [ ] Öffentliche API in `__init__.py` exportiert
- [ ] Wenn neuer Objekttyp: `constants.py` aktualisiert
