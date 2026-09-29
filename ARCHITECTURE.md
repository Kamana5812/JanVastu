# JanVastu architecture

Current implementation, 29 September 2026. Product requirements are in [PRD.md](PRD.md); historical proposals remain in numbered documents and `docs/`.

## Components

- React/Vite frontend, React Router, plain CSS tokens, Lucide icons, Leaflet maps and Context-based authentication and translation.
- FastAPI backend, SQLAlchemy, PostgreSQL 16/PostGIS and Alembic migrations in `backend/alembic`.
- Private MinIO evidence storage. API-mediated validation/upload/download; no public original-media URLs.
- Server-side Nominatim reverse geocoding with timeouts/cache and manual area fallback.
- Lightweight language detection and multilingual keyword category suggestions, with measured runs recorded in `pipeline_runs`.
- Docker Compose with database, storage, owner-only migration job, restricted API and Nginx frontend.

## Current API map

All routes have `/api/v1` prefix. FastAPI `/docs` is the generated endpoint reference.

| Area | Router and main paths |
|---|---|
| Authentication | `routers/auth.py`: `/auth/login`, `/auth/signup/citizen`, `/auth/access-request`, OTP/reset/Google/refresh; `/admin/login` |
| Profile/privacy | `routers/auth.py`: `/auth/me`; `routers/account.py`: consent, notifications and erasure |
| Reporting | `routers/citizen.py`: `/citizen/needs`, analyze, media and own-request detail |
| Volunteer | `routers/volunteer.py`: `/volunteer/stats`, `/volunteer/tasks`, sync and verification |
| Planning | `routers/planner.py`: `/planner/dashboard`, scoped needs and status changes |
| Public records | `routers/projects.py`: `/projects/search`, `/projects/{id}`, reviewed public evidence |
| Administration | `routers/admin.py` and `routers/governance.py`: `/admin/*` |
| Pipeline metrics | `routers/ai_ops.py`: `/ai-ops/pipelines` |

Earlier documents used `/requests`, `/volunteers` and `/dashboard/{scope}` as conceptual names; the current paths above replace those names. Frontend uses `src/api/client.js` with refresh handling. Features live under `auth`, `citizen`, `volunteer`, `planner`, `admin`, `public` and `role-selection`.

## Stored data

Users, access requests, consent records, auth challenges, rotating refresh sessions and rate limits support access control. `needs`, `evidence`, `need_events`, `moderation_notes` and `pipeline_runs` support reporting and review. `planning_context` holds normalized infrastructure/investment/vulnerability inputs with explicit sample flags. `projects`, `project_timeline_events` and `integrations_status` support public records. `audit_logs` has database triggers and runtime privileges that prohibit UPDATE, DELETE and TRUNCATE.

Project locations and progress may be null. Supplied dataset observations are preserved in `projects.dataset_record`, with source IDs, original text, reference dates, conflicts and related components. No coordinates or day-level dates are inferred from screenshots. Unknown-location records are omitted from maps and nearby search. Unverified status is excluded from active-project counts. Screenshot costs are not converted into sanctioned/actual cost fields or planning indices.

## Flows and boundaries

A report is analyzed, confirmed by the user, persisted with consent and a retry key, then receives independently validated media. Coordinates can be entered manually when device GPS is unavailable; area details can be entered if reverse geocoding fails. Media retries use a content hash and cannot duplicate stored evidence. Volunteers may verify another reporter's request only inside their jurisdiction. Officials may transition verified requests to planned and planned to resolved within their scope.

The gap indicator uses recency-weighted demand times vulnerability divided by infrastructure stock plus planned investment. Missing inputs remain unavailable; zero supply with positive demand is labeled unbounded. These normalized demonstration indices are not rupee amounts or official metrics.

Raw citizen media is private. A reviewed, separately redacted image can become public only after administrator attestation and active account/report consent. Withdrawing consent immediately removes public eligibility. Erasure removes identifying profile/report/media content, revokes sessions, removes reporter attribution and coarsens retained request locations. Audit history remains append-only.

Passwords use bcrypt. Every protected request checks current database role/status and token version. Frontend route guards are only a convenience. Demo OTP is explicit; production configuration rejects it. Google tokens require configured audience, nonce and verified authoritative email identity.

## Deployment scope

`docker-compose.yml`, environment examples and [deployment guide](DEPLOYMENT_GUIDE.md) are the local reference. The migration job runs as owner; the API uses `janvastu_api`. Seeds preserve existing data. No destructive reset is shipped.

Google, live channel delivery, government systems, production speech/vision, streaming and Kubernetes need external setup or further implementation. Adapter status remains planned/not connected. See [verification](docs/VERIFICATION.md) for what was actually exercised.
