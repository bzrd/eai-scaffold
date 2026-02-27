# AGENTS.md – tests/

## Rolle

Du erstellst oder pflegst Integrationstests und geteilte Testdaten (Fixtures). Integrationstests testen mehrere Komponenten zusammen gegen eine echte Umgebung.

---

## Regeln

- Du MUSST Integrationstests mit `@pytest.mark.integration` markieren.
- Du MUSST Testdaten vor dem Test anlegen und nach dem Test aufräumen.
- Du darfst NIEMALS Fixtures synthetisch generieren – nur echte oder echt-nahe PlanPro-Daten.
- Du MUSST die echte API testen, keine Mocks (in Integrationstests).
- Du MUSST sicherstellen, dass Integrationstests nicht den Produktivdatenbestand verändern.

---

## Navigationshinweis

| Aufgabe | Ort |
|---|---|
| Integrationstests schreiben | `tests/integration/` |
| Geteilte Fixtures verwalten | `tests/fixtures/` |
| Unit-Tests für eine Library | `libs/<name>/tests/` |
| Unit-Tests für einen Transformer | `transformers/<name>/tests/` |
| Unit-Tests für einen Base-Container | `base-containers/<name>/tests/` |
