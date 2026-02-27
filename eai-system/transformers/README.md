# transformers/ – Domänenlogik-Container

## Zweck

Dieser Ordner enthält alle Transformer. Ein Transformer ist ein eigenständiger Container der ausschließlich Domänenlogik enthält: PlanPro-XML zerlegen, Diffs berechnen, Daten transformieren. Transformer machen **kein I/O** – kein HTTP, keine Datenbankzugriffe, kein Dateisystem außer `INPUT_PATH` und `OUTPUT_PATH`.

---

## Struktur

```
transformers/
├── planpro-ingest/    # PlanPro-XML → JSON-Objekte für den Datenspeicher
├── planpro-export/    # JSON-Objekte → PlanPro-XML für Fachapplikationen
├── diff/              # Vergleicht zwei Stände und erzeugt einen Diff-Report
├── _template/         # Kopiervorlage für neue Transformer
├── README.md          # Diese Datei
└── AGENTS.md          # Anweisungen für AI-Agenten
```

Jeder Transformer hat folgende innere Struktur:

```
<transformer-name>/
├── <transformer_name>/
│   ├── __init__.py
│   ├── main.py          # Entrypoint (Config, Logger, I/O, Provenance)
│   └── transform.py     # Reine Domänenlogik
├── tests/
│   ├── conftest.py
│   ├── test_transform.py
│   └── fixtures/        # Transformer-spezifische Testdaten
├── pyproject.toml
└── README.md
```

---

## Konventionen

- **Ordnername:** `kebab-case` (z.B. `planpro-ingest`)
- **Python-Package:** `snake_case` (z.B. `planpro_ingest`)
- **Entrypoint:** Immer `main.py` mit dem Standard-Ablauf (siehe `_template/`)
- **Domänenlogik:** Immer in `transform.py` – getrennt vom Entrypoint
- **Exit-Codes:** `0` = Erfolg, `1` = Fachlicher Fehler, `2` = Technischer Fehler
- **Git-Tag:** `transformer-<name>/v<major>.<minor>.<patch>` (z.B. `transformer-ingest/v1.2.3`)
- **Container-Image:** `registry.intern/transformer-<name>:<version>`

---

## Abhängigkeiten

Transformer dürfen importieren:
- `libs/common` (Logging, Config, Provenance, Validierung)
- `libs/planpro-parser` (XML-Verarbeitung)

Transformer dürfen **NICHT** importieren:
- `libs/ds-client` (I/O-Library, nur für Base-Container)
- Andere Transformer
- Base-Container
- Externe Libraries ohne Abstimmung

---

## Beispiel: Neuen Transformer anlegen

1. `cp -r transformers/_template transformers/mein-transformer`
2. Package umbenennen: `_template/` → `mein_transformer/`
3. `transform.py` mit Domänenlogik implementieren
4. Tests in `tests/` schreiben
5. `README.md` aktualisieren
6. `pyproject.toml` anpassen (Name, Abhängigkeiten)

Detaillierte Anleitung: `transformers/_template/README.md`

---

## Checkliste für neue Transformer

- [ ] `main.py` folgt dem Standard-Entrypoint-Pattern
- [ ] Domänenlogik in `transform.py` isoliert
- [ ] Kein I/O (kein HTTP, kein DB, kein Dateisystem außer `INPUT_PATH`/`OUTPUT_PATH`)
- [ ] Structured JSON Logging über `common.logging`
- [ ] Provenance-Fragment wird erzeugt
- [ ] Unit-Tests in `tests/` vorhanden
- [ ] Alle Type Hints vollständig
- [ ] `mypy --strict` grün
- [ ] `README.md` beschreibt den Transformer
- [ ] Git-Tag nach Konvention gesetzt
