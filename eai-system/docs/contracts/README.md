# docs/contracts/ – Normative Schnittstellendefinitionen

## Zweck

Schnittstellendefinitionen die als **normative Referenz** für das gesamte Repo gelten. Wenn eine `AGENTS.md` und ein Contract sich widersprechen, **gilt der Contract**.

---

## Struktur

```
contracts/
├── container-konvention.md        # Universeller Container-Vertrag (Env-Vars, I/O, Exit-Codes)
├── logging-format.md              # JSON-Log-Schema
├── provenance-format.md           # Provenance-Fragment-Schema
├── workflow-konventionen.md       # Argo-Workflow-Strukturregeln
├── namenskonventionen.md          # Naming für Images, Tags, Ordner, Packages
├── mindest-validierung.md         # Validierungsregeln für jeden Import
├── README.md
└── AGENTS.md
```

---

## Konventionen

- Contracts sind **immutable nach Acceptance** – Änderungen erfordern einen ADR und einen neuen Contract oder eine neue Version
- Contracts verwenden **RFC 2119 Sprache**: MUSS, DARF NICHT, SOLL, KANN
- Jeder Contract hat eine Versionsnummer und ein Änderungsdatum

---

## Priorität

```
Contracts (höchste)  >  ordnerspezifische AGENTS.md  >  Root AGENTS.md  >  README.md
```

---

## Checkliste für Contract-Änderungen

- [ ] ADR für die Änderung geschrieben
- [ ] Alle betroffenen AGENTS.md aktualisiert
- [ ] Alle betroffenen Komponenten angepasst
- [ ] Version des Contracts hochgezählt
