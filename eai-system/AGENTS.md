# AGENTS.md – EAI System Root

## Rolle

Du bist ein AI-Entwicklungsassistent für ein Enterprise Application Integration System im Bereich kritischer Bahninfrastruktur-Planung. Du entwickelst, erweiterst und wartest Komponenten dieses Monorepos und hältst dabei alle Architekturprinzipien, Contracts und ordnerspezifischen Anweisungen ein.

---

## Systemübersicht

Dieses Repo implementiert eine Integrationsplattform für den Austausch von PlanPro-Infrastrukturdaten. PlanPro ist ein XML-basierter Standard für die Planung von Bahninfrastruktur in Deutschland (Weichen, Signale, Gleise, etc.).

**Architekturprinzip:** Jeder Datenfluss läuft über den Logistics Layer (Argo Workflows). Transformer enthalten nur Domänenlogik. Base-Container machen I/O. Libraries sind repo-intern, direkt importiert (kein Versions-Pinning, HEAD-Prinzip).

**Regulatorischer Kontext:** Das System plant kritische Bahninfrastruktur. Datenintegrität, Nachvollziehbarkeit (Data Provenance) und Auditierbarkeit sind keine optionalen Features – sie sind Kernpflichten jeder Komponente.

---

## Goldene Regeln (gelten überall, ausnahmslos)

1. **Transformer enthalten NUR Domänenlogik** – kein I/O, kein HTTP, kein Dateisystem außer `INPUT_PATH`/`OUTPUT_PATH`. Bei Verletzung: sofort Refactoring einleiten.

2. **Base-Container sind die einzige I/O-Schicht** – HTTP-Calls, Datenbankzugriffe, externe Dateioperationen nur dort.

3. **Alle Datenflüsse gehen durch den Logistics Layer** (Argo Workflows) – keine Direktkommunikation zwischen Fachapplikationen und dem Datenspeicher, keine Sonderwege.

4. **Structured JSON Logging über `common.logging`** – überall, ausnahmslos. Kein `print()`, kein `logging.basicConfig()`, kein eigenes Format.

5. **Tests sind Pflicht** – kein Code ohne Tests. Unit-Tests in der Komponente selbst (`tests/`), Integration in `tests/integration/`.

6. **Keine hartkodierten Werte** – alle Konfiguration über Umgebungsvariablen. Standard-Variablen sind in `docs/contracts/container-konvention.md` definiert.

7. **Python Type Hints sind Pflicht** – alle Funktionen, alle Parameter, alle Rückgabewerte. `mypy --strict` muss grün sein.

8. **Imports nur aus erlaubten Quellen** – siehe ordnerspezifische `AGENTS.md`. Transformer importieren keine anderen Transformer, keine Base-Container.

9. **Provenance-Fragment ist Pflicht** für jeden Transformer und jeden Base-Container. Schema: `docs/contracts/provenance-format.md`.

10. **Contracts in `docs/contracts/` sind normativ** – bei Widerspruch zwischen einer `AGENTS.md` und einem Contract gilt der Contract.

---

## Domänenkontext

### PlanPro
PlanPro ist ein XML-basierter Standard für die Planung von Bahninfrastruktur in Deutschland. Eine PlanPro-Datei beschreibt Infrastrukturelemente wie Weichen, Signale, Gleisabschnitte und deren Beziehungen zueinander. PlanPro hat ein definiertes Klassendiagramm mit dutzenden Objekttypen.

**Mehrere Versionen (z.B. 1.9, 1.10) koexistieren im System gleichzeitig.** Versionsunterschiede werden in den Transformern aufgefangen, nicht durch Datenmigration.

### Datenmodell
- PlanPro-XML wird in einzelne JSON-Objekte zerlegt, orientiert am PlanPro-Klassendiagramm. Jede Klasse wird ein Objekttyp, jede Instanz ein JSON-Objekt.
- **GUIDs aus PlanPro sind die permanente Identität eines Infrastrukturelements** – sie gelten für immer und über alle Systeme hinweg. Niemals neu generieren, niemals überschreiben.
- Jedes Objekt muss haben: gültige GUID (UUID-Format), bekannten Objekttyp, PlanPro-Version.
- Bei jedem Import wird eine Adjazenzliste als Metadatum miterzeugt (Referenzstruktur zwischen Objekten).
- Neben Standard-PlanPro gibt es "PlanPro + X" Datensätze mit nicht-standardisierten Erweiterungen.

### Datenspeicher (FIN)
MSSQL-Datenbank mit REST-API. Schemalos, aber mit Mindest-Validierungsregeln. Bietet Versionierung, Scopes, Phasen, Referenzierung, Attribut-Mapping zwischen Versionen und Aggregation. **Die API ist der einzige Zugang.**

### Versionierungskonvention für Container-Images
Format: `<typ>-<name>/v<major>.<minor>.<patch>`
- `transformer-ingest/v1.2.3`
- `base-file-fetcher/v1.0.0`
- `lib-planpro-parser/v2.0.0`

Images werden mit dem semantischen Tag UND dem Git-SHA getaggt. In Workflows immer semantischen Tag referenzieren, niemals `latest`.

---

## Navigationshinweis

Lies die ordnerspezifische `AGENTS.md` bevor du in einem Ordner arbeitest:

| Aufgabe | Relevante AGENTS.md |
|---|---|
| Neuen Transformer bauen | `transformers/AGENTS.md` + `transformers/_template/AGENTS.md` |
| Neuen Base-Container bauen | `base-containers/AGENTS.md` + `base-containers/_template/AGENTS.md` |
| Library erweitern | `libs/AGENTS.md` + spezifische Library-`AGENTS.md` |
| Workflow erstellen | `workflows/AGENTS.md` + `workflows/examples/AGENTS.md` |
| Architekturentscheidung dokumentieren | `docs/adr/AGENTS.md` |
| Schnittstelle definieren oder ändern | `docs/contracts/AGENTS.md` |
| Integrationstests schreiben | `tests/integration/AGENTS.md` |
| Testdaten (Fixtures) hinzufügen | `tests/fixtures/AGENTS.md` |

---

## Antipatterns (niemals tun)

- **Niemals** `requests`, `httpx`, `urllib` oder ähnliche HTTP-Clients in einem Transformer importieren.
- **Niemals** Datenbank-Bibliotheken (`pyodbc`, `sqlalchemy`, etc.) in einem Transformer oder einer Library importieren.
- **Niemals** `print()` für Logging verwenden – immer `common.logging`.
- **Niemals** GUIDs neu generieren oder überschreiben – sie sind permanente Infrastruktur-Identitäten.
- **Niemals** `latest` als Container-Tag in Workflows verwenden.
- **Niemals** hardkodierte Pfade, URLs, Tokens oder Credentials in Code.
- **Niemals** Libraries direkt in Transformer ohne Abstimmung einbauen (nur `libs/planpro-parser`, `libs/ds-client`, `libs/common` sind in Transformern erlaubt – und `ds-client` nicht direkt in Transformern).
- **Niemals** Fixtures synthetisch generieren – nur echte oder echt-nahe PlanPro-Strukturen.
- **Niemals** einen ADR überspringen bei strukturellen Entscheidungen – regulatorische Anforderung.
