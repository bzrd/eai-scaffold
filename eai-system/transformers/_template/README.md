# transformers/_template – Kopiervorlage für neue Transformer

Vorlage für neue Transformer. **Nicht direkt verwenden – immer kopieren.**

## Schnellstart

```bash
cp -r transformers/_template transformers/<name-kebab>
mv transformers/<name-kebab>/_template transformers/<name-kebab>/<name_snake>
```

| Datei | Was ändern |
|---|---|
| `<name_snake>/` (Ordner) | Umbenennen |
| `main.py` | Transformer-Name, Import-Pfad, I/O |
| `transform.py` | Domänenlogik implementieren |
| `tests/test_transform.py` | Tests für Domänenlogik |
| `pyproject.toml` | Name, Abhängigkeiten |
| `README.md` | Zweck, I/O-Format |

## Checkliste

- [ ] Template kopiert, Ordner umbenannt
- [ ] `transform.py` enthält nur reine Domänenlogik
- [ ] `main.py` folgt Standard-Entrypoint-Pattern
- [ ] Mindestens 5 Unit-Tests
- [ ] Fixtures aus echten/echt-nahen PlanPro-Daten
- [ ] `mypy --strict` + `ruff check` grün
