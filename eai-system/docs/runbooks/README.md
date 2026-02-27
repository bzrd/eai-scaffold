# docs/runbooks/ – Operative Anleitungen

## Zweck

Operative Anleitungen für wiederkehrende Aufgaben. Jedes Runbook ist eine Schritt-für-Schritt-Anleitung die auch von neuen Teammitgliedern oder AI-Agenten ausgeführt werden kann.

---

## Struktur

```
runbooks/
├── neuen-transformer-anlegen.md
├── neuen-base-container-anlegen.md
├── release-erstellen.md
├── integrationstests-ausfuehren.md
├── troubleshooting-pipeline.md
├── README.md
└── AGENTS.md
```

---

## Konventionen

### Runbook-Format

```markdown
# Titel

## Wann wird das benötigt
Trigger: Wann führt man dieses Runbook aus?

## Voraussetzungen
Was muss vorhanden/konfiguriert sein?

## Schritt-für-Schritt-Anleitung
1. Erster Schritt (mit Kommando oder Aktion)
2. Zweiter Schritt
3. ...

## Verifizierung
Wie prüft man ob es geklappt hat?

## Troubleshooting
Häufige Probleme und deren Lösung.
```

---

## Erwartete Runbooks

| Runbook | Trigger |
|---|---|
| `neuen-transformer-anlegen.md` | Neuer Transformer benötigt |
| `neuen-base-container-anlegen.md` | Neuer Base-Container benötigt |
| `release-erstellen.md` | Neue Version einer Komponente |
| `integrationstests-ausfuehren.md` | Vor größeren Releases |
| `troubleshooting-pipeline.md` | Pipeline schlägt fehl |

---

## Checkliste

- [ ] Trigger beschrieben
- [ ] Voraussetzungen dokumentiert
- [ ] Schritte vollständig und ausführbar
- [ ] Verifizierung beschrieben
- [ ] Troubleshooting für häufige Probleme
