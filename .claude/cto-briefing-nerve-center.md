# CTO Briefing: VT Nerve Center — Impact on Marketing Dashboard

**No:** CTO
**Kam:** AutoResearch PM (marketing dashboard developer)
**Datums:** 2026-04-11
**Prioritāte:** INFO — nav tūlītēja rīcība nepieciešama

---

## Kas ir VT Nerve Center?

Jauns centralizēts REST API gateway, kas kļūs par **vienīgo veidu** piekļūt Agent Tool MySQL datubāzei (`at_refactored` @ 92.240.68.128). Pašlaik production:

**URL:** `https://vt-nerve-center-production-da7f.up.railway.app`
**Auth:** `X-API-Key` header
**GitHub:** `egonslapins/vt-nerve-center` (private)
**Deploy:** Railway Pro (vt-internal-services projekts)

## API Endpoints (26 total)

| Endpoint | Avots DB | Apraksts |
|----------|----------|----------|
| `GET /api/orders` | `bi_at_orders` view | Pasūtījumi ar filtriem, pagināciju |
| `GET /api/orders/:id` | `at_projects_items` + `at_clients` + `at_projects_invoices` | Pilns pasūtījuma detail |
| `GET /api/orders/stats/summary` | `bi_at_orders` | Agregēta statistika (cached 10min) |
| `GET /api/clients` | `view_clients` | Klientu saraksts ar meklēšanu |
| `GET /api/clients/:id` | `at_clients` | Pilns klienta profils |
| `GET /api/clients/:id/orders` | `bi_at_orders` + `at_projects_items` | Klienta pasūtījumu vēsture |
| `GET /api/clients/stats/segments` | `at_projects_items` | VIP/returning/one_time/prospect |
| `GET /api/hotels` | `wb_hotels` | Viesnīcu saraksts |
| `GET /api/hotels/:id` | `wb_hotels` | Pilns viesnīcas detail ar AI content |
| `PUT /api/hotels/:id/ai` | `wb_hotels` | AI content update |
| `GET /api/hotels/stats/coverage` | `wb_hotels` | AI pārklājuma statistika |
| `GET /api/pages` | `wb_pages` | CMS lapu koks (nested set) |
| `GET /api/pages/:id` | `wb_pages` | Lapa ar bērniem |
| `PUT /api/pages/:id` | `wb_pages` | Meta/summary update |
| `GET /api/countries` | `wb_countries` | Aktīvās valstis (cached 30min) |
| `GET /api/countries/:id` | `wb_countries` | Valsts detail |
| `GET /api/deals` | `at_pipedrive_deals` | Pipedrive deals |
| `GET /api/deals/stats/pipeline` | `at_pipedrive_deals` | Pipeline summary |
| `GET /api/deals/stats/funnel` | `at_pipedrive_deals` | Funnel konversija |
| `GET /api/charter/search` | `at_charter_search_logs` | Čarteru meklēšana |
| `GET /api/charter/destinations` | `at_charter_search_logs` | Galamērķu stats |
| `GET /api/charter/price-history` | `at_charter_search_logs` | Cenu vēsture |
| `POST /api/llm/complete` | OpenRouter | Centralizēts LLM routing (auto Flash/Sonnet) |
| `GET /api/llm/models` | — | Pieejamo modeļu saraksts |
| `GET /health` | — | Publisks health check |
| `GET /health/cache` | — | Cache stats + invalidation |

## Pašreizējais statuss: PROXY FALLBACK MODE

Nerve Center nevar tieši pieslēgties MySQL (firewall — nav static IP šim servisam). Darbojas caur `vt-internal-services` proxy:
- Pieprasījums → Nerve Center → mēģina tiešo MySQL → timeout → fallback uz `portal.vanillatravel.lv/api/sales-ai/agent-tool/query`
- **Ierobežojums:** Proxy nepieņem SQL ar JOINiem un aliasiem. Visas queries rakstītas bez aliasiem.

## Ietekme uz Marketing Dashboard

### Pašlaik: **NULLE IETEKME**

Mārketinga dashboard datu ķēde:
```
Marketing Dashboard (localhost:3000)
  → CEO Executive Dashboard (Railway) — FB/Google/Analytics/Campaigns
  → MailerLite API — newsletters, subscribers
  → Netlify Functions — blog CMS
  → Facebook/Instagram API — publishing
  → Anthropic API — AI chat
```

**Neviena no šīm saistēm nav mainīta.** Nerve Center ir PAPILDUS slānis, kas nelaiž iekšā nevienam esošam servisam.

### Nākotnē (F2-F5, ~jūnijs-oktobris 2026): POTENCIĀLA IETEKME

1. **F2 (jūnijs):** Executive Dashboard konsolidācija → `vt-analytics`. Ja marketing dashboard iet caur executive dashboard, tas mainīsies.
2. **F3-F5:** Tiešās MySQL pieejas bloķēšana. Servisi kas šobrīd lieto `portal.vanillatravel.lv/api/sales-ai/agent-tool/query` vai tiešo MySQL tiks migrēti uz Nerve Center REST API.

### Ko tev vajadzētu zināt:

1. **Ja marketing dashboard vajag jaunus datus no Agent Tool MySQL** — lieto Nerve Center REST API, nevis tiešu MySQL vai proxy. Tas ir jaunais standarts.
2. **API Key** — jāpieprasa CTO (env `API_KEYS` Railway servisā).
3. **Kešošana** — Nerve Center kešo bieži pieprasītus datus (10-30 min TTL). Nav jābūvē savs keš.
4. **Rate limiting** — 120 req/min per IP.

## Migrācijas rekomendācija

Ja dashboard sāk pievienot jaunas datu funkcijas kas prasa Agent Tool MySQL datus:

```javascript
// ✅ PAREIZI — caur Nerve Center
const res = await fetch('https://vt-nerve-center-production-da7f.up.railway.app/api/orders/stats/summary', {
  headers: { 'X-API-Key': process.env.NERVE_CENTER_API_KEY }
});

// ❌ NEPAREIZI — tieša MySQL vai vecais proxy
const res = await fetch('https://portal.vanillatravel.lv/api/sales-ai/agent-tool/query?sql=...');
```

## Kontakts

Jautājumi par Nerve Center → CTO sesija (`claude-workspace/board-members/cto/`).
API Key pieprasījumi → CTO.

---
*Šis fails automātiski izdzēšams pēc izlasīšanas. Tas ir vienreizējs briefings.*
