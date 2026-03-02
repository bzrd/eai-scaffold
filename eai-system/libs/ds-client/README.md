# libs/ds-client – Datenspeicher REST-Client

Typisierter Python-Client für die FIN REST-API. Nur von Base-Containern (`ds-writer`, `ds-reader`) importiert – **niemals von Transformern**.

## Struktur

```
ds-client/
├── ds_client/
│   ├── client.py      # DsClient (write_objects, read_objects, get_version_diff)
│   ├── models.py      # DsObject, WriteResult, ReadResult
│   ├── exceptions.py  # DsError → DsApiError/DsAuthError/DsNotFoundError/DsValidationError
│   └── auth.py        # Token-basierte Auth
└── tests/
```

## Konventionen

- Alle Operationen synchron (kein async/await)
- Retry: 3 Versuche, exponentielles Backoff
- Git-Tag: `lib-ds-client/v<major>.<minor>.<patch>`

## Checkliste

- [ ] Type Hints vollständig, `mypy --strict` grün
- [ ] Unit-Tests mit gemocktem HTTP
- [ ] Neue Methode in `__init__.py` exportiert
- [ ] Kein direkter Import aus Transformern
