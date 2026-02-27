# docs/adr/ – Architecture Decision Records

## Zweck

Architecture Decision Records (ADRs) dokumentieren wichtige Architekturentscheidungen: Was wurde entschieden, warum, und was wurde verworfen.

---

## Struktur

```
adr/
├── NNN-kurzbeschreibung.md    # z.B. 001-planpro-format-im-ds.md
├── README.md
└── AGENTS.md
```

---

## Konventionen

### Dateiname
`NNN-kurzbeschreibung.md` (z.B. `001-planpro-format-im-ds.md`, `002-transformer-container-isolation.md`)

### ADR-Format

```markdown
# NNN – Titel

## Status
Proposed | Accepted | Deprecated | Superseded by NNN

## Kontext
Welches Problem wird gelöst? Was ist der Anlass für die Entscheidung?

## Entscheidung
Was wurde entschieden? Klare, eindeutige Formulierung.

## Konsequenzen
Was folgt aus dieser Entscheidung? Positive und negative Auswirkungen.

## Abgelehnte Alternativen
Was wurde geprüft und verworfen? Für jede Alternative: kurze Beschreibung und Begründung warum sie abgelehnt wurde.
```

---

## Wann wird ein ADR benötigt?

Bei jeder Entscheidung die:
- Die Systemstruktur betrifft (neue Komponenten, neue Schichten)
- Technologiewahl betrifft (neue Library, neues Framework)
- Das Datenmodell betrifft (neue Objekttypen, neue Felder)
- Schnittstellenkonventionen betrifft (API-Änderungen, neue Contracts)
- **Nicht trivial revidierbar ist**

---

## Beispiel

```markdown
# 001 – PlanPro-Objekte als einzelne JSON-Dokumente im Datenspeicher

## Status
Accepted

## Kontext
PlanPro-XML-Dateien enthalten hunderte Infrastrukturelemente. Wir müssen entscheiden wie diese Daten im Datenspeicher (FIN) abgelegt werden.

## Entscheidung
Jedes PlanPro-Element wird als einzelnes JSON-Dokument gespeichert, identifiziert durch seine GUID.

## Konsequenzen
- Positiv: Einzelne Elemente adressierbar, versionierbar, referenzierbar
- Negativ: Import und Export müssen viele einzelne Dokumente verarbeiten

## Abgelehnte Alternativen
- Gesamte XML-Datei als Blob: Abgelehnt weil einzelne Elemente nicht adressierbar wären
- Relationale Zerlegung: Abgelehnt weil das PlanPro-Klassendiagramm sich ändert und eine starre Tabellenstruktur nicht mithalten könnte
```

---

## Checkliste

- [ ] Nummernfolge fortlaufend
- [ ] Status gesetzt (Proposed/Accepted)
- [ ] Kontext beschreibt das Problem
- [ ] Entscheidung ist klar formuliert
- [ ] Konsequenzen umfassen positive UND negative Aspekte
- [ ] Mindestens eine abgelehnte Alternative mit Begründung
