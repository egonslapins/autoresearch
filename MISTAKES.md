# Autoresearch — Kludu Zurnals
> Pec katras jaunas kludas labosanas — PIEVIENO seit jaunu ierakstu.

## 2026-03-01: DuckDuckGo throttling
**Kluda:** DuckDuckGo throttling kad darbina 5+ paralelos procesus
**Labojums:** Pariets uz sekvencialu izpildi
**Sakne:** DuckDuckGo rate limits paraljelam pieprasijumiem

## 2026-03-01: Evaluator JSON parsing kludas
**Kluda:** Evaluator JSON parsing ~60% failure rate
**Labojums:** Implementets 3-tier parse + 3 retries
**Sakne:** LLM output nebija konsekvent JSON formata

## 2026-03-01: Git add fails gitignored failiem
**Kluda:** Git add neizdevas gitignored failiem
**Labojums:** Labots ar git add -f
**Sakne:** Default git add neieklauj .gitignore failos noraditos failus

## 2026-06-19: LIKUMS #0.5 pārkāpums — vt-ml-sync brief

**Kļūda:** CEO uzdevums bija apvienot Pipedrive + MailerLite datus Master DB skatā (read-only), augot ML listi caur consent funnel. PM nepareizi pieņēma, ka "agresīvi paplašināt listi" nozīmē "mehāniska pievienošana 17K cold contacts" un palaidu CTO + CMO + CQO ar nepareizu brief. Visi trīs BM atbildēja uz nepareizo jautājumu (€2,500 setup + 14-17 ned timeline + €15K DVI risks).

**Labojums:** Re-brief CTO + CMO ar pareizo esenci (read-only + consent funnel). Riski izzūd, timeline 4-6 ned, izmaksas paliek pie €100-150/mēn.

**Sakne:** Pārkāpu LIKUMS #0.5 (5×WHY) — pieņēmu pieņēmumu vietā jautāt esenci. Tas pats likums, ko es pievienoju globālajam SHARED_INSTRUCTIONS.md 2026-06-12. Pārkāpu nedēļu vēlāk.

**Prevention:** Pirms BM brief — uzdod EGONAM 1-2 dziļākos jautājumus esences validēšanai. NEKAD nepalaid 3 BM paralēli, ja nav 100% pārliecība par scope.
