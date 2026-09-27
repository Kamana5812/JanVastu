# JanVastu — Delivery Phases

Step-by-step, one phase at a time, with a checkpoint before advancing. Each phase now lists **Frontend** and **Backend** deliverables side by side, since the backend is real (FastAPI + PostgreSQL/PostGIS, see `ARCHITECTURE.md`), not mocked. Exit criteria cover both.

---

### Phase 0 — Foundation
**Frontend:**
- Vite + React scaffold, design tokens (`design-system/tokens.css`), core primitives (Button, Card, Badge, Input, Modal, EmptyState, LoadingState, ErrorState), `lucide-react` wired, i18n scaffold (`en.json` seeded, `hi.json`/`or.json` shells), `AuthContext` + `ProtectedRoute` + `rbac.js` skeleton, router with every route stubbed.

**Backend:**
- FastAPI project scaffold, `docker-compose.yml` (api + postgres/postgis + minio), Alembic set up, base `users` table + one health-check endpoint (`GET /api/v1/health`).
- `.env` files for both frontend and backend created (not committed) per `ARCHITECTURE.md` §8.

**Exit criteria:** `docker-compose up` brings up API + DB + storage; frontend boots and can successfully call the health-check endpoint; router navigates between placeholder screens; primitives render with brand tokens applied.

---

### Phase 1 — Public Entry
**Frontend:** Role Selection (`/auth/role`) — four cards per PRD §4.1, reference-image layout, footer link to `/auth/login`.
**Backend:** none required (static page).

**Exit criteria:** role selection matches brand + reference layout; every card CTA navigates correctly.

---

### Phase 2 — Authentication
**Frontend:** Login, Citizen Signup, Volunteer Signup, Official Access + Access Request, Auditor Access, Admin Login — full validation, loading/error/success states, OTP UI flow, role-based redirect after auth success.

**Backend:** `auth` router — real `POST /auth/signup/citizen`, `POST /auth/signup/volunteer` (creates `status=pending_approval`), `POST /auth/access-request` (writes to `access_requests`), `POST /auth/login` (real password check, issues JWT), `POST /admin/login` (separate, stricter path), `POST /auth/otp/verify` (mocked fixed-code check, but a real endpoint). Password hashing via `bcrypt`. RBAC dependency (`require_role`) scaffolded and applied to a first protected test route.

**Exit criteria:** every role can sign up/log in against the **real database** and land on the correct post-auth route; a citizen JWT genuinely cannot access an admin-only test route (403, not just a hidden nav item); Admin route is not discoverable from any public nav.

---

### Phase 3 — Citizen Experience
**Frontend:** Citizen Dashboard, Report a Need, My Requests, Nearby, Projects — full report flow, mobile-first pass.

**Backend:** `requests` router — `POST /requests` (real insert, calls `ai_pipeline.classify()` and `geocoding.reverse()` for real), `POST /requests/{id}/media` (real upload to MinIO), `GET /requests` scoped to the authenticated citizen.

**Exit criteria:** a citizen can complete the full report-to-tracking loop and the submitted request is a real row in Postgres with a real geocoded location, visible only to that citizen via `GET /requests`.

---

### Phase 4 — Volunteer Experience
**Frontend:** Volunteer Dashboard, Capture Request, Verification, Offline Queue/Sync — KPI tiles, capture flow, offline banner + local queue.

**Backend:** `volunteers` router — `POST /volunteers/sync` accepting a batch of offline-captured requests and inserting them attributed to the volunteer; KPI counts (`Requests Captured`, `Verified Today`, etc.) computed from real `requests` rows, not hardcoded numbers.

**Exit criteria:** a request captured offline and "synced" produces real rows queryable by the relevant district's dashboard endpoint.

---

### Phase 5 — Policymaker Dashboards
**Frontend:** District/State/National (`/dashboard/*`) — shared components, KPI row, Demand & Infrastructure Map with layer toggles, category filters, Gap Indicator panel (mandatory disclosure label), explainable recommendation cards. State adds district drill-down; National adds full filter set.

**Backend:** `dashboard` router — `GET /dashboard/{scope}` computing real KPIs from `requests`, and a real `gap_engine.compute()` running the Demand-Supply Gap Ratio formula over `requests` + seeded `infrastructure_stock` + `planned_investment`. Seed script populates sample infrastructure/investment data per district before this phase starts.

**Exit criteria:** switching scope reuses the same components against real filtered queries; the Gap Indicator value is a genuine computation over seeded data (never a hardcoded display number); every recommendation expands into its real contributing signals; the "not an official government metric" label is present everywhere.

---

### Phase 6 — Public Accountability
**Frontend:** `/accountability` (public, unauthenticated) — search, project cards, project detail with timeline and source badges, "Report an Issue" CTA.

**Backend:** `projects` router — `GET /projects/search`, `GET /projects/{id}` (both public, no auth), backed by the seeded `projects`/`project_timeline_events`/`citizen_evidence` tables, each field returning its real `source_badge`.

**Exit criteria:** every field in project detail reflects a real `source_badge` value from the database, including genuine "Information Not Available" rows where seed data is intentionally sparse — never a client-side placeholder standing in for a missing backend field.

---

### Phase 7 — Admin & Governance
**Frontend:** `/admin` (Overview, Users, Roles & Permissions, Requests, Moderation, Data Governance, Consent, Audit Logs, Integrations, System Health, Reports).

**Backend:** `admin` router — real user list/status management, `access_requests` approve/reject (this is what actually unlocks Volunteer/Official/Auditor accounts), `GET /admin/audit-logs` (read-only — the DB role has no UPDATE/DELETE grant on `audit_logs`, verified in a test), `GET/PATCH /admin/consent`, `GET /admin/integrations` reading `integrations_status` (always `not_connected`/`planned`).

**Exit criteria:** approving a pending volunteer/official/auditor application in the Admin UI genuinely changes that user's `status` in the database and unlocks their login; no integration shows "Connected"; an attempt to modify an existing audit-log row via the API fails.

---

### Phase 8 — AI & Data Operations
**Frontend:** AI/Data Ops panel (admin/auditor-visible) — per-pipeline metrics display.

**Backend:** `ai_ops` router — `GET /ai-ops/pipelines` returns **real** counters (requests processed, average latency, language-ID/category-classification distribution) computed from the actual lightweight pipeline runs logged during Phases 3–4, not invented figures. Clearly scoped as reflecting the lightweight hackathon pipeline, not production ASR/NLP models.

**Exit criteria:** the numbers on this screen move when new requests are submitted elsewhere in the app — proof they're real, not static mock values.

---

### Phase 9 — Cross-Cutting Polish & Hardening
- **Frontend:** accessibility pass, complete Hindi/Odia translations, responsive QA, full states audit, RBAC audit against the real backend (attempt every protected route as every other role's real JWT and confirm 403/redirect).
- **Backend:** input validation review, consistent error responses, basic rate limiting on `auth` endpoints, `pytest` coverage for at least the happy path + one RBAC-denial path per router, secrets/env review (nothing sensitive committed), seed-data reset script finalized for demo/reset use.

**Exit criteria:** the app can be demoed start-to-finish for any one role, in any of the three shipped languages, entirely against the real backend and database — no remaining screen silently reading from `mocks/`.

---

**Working rule for every phase:** don't start the next phase until the current one's exit criteria (frontend **and** backend) are confirmed. If scope needs to shift mid-phase, update this file and `MEMORY.md` rather than silently drifting.
