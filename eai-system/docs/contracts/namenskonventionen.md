# Contract: Namenskonventionen

**Version:** 1.0 | **Status:** Accepted

Gilt für alle Benennungen im gesamten Repository.

## Übersicht

| Element | Format | Beispiel |
|---|---|---|
| Container-Image | `registry.intern/<typ>-<name>:<version>` | `registry.intern/transformer-ingest:v1.2.3` |
| Git-Tag | `<typ>-<name>/v<major>.<minor>.<patch>` | `transformer-ingest/v1.2.3` |
| Workflow-Name | `<kategorie>-<beschreibung>` | `import-planpro` |
| Ordnername | `kebab-case` | `planpro-ingest` |
| Python-Package | `snake_case` | `planpro_ingest` |
| Umgebungsvariable | `UPPER_SNAKE_CASE` | `CORRELATION_ID` |

## Anforderungen

1. Container-Images: `registry.intern/<typ>-<name>:<version>`, `<typ>` = `transformer`/`base`.
2. Jedes Image MUSS zusätzlich mit Git-SHA getaggt werden.
3. Git-Tags: `<typ>-<name>/v<major>.<minor>.<patch>`, `<typ>` = `transformer`/`base`/`lib`/`workflow`.
4. Semantic Versioning: Major = Breaking, Minor = Feature, Patch = Bugfix.
5. Workflow-Namen: `<kategorie>-<beschreibung>`, Kategorien: `import`/`export`/`diff`/`sync`.
6. Ordnernamen: `kebab-case`.
7. Python-Package-Namen: `snake_case`, entspricht Ordnername mit `_` statt `-`.
8. Umgebungsvariablen: `UPPER_SNAKE_CASE`.
