# Business Class Only Flight Booking Platform: Startup Research Report

## Executive Summary

This report analyzes the opportunity to build a business-class-only flight deal subscription platform, modeled on the success of Going.com (formerly Scott's Cheap Flights) but focused exclusively on premium cabin fares. The global premium cabin market represents a ~$30B opportunity, and no dominant player has yet captured the business-class-deals subscription niche. This document covers market sizing, competitor analysis, technology requirements, revenue models, conversion benchmarks, and build strategy for a solo founder leveraging AI.

---

## Going.com (Scott's Cheap Flights) — Business Model Reference

### Company Overview
- **Founded:** 2015, originally as Scott's Cheap Flights by Scott Keyes
- **Rebranded:** Going.com (2022)
- **Headquarters:** Boulder, Colorado, United States
- **Team Size:** 50+ employees (38% employee growth year-over-year)
- **Business Model:** Subscription-based flight deal alert service

### Revenue & Financials
- **Estimated Annual Revenue:** ~$7.5M (per CompWorth estimate) [Source](https://compworth.com/company/scott-s-cheap-flights)
- **Alternative estimate:** $1–$10M range (IncFact) [Source](https://incfact.com/company/scottscheapflights-portland-or/)
- **Revenue per Employee:** ~$136,400
- **Revenue Growth:** ~100% year-over-year at peak growth stages
- **Total Member Savings Generated:** $100M+ in airfare savings for members
- **Largest Single Member Saving:** $31,000 (5 tickets to Bali on a mistake business class fare)

### Subscription Pricing
- **Free tier:** Limited deal alerts
- **Premium tier:** $49/year (economy deals)
- **Elite tier:** $199/year (includes business class and premium cabin deals)
- **Subscribers:** 2 million+ members

### Key Operational Facts
- Uses a hybrid model: automated software + human flight experts to vet deals
- Does **not** rely purely on affiliate links — focuses on deal quality over volume
- 100% remote team
- NAICS Code: 5615 — Travel Arrangement & Reservation Services [Source](https://incfact.com/company/scottscheapflights-portland-or/)

### Revenue Model Insights
- Primary revenue: subscription fees
- Secondary revenue: affiliate commissions when members book through tracked links
- The $199/year Elite tier (business class focus) is the highest-margin product, suggesting strong willingness to pay among premium travelers

---

## Market Opportunity: Premium Cabin Flights

### Market Size
- **Global premium cabin (business + first class) market:** ~$30 billion annually
- Business class passengers represent a disproportionately high share of airline revenue despite being a small percentage of total passengers
- Premium leisure travel (vs. corporate) is a fast-growing segment post-2020

### Why Business Class Deals Exist
1. **Error fares / mistake fares:** Airlines or GDS systems occasionally publish incorrect prices
2. **Seat inventory management:** Airlines discount unsold premium seats close to departure
3. **Mileage/points redemption sweet spots:** Partner award space released at low rates
4. **Currency arbitrage:** Booking in weaker currencies for the same itinerary
5. **Positioning flights:** Airlines need to move aircraft and offer steep discounts
6. **NDC pricing inconsistencies:** New Distribution Capability rollout creates temporary pricing gaps across channels

### Target Customer
- High-income professionals and frequent travelers
- "Aspirational premium" travelers who fly economy but want business class at a deal
- Corporate travelers with flexible booking policies
- Points/miles enthusiasts seeking cash deal alternatives

---

## Competitor Landscape

### Direct Competitors (Business Class Focus)

| Platform | Model | Price Point | Notes |
|---|---|---|---|
| **Going Elite** (Going.com) | Subscription | $199/year | Business class tier within Going.com |
| **Secret Flying** | Free + ads | Free | Aggregates error fares publicly; less curated |
| **Business Class Guru** | Free + affiliate | Free | Blog/deal alert hybrid; affiliate-driven |
| **SkyLux Travel** | Direct booking | Commission-based | Acts as travel agency; books discounted biz class |
| **Premium-Flights.com** | Subscription/affiliate | Varies | European-focused premium fare alerts |

### Indirect Competitors
- **Airfarewatchdog** — general fare alerts
- **Google Flights** — free fare tracking, no curation
- **Hopper** — predictive pricing, economy-focused
- **Thrifty Traveler Premium** — subscription, includes some business class deals
- **The Flight Deal** — free blog, ad-supported, posts public error fares

### Competitive Gap Analysis
- No platform is **exclusively** focused on business class deals with a premium subscription model
- Going Elite is a bolt-on to an economy-first product, not purpose-built for premium travelers
- SkyLux operates as a travel agency (takes booking risk) rather than an alert/information service
- Secret Flying and Business Class Guru are free/ad-supported with lower curation quality
- **Opportunity:** A purpose-built, subscription-first, business-class-only platform with AI-powered monitoring is an unoccupied niche

---

## Technology Stack: AI-Powered Fare Monitoring

### The Core Technical Challenge
Monitoring millions of fare combinations (origin × destination × date × cabin class × airline) in real time requires scalable infrastructure. A solo founder with AI tools can now accomplish what previously required large engineering teams.

### Fare Data Sources

#### GDS (Global Distribution Systems)
- **Amadeus**, **Sabre**, **Travelport (Galileo/Worldspan)**
- Traditional access route for flight inventory data
- Startup access is possible but requires IATA accreditation or a host agency relationship
- Cost: typically per-transaction or monthly minimums
- Best for: comprehensive historical and real-time fare data

#### NDC (New Distribution Capability)
- IATA's modern XML-based API standard replacing legacy GDS for many airlines
- Airlines (American, British Airways, Lufthansa, etc.) now offer direct NDC APIs
- **Advantage for startups:** Some airlines offer NDC API access without full IATA accreditation
- **Key NDC aggregators for startups:** Duffel, Verteil, Travelfusion
- Duffel in particular offers startup-friendly API access to NDC content from 300+ airlines
- NDC can surface fares not available in traditional GDS channels

#### Aggregator/Scraping APIs
- **Skyscanner API** — partnership program for fare data
- **Kiwi.com Tequila API** — startup-friendly, broad fare access
- **RapidAPI flight data providers** — lower cost entry points
- **Aviasales API** — strong for Eastern European/Asian routes

### AI Fare Monitoring Architecture (Solo Founder Viable)

```
Data Ingestion Layer
├── NDC API feeds (Duffel or direct airline APIs)
├── GDS query automation (via host agency or aggregator)
└── Public fare scraping (where permitted)

AI Processing Layer
├── Baseline fare modeling (ML model per route/cabin/season)
├── Anomaly detection (statistical deviation from baseline)
├── Error fare classification (is this a mistake or a sale?)
├── Deal scoring (savings %, reliability, booking window)
└── Natural language generation (deal description writing)

Distribution Layer
├── Email alert system (SendGrid, Postmark)
├── Push notifications (mobile app or web push)
├── Member preference matching (origin airports, destinations)
└── Webhook/API for power users
```

### AI Tools Applicable to Solo Founder Build
- **OpenAI API / Claude API:** Generate deal descriptions, classify fare types, answer member queries
- **Python + scikit-learn / statsmodels:** Build baseline fare models and anomaly detection
- **Airflow or Prefect:** Orchestrate scheduled fare monitoring jobs
- **Pinecone or Weaviate:** Vector database for storing fare patterns and similarity search
- **Vercel + Next.js:** Frontend for member portal
- **Supabase or PlanetScale:** Backend database for members and fare history

### Error Fare Detection Logic
1. Establish rolling baseline fare per route/cabin/season using 90-day historical data
2. Flag fares that deviate >40% below baseline as potential deals
3. Cross-reference against multiple data sources to confirm the fare is live
4. Classify: error fare (likely short-lived, book immediately) vs. sale fare (stable, days to book)
5. Score deal quality: savings %, number of travel dates available, airline reliability
6. Auto-generate alert copy via LLM with booking instructions and expiry urgency

---

## Revenue Model & Pricing Strategy

### Subscription Tiers (Recommended for Business-Class-Only Platform)

| Tier | Price | Features |
|---|---|---|
| **Free** | $0 | 1–2 deals/month, email only, 7-day delay |
| **Premium** | $199/year (~$16.58/mo) | All business class deals, instant alerts, all origins |
| **Elite** | $349/year (~$29/mo) | Premium + first class, concierge booking help, API access |

**Rationale:**
- Going.com charges $199/year for a bolt-on business class tier within an economy product
- A purpose-built business class platform justifies a higher price point ($199–$349/year)
- The target customer (premium traveler) has demonstrated willingness to pay for quality information
- A single deal saving $2,000–$5,000 on a business class ticket makes a $349/year subscription a 10–15x ROI

### Affiliate Revenue Layer
- When members click through to book, use tracked affiliate links via:
  - **Travelpayouts** — aggregates airline affiliate programs
  - **CJ Affiliate / Rakuten** — major airline programs (Delta, United, BA, etc.)
  - **Direct airline affiliate programs** — higher commission rates (1–5% of ticket value)
- Business class ticket average: $3,000–$8,000 → affiliate commission: $60–$400 per booking
- Even at low click-through rates, affiliate revenue can meaningfully supplement subscription income

### Revenue Model Comparison

| Model | Pros | Cons |
|---|---|---|
| Subscription only | Predictable MRR, no booking risk | Slower growth, churn risk |
| Affiliate only | No subscription friction | Unpredictable, algorithm-dependent |
| Hybrid (subscription + affiliate) | Best of both; aligns incentives | Slightly more complex |
| Travel agency (like SkyLux) | Higher revenue per transaction | Requires licensing, booking risk, staffing |

**Recommendation:** Hybrid model — subscription as primary revenue, affiliate as secondary. Avoid acting as a travel agency in early stages.

---

## SaaS Conversion Rate Benchmarks for Subscription Platforms

Understanding industry conversion benchmarks is critical for modeling subscriber growth and optimizing the funnel for a business-class flight deal subscription service. [Source](https://www.artisangrowthstrategies.com/blog/saas-conversion-rate-benchmarks-2026-data-1200-companies)

### Key Funnel Benchmarks (2026 Data, 1,200+ SaaS Companies)

| Funnel Stage | Bottom 25% | Average | Elite (Top 10%) |
|---|---|---|---|
| Visitor-to-Lead | <0.7% | 1.5–2.5% | 8–15% |
| MQL-to-SQL | <20% | 32–40% | 39–40%+ |
| SQL-to-Close | <15% | 20–25% | 30%+ |

### Free-to-Paid Conversion Rates by Trial Model

| Trial Model | Average | Top 10% |
|---|---|---|
| Freemium (self-serve) | 3–5% | 6–8% |
| Free Trial (no credit card) | 4–6% | 10–15% |
| Free Trial (credit card required) | 25–35% | 50–60% |
| Median free-to-paid (all models, 2025) | 34% | — |

**Key insight:** Opt-out trials (credit card required upfront) convert at **48.8%** on average vs. 18.2% for opt-in trials. For a premium subscription targeting high-income travelers, requiring a credit card at free trial signup is likely appropriate and will significantly improve conversion rates.

### Trial Duration Impact
- **7-day trials:** Highest conversion rate at **40.4%**
- **Trials over 60 days:** Conversion drops to **30.6%**
- **Recommendation:** Use a 7–14 day free trial with full access to demonstrate deal quality before charging

### Marketing Channel Conversion Benchmarks
- **SEO:** 2.1% visitor-to-lead rate — highest among organic channels
- **PPC:** 0.7% visitor-to-lead rate
- **LinkedIn:** Strong ROI with SQL-to-close rates of **39%** — highly relevant for targeting business travelers and corporate accounts
- **Implication:** For a business-class platform, SEO content (deal alerts, route guides, "best business class to X" articles) and LinkedIn outreach to frequent business travelers are the highest-ROI acquisition channels

### Application to Business Class Subscription Platform
- At average conversion rates (1.5–2.5% visitor-to-lead, ~18% free-to-paid for opt-in trial):
  - 10,000 monthly visitors → 150–250 leads → 27–45 new paid subscribers/month
- At elite conversion rates (8–15% visitor-to-lead, ~50% free-to-paid with credit card):
  - 10,000 monthly visitors → 800–1,500 leads → 400–750 new paid subscribers/month
- **Year 1 target:** 1,000 paid subscribers at $199/year = **$199,000 ARR**
- **Year 2 target:** 5,000 paid subscribers at blended $220/year = **$1.1M ARR**
- **Year 3 target:** 20,000 paid subscribers = **$4.4M ARR** (approaching Going.com's estimated revenue with a fraction of the team)

---

## Go-To-Market Strategy

### Phase 1: Validation (Months 1–3)
- Launch a free email newsletter with 2–3 business class deals per week
- Build audience via Reddit (r/churning, r/awardtravel, r/solotravel), Twitter/X, LinkedIn
- Target: 1,000 free subscribers before charging anything
- Use Beehiiv or Substack for zero-infrastructure newsletter launch
- Manually source deals to validate demand before building automation

### Phase 2: Monetization (Months 4–6)
- Introduce paid tier at $149–$199/year with 14-day free trial (credit card required)
- Gate best deals (error fares, same-day alerts) behind paywall
- Target: 200–500 paying subscribers = $30K–$100K ARR
- Begin building automated fare monitoring infrastructure in parallel

### Phase 3: Scale (Months 7–18)
- Launch full AI-powered monitoring platform
- Add origin airport personalization (members set home airports)
- Introduce referral program (1 month free per referral)
- SEO content strategy: "Business class deals from [City]" landing pages
- Target: 2,000–5,000 paying subscribers

### Acquisition Channels (Prioritized)
1. **SEO** — "cheap business class flights," "business class mistake fares," route-specific pages
2. **LinkedIn** — target frequent business travelers, corporate travel managers
3. **Reddit/communities** — r/churning, r/awardtravel, FlyerTalk forums
4. **Partnerships** — credit card bloggers, points/miles influencers (affiliate deals)
5. **PR** — pitch "I found a $400 business class to Tokyo" stories to travel media

---

## Unit Economics & Financial Model

### Key Metrics to Track
- **CAC (Customer Acquisition Cost):** Target <$30 for organic, <$80 for paid
- **LTV (Lifetime Value):** At $199/year with 3-year average retention = $597 LTV
- **LTV:CAC ratio:** Target >5:1 for sustainable growth
- **Monthly Churn:** Target <3%/month (36% annual) for subscription travel products
- **Net Revenue Retention:** Upsell from $199 → $349 Elite tier improves NRR above 100%

### Revenue Projections (Conservative)

| Year | Paid Subscribers | Avg. Revenue/Sub | ARR | Affiliate Revenue | Total Revenue |
|---|---|---|---|---|---|
| Year 1 | 1,000 | $199 | $199K | $20K | ~$220K |
| Year 2 | 5,000 | $210