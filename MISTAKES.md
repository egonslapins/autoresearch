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
