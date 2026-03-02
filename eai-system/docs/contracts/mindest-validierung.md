# Contract: Mindest-Validierung

**Version:** 1.0 | **Status:** Accepted

Gilt für jeden Import von PlanPro-Daten in den Datenspeicher.

## Validierungsregeln

### GUID

1. Jedes Objekt MUSS eine GUID haben.
2. GUID MUSS gültiges UUID-Format sein (RFC 4122):
   ```
   ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
   ```
3. GUIDs DÜRFEN NICHT verändert, normalisiert oder neu generiert werden.

### Objekttyp

4. Jedes Objekt MUSS einen Objekttyp haben.
5. Objekttyp MUSS aus der bekannten Liste in `libs/common/constants.py` stammen.

### PlanPro-Version

6. Jedes Objekt MUSS eine PlanPro-Version haben.
7. Version MUSS in `libs/common/constants.py` bekannt sein.

### Pflicht-Referenzen

8. Objekttyp-spezifische Pflicht-Referenzen MÜSSEN vorhanden sein (siehe `libs/planpro-parser/constants.py`).

## Fehlerbehandlung

9. Ungültige Objekte MÜSSEN abgewiesen werden, der Import läuft weiter.
10. Jede Abweisung MUSS strukturiert geloggt werden (GUID, Objekttyp, Grund).
11. Abgewiesene Objekte MÜSSEN in `error_info` im Provenance-Fragment dokumentiert werden.
12. Wenn ALLE Objekte abgewiesen werden → Exit-Code 1.
