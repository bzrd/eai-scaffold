# AGENTS.md – docs/adr/

## Rolle

Du erstellst Architecture Decision Records (ADRs). Du dokumentierst Architekturentscheidungen vollständig und nachvollziehbar.

---

## Regeln

- Du MUSST einen ADR vorschlagen bei jeder Entscheidung die die Systemstruktur, Technologiewahl, Datenmodell oder Schnittstellenkonventionen betrifft und die nicht trivial revidierbar ist.
- Du MUSST das ADR-Format einhalten: Status, Kontext, Entscheidung, Konsequenzen, Abgelehnte Alternativen.
- Du MUSST mindestens eine abgelehnte Alternative mit Begründung dokumentieren.
- Du MUSST die fortlaufende Nummerierung einhalten.
- Du darfst NIEMALS einen ADR löschen – stattdessen Status auf "Deprecated" oder "Superseded" setzen.
- Du darfst NIEMALS einen accepted ADR inhaltlich ändern – bei Revisionen einen neuen ADR erstellen der den alten superseded.

---

## Patterns

### Neuen ADR erstellen

1. Höchste vorhandene Nummer ermitteln
2. Datei anlegen: `<N+1>-kurzbeschreibung.md`
3. Template ausfüllen
4. Status auf "Proposed" setzen
5. Nach Review und Annahme: Status auf "Accepted" ändern

---

## Antipatterns

- **Keine ADRs ohne abgelehnte Alternativen** – der Wert liegt im Nachvollziehen WARUM.
- **Keine ADRs löschen** – sie sind Teil des Audit-Trails.
- **Keine rückwirkenden Änderungen** an accepted ADRs.

---

## Testanforderungen

- ADR hat alle Pflichtabschnitte
- Nummerierung ist fortlaufend
- Status ist gesetzt

---

## Abhängigkeiten

- ADRs können auf Contracts verweisen die sie begründen
- Contracts können ADRs referenzieren die sie veranlasst haben

---

## Kontext

ADRs sind ein zentrales Element der regulatorischen Nachvollziehbarkeit. In einem System das Jahrzehnte läuft und kritische Bahninfrastruktur plant, müssen zukünftige Entwickler und Auditoren verstehen können, WARUM Entscheidungen getroffen wurden – nicht nur WAS entschieden wurde.
