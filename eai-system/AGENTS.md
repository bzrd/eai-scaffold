# AGENTS.md – EAI System Root

## Rolle

AI-Entwicklungsassistent für eine Bahninfrastruktur-Integrationsplattform. Hält Architekturprinzipien, Contracts und ordnerspezifische Anweisungen ein.

## Goldene Regeln

1. **Transformer = nur Domänenlogik** – kein I/O, kein HTTP, kein DB außer `INPUT_PATH`/`OUTPUT_PATH`.
2. **Base-Container = einzige I/O-Schicht** – HTTP, Datenbankzugriffe, externe Dateioperationen.
3. **Alle Flows durch Argo Workflows** – keine Direktkommunikation Fachapplikation ↔ Datenspeicher.
4. **`common.logging` überall** – kein `print()`, kein `logging.basicConfig()`.
5. **Tests sind Pflicht** – Unit-Tests in Komponente, Integration in `tests/integration/`.
6. **Keine hartkodierten Werte** – alles über Umgebungsvariablen.
7. **Type Hints Pflicht** – `mypy --strict` grün.
8. **Keine verbotenen Imports** – siehe ordnerspezifische AGENTS.md.
9. **Provenance-Fragment Pflicht** – Schema: `docs/contracts/provenance-format.md`.
10. **Contracts sind normativ** – `docs/contracts/` schlägt jede AGENTS.md.

## Domänenkontext

- **PlanPro:** XML-Standard für Bahninfrastruktur (Weichen, Signale, Gleise). Versionen 1.9/1.10 koexistieren.
- **GUIDs:** Permanente Infrastruktur-Identitäten. Niemals neu generieren oder verändern.
- **Datenspeicher (FIN):** MSSQL + REST-API, schemalos mit Mindestvalidierung. Nur via `ds-client`.
- **Container-Versionierung:** `<typ>-<name>/v<major>.<minor>.<patch>`, niemals `latest` in Workflows.

## Navigation

| Aufgabe | Relevante AGENTS.md |
|---|---|
| Neuen Transformer | `transformers/AGENTS.md` + `transformers/_template/AGENTS.md` |
| Neuen Base-Container | `base-containers/AGENTS.md` + `base-containers/_template/AGENTS.md` |
| Library erweitern | `libs/AGENTS.md` + Library-`AGENTS.md` |
| Workflow erstellen | `workflows/AGENTS.md` |
| Contract ändern | `docs/contracts/` + ADR |
