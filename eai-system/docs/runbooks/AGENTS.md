# AGENTS.md – docs/runbooks/

## Rolle

Du erstellst oder aktualisierst operative Runbooks. Runbooks sind Schritt-für-Schritt-Anleitungen für wiederkehrende Aufgaben.

---

## Regeln

- Du MUSST nach jeder neuen Komponente oder jedem neuen Prozess ein passendes Runbook erstellen oder aktualisieren.
- Du MUSST das Runbook-Format einhalten: Trigger, Voraussetzungen, Schritte, Verifizierung, Troubleshooting.
- Du MUSST Schritte so formulieren, dass sie auch von neuen Teammitgliedern ausführbar sind.
- Du darfst NIEMALS Runbooks mit veralteten Informationen stehen lassen – bei Änderungen an Prozessen sofort aktualisieren.

---

## Patterns

### Runbook erstellen

1. Identifiziere den Prozess der dokumentiert werden muss
2. Führe den Prozess mental oder tatsächlich durch und notiere jeden Schritt
3. Beschreibe Voraussetzungen und Verifizierung
4. Ergänze Troubleshooting aus bekannten Problemen

---

## Antipatterns

- **Keine unvollständigen Runbooks** – lieber kein Runbook als eines das mittendrin aufhört.
- **Keine veralteten Runbooks** – aktiv pflegen.
- **Keine impliziten Schritte** – alles explizit dokumentieren.

---

## Testanforderungen

- Runbook hat alle Pflichtabschnitte
- Schritte sind ausführbar (Kommandos sind korrekt)
- Verifizierung ist möglich

---

## Abhängigkeiten

- Verweist auf Prozesse in `transformers/_template/`, `base-containers/_template/`
- Verweist auf Contracts in `docs/contracts/`

---

## Kontext

Runbooks sind ein zentrales Werkzeug für die Wartbarkeit eines langlebigen Systems. Sie stellen sicher, dass wiederkehrende Aufgaben korrekt und konsistent ausgeführt werden – unabhängig davon wer (Mensch oder AI-Agent) sie ausführt.
