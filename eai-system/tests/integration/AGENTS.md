# AGENTS.md – tests/integration/

## Rolle

Du erstellst oder pflegst Integrationstests. Diese Tests testen das Zusammenspiel mehrerer Komponenten gegen die echte Datenspeicher-API.

---

## Regeln

- Du MUSST alle Tests mit `@pytest.mark.integration` markieren.
- Du MUSST Testdaten vor dem Test anlegen und nach dem Test aufräumen (auch bei Fehler – `try/finally` oder Fixture mit Cleanup).
- Du MUSST einen eigenen Test-Scope im Datenspeicher verwenden – NIEMALS den Produktiv- oder Haupt-Scope.
- Du MUSST die echte API testen – KEINE Mocks in Integrationstests.
- Du darfst NIEMALS Integrationstests in die reguläre CI-Pipeline einhängen – nur manuell oder Nightly.
- Du MUSST `DS_API_URL` und `DS_API_TOKEN` als Umgebungsvariablen voraussetzen.
- Du MUSST Fixtures aus `tests/fixtures/` verwenden – keine synthetischen Testdaten.

---

## Patterns

### Shared Fixture mit Cleanup

```python
# conftest.py
import pytest
from ds_client import DsClient
from common.config import get_config

@pytest.fixture
def ds_client() -> DsClient:
    config = get_config()
    return DsClient(base_url=config.ds_api_url, token=config.ds_api_token)

@pytest.fixture
def test_scope(ds_client: DsClient):
    scope_name = f"test-{uuid4()}"
    ds_client.create_scope(scope_name)
    yield scope_name
    ds_client.delete_scope(scope_name)  # Cleanup
```

### End-to-End Import Test

```python
@pytest.mark.integration
def test_import_workflow(ds_client, test_scope, planpro_fixture_path):
    # 1. XML-Datei laden (aus Fixtures)
    xml_content = Path(planpro_fixture_path).read_text()

    # 2. Ingest-Transformer ausführen
    result = run_transformer("planpro-ingest", input_data=xml_content)
    assert result.exit_code == 0

    # 3. Objekte in Datenspeicher schreiben
    write_result = ds_client.write_objects(result.objects, scope=test_scope)
    assert len(write_result.written) == len(result.objects)

    # 4. Objekte zurücklesen und vergleichen
    read_result = ds_client.read_objects(
        guids=[obj.guid for obj in result.objects],
        scope=test_scope,
    )
    assert len(read_result.objects) == len(result.objects)
```

---

## Antipatterns

- **Keine Mocks** in Integrationstests – das ist der Zweck dieser Tests.
- **Kein Hauptdatenbestand** – immer eigenen Test-Scope.
- **Keine Tests ohne Cleanup** – Testdaten müssen aufgeräumt werden.
- **Keine synthetischen Fixtures** – echte PlanPro-Daten verwenden.

---

## Testanforderungen

- Framework: `pytest`
- Marker: `@pytest.mark.integration`
- Umgebungsvariablen: `DS_API_URL`, `DS_API_TOKEN`
- Cleanup: Testdaten nach dem Test aufräumen

---

## Abhängigkeiten

- Du DARFST importieren: `ds_client`, `planpro_parser`, `common`, alle Libraries
- Fixtures aus `tests/fixtures/`
- Laufende Dev-Umgebung

---

## Kontext

Integrationstests sind der letzte Qualitätscheck vor einem Release. Sie testen das echte Zusammenspiel: XML → Parser → Transformer → API → Datenspeicher → Zurücklesen → Vergleich. Sie fangen Probleme die Unit-Tests nicht sehen: Serialisierungsfehler, API-Inkonsistenzen, Netzwerk-Timing.
