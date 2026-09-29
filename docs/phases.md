> Earlier proposal. The current hackathon specification is [the root PRD](../PRD.md). See [implementation status](../IMPLEMENTATION_SUMMARY.md) for delivered scope and external dependencies.

# JanVastu — Phase-Wise Build Plan (for Antigravity)

**Last Updated**: 2025

This document is the working build plan for JanVastu. Each phase below is written as a self-contained task brief to paste into an agentic coding tool (e.g. Google Antigravity). Run phases **in order** — Phases 2–5 depend on Phase 1's API contract being stable.

**Before running Phase 0**, tell the agent explicitly:

> Before scaffolding, read all files in `docs/` and treat `rules.md`, `architecture.md`, and `PRD.md` as binding specs for coding standards, data model, and requirements.

After each phase: review the agent's walkthrough/Artifact, **manually verify** using the verification step listed, then commit and push before starting the next phase.

---

## Phase 0 — Repo Bootstrap

```
Create a new repository named "janvastu" for a Digital Public Good backend project.
Set up this exact folder structure (empty placeholder files/READMEs where needed):

janvastu/
├── docker-compose.yml
├── .env.example
├── Makefile
├── backend/
│   ├── pyproject.toml
│   ├── alembic/versions/
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── db/
│       ├── models/
│       ├── schemas/
│       ├── api/v1/
│       ├── core/
│       └── services/
│   └── tests/
├── ai-pipeline/{asr,nlu,vision,pipelines}/
├── decision-support/
├── channels/{ivr,whatsapp-bot,mobile-app,csc-terminal}/
├── frontend/{policymaker-dashboard,public-portal}/
├── integrations/
├── infra/{terraform,helm,k8s}/
└── docs/

Use Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL+PostGIS, Poetry for backend dependency management.
License: Apache 2.0.
Do NOT write business logic yet — just scaffold structure, pyproject.toml with dependencies (fastapi, uvicorn, sqlalchemy, alembic, psycopg2-binary, geoalchemy2, pydantic-settings, python-multipart), and a working `docker-compose.yml` with services: postgres (postgis/postgis:16-3.4 image), redis, minio.
Verify by running `docker-compose up -d` and confirming all three containers start healthy.
```

**Verify**: `docker-compose up -d` → all three containers healthy.

---

## Phase 1 — Database Schema + Core API

```
Working in the janvastu/backend directory, implement the core data layer and first API endpoints.

1. SQLAlchemy models in app/models/:
   - AdminUnit (village/block/district/state, PostGIS geometry boundary)
   - Consent (id, purpose, language, channel, timestamp, consent_hash — NOT linked to citizen identity)
   - Feedback (id, consent_id FK, category enum [Road,Water,Health,Education,Electricity,Sanitation,Housing,Other], description_text, language, geo location as PostGIS Point, admin_unit_id FK, status enum [new,triaged,in_progress,resolved], media_urls array, created_at)
   - Asset (id, name, type, geo location, admin_unit_id FK, source system enum [IIG,eSAKSHI,PMGSY])
   - AccountabilityRecord (id, asset_id FK, contractor_name, sanctioned_cost, actual_cost, planned_completion_date, actual_completion_date, responsible_official, department)

2. Alembic migration for all tables, with PostGIS extension enabled.

3. Pydantic schemas in app/schemas/ matching the models (Create/Read variants).

4. API endpoints in app/api/v1/:
   - POST /consent — records consent, returns consent_id
   - POST /feedback — requires valid consent_id, accepts category/description/language/lat/lon/media_urls, reverse-resolves admin_unit_id from lat/lon (stub this resolution for now, return null if no match), returns feedback_id
   - GET /feedback/{id} — returns feedback record
   - GET /accountability?lat=&lon=&radius_m= — finds nearest Asset(s) within radius and returns their AccountabilityRecord
   - GET /health — returns {"status": "ok"} and DB connectivity check

5. Anonymization rule: Feedback table must never store a citizen identifier or phone number directly — only the consent_id foreign key.

Write basic pytest tests for POST /consent and POST /feedback happy paths.
Verify by running the FastAPI app, hitting /docs, and successfully POSTing a consent then a feedback item via curl, confirming rows appear in Postgres.
```

**Verify**: `/docs` loads → POST consent → POST feedback → rows visible in Postgres via `psql`.

---

## Phase 2 — Collection Channel (WhatsApp-style webhook)

```
In janvastu/channels/whatsapp-bot, build a FastAPI webhook service that simulates a WhatsApp Business API integration (do not require real Meta API keys yet — build against a mock/local sender first, with a clearly marked adapter point to plug in Gupshup/Meta credentials later).

Flow to implement (matches janvastu/docs/consent-flow.md):
1. Incoming message webhook receives sender_id, message_type (text/voice/image), payload, language_hint
2. On first contact from a sender, service replies with consent notice text (mock multilingual — support at least English and Hindi text) and awaits "yes"/"no"
3. On consent "yes", call backend POST /consent, store the returned consent_id keyed to a short-lived session (NOT to sender identity long-term)
4. Subsequent messages from that session are forwarded to backend POST /feedback with category left null (to be filled by AI pipeline later) and description_text = raw message text
5. Bot replies with the feedback_id as a tracking reference

Include a simple local test harness (a script or /simulate endpoint) that lets me POST fake incoming messages without a real WhatsApp account, so I can verify the full consent → feedback flow end-to-end against the Phase 1 backend running locally.

Verify by running both services together and completing one full simulated conversation, confirming a Feedback row with linked Consent row exists in Postgres.
```

**Verify**: full simulated conversation → linked Consent + Feedback rows in Postgres.

---

## Phase 3 — AI Processing (rules-based first, model-ready structure)

```
In janvastu/ai-pipeline, build the intent classification and language ID stages as a Kafka-free, callable Python module first (no Kafka yet — that comes in Phase 3b), so it can be unit tested and later wired into the ingestion path.

1. ai-pipeline/nlu/language_id.py — function detect_language(text: str) -> str, initially using a simple heuristic/langdetect library fallback, with a clearly marked TODO and interface contract for swapping in a FastText model later.
2. ai-pipeline/nlu/intent_classifier.py — function classify_intent(text: str, language: str) -> list[str], initially implemented as a keyword/rule-based classifier mapping to categories [Road, Water, Health, Education, Electricity, Sanitation, Housing, Other] with multi-label support, with a TODO marker for swapping in fine-tuned IndicBERT/MuRIL later.
3. A pipeline function process_feedback_text(feedback_id: int) that: fetches the Feedback row via the backend API, runs language_id + intent_classifier, and PATCHes the Feedback row's category and language fields back via a new PATCH /feedback/{id}/enrich endpoint (add this endpoint to backend/app/api/v1/feedback.py).

Write unit tests for language_id and intent_classifier with at least 5 sample sentences per category (English + Hindi transliterated).
Verify by running process_feedback_text against a real feedback_id created in Phase 1/2 and confirming the category field updates in Postgres.
```

**Verify**: run `process_feedback_text` on a real feedback_id → `category`/`language` fields update in Postgres.

---

## Phase 4 — Decision Support (Gap Ratio + hotspot dashboard)

```
In janvastu/decision-support, implement:

1. gap_ratio.py — the function from rules.md:
   def compute_gap_ratio(demand_score: float, infra_stock: float, planned_investment: float) -> float
   (return float("inf") if denominator is zero), fully type-hinted, PEP 8, with docstring and unit tests.

2. demand_intensity.py — function compute_demand_intensity(admin_unit_id) that queries the backend for Feedback count grouped by category within that admin unit over the last 90 days, weighted by a simple recency decay, returns a float score.

3. A new backend endpoint GET /dashboard/hotspots that, for every AdminUnit with at least one Feedback record, returns {admin_unit_id, name, lat, lon, demand_intensity, gap_ratio, dominant_category}. Use placeholder infra_stock=1.0 and planned_investment=0.0 for now (real values come from IIG/eSAKSHI integration later — leave a TODO).

4. In janvastu/frontend/policymaker-dashboard, scaffold a minimal React + Leaflet (or Mapbox GL) app that calls GET /dashboard/hotspots and renders a heatmap/marker map colored by gap_ratio, with a sidebar table sortable by gap_ratio descending.

Verify by seeding at least 10 feedback items across 3 different admin units via the Phase 1 API, then confirming the dashboard renders 3 distinct hotspot markers with correct relative gap_ratio ordering.
```

**Verify**: seed 10+ feedback items across 3 admin units → dashboard shows 3 distinct hotspots, correctly ordered by gap ratio.

---

## Phase 5 — Accountability Module (public-facing)

```
In janvastu/frontend/public-portal, build a minimal public React page where a citizen can:
1. Search by admin unit name or drop a pin on a map
2. Call backend GET /accountability?lat=&lon=&radius_m=500
3. Display results as cards: asset name, contractor_name, sanctioned_cost vs actual_cost, planned vs actual completion date, responsible_official, department — with a clear "no project found nearby" empty state

Seed the backend with 5 mock Asset + AccountabilityRecord rows (via a seed script in backend/app/db/seed.py) spread across the same admin units used in Phase 4, so this page has real data to show.

Verify by running the seed script, then loading the public-portal page, searching one of the seeded admin units, and confirming the correct accountability card renders with matching data from Postgres.
```

**Verify**: run seed script → search seeded admin unit on public portal → correct accountability card renders.

---

## Upcoming Phases (not yet detailed)

- **Phase 3b** — Wire the AI pipeline (Phase 3) into Kafka for real-time ingestion instead of manual invocation.
- **Phase 6** — Deployment: Helm charts + Kubernetes manifests in `infra/`, per `architecture.md §5` and `§10`.
- **Phase 7+** — Real integrations with PFMS, IIG, and eSAKSHI once MoUs are signed (currently "Pending" per `architecture.md §7` and `PRD.md §8`); IVR gateway (Asterisk/FreeSWITCH); CSC terminal UI; mobile app (React Native) offline sync.

---

## Working Notes

- Keep agent runs sequential across phases — don't parallelize Phases 2–5 until Phase 1's API contract is stable.
- Manually verify each phase yourself (curl, psql, browser) rather than trusting the agent's self-reported walkthrough alone — PostGIS geometry/SRID issues and multi-service docker-compose wiring are common failure points.
- Keep `.env.example` updated as each phase introduces new services/credentials.
- Commit and push after each verified phase for a clean rollback trail.
