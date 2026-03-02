# AGENTS.md – transformers/_template/

## Rolle

Du erzeugst einen neuen Transformer auf Basis dieser Vorlage.

## Regeln

- Du MUSST `_template/` kopieren – niemals direkt darin arbeiten.
- Du MUSST den Package-Ordner zu `<name_snake>/` umbenennen.
- Du MUSST Domänenlogik in `transform.py` isolieren.
- Du MUSST mindestens 5 Unit-Tests schreiben.
- Du darfst NIEMALS HTTP-Calls, DB-Zugriffe oder externes I/O einbauen.
- Du MUSST `common.logging`, `common.config`, `common.provenance` verwenden.

## Schritte

1. Template kopieren + umbenennen
2. `transform.py` implementieren:
   ```python
   @dataclass
   class TransformResult:
       objects: list[dict]
       input_refs: list[str]
       output_refs: list[str]
   def transform(input_data: ...) -> TransformResult: ...
   ```
3. `main.py` anpassen (Import-Pfad, Name, Version)
4. Tests schreiben (`@pytest.mark.unit`)
5. Fixtures anlegen (echte/echt-nahe PlanPro-Daten)
6. `pyproject.toml` anpassen

## Abhängigkeiten

- DARFST: `common`, `planpro_parser`
- NICHT: `ds_client`, andere Transformer, Base-Container
