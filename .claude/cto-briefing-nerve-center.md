# CTO Briefing: VT Nerve Center — Impact on Marketing Dashboard

**No:** CTO
**Kam:** AutoResearch PM (marketing dashboard developer)
**Datums:** 2026-04-11
**Prioritāte:** 🔴 AUGSTA — migrēt uz Nerve Center TAGAD, ne gaidīt

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

### 🔴 TUVĀKAJĀS DIENĀS — OBLIGĀTA MIGRĀCIJA

CEO norādījums: konsolidācija notiek DIENĀS, ne mēnešos. Tāpēc:

1. **TAGAD migrēt visus jaunus datu pieprasījumus uz Nerve Center REST API.** Nekādas jaunas tiešas MySQL vai proxy queries.
2. **Esošie executive dashboard pieprasījumi** — plānot pāreju uz Nerve Center tuvākajās dienās. Kad CTO paziņo "tiešā MySQL bloķēta" — vecais ceļš pārstās strādāt.
3. **Ja vajag endpoint kas Nerve Center vēl nav** — pieprasi CTO, viņš pievienos ātri.

### Ko tev OBLIGĀTI jādara:

1. **Visas jaunas datu funkcijas** — TIKAI caur Nerve Center REST API.
2. **API Key** — pieprasi CTO (vai lieto to pašu kas jau ir Railway `API_KEYS` env).
3. **Kešošana** — Nerve Center jau kešo bieži pieprasītus datus (10-30 min TTL). Nav jābūvē savs keš.
4. **Rate limiting** — 120 req/min per IP.
5. **Ja vajag SQL query kas nav endpoint** — NERAKSTI tiešu SQL caur proxy. Pieprasi CTO pievienot endpoint.

## Migrācijas piemērs

```javascript
// ✅ PAREIZI — caur Nerve Center (VIENĪGAIS PIEĻAUJAMAIS VEIDS)
const NERVE = 'https://vt-nerve-center-production-da7f.up.railway.app';
const API_KEY = process.env.NERVE_CENTER_API_KEY;

// Pasūtījumu statistika
const orders = await fetch(`${NERVE}/api/orders/stats/summary`, {
  headers: { 'X-API-Key': API_KEY }
});

// Klientu segmenti
const segments = await fetch(`${NERVE}/api/clients/stats/segments`, {
  headers: { 'X-API-Key': API_KEY }
});

// Deals pipeline
const deals = await fetch(`${NERVE}/api/deals/stats/pipeline`, {
  headers: { 'X-API-Key': API_KEY }
});

// Viesnīcu AI pārklājums
const coverage = await fetch(`${NERVE}/api/hotels/stats/coverage`, {
  headers: { 'X-API-Key': API_KEY }
});

// ❌ NEPAREIZI — tieša MySQL vai vecais proxy (DRĪZ PĀRSTĀS STRĀDĀT!)
const res = await fetch('https://portal.vanillatravel.lv/api/sales-ai/agent-tool/query?sql=...');
```

## Ja tev vajag endpoint kas vēl neeksistē

Raksti pieprasījumu šeit (CTO to izlasīs):

```
### ENDPOINT REQUEST
- Kādi dati vajadzīgi: [apraksts]
- Kādā formātā: [JSON struktūra]  
- Cik bieži: [reāllaiks / cached ok]
- Priekš kā: [dashboard sekcija / automatizācija]
```

## Kontakts

Jautājumi par Nerve Center → CTO sesija (`claude-workspace/board-members/cto/`).
API Key — jau ir Railway `API_KEYS` env, vai pieprasi CTO papildus.

---
**⚠️ ŠIS NAV INFORMATĪVS DOKUMENTS — ŠĪ IR OBLIGĀTA MIGRĀCIJAS INSTRUKCIJA.**
Tiešā MySQL pieeja tiks bloķēta tuvākajās dienās.
