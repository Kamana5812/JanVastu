> Historical copy. Current source: [ARCHITECTURE.md](ARCHITECTURE.md). Current implementation status: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md).

# JanVastu — Full-Stack Architecture

Companion to `PRD.md`. Defines how the app is built, not what it does. Updated to include a **real backend and real database**, per the "hackathon architecture" defined in the original JanVastu proposal (single PostgreSQL+PostGIS instance, simple REST endpoints) — the fuller Kafka/Debezium/Kubernetes production architecture from that same proposal remains explicitly out of scope for this build (see §11).

## 1. Stack

| Concern | Choice | Why |
|---|---|---|
| Frontend build tool | **Vite** | Fast dev server, matches the spec exactly |
| Frontend framework | **React** (function components + hooks) | Matches existing skillset and the spec |
| Styling | **Plain CSS / CSS Modules** | Spec explicitly forbids Tailwind unless the existing project already requires it — none does yet |
| Routing | **React Router v6** | Standard, supports nested layouts + guards cleanly |
| Icons | **lucide-react** | Spec explicitly requires a professional SVG icon set, no emojis |
| Frontend state | **React Context + hooks**, local component state | The app talks to one backend, not many services; no heavier store is justified yet |
| Backend framework | **FastAPI (Python)** | Matches the proposal's own tech stack; fast to build REST endpoints; natural fit if real AI/ML models are added later |
| Database | **PostgreSQL + PostGIS** | The proposal's own "hackathon architecture" choice — genuinely necessary since demand/project data is geospatial |
| ORM / migrations | **SQLAlchemy + Alembic** | Standard pairing with FastAPI, keeps schema changes versioned |
| Auth | **JWT (access + refresh tokens)**, `passlib`/`bcrypt` password hashing | Real, not mocked — see §5 |
| File/media storage | **MinIO** (S3-compatible, self-hosted) for local/dev; a real S3 bucket is a drop-in swap later | Matches the proposal's "S3-compatible object storage" without requiring a paid cloud account for the hackathon |
| Geocoding | **OpenStreetMap Nominatim**, called server-side | A real, free, no-auth-required integration — matches the proposal's OSM-first geocoding decision; Bhuvan stays a future/production integration |
| AI/NLP (this phase) | Lightweight, real but modest: `langdetect`/`fasttext` for language ID, a simple keyword/rule-based classifier for category, stored behind one internal interface | The proposal's own "hackathon vs. production" split says not to claim IndicConformer/IndicBERT-level production readiness yet — but the pipeline is real, not faked, and swappable later |
| Local orchestration | **Docker Compose** (api + postgres/postgis + minio) | Matches the proposal's hackathon-stage deployment target |
| i18n | **A lightweight key-based dictionary** (`t(key)` hook backed by JSON per language) | Spec requires translation keys, not hard-coded text |

## 2. Repository Structure

```
frontend/
  src/
    app/                     # App.jsx, routes.jsx
    auth/                    # AuthContext, ProtectedRoute, api/authApi.js
    i18n/
    design-system/
    layouts/
    features/
      role-selection/  auth/  citizen/  volunteer/  policymaker/  accountability/  admin/  ai-ops/
    api/                     # thin fetch/axios clients per resource, one file per backend router
    utils/

backend/
  app/
    main.py                  # FastAPI app, router registration, CORS
    core/
      config.py               # settings from env vars
      security.py              # JWT issue/verify, password hashing
      rbac.py                  # role → permission map, FastAPI dependency
    db/
      base.py                  # SQLAlchemy engine/session
      models/                  # one file per table (see §4)
      migrations/               # Alembic
    routers/
      auth.py  users.py  requests.py  volunteers.py  projects.py
      dashboard.py  admin.py  ai_ops.py  integrations.py
    services/
      geocoding.py              # Nominatim client
      storage.py                 # MinIO client
      ai_pipeline.py              # language ID + category classification (real, lightweight)
      gap_engine.py                # Demand-Supply Gap Ratio computation (real formula, seeded data)
    schemas/                   # Pydantic request/response models, mirrored 1:1 with frontend api/ clients
    seed/
      seed_data.py               # seeds sample users, infrastructure stock, sample projects (esakshi-style)
  tests/
  docker-compose.yml
  Dockerfile
```

## 3. API Surface (v1, all under `/api/v1`)

| Router | Key endpoints | Auth required |
|---|---|---|
| `auth` | `POST /auth/signup/citizen`, `POST /auth/signup/volunteer`, `POST /auth/access-request`, `POST /auth/login`, `POST /admin/login`, `POST /auth/otp/verify` (mocked fixed-code verification) | No (these *are* the entry points) |
| `users` | `GET /users/me`, `PATCH /users/me` | Yes |
| `requests` | `POST /requests` (citizen/volunteer create), `GET /requests` (own, or scoped for officials), `GET /requests/{id}`, `POST /requests/{id}/media` (upload to MinIO) | Yes |
| `volunteers` | `POST /volunteers/sync` (batch upload of offline-captured requests) | Yes, volunteer role |
| `projects` | `GET /projects/search`, `GET /projects/{id}` (public — no auth) | No |
| `dashboard` | `GET /dashboard/{scope}` where scope ∈ `district|state|national`, with query filters; returns KPIs, map layer data, Gap Indicator values, recommendation explanations | Yes, official role scoped accordingly |
| `admin` | `GET/PATCH /admin/users`, `GET /admin/moderation`, `GET /admin/audit-logs` (read-only), `GET/PATCH /admin/consent`, `GET /admin/integrations` (always `not_connected`/`planned`) | Yes, admin role |
| `ai_ops` | `GET /ai-ops/pipelines` — real counters/latency pulled from the actual (lightweight) pipeline run in this app, not invented | Yes, admin/auditor role |

Every response schema mirrors a frontend `api/*Api.js` client 1:1, so the frontend never needs to reshape data.

## 4. Database Schema (PostgreSQL + PostGIS, real tables)

- **users** — id, role (`citizen|volunteer|district_official|state_planner|national_planner|auditor|admin`), name, mobile, email (nullable), password_hash, preferred_language, state, district, locality, ward_village (nullable), status (`active|pending_approval|suspended`), created_at.
- **access_requests** — id, user_id, role_requested, organization, designation, reason, status (`pending|approved|rejected`), reviewed_by, reviewed_at. Drives the Volunteer/Official/Auditor approval flow — nothing is auto-approved.
- **requests** (citizen demand records) — id, submitted_by (user_id), category, description, transcript, language, location `geography(Point, 4326)`, state/district/locality (denormalized for fast filtering), status, demand_intensity_component (computed, not fabricated), created_at.
- **request_media** — id, request_id, type (`photo|video`), storage_key (MinIO), uploaded_at.
- **infrastructure_stock** — id, category, location `geography(Point, 4326)`, district, capacity/condition fields, source (`pmgsy_seed|esakshi_seed|manual_seed`) — **seeded sample data**, clearly labeled as such, never presented as live government data.
- **planned_investment** — id, district, category, amount, source — seeded, same labeling discipline.
- **projects** (accountability records) — id, name, department, contractor, sanctioned_cost, actual_cost, planned_start, planned_completion, actual_completion, status, responsible_agency, location `geography(Point,4326)`, each field carrying a `source_badge` enum (`verified|citizen_submitted|government_dataset|integrated_dataset|unavailable`).
- **project_timeline_events** — id, project_id, stage (`sanctioned|tendered|awarded|started|in_progress|completed`), occurred_at.
- **citizen_evidence** — id, project_id (nullable), request_id (nullable), media/storage_key, anonymized flag.
- **audit_logs** — id, timestamp, actor_id, role, action, resource, result. **Insert-only**: the database role the API uses has no `UPDATE`/`DELETE` grant on this table, enforced at the DB level, not just the UI.
- **consent_records** — id, user_id, consent_version, status (`active|withdrawn|pending`), recorded_at.
- **integrations_status** — id, name (`pfms|iig|esakshi|pmgsy_gis|cpgrams|state_edistrict|csc|depa`), status (`not_connected|planned`) — never `connected` until a real integration is built.

Seed script (`seed/seed_data.py`) populates infrastructure_stock, planned_investment, and a handful of eSAKSHI-styled sample projects so the dashboards and accountability portal have real rows to query — sample data, explicitly labeled, never claimed as live.

## 5. Auth & RBAC — now real, not just a frontend convention

- Signup/login issue a real JWT (short-lived access token + refresh token) containing `sub` (user id) and `role`.
- `core/rbac.py` defines the same `permissions[role]` map referenced in the frontend, but here it's a **FastAPI dependency** (`require_role(...)`) applied to every protected router — this is the actual authorization boundary now.
- The frontend `ProtectedRoute` and `rbac.js` remain in place for UX (don't show a citizen an admin nav item) but are no longer the security boundary — the backend independently re-checks role on every request, per `RULES.md`.
- OTP/MFA endpoints exist and are called for real by the frontend, but verification is a fixed mock code in this phase (no real SMS/email gateway) — documented as a stub, not silently pretended to be production-grade.
- Passwords are always hashed (`bcrypt` via `passlib`); plaintext passwords are never logged or stored.

## 6. Data Flow (now real network calls, not in-memory mocks)

### 6.1 Citizen report flow
```
ReportNeed form
  → POST /api/v1/requests {category?, description, language, lat/lng}
      backend: ai_pipeline.classify() (real lightweight langID + keyword category check)
             → geocoding.reverse(lat,lng) via Nominatim
             → INSERT INTO requests
  → POST /api/v1/requests/{id}/media (photo/video → MinIO)
  → GET /api/v1/requests (My Requests, filtered to current user)
```

### 6.2 Policymaker dashboard flow
```
GET /api/v1/dashboard/district?district=X&category=Y
  → gap_engine.compute(district, category)
      SELECT demand from requests + infrastructure_stock + planned_investment
      → Demand-Supply Gap Ratio = Demand Intensity / (Infrastructure Stock + Planned Investment), vulnerability-weighted
  → response includes contributing signals per surfaced area (for the "why was this surfaced" explanation)
```
Every ratio in the response is tagged so the frontend can render the mandatory "JanVastu Analytical Indicator — not an official government metric" label — this label is a **rule**, not a suggestion (see `RULES.md`).

### 6.3 Accountability flow
```
GET /api/v1/projects/search?q=... (public, no auth)
GET /api/v1/projects/{id} → every field carries its source_badge from the DB
```

## 7. Integration Points — status honesty preserved
`integrations_status` table + `GET /admin/integrations` are the single source of truth for PFMS, IIG, eSAKSHI, PMGSY GIS, CPGRAMS, State e-District, CSC, DEPA. All rows start at `not_connected` or `planned`; nothing flips to `connected` until a real adapter exists. OSM/Nominatim is the one exception — it's a genuinely live, working integration in this phase, and is tracked separately from that table (it's infrastructure, not a civic data source).

## 8. Environment & Secrets
- `backend/.env` (never committed): `DATABASE_URL`, `JWT_SECRET`, `MINIO_*` credentials, `NOMINATIM_BASE_URL`.
- `frontend/.env`: `VITE_API_BASE_URL` only — no secrets ever ship to the frontend.
- `docker-compose.yml` wires `api`, `postgres` (with PostGIS extension enabled on init), and `minio` together for one-command local startup.

## 9. Testing Approach
- Backend: `pytest` + `httpx` for endpoint tests — at minimum, one test per router covering the happy path and one RBAC-denial path (e.g. a citizen token hitting an admin-only endpoint must get 403).
- Frontend: component smoke tests for design-system primitives; one integration test per critical flow (login → redirect by role; citizen report submit → appears in My Requests), now hitting a test instance of the real API rather than a mock.
- A seed/reset script for tests so the database starts from a known state each run.

## 10. Migration Notes from the Mock-Data Phase
- Frontend `mocks/services/*` files are replaced by `frontend/src/api/*Api.js` clients with the **same function signatures**, so feature components barely change — only the data-fetching layer underneath does.
- `mocks/data/*` sample records become the seed data in `backend/app/seed/seed_data.py` instead of being deleted — the same sample citizens/requests/projects now live in Postgres.
- Everything in `RULES.md` about never fabricating data, never showing false "Connected" integrations, and always labeling the Gap Indicator applies identically — only *where* the data lives has changed.

## 11. Still Explicitly Out of Scope (unchanged from the proposal's own staging)
- Kafka/Debezium streaming and change-data-capture — proposal's own Stage 3–4 production roadmap, not this build.
- Kubernetes/multi-node deployment — Docker Compose is the target for this phase.
- Real integrations with PFMS/IIG/eSAKSHI/PMGSY GIS/CPGRAMS/e-District/CSC/DEPA — stubbed via `integrations_status`.
- Production-grade ASR (IndicConformer/Vak) and heavy NLP/vision models (IndicBERT, YOLOv8 fine-tunes) — the lightweight real pipeline in §1/§6.1 stands in for now, behind an interface designed to swap them in later without an API contract change.
- Real SMS/email delivery for OTP/MFA — endpoints exist, verification is a fixed mock code.
