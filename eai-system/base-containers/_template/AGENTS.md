# AGENTS.md – base-containers/_template/

## Rolle

Du erzeugst einen neuen Base-Container auf Basis dieser Vorlage. Base-Container DÜRFEN I/O machen.

## Regeln

- Du MUSST `_template/` kopieren – niemals direkt darin arbeiten.
- Du MUSST I/O in `handler.py` isolieren.
- Du MUSST Retry für transiente Netzwerkfehler implementieren.
- Du MUSST alle I/O in Unit-Tests mocken.
- Du darfst NIEMALS Domänenlogik einbauen.
- Du darfst NIEMALS `planpro_parser` importieren.

## Schritte

1. Template kopieren + umbenennen
2. `handler.py` implementieren (HTTP, Datei-I/O oder `ds_client`)
3. `main.py` anpassen (Name, Import-Pfad)
4. Tests schreiben (alle I/O gemockt)
5. `pyproject.toml` und `README.md` anpassen

## Abhängigkeiten

- DARFST: `common`, `ds_client` (bei DS-Containern), `requests`/`httpx`
- NICHT: `planpro_parser`, andere Base-Container, Transformer
