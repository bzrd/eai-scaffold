# AGENTS.md – libs/planpro-parser/

## Rolle

Du erweiterst oder pflegst die PlanPro-XML-Parser-Library. Diese Library hat KEIN Wissen über den Datenspeicher oder die API. Sie verarbeitet PlanPro-XML und erzeugt Python-Datenstrukturen. Keine Netzwerk-Calls, keine Dateisystem-Annahmen außer dem übergebenen XML-String oder Dateipfad.

---

## Regeln

- Du MUSST diese Library als reine Verarbeitungslogik halten: XML rein, Python-Datenstrukturen raus. Kein anderer Seiteneffekt.
- Du darfst NIEMALS HTTP-Calls, REST-API-Zugriffe oder Datenbankzugriffe einbauen.
- Du darfst NIEMALS `ds_client` oder andere Transformer/Base-Container importieren.
- Du MUSST GUIDs exakt aus dem XML übernehmen – niemals transformieren, normalisieren oder neu generieren. GUIDs sind permanente Infrastruktur-Identitäten.
- Du MUSST alle PlanPro-Versionen aus `constants.py` unterstützen. Wenn eine neue Version hinzukommt, muss `constants.py` als erstes aktualisiert werden.
- Du MUSST eigene Exception-Klassen für Fehler definieren: `PlanProParseError`, `GUIDValidationError`. Keine generischen `ValueError` oder `RuntimeError` nach außen geben.
- Du MUSST Fixtures aus `tests/fixtures/planpro/` für Tests nutzen – niemals synthetische XML-Strings erzeugen, es sei denn es ist ein Minimalbeispiel für einen spezifischen Edge Case.
- Du MUSST `mypy --strict` einhalten. Keine ungetypten Daten nach außen geben.

---

## Patterns

### XML-Zerlegung (Kernmuster)

```python
# planpro_parser/parser.py
from planpro_parser.types import PlanProObject, ParseResult
from planpro_parser.constants import PLANPRO_NAMESPACES, KNOWN_OBJECT_TYPES

def parse_xml(xml_content: str) -> ParseResult:
    """
    Zerlegt PlanPro-XML in eine Liste von PlanProObject-Instanzen.

    Args:
        xml_content: PlanPro-XML als String

    Returns:
        ParseResult mit objects, version, adjacency_list

    Raises:
        PlanProParseError: Bei strukturell ungültigem XML
        GUIDValidationError: Wenn ein GUID nicht dem UUID-Format entspricht
    """
    ...
```

### Typdefinitionen

```python
# planpro_parser/types.py
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class PlanProObject:
    guid: str              # UUID aus PlanPro, unveränderlich
    object_type: str       # PlanPro-Klassenname
    planpro_version: str   # z.B. "1.9", "1.10"
    data: dict[str, Any]   # Alle Attribute als JSON-kompatibles Dict
    references: list[str]  # GUIDs auf die dieses Objekt referenziert

@dataclass(frozen=True)
class ParseResult:
    objects: list[PlanProObject]
    planpro_version: str
    adjacency_list: dict[str, list[str]]  # guid -> [referenzierte guids]
```

### Validierung

```python
# planpro_parser/validator.py
import re
from planpro_parser.constants import KNOWN_OBJECT_TYPES

UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)

def validate_guid(guid: str) -> None:
    """Raises GUIDValidationError wenn guid kein gültiges UUID-Format hat."""
    if not UUID_PATTERN.match(guid):
        raise GUIDValidationError(f"Ungültige GUID: {guid!r}")

def validate_object_type(object_type: str) -> None:
    """Raises UnknownObjectTypeError wenn object_type nicht bekannt."""
    if object_type not in KNOWN_OBJECT_TYPES:
        raise UnknownObjectTypeError(f"Unbekannter Objekttyp: {object_type!r}")
```

---

## Antipatterns

- **Kein `requests.get/post`** – diese Library macht kein I/O außer XML-Parsing.
- **Keine GUIDs verändern** – nicht normalisieren, nicht case-folden, nicht neu generieren.
- **Kein Wissen über FIN-API-Formate** – der Output ist PlanPro-orientiert, nicht API-orientiert.
- **Keine globalen Variablen** für Parsingzustand – Parser-Funktionen sind pure functions oder Klassen ohne Seiteneffekte.
- **Keine `print()`-Statements** – wenn Logging nötig ist, `common.logging` verwenden.
- **Keine synthetischen Fixture-Daten** für Tests wenn eine echte Fixture verfügbar ist.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `planpro-parser/tests/`
- Fixtures laden aus `tests/fixtures/planpro/` (relative zu Repo-Root)
- Alle Tests mit `@pytest.mark.unit` markieren

**Mindestanforderungen für jede neue Funktion:**
1. Happy Path mit gültiger PlanPro-Datei (Fixture)
2. Korrekte GUID-Extraktion verifizieren
3. Korrekter Objekttyp verifiziert
4. Korrekte Version ermittelt
5. Error Case: ungültige GUID → `GUIDValidationError`
6. Error Case: unbekannter Objekttyp → `UnknownObjectTypeError`
7. Edge Case: minimale PlanPro-Datei mit 1 Objekt

**Assertion-Pattern:**
```python
def test_parse_xml_extracts_guid(minimal_planpro_xml: str) -> None:
    result = parse_xml(minimal_planpro_xml)
    assert len(result.objects) == 1
    assert result.objects[0].guid == "12345678-1234-1234-1234-123456789012"
    assert UUID_PATTERN.match(result.objects[0].guid)
```

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `lxml`, `xml.etree.ElementTree`, Python-Standardbibliothek
- Du darfst NICHT importieren: `ds_client`, andere Transformer, Base-Container, `requests`, `httpx`

---

## Kontext

PlanPro hat viele Versionen (derzeit 1.9, 1.10). Die Library muss versionstransparent arbeiten. Der Aufrufer soll sich nicht um XML-Parsing-Details kümmern müssen. GUIDs sind das einzige stabile Identifikationsmerkmal über alle Systeme und Versionen hinweg – sie werden in FIN als Primary Keys der Infrastrukturelemente behandelt.
