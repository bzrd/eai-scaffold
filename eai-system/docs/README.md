# docs/ – Dokumentation

## Zweck

Zentrale Dokumentation des EAI-Systems: Architecture Decision Records, operative Runbooks und normative Schnittstellenverträge (Contracts).

---

## Struktur

```
docs/
├── adr/               # Architecture Decision Records
├── runbooks/          # Operative Anleitungen
├── contracts/         # Normative Schnittstellendefinitionen (höchste Priorität)
├── README.md
└── AGENTS.md
```

---

## Konventionen

- **Contracts sind normativ** – bei Widerspruch zwischen AGENTS.md und Contract gilt der Contract
- **ADRs dokumentieren Entscheidungen** – nicht nur WAS entschieden wurde, sondern WARUM und was abgelehnt wurde
- **Runbooks sind operativ** – Schritt-für-Schritt-Anleitungen für wiederkehrende Aufgaben

---

## Prioritätsreihenfolge bei Widersprüchen

1. `docs/contracts/` (höchste Priorität – normativ)
2. `AGENTS.md` im spezifischen Ordner
3. `AGENTS.md` in Root
4. `README.md`
