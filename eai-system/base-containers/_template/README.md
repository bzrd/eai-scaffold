# base-containers/_template – Kopiervorlage für neue Base-Container

## Zweck

Kopiervorlage für neue Base-Container. Enthält die Standardstruktur, den Standard-Entrypoint und das Standard-Testpattern. **Wird nicht direkt verwendet, sondern kopiert und angepasst.**

Der entscheidende Unterschied zu Transformern: Base-Container **DÜRFEN I/O machen** (HTTP, Dateisystem, Datenbank). Sie sind die Brücke zwischen der Außenwelt und den Transformern.

---

## Struktur

```
_template/
├── _template/
│   ├── __init__.py
│   ├── main.py          # Standard-Entrypoint
│   └── handler.py       # Hier die I/O-Logik implementieren
├── tests/
│   ├── conftest.py
│   ├── test_handler.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## Anleitung: Neuen Base-Container erzeugen

### 1. Template kopieren
```bash
cp -r base-containers/_template base-containers/mein-container
```

### 2. Package umbenennen
```bash
mv base-containers/mein-container/_template base-containers/mein-container/mein_container
```

### 3. `handler.py` implementieren
Die I/O-Logik: HTTP-Calls, Datei-Operationen, API-Zugriffe.

### 4. Tests schreiben
Alle I/O mocken – Unit-Tests machen keine echten externen Calls.

### 5. Dateien anpassen
- `main.py`: Container-Name, Import-Pfad
- `pyproject.toml`: Name, Abhängigkeiten
- `README.md`: Beschreibung

---

## Was muss geändert werden

| Datei | Was anpassen |
|---|---|
| `_template/` (Ordner) | Umbenennen zu `<name_snake>/` |
| `main.py` | Container-Name, Import-Pfad |
| `handler.py` | Komplette I/O-Logik |
| `tests/test_handler.py` | Tests für die I/O-Logik (gemockt) |
| `pyproject.toml` | Name, Version, Abhängigkeiten |
| `README.md` | Beschreibung |

---

## Checkliste

- [ ] Template kopiert und umbenannt
- [ ] `handler.py` implementiert (I/O-Logik)
- [ ] Retry-Logik für transiente Fehler
- [ ] Structured JSON Logging
- [ ] Provenance-Fragment
- [ ] Unit-Tests mit gemocktem I/O
- [ ] Type Hints vollständig
- [ ] `mypy --strict` grün
