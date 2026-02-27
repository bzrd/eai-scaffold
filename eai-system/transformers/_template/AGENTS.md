# AGENTS.md – transformers/_template/

## Rolle

Du erzeugst einen neuen Transformer auf Basis dieser Vorlage. Du kopierst das Template, benennst es um, implementierst die Domänenlogik und schreibst Tests.

---

## Regeln

- Du MUSST das Template-Verzeichnis kopieren, nicht direkt im `_template/` arbeiten.
- Du MUSST den Package-Ordner von `_template/` zu `<name_snake>/` umbenennen.
- Du MUSST `main.py` als Entrypoint beibehalten und dem Standard-Ablauf folgen.
- Du MUSST die Domänenlogik in `transform.py` isolieren – nicht in `main.py`.
- Du MUSST mindestens 5 Unit-Tests schreiben (Happy Path, Edge Cases, Error Cases).
- Du darfst NIEMALS das `_template/`-Verzeichnis selbst modifizieren – es ist die Vorlage für alle.
- Du darfst NIEMALS HTTP-Calls, Datenbankzugriffe oder externes I/O einbauen.
- Du MUSST `common.logging`, `common.config` und `common.provenance` verwenden.

---

## Patterns

### Schritt-für-Schritt-Anleitung

1. **Template kopieren:**
   ```bash
   cp -r transformers/_template transformers/<name-kebab>
   mv transformers/<name-kebab>/_template transformers/<name-kebab>/<name_snake>
   ```

2. **`transform.py` implementieren:**
   ```python
   # transform.py – reine Domänenlogik
   from dataclasses import dataclass

   @dataclass
   class TransformResult:
       objects: list[dict]
       input_refs: list[str]
       output_refs: list[str]

   def transform(input_data: ...) -> TransformResult:
       # Hier die Domänenlogik implementieren
       ...
   ```

3. **`main.py` anpassen:**
   - Import-Pfad auf neuen Package-Namen ändern
   - Transformer-Name und Version setzen
   - Input-Deserialisierung implementieren
   - Output-Serialisierung implementieren

4. **Tests schreiben:**
   ```python
   # tests/test_transform.py
   import pytest
   from <name_snake>.transform import transform

   @pytest.mark.unit
   def test_transform_happy_path(sample_input):
       result = transform(sample_input)
       assert len(result.objects) > 0
       assert all(obj["guid"] for obj in result.objects)
   ```

5. **Fixtures anlegen:** Testdaten in `tests/fixtures/` – echte oder echt-nahe Daten, keine synthetischen.

6. **`pyproject.toml` anpassen:**
   ```toml
   [project]
   name = "<name-kebab>"
   version = "0.1.0"
   requires-python = ">=3.12"
   dependencies = ["common", "planpro-parser"]
   ```

7. **`README.md` aktualisieren** mit Zweck, Input/Output-Format, Beispiel.

---

## Antipatterns

- **Nicht direkt im `_template/` arbeiten** – immer kopieren.
- **Keine Domänenlogik in `main.py`** – `main.py` ist nur Orchestrierung.
- **Kein I/O in `transform.py`** – die Funktion bekommt Daten rein und gibt Daten zurück.
- **Keine synthetischen Testdaten** – echte oder echt-nahe PlanPro-Strukturen verwenden.

---

## Testanforderungen

- Framework: `pytest`
- Testort: `<neuer-transformer>/tests/`
- Alle Tests mit `@pytest.mark.unit` markieren
- Fixtures in `tests/fixtures/` oder aus `tests/fixtures/` (Repo-Root)

**Mindestanforderungen:**
1. Happy Path: gültige Eingabe → korrekte Ausgabe
2. Edge Case: minimale Eingabe
3. Edge Case: leere Eingabe
4. Error Case: ungültige Eingabe
5. GUID-Integrität: GUIDs im Output stimmen mit Input überein

---

## Abhängigkeiten

- Du DARFST importieren: `common`, `planpro_parser`
- Du darfst NICHT importieren: `ds_client`, andere Transformer, Base-Container

---

## Kontext

Jeder neue Transformer wird Teil des Logistics Layer (Argo Workflows). Er läuft als Container in einem Workflow-Step. Input kommt von einem vorherigen Step (typischerweise ein Base-Container) als Datei, Output geht als Datei an den nächsten Step. Der Transformer weiß nichts über Argo, Kubernetes oder die Infrastruktur – er sieht nur `INPUT_PATH` und `OUTPUT_PATH`.
