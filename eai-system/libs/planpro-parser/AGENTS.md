# AGENTS.md – libs/planpro-parser/

## Rolle

Du pflegst die PlanPro-XML-Parser-Library. XML rein, typisierte Dataclasses raus. Kein I/O, kein Netzwerk, kein Datenbankzugriff.

## Regeln

- Du MUSST jeden PlanPro-Elementtyp als eigenes `@dataclass(frozen=True)` implementieren – kein `dict[str, Any]`.
- Du MUSST alle Typen zuerst im **Elementkatalog** (unten) eintragen, bevor du Code schreibst.
- Du MUSST `ObjectType`-Enum und `XPATH_MAP` in `constants.py` synchron zum Katalog halten.
- Du MUSST für jeden Katalogeintrag Tests in `test_types.py` generieren.
- Du darfst NIEMALS GUIDs verändern.
- Du darfst NIEMALS `ds_client`, Transformer oder Base-Container importieren.
- Du MUSST `mypy --strict` einhalten.

---

## Elementkatalog

Normative Quelle für alle Typen. Aus diesem Katalog werden `types.py`, `constants.py` und `test_types.py` generiert.

### Katalog-Schema

```yaml
KlassennamePascalCase:
  xml_path: <XPath ab LST-Zustand-Root>
  guid_xpath: <XPath zur GUID, relativ zum Element>
  felder:
    - name: <snake_case>
      xml_xpath: <XPath relativ zum Element>
      typ: <Python-Typ>       # str, int, float, bool, "str | None", "int | None" …
      required: <true|false>  # false → typ bekommt | None
```

### Katalog

```yaml
Signal:
  xml_path: ".//Signal"
  guid_xpath: "Identitaet/Wert"
  felder:
    - name: bezeichnung
      xml_xpath: "Bezeichnung_Signal/Identifikation_Signal/Bezeichnung_Lageplan_Lang/Wert"
      typ: "str"
      required: true
    - name: form
      xml_xpath: "Signal_Real/Signal_Real_Aktiv_Schirm/Signal_Rahmen/Signal_Rahmen_Art/Wert"
      typ: "str | None"
      required: false

WKrGspKomponente:
  xml_path: ".//W_Kr_Gsp_Komponente"
  guid_xpath: "Identitaet/Wert"
  felder:
    - name: zungenpaar_anzahl
      xml_xpath: "Weiche_Element/Weiche_Element_Allg/Zungenpaar_Anzahl/Wert"
      typ: "int | None"
      required: false

GleisAbschnitt:
  xml_path: ".//Gleis_Abschnitt"
  guid_xpath: "Identitaet/Wert"
  felder:
    - name: bezeichnung
      xml_xpath: "Bezeichnung_Gleis_Abschnitt/Bezeichnung_Tabelle/Wert"
      typ: "str | None"
      required: false

BahnsteigKante:
  xml_path: ".//Bahnsteig_Kante"
  guid_xpath: "Identitaet/Wert"
  felder:
    - name: laenge
      xml_xpath: "Bahnsteig_Kante_Allg/Bahnsteig_Laenge/Wert"
      typ: "float | None"
      required: false

Betriebsstelle:
  xml_path: ".//Betriebsstelle"
  guid_xpath: "Identitaet/Wert"
  felder:
    - name: bezeichnung
      xml_xpath: "Bezeichnung_Betriebsstelle/Identifikation_Betriebsstelle/Abkuerzung/Wert"
      typ: "str"
      required: true

Oertlichkeit:
  xml_path: ".//Oertlichkeit"
  guid_xpath: "Identitaet/Wert"
  felder:
    - name: bezeichnung
      xml_xpath: "Bezeichnung_Oertlichkeit/Oertlichkeit_Abkuerzung/Wert"
      typ: "str"
      required: true
    - name: art
      xml_xpath: "Oertlichkeit_Allg/Oertlichkeit_Art/Wert"
      typ: "str | None"
      required: false
```

> XPaths gegen die jeweilige PlanPro-XSD verifizieren. Versionsdifferenzen (1.9 vs 1.10) als Overrides in `constants.py` eintragen.

---

## Generierungsregeln

### types.py

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Signal:
    guid: str            # immer Pflicht
    planpro_version: str # immer Pflicht
    bezeichnung: str     # required: true  → kein None
    form: str | None     # required: false → | None

# Analog für alle weiteren Katalogeinträge.

PlanProElement = Signal | WKrGspKomponente | GleisAbschnitt | BahnsteigKante | Betriebsstelle | Oertlichkeit

@dataclass(frozen=True)
class ParseResult:
    objects: list[PlanProElement]
    planpro_version: str
```

### constants.py

```python
from enum import StrEnum

class ObjectType(StrEnum):
    SIGNAL           = "Signal"
    W_KR_GSP_KOMP    = "WKrGspKomponente"
    GLEIS_ABSCHNITT  = "GleisAbschnitt"
    BAHNSTEIG_KANTE  = "BahnsteigKante"
    BETRIEBSSTELLE   = "Betriebsstelle"
    OERTLICHKEIT     = "Oertlichkeit"

KNOWN_OBJECT_TYPES: frozenset[str] = frozenset(t.value for t in ObjectType)

XPATH_MAP: dict[str, str] = {
    "Signal":           ".//Signal",
    "WKrGspKomponente": ".//W_Kr_Gsp_Komponente",
    "GleisAbschnitt":   ".//Gleis_Abschnitt",
    "BahnsteigKante":   ".//Bahnsteig_Kante",
    "Betriebsstelle":   ".//Betriebsstelle",
    "Oertlichkeit":     ".//Oertlichkeit",
}

class PlanProVersion(StrEnum):
    V1_9  = "1.9"
    V1_10 = "1.10"

KNOWN_PLANPRO_VERSIONS: frozenset[str] = frozenset(v.value for v in PlanProVersion)
```

### test_types.py

Für jeden Katalogeintrag eine Testklasse. Vollständiges Beispiel für `Signal`, alle weiteren analog:

```python
import dataclasses, pytest
from typing import get_type_hints
from planpro_parser.types import Signal, WKrGspKomponente  # …alle Typen
from planpro_parser.constants import KNOWN_OBJECT_TYPES, XPATH_MAP

VALID_GUID = "12345678-1234-1234-1234-123456789012"

@pytest.mark.unit
class TestObjectTypeCatalog:
    def test_all_types_in_known_object_types(self) -> None:
        for name in ["Signal", "WKrGspKomponente", "GleisAbschnitt",
                     "BahnsteigKante", "Betriebsstelle", "Oertlichkeit"]:
            assert name in KNOWN_OBJECT_TYPES

    def test_all_types_in_xpath_map(self) -> None:
        for name in KNOWN_OBJECT_TYPES:
            assert name in XPATH_MAP

@pytest.mark.unit
class TestSignal:
    def _make(self, **kw: object) -> Signal:
        return Signal(guid=VALID_GUID, planpro_version="1.10",
                      bezeichnung="S1", form=None, **kw)  # type: ignore[arg-type]

    def test_fields_exist(self) -> None:
        names = {f.name for f in dataclasses.fields(Signal)}
        assert {"guid", "planpro_version", "bezeichnung", "form"} <= names

    def test_field_types(self) -> None:
        h = get_type_hints(Signal)
        assert h["guid"] is str
        assert h["bezeichnung"] is str   # required → kein None
        assert h["form"] == str | None   # optional → | None

    def test_is_frozen(self) -> None:
        obj = self._make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            object.__setattr__(obj, "bezeichnung", "X")  # type: ignore[misc]

# TestWKrGspKomponente, TestGleisAbschnitt, … analog
```

---

## Antipatterns

- **Kein `dict[str, Any]`** für Domänendaten.
- **Kein Code ohne Katalogeintrag** – Katalog ist immer zuerst.
- **Keine GUIDs verändern.**
- **Kein I/O, kein Netzwerk.**

## Abhängigkeiten

- DARFST importieren: `common`, `xml.etree.ElementTree` / `lxml`
- NICHT importieren: `ds_client`, Transformer, Base-Container
