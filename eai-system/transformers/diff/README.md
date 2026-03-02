# transformers/diff – Differenz-Transformer

Vergleicht zwei Stände von PlanPro-Objekten per GUID und erzeugt einen strukturierten Diff-Report.

## I/O

- Input: Zwei JSON-Dateien (Stand 1 und Stand 2) unter `INPUT_PATH`
- Output: `{"added": [...], "removed": [...], "modified": [...], "unchanged_count": N}` unter `OUTPUT_PATH`
- Git-Tag: `transformer-diff/v<major>.<minor>.<patch>`

## Checkliste

- [ ] Diff GUID-basiert (nicht Index-basiert)
- [ ] Added, Removed, Modified korrekt klassifiziert
- [ ] Modified enthält feldweise Änderungen
- [ ] Provenance-Fragment erzeugt
