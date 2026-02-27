# transformers/_template – Kopiervorlage für neue Transformer

## Zweck

Dieser Ordner ist die Kopiervorlage für jeden neuen Transformer. Er enthält die Standardstruktur, den Standard-Entrypoint und das Standard-Testpattern. **Dieser Ordner wird nicht direkt verwendet, sondern kopiert und angepasst.**

---

## Struktur

```
_template/
├── _template/
│   ├── __init__.py          # → umbenennen nach <transformer_name>/
│   ├── main.py              # Standard-Entrypoint – nur Orchestrierung anpassen
│   └── transform.py         # Hier die Domänenlogik implementieren
├── tests/
│   ├── conftest.py          # Fixtures und Test-Setup
│   ├── test_transform.py    # Standard-Testpattern
│   └── fixtures/            # Transformer-spezifische Testdaten
├── pyproject.toml           # Name und Abhängigkeiten anpassen
└── README.md                # Beschreibung des neuen Transformers
```

---

## Anleitung: Neuen Transformer erzeugen

### 1. Template kopieren
```bash
cp -r transformers/_template transformers/mein-neuer-transformer
```

### 2. Package umbenennen
```bash
mv transformers/mein-neuer-transformer/_template transformers/mein-neuer-transformer/mein_neuer_transformer
```

### 3. `transform.py` implementieren
Die Datei `transform.py` enthält die reine Domänenlogik. Kein I/O, kein Logging – nur Datenverarbeitung.

### 4. `main.py` anpassen
- Transformer-Namen und -Version aktualisieren
- Import von `transform.py` anpassen
- Input-/Output-Serialisierung implementieren

### 5. Tests schreiben
- `test_transform.py` für die Domänenlogik
- Fixtures in `tests/fixtures/` anlegen (echte oder echt-nahe Daten)

### 6. `pyproject.toml` anpassen
- Package-Name aktualisieren
- Abhängigkeiten eintragen

### 7. `README.md` aktualisieren
- Zweck beschreiben
- Input/Output-Format dokumentieren
- Beispiel ergänzen

---

## Konventionen

- **Ordnername:** `kebab-case` (z.B. `mein-neuer-transformer`)
- **Package-Name:** `snake_case` (z.B. `mein_neuer_transformer`)
- **Entrypoint:** `main.py` mit Standard-Ablauf
- **Domänenlogik:** `transform.py` isoliert
- **Git-Tag:** `transformer-<name>/v1.0.0`

---

## Was muss geändert werden

| Datei | Was anpassen |
|---|---|
| `_template/` (Ordner) | Umbenennen zu `<name_snake>/` |
| `main.py` | Transformer-Name, Import-Pfad, I/O-Logik |
| `transform.py` | Komplette Domänenlogik implementieren |
| `tests/test_transform.py` | Tests für die spezifische Logik |
| `tests/fixtures/` | Testdaten anlegen |
| `pyproject.toml` | Name, Version, Abhängigkeiten |
| `README.md` | Beschreibung, Input/Output, Beispiele |

---

## Checkliste für den neuen Transformer

- [ ] Template kopiert und umbenannt
- [ ] `transform.py` implementiert (reine Domänenlogik)
- [ ] `main.py` angepasst (Name, Version, I/O)
- [ ] Unit-Tests geschrieben
- [ ] Fixtures angelegt (echte oder echt-nahe Daten)
- [ ] `pyproject.toml` angepasst
- [ ] `README.md` aktualisiert
- [ ] Kein I/O in `transform.py` (kein HTTP, DB, Dateisystem)
- [ ] Structured JSON Logging über `common.logging`
- [ ] Provenance-Fragment wird erzeugt
- [ ] Alle Type Hints vollständig
- [ ] `mypy --strict` grün
- [ ] `ruff check` grün
