# libs/planpro-parser – PlanPro XML Parser

## Zweck

Zerlegt PlanPro-XML in typisierte Python-Dataclasses (eine Klasse pro Elementtyp). Der **Elementkatalog in `AGENTS.md`** ist die normative Quelle aller Typendefinitionen.

## Struktur

```
planpro-parser/
├── planpro_parser/
│   ├── __init__.py      # Öffentliche API
│   ├── parser.py        # parse_xml(str) → ParseResult
│   ├── validator.py     # GUID-Format, Objekttyp prüfen
│   ├── types.py         # ⚠ aus Katalog generiert – Dataclasses + ParseResult
│   └── constants.py     # ⚠ aus Katalog generiert – ObjectType, XPATH_MAP
└── tests/
    ├── conftest.py
    ├── test_parser.py
    ├── test_validator.py
    └── test_types.py    # ⚠ aus Katalog generiert
```

⚠ = bei Katalogerweiterung neu generieren.

## Neuen Typ hinzufügen

1. Eintrag im Elementkatalog (`AGENTS.md`) anlegen
2. `types.py` regenerieren (neues Dataclass)
3. `constants.py` regenerieren (`ObjectType` + `XPATH_MAP`)
4. `test_types.py` regenerieren (neue Testklasse)

## Checkliste

- [ ] Katalogeintrag vollständig (xml_path, guid_xpath, alle Felder)
- [ ] `types.py`, `constants.py`, `test_types.py` regeneriert
- [ ] `mypy --strict` grün, alle Tests grün
- [ ] Neuer Typ in `__init__.py` exportiert
