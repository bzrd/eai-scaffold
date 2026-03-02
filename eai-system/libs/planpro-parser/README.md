# libs/planpro-parser – PlanPro XML Parser

## Zweck

Die zentrale Library für die Verarbeitung von PlanPro-XML-Dateien. Sie zerlebt PlanPro-Dateien in **typisierte Python-Dataclasses** (eine Klasse pro PlanPro-Elementtyp), extrahiert GUIDs, erkennt Referenzen zwischen Objekten und erzeugt Adjazenzlisten.

Diese Library ist die **meistgenutzte Library im Repo**. Sie wird von `transformer-planpro-ingest`, `transformer-planpro-export`, `transformer-diff` und Validierungslogik verwendet.

**Normative Quelle für alle Typendefinitionen:** Die `## Elementkatalog`-Sektion in `AGENTS.md`. Dort ist festgelegt, welche PlanPro-Elemente als Dataclasses existieren, unter welchem XML-Pfad sie gefunden werden und welche Felder sie haben.

---

## Struktur

```
planpro-parser/
├── planpro_parser/
│   ├── __init__.py          # Öffentliche API – alle Dataclasses und Parser-Funktionen
│   ├── parser.py            # XML-Zerlegung: parse_xml(), parse_file()
│   ├── extractor.py         # GUID- und Referenz-Extraktion aus XML-Elementen
│   ├── adjacency.py         # Adjazenzlisten-Erzeugung aus Referenzfeldern
│   ├── validator.py         # GUID-Format, Objekttyp gegen constants.py prüfen
│   ├── types.py             # ⚠ GENERIERT aus Elementkatalog in AGENTS.md –
│   │                        #   typisierte Dataclasses für jeden PlanPro-Typ,
│   │                        #   plus generische ParseResult- und AdjacencyList-Typen
│   └── constants.py         # ⚠ GENERIERT aus Elementkatalog in AGENTS.md –
│                            #   ObjectType-Enum, PlanPro-Versionen, XML-Namespaces,
│                            #   XPATH_MAP (Klassenname → XPath)
├── tests/
│   ├── conftest.py          # Fixtures (lädt PlanPro-Beispieldateien)
│   ├── test_parser.py       # Tests für parse_xml() und parse_file()
│   ├── test_extractor.py    # Tests für GUID- und Referenz-Extraktion
│   ├── test_adjacency.py    # Tests für Adjazenzlisten-Erzeugung
│   ├── test_validator.py    # Tests für Validierungslogik
│   └── test_types.py        # ⚠ GENERIERT aus Elementkatalog – prüft dass alle
│                            #   Dataclasses die richtigen Felder und Typen haben
└── pyproject.toml
```

Dateien mit ⚠ werden **aus dem Elementkatalog** in `AGENTS.md` generiert und müssen bei Katalogerweiterungen neu generiert werden.

---

## Konventionen

- **Jeder PlanPro-Elementtyp ist ein eigenes Dataclass** – kein generisches `dict[str, Any]`
- **Alle Dataclasses sind `frozen=True`** – Infrastrukturdaten sind unveränderlich
- **GUIDs werden niemals verändert** – sie sind permanente Infrastruktur-Identitäten
- **Mehrere PlanPro-Versionen** (1.9, 1.10, ...) werden durch optionale Felder und Versionsangaben abgedeckt
- **Der Elementkatalog in `AGENTS.md` ist die einzige Stelle** an der neue Elemente und Felder definiert werden
- Fehlerbehandlung: `PlanProParseError` bei ungültigem XML, `GUIDValidationError` bei GUID-Format-Fehler, `UnknownObjectTypeError` bei unbekanntem Typ
- Python-Package-Name: `planpro_parser`

---

## Abhängigkeiten

- Python-Standardbibliothek (`xml.etree.ElementTree` oder `lxml`)
- `libs/common` (Logging, GUID-Validierungsfehler)
- **Keine anderen repo-internen Libraries**

---

## Beispiel: Neuen Objekttyp hinzufügen

1. **Elementkatalog in `AGENTS.md` erweitern** (neuen Eintrag unter `## Elementkatalog` anlegen)
2. **`types.py` regenerieren**: LLM liest Katalog → generiert `@dataclass`
3. **`constants.py` regenerieren**: LLM liest Katalog → ergänzt `ObjectType`-Enum und `XPATH_MAP`
4. **`test_types.py` regenerieren**: LLM liest Katalog → generiert Typ- und Feldtests
5. **Parser-Logik in `extractor.py`** erweitern wenn nötig (bei komplexen Referenzstrukturen)

Neue PlanPro-Version unterstützen:
1. Namespace und Version in `constants.py` eintragen
2. Versionserkennungslogik in `parser.py` anpassen
3. Regressionstests gegen alle bekannten Versionen sicherstellen

---

## Beispiel: Dataclass-Ausgabe (generiert aus Katalog)

```python
# planpro_parser/types.py (Ausschnitt – generiert)

@dataclass(frozen=True)
class Signal:
    # Pflichtfelder (immer vorhanden)
    guid: str                    # UUID aus PlanPro, unveränderlich
    planpro_version: str         # z.B. "1.9", "1.10"

    # Domänenfelder (aus Katalog)
    bezeichnung: str
    form: str | None             # optional im Standard
    id_betriebsstelle: str | None  # GUID-Verweis auf Betriebsstelle

@dataclass(frozen=True)
class ParseResult:
    objects: list[Signal | WKrGspKomponente | GleisAbschnitt | ...]
    planpro_version: str
    adjacency_list: dict[str, list[str]]   # guid → [referenzierte guids]
```

---

## Checkliste für Katalogerweiterungen

- [ ] Neuer Eintrag im Elementkatalog (`AGENTS.md`) mit XML-Pfad und allen Feldern
- [ ] `types.py` aus Katalog regeneriert und committet
- [ ] `constants.py` aus Katalog regeneriert (ObjectType-Enum + XPATH_MAP)
- [ ] `test_types.py` aus Katalog regeneriert – alle Tests grün
- [ ] `mypy --strict` grün
- [ ] Öffentliche API in `__init__.py` exportiert
- [ ] Fixture für den neuen Typ in `tests/fixtures/planpro/` vorhanden (echte Daten)
