# libs/ds-client – Datenspeicher REST-API Client

## Zweck

Typisierter Python-Client für die REST-API des Datenspeichers (FIN). Kapselt alle CRUD-Operationen, Auth-Handling, Fehlerbehandlung und Versionierungsoperationen. Wird von Base-Containern (`ds-writer`, `ds-reader`) genutzt.

**Wichtig:** Transformer dürfen diesen Client **nicht direkt** importieren. Transformer haben keinen Netzwerkzugriff.

---

## Struktur

```
ds-client/
├── ds_client/
│   ├── __init__.py          # Öffentliche API
│   ├── client.py            # DsClient Hauptklasse
│   ├── auth.py              # Token-basierte Authentifizierung
│   ├── models.py            # Typisierte Request/Response-Modelle
│   ├── exceptions.py        # Eigene Exception-Klassen
│   ├── versioning.py        # Versionierungsoperationen (Stände vergleichen)
│   └── scopes.py            # Scope- und Phasen-Management
├── tests/
│   ├── conftest.py          # Fixtures (Mock-API-Server oder Responses)
│   ├── test_client.py
│   ├── test_auth.py
│   └── test_versioning.py
└── pyproject.toml
```

---

## Konventionen

- **Alle API-Operationen sind synchron** (keine async/await) – Argo-Steps laufen als einzelne Prozesse
- **Eigene Exception-Klassen** für alle Fehlerkategorien: `DsApiError`, `DsAuthError`, `DsNotFoundError`, `DsValidationError`
- **Typisierte Modelle** für alle Request- und Response-Objekte (`dataclass` oder `TypedDict`)
- **Retry-Logik** für transiente Netzwerkfehler (3 Versuche, exponentielles Backoff)
- Python-Package-Name: `ds_client`
- Auth: Token wird über Umgebungsvariable `DS_API_TOKEN` bereitgestellt

---

## Abhängigkeiten

- `libs/common` (Logging, Config, Konstanten)
- `requests` oder `httpx` (HTTP-Client)
- **Keine anderen repo-internen Libraries**

---

## Beispiel: Verwendung in einem Base-Container

```python
from ds_client import DsClient
from ds_client.models import DsObject, WriteRequest
from common.config import get_config
from common.logging import get_logger

logger = get_logger(__name__)
config = get_config()

client = DsClient(
    base_url=config.ds_api_url,
    token=config.ds_api_token,
)

# Objekte schreiben
result = client.write_objects(
    objects=[DsObject(guid="...", object_type="Signal", data={...})],
    scope="projekt-abc",
    phase="planung",
)
logger.info("Objekte gespeichert", extra={"count": len(result.written)})
```

---

## Checkliste

- [ ] Neue API-Methode mit vollständigen Type Hints
- [ ] Exception-Klasse für Fehlerfall definiert
- [ ] Unit-Test mit gemockter HTTP-Antwort
- [ ] Retry-Logik für transiente Fehler vorhanden
- [ ] Öffentliche API in `__init__.py` exportiert
- [ ] `mypy --strict` grün
- [ ] Kein direkter Import aus Transformern
