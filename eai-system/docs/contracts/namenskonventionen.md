# Contract: Namenskonventionen

**Version:** 1.0
**Stand:** 2026-02-27
**Status:** Accepted

---

## Geltungsbereich

Gilt für **alle Benennungen** im gesamten Repository: Container-Images, Git-Tags, Workflows, Ordner, Python-Packages, Umgebungsvariablen.

---

## Container-Images

### Format

```
registry.intern/<typ>-<name>:<version>
```

### Anforderungen

1. Container-Images MÜSSEN dem Format `registry.intern/<typ>-<name>:<version>` folgen.
2. `<typ>` MUSS einer der Werte `transformer` oder `base` sein.
3. `<name>` MUSS in `kebab-case` sein.
4. `<version>` MUSS eine semantische Version sein (`v<major>.<minor>.<patch>`).
5. Zusätzlich MUSS jedes Image mit dem Git-SHA getaggt werden.

### Beispiele

```
registry.intern/transformer-ingest:v1.2.3
registry.intern/transformer-ingest:abc123f
registry.intern/base-file-fetcher:v1.0.0
registry.intern/base-ds-writer:v2.1.0
```

---

## Git-Tags

### Format

```
<typ>-<name>/v<major>.<minor>.<patch>
```

### Anforderungen

6. Git-Tags MÜSSEN dem Format `<typ>-<name>/v<major>.<minor>.<patch>` folgen.
7. `<typ>` MUSS einer der Werte `transformer`, `base`, `lib`, `workflow` sein.
8. Semantic Versioning MUSS eingehalten werden: Major für Breaking Changes, Minor für neue Features, Patch für Bugfixes.

### Beispiele

```
transformer-ingest/v1.2.3
transformer-diff/v0.1.0
base-file-fetcher/v1.0.0
lib-planpro-parser/v2.0.0
workflow-import/v1.1.0
```

---

## Workflow-Namen

### Format

```
<kategorie>-<beschreibung>
```

### Anforderungen

9. Workflow-Namen MÜSSEN dem Format `<kategorie>-<beschreibung>` folgen.
10. `<kategorie>` MUSS einer der Werte `import`, `export`, `diff`, `sync` sein.
11. `<beschreibung>` MUSS in `kebab-case` sein.

### Beispiele

```
import-planpro
export-system-a
diff-entwurf-genehmigung
sync-external-catalog
```

---

## Ordnernamen

### Anforderungen

12. Ordnernamen MÜSSEN in `kebab-case` sein.

### Beispiele

```
planpro-ingest     (korrekt)
planpro_ingest     (FALSCH)
PlanProIngest      (FALSCH)
```

---

## Python-Packages

### Anforderungen

13. Python-Package-Namen MÜSSEN in `snake_case` sein.
14. Der Package-Name MUSS dem Ordnernamen entsprechen, mit `_` statt `-`.

### Beispiele

```
planpro_parser     (Ordner: planpro-parser)
ds_client          (Ordner: ds-client)
planpro_ingest     (Ordner: planpro-ingest)
file_fetcher       (Ordner: file-fetcher)
```

---

## Umgebungsvariablen

### Anforderungen

15. Umgebungsvariablen MÜSSEN in `UPPER_SNAKE_CASE` sein.

### Beispiele

```
CORRELATION_ID
LOG_LEVEL
INPUT_PATH
OUTPUT_PATH
DS_API_URL
DS_API_TOKEN
```

---

## Zusammenfassung

| Element | Format | Beispiel |
|---|---|---|
| Container-Image | `registry.intern/<typ>-<name>:<version>` | `registry.intern/transformer-ingest:v1.2.3` |
| Git-Tag | `<typ>-<name>/v<major>.<minor>.<patch>` | `transformer-ingest/v1.2.3` |
| Workflow-Name | `<kategorie>-<beschreibung>` | `import-planpro` |
| Ordnername | `kebab-case` | `planpro-ingest` |
| Python-Package | `snake_case` | `planpro_ingest` |
| Umgebungsvariable | `UPPER_SNAKE_CASE` | `CORRELATION_ID` |
