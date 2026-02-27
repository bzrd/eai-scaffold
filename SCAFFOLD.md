Prompt: EAI Monorepo Scaffold Generator
Kontext
Du erstellst das Grundgerüst eines Monorepos für ein Enterprise Application Integration (EAI) System im Bereich Bahninfrastruktur-Planung. Das System dient dem Austausch von PlanPro-Daten zwischen heterogenen Fachapplikationen über eine zentrale Integrationsplattform.
Das System wird Jahrzehnte laufen und ist regulatorisch relevant. Entscheidungen priorisieren Langlebigkeit, Nachvollziehbarkeit und Wartbarkeit durch zukünftige Entwickler und AI-Agenten.
Technologie-Stack

Python 3.12+
Argo Workflows auf Kubernetes
Container-basierte Transformer (Docker)
MSSQL Datenspeicher mit REST-API (Plattform "FIN")
GitLab CI/CD
ArgoCD für Deployment
pytest als Test-Framework
ruff als Linter/Formatter
mypy für Type-Checking

Domänenkontext
PlanPro
PlanPro ist ein XML-basierter Standard für die Planung von Bahninfrastruktur in Deutschland. Eine PlanPro-Datei beschreibt Infrastrukturelemente wie Weichen, Signale, Gleisabschnitte und deren Beziehungen zueinander. PlanPro hat ein definiertes Klassendiagramm mit dutzenden Objekttypen. Der Standard wird aktiv weiterentwickelt, es existieren mehrere Versionen (z.B. 1.9, 1.10) gleichzeitig.
Datenmodell-Entscheidungen

PlanPro-XML wird in einzelne JSON-Objekte zerlegt, orientiert am PlanPro-Klassendiagramm. Jede Klasse wird ein Objekttyp, jede Instanz ein JSON-Objekt.
GUIDs aus PlanPro sind die permanente Identität eines Infrastrukturelements – sie gelten für immer und über alle Systeme hinweg.
Mehrere PlanPro-Versionen koexistieren im Speicher. Versionsunterschiede werden in den Transformern aufgefangen, nicht durch Datenmigration.
Der Datenspeicher ist schemalos (kein JSON-Schema in FIN), aber es gelten Mindest-Validierungsregeln: Jedes Objekt muss eine gültige GUID, einen bekannten Objekttyp und eine PlanPro-Version haben.
Neben PlanPro-Daten gibt es erweiterte Datensätze ("PlanPro + X") mit nicht-standardisierten Erweiterungen.
Bei jedem Import wird eine Adjazenzliste als Metadatum miterzeugt, die die Referenzstruktur zwischen den importierten Objekten abbildet.

Datenspeicher (FIN)
MSSQL-Datenbank mit REST-API. Speichert beliebige JSON-Objekte. Bietet Versionierung, Scopes, Phasen, Referenzierung zwischen Objekten, Attribut-Mapping zwischen Versionen und Aggregation. Die API ist der einzige Zugang zum Speicher.
Logistics Layer
Architektur-Constraint: Jegliche Anbindung externer Systeme erfolgt zwingend über den Logistics Layer (Argo Workflows). Keine direkten API-Zugriffe auf den Datenspeicher durch Fachapplikationen. Alle Datenflüsse sind asynchron.
Regulatorischer Kontext
Das System dient der Planung kritischer Bahninfrastruktur. Es gelten Anforderungen an Datenintegrität, Nachvollziehbarkeit (Data Provenance) und Auditierbarkeit. Jede Datenveränderung muss rückverfolgbar sein: Woher kamen die Daten, wann, durch welchen Transformer in welcher Version.
Architektur-Prinzipien

Jeder Transformer ist ein eigenständiger Container der nur Domänenlogik enthält
Transformer lesen Input von einem lokalen Dateipfad und schreiben Output auf einen lokalen Dateipfad
Transformer haben kein Wissen über Argo, Kubernetes oder die Infrastruktur
Transformer machen KEIN I/O (kein HTTP, kein Dateisystem außer INPUT_PATH/OUTPUT_PATH, kein Datenbankzugriff)
Base-Container übernehmen I/O (Dateien holen, API-Calls, Datenbank-Operationen)
Libraries werden repo-intern direkt importiert, nicht über Versionen gepinnt (HEAD-Prinzip)
Workflows werden als YAML oder Hera (Python SDK) definiert
Container-Images werden über Prefixed Git Tags versioniert
Alle Container folgen einem einheitlichen Vertrag (definiert in docs/contracts/container-konvention.md)

Versionierungskonvention
Container-Images werden über Prefixed Git Tags versioniert. Das Format ist:
<komponenten-typ>-<name>/v<major>.<minor>.<patch>
Beispiele:
transformer-ingest/v1.2.3
transformer-diff/v0.1.0
base-file-fetcher/v1.0.0
lib-planpro-parser/v2.0.0
workflow-import/v1.1.0
Semantic Versioning: Major für Breaking Changes, Minor für neue Features, Patch für Bugfixes.
CI reagiert auf Tags und baut selektiv:

Tags mit transformer-* triggern den Transformer-Build
Tags mit base-* triggern den Base-Container-Build
Tags mit lib-* triggern Library-Tests und alle abhängigen Container-Builds

Container-Images werden mit dem semantischen Tag UND dem Git-SHA getaggt:
registry.intern/transformer-ingest:v1.2.3
registry.intern/transformer-ingest:abc123f
In Workflows wird immer der semantische Tag referenziert, niemals latest.
Aufgabe
Erstelle die komplette Verzeichnisstruktur des Monorepos. Erstelle KEINE Implementierungsdateien (kein Python-Code, keine Dockerfiles, keine CI-Configs). Erstelle stattdessen:

README.md in jedem Ordner – beschreibt den Zweck des Ordners, die erwartete Struktur, Konventionen und Beispiele.
AGENTS.md in jedem Ordner – Anweisungen für AI-Agenten die in diesem Ordner arbeiten. Diese Dateien steuern wie ein AI-Agent Code erzeugt, welche Patterns er verwenden soll, welche Antipatterns er vermeiden muss und welche Abhängigkeiten gelten.
Projekt-Konfigurationsdateien die tatsächlich angelegt werden: pyproject.toml (Root), .pre-commit-config.yaml, Makefile, .gitignore

Verzeichnisstruktur
eai-system/
├── libs/
│   ├── planpro-parser/
│   ├── ds-client/
│   └── common/
├── transformers/
│   ├── planpro-ingest/
│   ├── planpro-export/
│   ├── diff/
│   └── _template/
├── base-containers/
│   ├── file-fetcher/
│   ├── file-pusher/
│   ├── http-trigger/
│   ├── ds-writer/
│   ├── ds-reader/
│   └── _template/
├── workflows/
│   ├── templates/
│   └── examples/
├── docker/
├── ci/
├── docs/
│   ├── adr/
│   ├── runbooks/
│   └── contracts/
└── tests/
    ├── integration/
    └── fixtures/
Anforderungen an README.md Dateien
Jede README.md muss enthalten:

Zweck – Ein Satz der beschreibt wofür dieser Ordner existiert
Struktur – Welche Dateien und Unterordner erwartet werden mit Erklärung
Konventionen – Namensgebung, Patterns, Coding-Standards die in diesem Ordner gelten
Abhängigkeiten – Welche Libraries oder anderen Teile des Repos hier genutzt werden dürfen
Beispiel – Ein konkretes Beispiel wie eine neue Komponente in diesem Ordner aussehen würde
Checkliste – Was muss erledigt sein bevor eine neue Komponente in diesem Ordner als fertig gilt

Anforderungen an AGENTS.md Dateien
Jede AGENTS.md muss enthalten:
Abschnitt: Rolle
Beschreibt in einem Satz was ein AI-Agent in diesem Ordner tut.
Abschnitt: Regeln
Strikte Anweisungen die der Agent befolgen MUSS. Formuliert als klare Gebote und Verbote. Beispiele:

"Du MUSST jeden Transformer mit einem main.py Entrypoint versehen"
"Du darfst NIEMALS HTTP-Calls, Datenbankzugriffe oder Dateisystem-Operationen außerhalb von INPUT_PATH und OUTPUT_PATH in einen Transformer einbauen"
"Du MUSST structured JSON Logging über die common Library verwenden"

Abschnitt: Patterns
Code-Patterns die der Agent verwenden soll, als Pseudocode oder Strukturbeschreibung. Beispiel:
Jeder Transformer folgt diesem Ablauf:
1. Config aus Umgebungsvariablen laden (common.config)
2. Logger initialisieren (common.logging)
3. Input lesen von INPUT_PATH
4. Transformation ausführen
5. Output schreiben nach OUTPUT_PATH
6. Provenance-Fragment erzeugen (common.provenance)
7. Exit 0 bei Erfolg, Exit 1 bei Fehler
Abschnitt: Antipatterns
Was der Agent NICHT tun darf, mit Begründung. Beispiele:

"Kein requests.get/post in Transformern – I/O gehört in Base-Container"
"Keine globalen Variablen für Zustand – Container sind stateless"
"Keine eigenen Logging-Formate – immer common.logging verwenden"
"Keine hartkodierten Pfade – immer über Umgebungsvariablen"

Abschnitt: Testanforderungen
Wie der Agent Tests schreiben muss:

Welches Framework (pytest)
Wo Tests liegen (tests/ Unterordner der Komponente)
Was getestet werden muss (Mindestanforderungen)
Wie Fixtures verwendet werden
Welche Assertion-Patterns erwartet werden

Abschnitt: Abhängigkeiten
Welche Imports erlaubt sind und welche nicht:

"Du DARFST importieren: libs/planpro-parser, libs/ds-client, libs/common"
"Du darfst NICHT importieren: andere Transformer, Base-Container, externe Libraries ohne Abstimmung"

Abschnitt: Kontext
Hintergrundwissen das der Agent braucht um gute Entscheidungen zu treffen. Hier wird der relevante Domänenkontext aus dem Abschnitt "Domänenkontext" dieses Prompts ordnerspezifisch zusammengefasst.
Anforderungen an spezifische Ordner
libs/planpro-parser/
Die zentrale Library für PlanPro XML Verarbeitung. Verantwortlichkeiten:

PlanPro XML zu JSON zerlegen, orientiert am Klassendiagramm
GUIDs extrahieren und validieren (UUID-Format)
Referenzen zwischen Objekten erkennen (ID-Refs in der XML)
PlanPro-Version aus XML ermitteln
Adjazenzliste aus den erkannten Referenzen erzeugen
Objekttyp-Erkennung anhand des Klassendiagramms

Ist die meistgenutzte Library im Repo. Wird von Import- und Export-Transformern, vom Diff-Transformer und potenziell von Validierungslogik verwendet.
AGENTS.md muss betonen: Diese Library hat KEIN Wissen über den Datenspeicher oder die API. Sie verarbeitet PlanPro-XML und erzeugt Python-Datenstrukturen. Keine Netzwerk-Calls, keine Dateisystem-Annahmen außer dem übergebenen XML-String oder Dateipfad.
libs/ds-client/
Typisierter Python-Client für die Datenspeicher REST-API. Verantwortlichkeiten:

CRUD-Operationen auf JSON-Objekte
Auth-Handling (Token-basiert)
Fehlerbehandlung mit eigenen Exception-Klassen
Typisierte Datenmodelle für API-Requests und Responses
Versionierungsoperationen (Stände abfragen, vergleichen)
Scope- und Phasen-Management

Wird von Base-Containern (ds-writer, ds-reader) genutzt, NICHT direkt von Transformern. AGENTS.md muss dieses Verbot explizit formulieren und begründen: Transformer haben keinen Netzwerkzugriff, der ds-client ist eine I/O-Library.
libs/common/
Shared Utilities die überall genutzt werden. Verantwortlichkeiten:

Strukturiertes JSON-Logging mit Correlation-ID, Timestamp, Component-Name, Log-Level
Provenance-Fragment-Erzeugung (Transformer-Name, Version, Input-Refs, Output-Refs, Timestamp)
Konfigurationshandling: Umgebungsvariablen lesen, validieren, typisiert bereitstellen
Shared Constants: Standard-Umgebungsvariablen-Namen, Objekttyp-Enums, Exit-Codes
Mindest-Validierung: GUID-Format prüfen, Objekttyp gegen bekannte Liste prüfen, PlanPro-Version vorhanden

AGENTS.md muss betonen: Diese Library darf KEINE Abhängigkeiten auf planpro-parser oder ds-client haben. Sie ist die unterste Schicht, von der alles andere abhängt.
transformers/_template/
Ein Template-Ordner der als Kopiervorlage für neue Transformer dient. Enthält:

main.py mit dem Standard-Entrypoint-Pattern (Config laden, Logger init, Input lesen, Transform, Output schreiben, Provenance, Exit)
Eine leere transform.py für die eigentliche Domänenlogik
tests/test_transform.py mit dem Standard-Testpattern
tests/fixtures/ als leerer Ordner für Testdaten
Eine README.md die beschreibt was zu ändern ist

Die AGENTS.md in diesem Ordner beschreibt wie ein Agent einen neuen Transformer erzeugt:

Template-Ordner kopieren
Ordner umbenennen nach Konvention
transform.py implementieren
Tests schreiben
Fixtures anlegen
README.md aktualisieren

base-containers/_template/
Analog zum Transformer-Template, aber für Base-Container. Der entscheidende Unterschied: Base-Container DÜRFEN I/O machen (HTTP, Dateisystem, Datenbank). Sie sind die Brücke zwischen der Außenwelt und den Transformern.
AGENTS.md muss den Unterschied zu Transformern klar machen und beschreiben welche Art von I/O erwartet wird: Dateien von externen Systemen holen/ablegen, REST-API-Calls gegen den Datenspeicher, Datenbank-Operationen gegen externe Systeme.
base-containers/ds-reader/ und base-containers/ds-writer/
Lesen bzw. schreiben Objekte gegen die Datenspeicher REST-API. Nutzen libs/ds-client. Diese Container sind die einzigen, die mit dem Datenspeicher kommunizieren.
base-containers/http-trigger/
Ein dauerlaufender FastAPI-Service, der Webhooks entgegennimmt und Argo-Workflows triggert. Anders als alle anderen Container ist dieser nicht ein Run-to-Completion-Container, sondern ein Long-Running-Service. AGENTS.md und README.md müssen diesen Unterschied betonen. Er braucht ein eigenes Dockerfile und ein eigenes Deployment-Modell (Kubernetes Deployment statt Argo-Step).
workflows/templates/
Wiederverwendbare Argo Workflow Templates. Mindestens:

retry-defaults.yaml – Standard Retry-Policy (3 Versuche, exponentielles Backoff ab 30s)
common-env.yaml – Standard-Umgebungsvariablen die jeder Container bekommt
error-handler.yaml – Standard Exit-Handler für fehlgeschlagene Schritte

AGENTS.md beschreibt wie Templates strukturiert sein müssen und wie sie in Workflows referenziert werden.
workflows/examples/
Vollständig kommentierte Beispiel-Workflows als Referenz:

Ein einfacher Import-Workflow (Fetch → Transform → Store)
Ein Export-Workflow (Read → Transform → Push)
Ein Diff-Workflow (Read Stand 1 → Read Stand 2 → Diff → Store Report)

Jedes Beispiel dokumentiert in Kommentaren: Warum dieser Schritt, welche Artifacts fließen, welche Env-Vars gesetzt werden. AGENTS.md beschreibt, dass diese Beispiele die normative Referenz für neue Workflows sind.
docker/
Enthält alle Docker-relevanten Dateien:

Dockerfile.transformer – Shared Dockerfile für alle Transformer. Installiert libs aus dem Repo, kopiert Transformer-Code, setzt Entrypoint.
Dockerfile.base – Shared Dockerfile für Base-Container.
Dockerfile.http-trigger – Eigenes Dockerfile für den dauerlaufenden HTTP-Trigger.
docker-compose.yaml – Lokaler Dev-Stack zum Testen der gesamten Pipeline.

AGENTS.md beschreibt:

Wie Dockerfiles strukturiert sein müssen (Multi-Stage Builds, minimale Images, non-root User)
Dass Transformer auch OHNE Docker entwickelbar sein müssen (python main.py mit lokaler Input-Datei reicht für die tägliche Arbeit)
Wie docker-compose.yaml strukturiert ist und welche Services darin definiert sind
Dass docker-compose.yaml NUR für lokale Entwicklung gedacht ist, nicht für Produktion

ci/
Enthält alle CI/CD-relevanten Dateien:

.gitlab-ci.yml – Haupt-Pipeline-Definition
build-transformer.yml – Wiederverwendbares Template für Transformer-Builds
build-base.yml – Wiederverwendbares Template für Base-Container-Builds
build-lib.yml – Template für Library-Tests
path-filters.yml – Mapping welcher Pfad welchen Build triggert

AGENTS.md beschreibt:

Wie die Pipeline auf Prefixed Git Tags reagiert
Wie Path-Filter funktionieren (Änderung in libs/planpro-parser/ triggert alle abhängigen Builds)
Dass die Pipeline selektiv baut (nicht alles bei jedem Commit)
Die Stages: lint → test → build → push → deploy-dev (automatisch) → deploy-int (manuell) → deploy-prod (manuell)
Dass ArgoCD für das Deployment auf den Cluster zuständig ist

docs/adr/
Architecture Decision Records. Jeder ADR folgt dem Format:

Titel
Status (Proposed, Accepted, Deprecated, Superseded)
Kontext (Welches Problem wird gelöst)
Entscheidung (Was wurde entschieden)
Konsequenzen (Was folgt daraus)
Abgelehnte Alternativen (Was wurde geprüft und verworfen, mit Begründung)

Dateinamenskonvention: NNN-kurzbeschreibung.md (z.B. 001-planpro-format-im-ds.md)
AGENTS.md beschreibt wann ein Agent einen ADR vorschlagen soll: Bei jeder Entscheidung die die Systemstruktur, Technologiewahl, Datenmodell oder Schnittstellenkonventionen betrifft und die nicht trivial revidierbar ist.
docs/runbooks/
Operative Anleitungen für wiederkehrende Aufgaben. Jedes Runbook folgt dem Format:

Titel
Wann wird das benötigt (Trigger)
Voraussetzungen
Schritt-für-Schritt-Anleitung
Verifizierung (Wie prüft man ob es geklappt hat)
Troubleshooting (Häufige Probleme)

AGENTS.md beschreibt dass ein Agent nach jeder neuen Komponente oder jedem neuen Prozess ein passendes Runbook erstellen oder aktualisieren soll.
docs/contracts/
Schnittstellendefinitionen. Diese Dateien sind die normative Referenz für alle AGENTS.md im Repo. Wenn eine AGENTS.md und ein Contract sich widersprechen, gilt der Contract.
Folgende Contract-Dokumente müssen erstellt werden:
container-konvention.md – Der universelle Container-Vertrag:

Standard-Umgebungsvariablen: CORRELATION_ID, LOG_LEVEL, INPUT_PATH, OUTPUT_PATH, DS_API_URL, DS_API_TOKEN
Input/Output-Konvention: Lesen von INPUT_PATH (Default /tmp/input), Schreiben nach OUTPUT_PATH (Default /tmp/output)
Exit-Codes: 0 = Erfolg, 1 = Fachlicher Fehler, 2 = Technischer Fehler
Provenance: Jeder Container gibt ein Provenance-Fragment als separate Datei unter /tmp/provenance.json aus

logging-format.md – Das JSON-Log-Schema:

Pflichtfelder: timestamp, level, message, correlation_id, component
Optionale Felder: object_id, planpro_version, error_type, duration_ms
Logs gehen nach stdout, niemals in Dateien
Kein Multi-Line-Logging, jede Zeile ist ein vollständiges JSON-Objekt

provenance-format.md – Das Provenance-Fragment-Schema:

Pflichtfelder: transformer_name, transformer_version, timestamp, correlation_id, input_refs (Liste von Objekt-IDs), output_refs (Liste von Objekt-IDs)
Optionale Felder: planpro_version, scope, phase, error_info
Format: JSON-Datei unter /tmp/provenance.json

workflow-konventionen.md – Wie Argo Workflows strukturiert werden:

Artifact Passing als Default-Mechanismus für Datenübergabe zwischen Schritten
Shared Volumes nur bei großen Payloads (>100MB), mit dokumentierter Pfadkonvention
Parameters für Metadaten und Steuerungsinformation (IDs, Counts, Flags)
Retry-Defaults: 3 Versuche, exponentielles Backoff ab 30s
Exit-Handler für jeden Workflow der Fehler in strukturiertes Log schreibt
Jeder Workflow muss ein Annotation-Label haben: Verantwortliches Team, Kategorie (import/export/diff/sync)

namenskonventionen.md – Wie Dinge benannt werden:

Container-Images: registry.intern/<typ>-<name>:<version> (z.B. registry.intern/transformer-ingest:v1.3.2)
Git Tags: <typ>-<name>/v<major>.<minor>.<patch>
Workflow-Namen: <kategorie>-<beschreibung> (z.B. import-planpro, export-system-a)
Ordnernamen: Kebab-Case (z.B. planpro-ingest, file-fetcher)
Python-Packages: Snake-Case (z.B. planpro_parser, ds_client)
Umgebungsvariablen: UPPER_SNAKE_CASE

mindest-validierung.md – Was bei jedem Import geprüft werden muss:

GUID vorhanden und gültiges UUID-Format
Objekttyp vorhanden und aus bekannter Liste
PlanPro-Version vorhanden
Pflicht-Referenzen vorhanden (abhängig vom Objekttyp)
Bei Verletzung: Objekt wird abgewiesen, Fehler wird strukturiert geloggt

tests/integration/
Integrationstests die mehrere Komponenten zusammen testen. Laufen gegen die echte REST-API in der Dev-Umgebung. AGENTS.md beschreibt:

Dass diese Tests NICHT in der CI bei jedem Commit laufen, sondern manuell oder als Nightly-Job
Dass sie eine laufende Dev-Umgebung voraussetzen
Dass sie Testdaten vor dem Test anlegen und nach dem Test aufräumen
Dass sie die echte API testen, keine Mocks

tests/fixtures/
Geteilte Testdaten die von mehreren Komponenten genutzt werden:

Echte PlanPro-Beispieldateien in verschiedenen Versionen (1.9, 1.10)
Mindestens eine minimale PlanPro-Datei mit wenigen Objekten für schnelle Tests
Mindestens eine realistische PlanPro-Datei mit komplexen Referenzen
Erwartete JSON-Outputs für die Zerlegung
Beispiel-Diff-Reports

AGENTS.md beschreibt dass Fixtures NIEMALS generiert oder synthetisch erzeugt werden sollen – sie müssen echte oder echt-nahe PlanPro-Strukturen abbilden. Ein Agent darf vorhandene Fixtures nutzen, aber keine neuen erfinden.
Anforderungen an Root-Dateien
pyproject.toml
Konfiguration für ruff und mypy. Python 3.12 als Mindestversion. Ruff-Regeln für den gesamten Repo. Enthält KEINE Package-Definition – das Root ist kein installierbares Package.
.pre-commit-config.yaml
Pre-Commit Hooks für ruff format, ruff check, mypy. Muss funktionsfähig sein.
Makefile
Targets:

make lint – ruff check und mypy über das gesamte Repo
make format – ruff format über das gesamte Repo
make test – alle Unit-Tests
make test-unit – nur Unit-Tests
make test-integration – nur Integrationstests
make build-all – alle Container-Images bauen
make build COMPONENT=transformer-ingest – einzelnes Image bauen
make clean – Build-Artefakte aufräumen

.gitignore
Python (pycache, .venv, *.egg-info, dist/, build/), Docker, IDE (.idea/, .vscode/), OS (.DS_Store, Thumbs.db), mypy (.mypy_cache/), pytest (.pytest_cache/), Umgebungsvariablen (.env)
README.md (Root)
Überblick über das Gesamtsystem mit:

Einzeiler was das System tut
Architekturüberblick (Datenspeicher, Logistics Layer, Transformer, Base-Container)
Setup-Anleitung für neue Entwickler (Repo klonen, venv anlegen, pre-commit installieren, erster Test)
Wie man einen neuen Transformer anlegt (Verweis auf _template und Runbook)
Links zu den wichtigsten Docs (Contracts, ADRs, Runbooks)
Verweis auf AGENTS.md für AI-gestützte Entwicklung

AGENTS.md (Root)
Globale Anweisungen für AI-Agenten. Dieses Dokument ist das erste, das ein AI-Agent liest, bevor er im Repo arbeitet.
Enthält:
Systemübersicht – Was ist dieses Repo, was ist das Ziel, wie ist es strukturiert. Verweist auf die ordnerspezifischen AGENTS.md für Details.
Goldene Regeln die überall gelten:

Transformer enthalten NUR Domänenlogik – kein I/O, kein HTTP, kein Dateisystem außer INPUT_PATH/OUTPUT_PATH
Base-Container sind die einzige Schicht die I/O macht
Alle Datenflüsse gehen durch den Logistics Layer (Argo Workflows) – keine Sonderwege
Structured JSON Logging über common.logging – überall, ausnahmslos
Tests sind Pflicht – kein Code ohne Tests
Keine hartkodierten Werte – alles über Umgebungsvariablen oder Konfiguration
Python Type Hints sind Pflicht – alle Funktionen, alle Parameter, alle Rückgabewerte
Imports nur aus erlaubten Quellen – siehe ordnerspezifische AGENTS.md
Provenance-Fragment ist Pflicht für jeden Transformer und jeden Base-Container
Contracts in docs/contracts/ sind normativ – bei Widerspruch gilt der Contract

Navigationshinweis – Welche AGENTS.md für welche Aufgabe relevant ist:

Neuen Transformer bauen → transformers/AGENTS.md und transformers/_template/AGENTS.md
Neuen Base-Container bauen → base-containers/AGENTS.md und base-containers/_template/AGENTS.md
Library erweitern → libs/AGENTS.md und die spezifische Library-AGENTS.md
Workflow erstellen → workflows/AGENTS.md und workflows/examples/AGENTS.md
Architekturentscheidung dokumentieren → docs/adr/AGENTS.md
Schnittstelle definieren oder ändern → docs/contracts/AGENTS.md

Domänenkontext – Zusammenfassung des PlanPro-Domänenwissens, des Datenspeicher-Modells und der regulatorischen Anforderungen (aus dem Abschnitt "Domänenkontext" dieses Prompts übernehmen).
Ausgabeformat
Erstelle alle Dateien vollständig. Jede README.md und AGENTS.md soll inhaltlich komplett sein, nicht nur Platzhalter. Die Konfigurationsdateien (pyproject.toml, Makefile etc.) sollen funktionsfähig sein.
Arbeite das Repo Ordner für Ordner ab. Beginne mit den Root-Dateien, dann libs/, dann transformers/, dann base-containers/, dann workflows/, dann docker/, dann ci/, dann docs/, dann tests/.
Erstelle jeden Ordner mit seinen README.md und AGENTS.md Dateien. Die Contract-Dokumente in docs/contracts/ sollen ebenfalls vollständig erstellt werden, da sie die normative Referenz für das gesamte Repo sind.