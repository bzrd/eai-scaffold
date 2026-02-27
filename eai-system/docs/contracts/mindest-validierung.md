# Contract: Mindest-Validierung

**Version:** 1.0
**Stand:** 2026-02-27
**Status:** Accepted

---

## Geltungsbereich

Gilt für **jeden Import** von PlanPro-Daten in den Datenspeicher. Die Validierung wird durch den Import-Transformer (`planpro-ingest`) und die Validierungslogik in `libs/common` durchgeführt.

---

## Definitionen

- **Import:** Übernahme von PlanPro-Objekten in den Datenspeicher.
- **Objekt:** Ein einzelnes JSON-Dokument das ein PlanPro-Infrastrukturelement repräsentiert.
- **GUID:** Globally Unique Identifier im UUID-Format – permanente Identität eines Infrastrukturelements.
- **Objekttyp:** PlanPro-Klassenname (z.B. `Signal`, `Weiche`, `Gleisabschnitt`).

---

## Validierungsregeln

### 1. GUID

**Anforderungen:**

1. Jedes Objekt MUSS eine GUID haben.
2. Die GUID MUSS ein gültiges UUID-Format haben (RFC 4122).
3. Das UUID-Format MUSS dem Regex-Pattern entsprechen:
   ```
   ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$
   ```
   (Case-insensitive)
4. GUIDs DÜRFEN NICHT verändert, normalisiert oder neu generiert werden.

### 2. Objekttyp

**Anforderungen:**

5. Jedes Objekt MUSS einen Objekttyp haben.
6. Der Objekttyp MUSS aus der bekannten Liste in `libs/common/constants.py` stammen.
7. Unbekannte Objekttypen MÜSSEN abgewiesen werden.

### 3. PlanPro-Version

**Anforderungen:**

8. Jedes Objekt MUSS eine PlanPro-Version haben.
9. Die PlanPro-Version MUSS einer der bekannten Versionen in `libs/common/constants.py` entsprechen.

### 4. Pflicht-Referenzen

**Anforderungen:**

10. Objekttyp-spezifische Pflicht-Referenzen MÜSSEN vorhanden sein.
11. Die Pflicht-Referenzen sind abhängig vom Objekttyp und werden in `libs/planpro-parser/constants.py` definiert.

---

## Fehlerbehandlung

### Anforderungen

12. Bei Verletzung einer Validierungsregel MUSS das betroffene Objekt abgewiesen werden.
13. Die Abweisung DARF NICHT den gesamten Import abbrechen – andere gültige Objekte MÜSSEN weiterverarbeitet werden.
14. Jede Abweisung MUSS strukturiert geloggt werden (gemäß `logging-format.md`).
15. Das Log MUSS enthalten: GUID (falls vorhanden), Objekttyp (falls vorhanden), Grund der Abweisung.
16. Abgewiesene Objekte MÜSSEN im Provenance-Fragment unter `error_info` dokumentiert werden.
17. Wenn ALLE Objekte abgewiesen werden, MUSS der Container mit Exit-Code 1 (fachlicher Fehler) beenden.

---

## Beispiele

### Korrekt: Gültiges Objekt

```json
{
  "guid": "12345678-1234-1234-1234-123456789012",
  "object_type": "Signal",
  "planpro_version": "1.10",
  "data": { "bezeichnung": "S1" }
}
```

### Abgewiesen: Fehlende GUID

```json
{
  "object_type": "Signal",
  "planpro_version": "1.10",
  "data": { "bezeichnung": "S1" }
}
```
*Grund: GUID fehlt (Regel 1)*

### Abgewiesen: Ungültiges UUID-Format

```json
{
  "guid": "not-a-valid-uuid",
  "object_type": "Signal",
  "planpro_version": "1.10"
}
```
*Grund: GUID hat kein gültiges UUID-Format (Regel 3)*

### Abgewiesen: Unbekannter Objekttyp

```json
{
  "guid": "12345678-1234-1234-1234-123456789012",
  "object_type": "UnbekannterTyp",
  "planpro_version": "1.10"
}
```
*Grund: Objekttyp nicht in bekannter Liste (Regel 6)*

### Log-Eintrag bei Abweisung

```json
{
  "timestamp": "2026-02-27T14:30:00.123Z",
  "level": "WARNING",
  "message": "Objekt abgewiesen: ungültiges UUID-Format",
  "correlation_id": "wf-abc-123",
  "component": "transformer-ingest",
  "object_id": "not-a-valid-uuid",
  "error_type": "GUIDValidationError"
}
```
