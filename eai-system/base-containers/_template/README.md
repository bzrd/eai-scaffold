# base-containers/_template – Kopiervorlage für neue Base-Container

Vorlage für neue Base-Container. **Nicht direkt verwenden – immer kopieren.**

## Schnellstart

```bash
cp -r base-containers/_template base-containers/<name-kebab>
mv base-containers/<name-kebab>/_template base-containers/<name-kebab>/<name_snake>
```

| Datei | Was ändern |
|---|---|
| `<name_snake>/` (Ordner) | Umbenennen |
| `main.py` | Container-Name, Import-Pfad |
| `handler.py` | I/O-Logik implementieren |
| `tests/test_handler.py` | Tests (alles mocken) |
| `pyproject.toml` | Name, Abhängigkeiten |

## Checkliste

- [ ] I/O in `handler.py`, Retry für transiente Fehler
- [ ] Unit-Tests mit gemocktem I/O
- [ ] Provenance-Fragment erzeugt
- [ ] `mypy --strict` grün
