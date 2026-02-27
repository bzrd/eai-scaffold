# AGENTS.md – docs/contracts/

## Rolle

Du erstellst oder änderst normative Schnittstellendefinitionen. Contracts sind das verbindlichste Dokument im Repo – sie haben Vorrang vor allen AGENTS.md und README.md Dateien.

---

## Regeln

- Du darfst NIEMALS einen accepted Contract ohne ADR ändern.
- Du MUSST bei Contract-Änderungen alle betroffenen Komponenten und AGENTS.md identifizieren und aktualisieren.
- Du MUSST RFC 2119 Sprache verwenden (MUSS, DARF NICHT, SOLL, KANN).
- Du MUSST eine Versionsnummer und ein Änderungsdatum angeben.
- Du MUSST Contracts so formulieren, dass sie maschinenlesbar testbar sind (z.B. JSON-Schemata, Regex-Patterns).
- Du darfst NIEMALS Contracts im Widerspruch zueinander erstellen.

---

## Patterns

### Contract-Struktur

```markdown
# Contract: <Name>
Version: 1.0
Stand: YYYY-MM-DD
Status: Accepted

## Geltungsbereich
Für welche Komponenten gilt dieser Contract?

## Definitionen
Begriffserklärungen.

## Anforderungen
Nummerierte Anforderungen mit MUSS/DARF NICHT/SOLL/KANN.

## Beispiele
Konkrete Beispiele für korrektes und inkorrektes Verhalten.
```

---

## Antipatterns

- **Keine Contracts ohne ADR** bei Änderungen.
- **Keine vagen Formulierungen** – immer MUSS/DARF NICHT/SOLL/KANN.
- **Keine Widersprüche** zwischen Contracts.
- **Keine Contracts ohne Beispiele** – abstrakte Regeln allein sind nicht eindeutig.

---

## Testanforderungen

- Jeder Contract muss testbare Anforderungen enthalten
- Tests sollten automatisierbar sein (z.B. JSON-Schema-Validierung, Regex-Prüfung)

---

## Abhängigkeiten

- ADRs verweisen auf Contracts
- Alle AGENTS.md im Repo verweisen auf relevante Contracts

---

## Kontext

Contracts sind die Grundlage für die Interoperabilität aller Komponenten. Da Container unabhängig voneinander entwickelt und versioniert werden, sind klare Schnittstellenverträge der einzige Mechanismus der sicherstellt, dass alles zusammenpasst. In einem regulatorisch relevanten System ist diese Formalisierung nicht optional.
