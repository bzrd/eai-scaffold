# AGENTS.md – transformers/planpro-ingest/

## Rolle

Du entwickelst den PlanPro-Ingest-Transformer. Er liest PlanPro-XML von `INPUT_PATH`, konvertiert es in plain-dict JSON-Objekte und schreibt sie nach `OUTPUT_PATH`. Die gesamte XML-Logik lebt in `convert.py`.

## Regeln

- Du MUSST die XML-Konvertierungslogik in `convert.py` implementieren – nicht in `main.py`.
- Du MUSST Objekte als plain `dict` zurückgeben – keine Dataclasses, keine TypedDicts.
- Du MUSST jedes Objekt auf GUID (UUID-Format), Objekttyp (bekannt) und PlanPro-Version prüfen.
- Du MUSST ungültige Objekte abweisen und weiterverarbeiten (kein Abbruch).
- Du darfst NIEMALS GUIDs verändern oder neu generieren.
- Du darfst NIEMALS `ds_client` importieren.
- Du darfst NIEMALS `planpro_parser` importieren – diese Library existiert nicht mehr.
- Wenn Export-Transformer JSON→XML-Rekonstruktion brauchen: erst dann gemeinsame Library extrahieren, nicht prophylaktisch.

## Struktur

```
planpro-ingest/
├── main.py      # Entrypoint: Config, I/O, Provenance
├── convert.py   # XML→JSON (reine Funktion, kein I/O, kein HTTP)
└── tests/
    ├── test_convert.py
    └── fixtures/
        ├── sample_1.9.xml
        ├── sample_1.10.xml
        └── expected_output.json
```

## Pattern: convert.py

```python
import xml.etree.ElementTree as ET

def convert(xml_content: str) -> dict:
    """Konvertiert PlanPro-XML zu plain-dict JSON-Struktur."""
    root = ET.fromstring(xml_content)
    planpro_version = _extract_version(root)
    objects = []
    for element in _iter_objects(root):
        obj = _element_to_dict(element, planpro_version)
        if _is_valid(obj):
            objects.append(obj)
        else:
            # strukturiert loggen, weiter
            pass
    return {"planpro_version": planpro_version, "objects": objects}
```

## Testanforderungen

1. Gültige PlanPro 1.9 → korrekte JSON-Objekte (Keys + Typen prüfen)
2. Gültige PlanPro 1.10 → korrekte JSON-Objekte
3. Ungültige GUID → abgewiesen, Rest verarbeitet
4. Unbekannter Objekttyp → abgewiesen
5. Minimale PlanPro-Datei → 1 Objekt extrahiert
6. PlanPro-Version korrekt ermittelt

Fixtures: echte oder echt-nahe PlanPro-XML-Strukturen in `tests/fixtures/`.

## Abhängigkeiten

- DARFST: `common`, `xml.etree.ElementTree` (stdlib), `lxml`
- NICHT: `planpro_parser`, `ds_client`, andere Transformer, Base-Container
