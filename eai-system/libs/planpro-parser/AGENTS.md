# AGENTS.md – libs/planpro-parser/

## Rolle

Du erweiterst oder pflegst die PlanPro-XML-Parser-Library. Diese Library hat KEIN Wissen über den Datenspeicher oder die API. Sie verarbeitet PlanPro-XML und erzeugt typisierte Python-Dataclasses. Keine Netzwerk-Calls, keine Dateisystem-Annahmen außer dem übergebenen XML-String oder Dateipfad.

**Der Elementkatalog weiter unten in dieser Datei ist die normative Quelle aller Typendefinitionen.** Wenn du eine neue PlanPro-Klasse hinzufügst oder ein Feld änderst, fängst du immer im Elementkatalog an – niemals direkt in `types.py` oder `constants.py`.

---

## Regeln

- Du MUSST diese Library als reine Verarbeitungslogik halten: XML rein, typisierte Dataclasses raus. Kein anderer Seiteneffekt.
- Du darfst NIEMALS HTTP-Calls, REST-API-Zugriffe oder Datenbankzugriffe einbauen.
- Du darfst NIEMALS `ds_client` oder andere Transformer/Base-Container importieren.
- Du MUSST GUIDs exakt aus dem XML übernehmen – niemals transformieren, normalisieren oder neu generieren. GUIDs sind permanente Infrastruktur-Identitäten.
- Du MUSST jeden PlanPro-Elementtyp als **eigene typisierte Dataclass** implementieren – kein generisches `dict[str, Any]` für Domänendaten.
- Du MUSST alle Dataclasses als `frozen=True` definieren – Infrastrukturobjekte sind unveränderlich.
- Du MUSST alle im Elementkatalog definierten Typen in `ObjectType` (constants.py) und `XPATH_MAP` (constants.py) registrieren.
- Du MUSST für jeden Typ im Elementkatalog Tests in `test_types.py` generieren.
- Du MUSST alle PlanPro-Versionen aus `constants.py` unterstützen. Wenn eine neue Version hinzukommt, muss `constants.py` als erstes aktualisiert werden.
- Du MUSST eigene Exception-Klassen verwenden: `PlanProParseError`, `GUIDValidationError`, `UnknownObjectTypeError`.
- Du MUSST `mypy --strict` einhalten.

---

## Elementkatalog

Dies ist die **einzige normative Quelle** für PlanPro-Typendefinitionen im Repo.

Aus diesem Katalog werden generiert:
- `planpro_parser/types.py` – eine `@dataclass` pro Eintrag
- `planpro_parser/constants.py` – `ObjectType`-Enum-Werte und `XPATH_MAP`
- `planpro_parser/tests/test_types.py` – Feld- und Typ-Verifikationstests

### Schema eines Katalogeintrags

```yaml
<KlassennamePascalCase>:
  xml_path: <XPath-Ausdruck ab LST-Zustand-Root>
  guid_xpath: <XPath zur GUID, relativ zum Element>
  felder:
    - name: <feldname_snake_case>
      xml_xpath: <XPath zum Wert, relativ zum Element>
      typ: <Python-Typ: str | int | float | bool | "str | None" usw.>
      required: <true|false>
      referenz: <true|false>          # true → dieses Feld enthält eine GUID auf ein anderes Objekt
      referenziert: <KlassennamePascalCase>  # nur wenn referenz: true
```

**Feldbeschreibung:**
- `name`: Feldname im Python-Dataclass (snake_case)
- `xml_xpath`: XPath relativ zum jeweiligen XML-Element (nicht zum Root)
- `typ`: Python-Typ-Annotation; optionale Felder immer mit `"str | None"` annotieren
- `required`: Ob das Feld im XML immer vorhanden ist
- `referenz: true`: Das Feld enthält eine GUID die auf ein anderes PlanPro-Objekt verweist; dieses Feld wird automatisch in die Adjazenzliste aufgenommen
- `referenziert`: Welchen Klassentyp die GUID referenziert (nur informativer Hinweis, keine strenge Validierung)

---

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
    - name: id_betriebsstelle
      xml_xpath: "ID_Betriebsstelle_Element/Wert"
      typ: "str | None"
      required: false
      referenz: true
      referenziert: "Betriebsstelle"

WKrGspKomponente:
  xml_path: ".//W_Kr_Gsp_Komponente"
  guid_xpath: "Identitaet/Wert"
  felder:
    - name: zungenpaar_anzahl
      xml_xpath: "Weiche_Element/Weiche_Element_Allg/Zungenpaar_Anzahl/Wert"
      typ: "int | None"
      required: false
    - name: id_gleis_abschnitt
      xml_xpath: "ID_Gleis_Abschnitt/Wert"
      typ: "str | None"
      required: false
      referenz: true
      referenziert: "GleisAbschnitt"

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
    - name: id_bahnsteig
      xml_xpath: "ID_Bahnsteig/Wert"
      typ: "str | None"
      required: false
      referenz: true
      referenziert: "Oertlichkeit"

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

> **Hinweis zu XPaths:** Die hier angegebenen Pfade basieren auf der PlanPro-Schemastruktur und müssen gegen die jeweilige XSD-Version verifiziert werden. Abweichungen zwischen 1.9 und 1.10 werden in `constants.py` als versionsspezifische Overrides definiert.

### Elementkatalog erweitern

Um einen neuen PlanPro-Elementtyp hinzuzufügen:

1. Neuen YAML-Eintrag im Katalog oben anlegen (nach dem Schema)
2. Aus dem Katalog generieren:
   - `types.py`: neue `@dataclass` (Feldname → Python-Annotation, Pflichtfelder ohne None, optionale mit `| None`)
   - `constants.py`: neuer `ObjectType`-Enum-Wert + `XPATH_MAP`-Eintrag
   - `test_types.py`: neue Testklasse (Felder vorhanden + Typen korrekt)
3. Fixture anlegen (echte PlanPro-XML mit diesem Elementtyp)
4. Checkliste in `README.md` abarbeiten

---

## Patterns

### Generierungsregel: types.py

Für jeden Katalogeintrag wird ein Dataclass nach diesem Muster generiert:

```python
# planpro_parser/types.py
from __future__ import annotations
from dataclasses import dataclass

# --- Infrastruktur-Typen (nicht aus Katalog) ---

@dataclass(frozen=True)
class ParseResult:
    """Ergebnis eines parse_xml() Aufrufs."""
    objects: list[Signal | WKrGspKomponente | GleisAbschnitt | BahnsteigKante | Betriebsstelle | Oertlichkeit]
    planpro_version: str
    adjacency_list: AdjacencyList

AdjacencyList = dict[str, list[str]]   # guid → [referenzierte guids]

# --- Generiert aus Elementkatalog ---

@dataclass(frozen=True)
class Signal:
    # Pflichtfelder (immer in jedem Objekt)
    guid: str                       # UUID, aus guid_xpath
    planpro_version: str            # z.B. "1.9", "1.10"

    # Domänenfelder (aus Katalog)
    bezeichnung: str                # required: true  → kein | None
    form: str | None                # required: false → | None
    id_betriebsstelle: str | None   # required: false, referenz: true → GUID-Verweis

@dataclass(frozen=True)
class WKrGspKomponente:
    guid: str
    planpro_version: str
    zungenpaar_anzahl: int | None
    id_gleis_abschnitt: str | None

@dataclass(frozen=True)
class GleisAbschnitt:
    guid: str
    planpro_version: str
    bezeichnung: str | None

# ... weitere Klassen analog
```

### Generierungsregel: constants.py

```python
# planpro_parser/constants.py
from enum import StrEnum

class ObjectType(StrEnum):
    """Alle bekannten PlanPro-Elementtypen. Generiert aus Elementkatalog."""
    SIGNAL            = "Signal"
    W_KR_GSP_KOMP     = "WKrGspKomponente"
    GLEIS_ABSCHNITT   = "GleisAbschnitt"
    BAHNSTEIG_KANTE   = "BahnsteigKante"
    BETRIEBSSTELLE    = "Betriebsstelle"
    OERTLICHKEIT      = "Oertlichkeit"

KNOWN_OBJECT_TYPES: frozenset[str] = frozenset(t.value for t in ObjectType)

# XML-Pfad für jeden Typ (aus guid_xpath des Katalogs – Lookup für den Parser)
XPATH_MAP: dict[str, str] = {
    "Signal":           ".//Signal",
    "WKrGspKomponente": ".//W_Kr_Gsp_Komponente",
    "GleisAbschnitt":   ".//Gleis_Abschnitt",
    "BahnsteigKante":   ".//Bahnsteig_Kante",
    "Betriebsstelle":   ".//Betriebsstelle",
    "Oertlichkeit":     ".//Oertlichkeit",
}

# GUID-XPath für jeden Typ
GUID_XPATH_MAP: dict[str, str] = {
    "Signal":           "Identitaet/Wert",
    "WKrGspKomponente": "Identitaet/Wert",
    "GleisAbschnitt":   "Identitaet/Wert",
    "BahnsteigKante":   "Identitaet/Wert",
    "Betriebsstelle":   "Identitaet/Wert",
    "Oertlichkeit":     "Identitaet/Wert",
}

class PlanProVersion(StrEnum):
    V1_9  = "1.9"
    V1_10 = "1.10"

KNOWN_PLANPRO_VERSIONS: frozenset[str] = frozenset(v.value for v in PlanProVersion)

PLANPRO_NAMESPACES: dict[str, str] = {
    "pp":  "http://www.plan-pro.de/modell/PlanPro/1.10.0",
    "pp9": "http://www.plan-pro.de/modell/PlanPro/1.9.0",
}
```

### Generierungsregel: test_types.py

Für jeden Katalogeintrag wird eine Testklasse nach diesem Muster generiert:

```python
# planpro_parser/tests/test_types.py
"""
Tests für die aus dem Elementkatalog generierten Dataclasses.
Diese Datei ist GENERIERT – Änderungen müssen im Elementkatalog (AGENTS.md) gemacht werden.

Sinn dieser Tests: Sicherstellen, dass das LLM die Typen korrekt aus dem Katalog
implementiert hat. Jeder Test prüft:
  1. Dass das Dataclass existiert und instanziierbar ist
  2. Dass alle Felder aus dem Katalog vorhanden sind
  3. Dass die Typen korrekt annotiert sind (via get_type_hints)
  4. Dass frozen=True gilt (Mutation schlägt fehl)
"""
import dataclasses
import pytest
from typing import get_type_hints
from planpro_parser.types import Signal, WKrGspKomponente, GleisAbschnitt, BahnsteigKante, Betriebsstelle, Oertlichkeit
from planpro_parser.constants import ObjectType, KNOWN_OBJECT_TYPES, XPATH_MAP

# --- Infrastruktur-Tests (immer) ---

@pytest.mark.unit
class TestObjectTypeCatalog:
    def test_all_catalog_types_in_enum(self) -> None:
        """Jeder Katalogeintrag muss als ObjectType existieren."""
        expected = {"Signal", "WKrGspKomponente", "GleisAbschnitt",
                    "BahnsteigKante", "Betriebsstelle", "Oertlichkeit"}
        assert expected.issubset(KNOWN_OBJECT_TYPES)

    def test_all_catalog_types_in_xpath_map(self) -> None:
        """Jeder Katalogeintrag muss einen XPATH_MAP-Eintrag haben."""
        for name in KNOWN_OBJECT_TYPES:
            assert name in XPATH_MAP, f"XPATH_MAP Eintrag fehlt für: {name}"

# --- Generiert pro Katalogeintrag ---

@pytest.mark.unit
class TestSignal:
    def _make(self, **overrides: object) -> Signal:
        defaults: dict[str, object] = {
            "guid": "12345678-1234-1234-1234-123456789012",
            "planpro_version": "1.10",
            "bezeichnung": "S1",
            "form": None,
            "id_betriebsstelle": None,
        }
        return Signal(**{**defaults, **overrides})  # type: ignore[arg-type]

    def test_fields_exist(self) -> None:
        field_names = {f.name for f in dataclasses.fields(Signal)}
        assert "guid" in field_names
        assert "planpro_version" in field_names
        assert "bezeichnung" in field_names
        assert "form" in field_names
        assert "id_betriebsstelle" in field_names

    def test_field_types(self) -> None:
        hints = get_type_hints(Signal)
        assert hints["guid"] is str
        assert hints["planpro_version"] is str
        assert hints["bezeichnung"] is str
        # Optionale Felder: str | None
        assert hints["form"] == str | None
        assert hints["id_betriebsstelle"] == str | None

    def test_is_frozen(self) -> None:
        obj = self._make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            object.__setattr__(obj, "bezeichnung", "S2")  # type: ignore[misc]

    def test_instantiation_required_fields(self) -> None:
        obj = self._make(bezeichnung="EINFAHRT")
        assert obj.bezeichnung == "EINFAHRT"
        assert obj.form is None

    def test_instantiation_with_all_fields(self) -> None:
        obj = self._make(
            bezeichnung="S1",
            form="Hp",
            id_betriebsstelle="87654321-4321-4321-4321-210987654321",
        )
        assert obj.bezeichnung == "S1"
        assert obj.form == "Hp"
        assert obj.id_betriebsstelle == "87654321-4321-4321-4321-210987654321"


@pytest.mark.unit
class TestWKrGspKomponente:
    def _make(self, **overrides: object) -> WKrGspKomponente:
        defaults: dict[str, object] = {
            "guid": "12345678-1234-1234-1234-123456789012",
            "planpro_version": "1.10",
            "zungenpaar_anzahl": None,
            "id_gleis_abschnitt": None,
        }
        return WKrGspKomponente(**{**defaults, **overrides})  # type: ignore[arg-type]

    def test_fields_exist(self) -> None:
        field_names = {f.name for f in dataclasses.fields(WKrGspKomponente)}
        assert "guid" in field_names
        assert "zungenpaar_anzahl" in field_names
        assert "id_gleis_abschnitt" in field_names

    def test_field_types(self) -> None:
        hints = get_type_hints(WKrGspKomponente)
        assert hints["zungenpaar_anzahl"] == int | None
        assert hints["id_gleis_abschnitt"] == str | None

    def test_is_frozen(self) -> None:
        obj = self._make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            object.__setattr__(obj, "zungenpaar_anzahl", 2)  # type: ignore[misc]


@pytest.mark.unit
class TestGleisAbschnitt:
    def _make(self, **overrides: object) -> GleisAbschnitt:
        defaults: dict[str, object] = {
            "guid": "12345678-1234-1234-1234-123456789012",
            "planpro_version": "1.10",
            "bezeichnung": None,
        }
        return GleisAbschnitt(**{**defaults, **overrides})  # type: ignore[arg-type]

    def test_fields_exist(self) -> None:
        field_names = {f.name for f in dataclasses.fields(GleisAbschnitt)}
        assert "guid" in field_names
        assert "bezeichnung" in field_names

    def test_field_types(self) -> None:
        hints = get_type_hints(GleisAbschnitt)
        assert hints["bezeichnung"] == str | None

    def test_is_frozen(self) -> None:
        obj = self._make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            object.__setattr__(obj, "bezeichnung", "GA1")  # type: ignore[misc]


@pytest.mark.unit
class TestBahnsteigKante:
    def _make(self, **overrides: object) -> BahnsteigKante:
        defaults: dict[str, object] = {
            "guid": "12345678-1234-1234-1234-123456789012",
            "planpro_version": "1.10",
            "laenge": None,
            "id_bahnsteig": None,
        }
        return BahnsteigKante(**{**defaults, **overrides})  # type: ignore[arg-type]

    def test_fields_exist(self) -> None:
        field_names = {f.name for f in dataclasses.fields(BahnsteigKante)}
        assert "laenge" in field_names
        assert "id_bahnsteig" in field_names

    def test_field_types(self) -> None:
        hints = get_type_hints(BahnsteigKante)
        assert hints["laenge"] == float | None
        assert hints["id_bahnsteig"] == str | None

    def test_is_frozen(self) -> None:
        obj = self._make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            object.__setattr__(obj, "laenge", 200.0)  # type: ignore[misc]


@pytest.mark.unit
class TestBetriebsstelle:
    def _make(self, **overrides: object) -> Betriebsstelle:
        defaults: dict[str, object] = {
            "guid": "12345678-1234-1234-1234-123456789012",
            "planpro_version": "1.10",
            "bezeichnung": "BF",
        }
        return Betriebsstelle(**{**defaults, **overrides})  # type: ignore[arg-type]

    def test_fields_exist(self) -> None:
        field_names = {f.name for f in dataclasses.fields(Betriebsstelle)}
        assert "bezeichnung" in field_names

    def test_field_types(self) -> None:
        hints = get_type_hints(Betriebsstelle)
        assert hints["bezeichnung"] is str   # required: true → kein None

    def test_is_frozen(self) -> None:
        obj = self._make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            object.__setattr__(obj, "bezeichnung", "X")  # type: ignore[misc]


@pytest.mark.unit
class TestOertlichkeit:
    def _make(self, **overrides: object) -> Oertlichkeit:
        defaults: dict[str, object] = {
            "guid": "12345678-1234-1234-1234-123456789012",
            "planpro_version": "1.10",
            "bezeichnung": "Bf Muster",
            "art": None,
        }
        return Oertlichkeit(**{**defaults, **overrides})  # type: ignore[arg-type]

    def test_fields_exist(self) -> None:
        field_names = {f.name for f in dataclasses.fields(Oertlichkeit)}
        assert "bezeichnung" in field_names
        assert "art" in field_names

    def test_field_types(self) -> None:
        hints = get_type_hints(Oertlichkeit)
        assert hints["bezeichnung"] is str
        assert hints["art"] == str | None

    def test_is_frozen(self) -> None:
        obj = self._make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            object.__setattr__(obj, "art", "Bahnhof")  # type: ignore[misc]
```

---

## Antipatterns

- **Kein `dict[str, Any]` für Domänendaten** – jedes PlanPro-Element ist ein typisiertes Dataclass.
- **Keine Typen direkt in `types.py` oder `constants.py` anlegen ohne Katalogeintrag** – der Katalog ist die Quelle der Wahrheit.
- **Kein `requests.get/post`** – diese Library macht kein I/O außer XML-Parsing.
- **Keine GUIDs verändern** – nicht normalisieren, nicht case-folden, nicht neu generieren.
- **Kein Wissen über FIN-API-Formate** – der Output sind Python-Dataclasses, nicht API-Payloads.
- **Keine globalen Variablen** für Parsingzustand – Parser-Funktionen sind pure functions.
- **Keine `print()`-Statements** – `common.logging` verwenden.
- **Keine synthetischen Fixture-Daten** für Tests wenn eine echte Fixture verfügbar ist.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `planpro-parser/tests/`
- Fixtures laden aus `tests/fixtures/planpro/` (relativ zu Repo-Root)
- Alle Tests mit `@pytest.mark.unit` markieren

**`test_types.py` (aus Katalog generiert):**
- Für jeden Katalogeintrag eine Testklasse
- Jede Klasse prüft: Felder vorhanden, Typen korrekt (`get_type_hints`), `frozen=True`, Instanziierung mit Pflichtfeldern, Instanziierung mit optionalen Feldern

**`test_parser.py` (manuell):**
- Happy Path: gültige PlanPro-Datei → `ParseResult` mit typisierten Objekten
- Korrekte GUID-Extraktion
- Korrekte Version ermittelt
- Error Case: ungültige GUID → `GUIDValidationError`
- Error Case: unbekannter Objekttyp → `UnknownObjectTypeError`
- Edge Case: minimale PlanPro-Datei mit 1 Objekt

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `lxml`, `xml.etree.ElementTree`, Python-Standardbibliothek
- Du darfst NICHT importieren: `ds_client`, andere Transformer, Base-Container, `requests`, `httpx`

---

## Kontext

PlanPro hat viele Versionen (derzeit 1.9, 1.10). Die Library muss versionstransparent arbeiten. GUIDs sind das einzige stabile Identifikationsmerkmal über alle Systeme und Versionen hinweg – sie werden in FIN als Primary Keys behandelt. Typisierte Dataclasses statt generischer Dicts ermöglichen mypy-Prüfung und machen Tippfehler in Feldnamen zur Compile-Zeit sichtbar statt erst zur Laufzeit.
