> Historical audit. Findings below describe the original code on 27 September 2026. Remediation and current checks are tracked in [verification](VERIFICATION.md) and [implementation status](../IMPLEMENTATION_SUMMARY.md).

# JanVastu documentation and implementation audit

Reviewed: 27 September 2026.

## Verdict

**No: all documented requirements are not included.** The repository contains a partial full-stack prototype with substantial missing functionality, disconnected flows, and a failing frontend build. Existing claims of complete implementation and production readiness are not supported by the current source.

This review compares local documents with source code and configuration. A file or screen existing is not proof that its workflow works. No live database, deployment, visual layout, or legal compliance was certified.

## Documents reviewed and scope

Reviewed all 15 project Markdown documents present before this audit, plus the Alembic README:

- Root: `README.md`, `PRD (3).md`, `ARCHITECTURE (4).md`, `DESIGN (2).md`, `RULES (4).md`, `PHASES (4).md`, `MEMORY (2).md`, `IMPLEMENTATION_SUMMARY.md`, `DEPLOYMENT_GUIDE.md`.
- `docs/`: `PRD.md`, `architecture.md`, `rules.md`, `phases.md`, `consent-flow.md`.
- `frontend/README.md` and `backend/alembic/README`.

Also inspected frontend routes/components, backend routes/models/services, test sources, migration setup, seed script, AI and WhatsApp services, decision functions, integration adapters, dependency manifests, deployment configuration, and the license header.

The root full-stack PRD explicitly calls itself the working implementation specification. It is the primary basis for the current-build checklist. The older `docs/` specifications describe a broader product and a different API/data model. Their requirements are tracked separately below because the two sets have not been reconciled.

## Current-build coverage

| Area | Status | Evidence and missing requirements |
|---|---|---|
| Foundation | Partial | React/Vite, FastAPI, PostgreSQL/PostGIS configuration, MinIO helpers, design tokens, core UI components, and Docker Compose exist. The frontend build fails; migration source files are absent. |
| Public entry | Mostly present in source | Four role cards and their navigation targets exist; admin is absent from public role selection. `/` renders role selection, so the existing branded landing page assumed by the PRD is not included as a separate page. Reference-image fidelity could not be checked because the reference is absent. |
| Authentication | Partial / disconnected | Password hashing, JWT issuance, signup, pending volunteer status, access requests, login, and a fixed-code OTP endpoint exist. Session handling is inconsistent across screens. No refresh endpoint or working OTP/MFA UI flow, password recovery, Google OAuth, or login throttling was found. Signup lacks consent and password confirmation; language selection is absent. |
| Citizen reporting | Partial / disconnected | Location, image, description, submission, and nearby-needs code exist. Location is a fixed Delhi coordinate; there is no real geolocation or reverse geocoding. No voice/video flow, AI understanding confirmation, or working own-request tracking exists. Nearby needs are not the nearby sanctioned projects requested by the PRD. |
| Volunteer experience | Partial | Nearby verification list and status update code exist. Detail content is hard-coded. Capture-on-behalf flow, required KPIs, offline banner/queue, and batch sync endpoint are missing. Citizen capture pages exclude volunteers at the frontend route guard. |
| Planning dashboards | Partial | Three role routes reuse a dashboard with status totals, a chart, a needs table, and status updates. Geographic scope enforcement, layered map, category/hierarchy/time/status filters, infrastructure/investment data, connected gap computation, vulnerability weighting, explainable recommendations, and indicator disclosure are missing. |
| Public accountability | Placeholder / incomplete | Public page exists but calls a planner-protected statistics endpoint and substitutes fabricated totals on an unsuccessful HTTP response. No public project search/detail API, project cards, contractor/cost/agency fields, timeline, field source badges, linked anonymized evidence, or issue-report flow exists. |
| Admin and governance | Partial / broken | User list and status-change code exist, but field/status mismatches break the approval workflow. Moderation, roles/permissions management, governance, consent center, immutable audit logs, integration statuses, reports, and required system-health sections are absent. |
| Auditor | Missing dedicated experience | Auditor enum and public role card exist. Login redirects to public accountability. `/audit` is absent, and both AI-ops guards permit only admins. |
| AI processing and operations | Mocked / disconnected | Keyword-classification helpers and a separate polling service exist. Citizen submission does not call them. Language ID and Nominatim are absent. AI-ops figures are random or fixed, with model names/accuracy claims unrelated to recorded runs. |
| Localization | Missing implementation | English dictionary contains five keys; Hindi and Odia files are empty objects. No translation provider/hook is wired, and screen strings are hard-coded. |
| Accessibility and responsive polish | Partial / unverified | Reusable components exist, but inputs lack label association and remove focus outlines; modal semantics/focus management are absent. Several fixed-column layouts lack mobile breakpoints. Visual and keyboard QA remain unperformed. |
| Security and privacy | Partial | Backend role checks and password hashing exist. Geographic authorization, active-account checks on protected requests, token-type checks, consent persistence, ingestion anonymization, erasure flow, and database-enforced append-only audit records are missing. |
| Testing and deployment | Incomplete | Tests address an older, unregistered consent/feedback API; their database override targets a different dependency from current routers. Deployment instructions disagree with actual settings. Build and current-role workflow verification are incomplete. |

## Concrete blockers

1. **Frontend build failure.** `frontend/src/features/planner/PlannerDashboard.jsx:2` imports `recharts`, but `frontend/package.json` does not declare it. Running the build produced an unresolved-import error.

2. **Login does not provide the token where feature pages expect it.** `frontend/src/auth/AuthContext.jsx:6` keeps the user/token only in React state; login calls that state setter. Feature pages read `localStorage.getItem('token')`, but there is no corresponding storage write. A normal login therefore leaves those requests without the token they expect. Reload also loses the authenticated context.

3. **Deployment URL configuration is bypassed.** Authentication and health use `VITE_API_BASE_URL`, while citizen, volunteer, planner, admin, and AI-ops pages hard-code `http://localhost:8000`. Hosted feature pages would target the visitor's own machine.

4. **Admin approval contract does not match the backend.** `AdminDashboard.jsx` sends `pending` and `rejected`; the backend enum allows `pending_approval`, `active`, and `suspended`. The `/admin/users` response also reads `u.full_name`, `u.department`, and `u.jurisdiction`, none of which are columns on `User`. Valid nonempty list results would encounter missing attributes. Access requests are stored only as pending users; organization, designation, and reason are discarded.

5. **Citizen tracking is unwired.** `CitizenDashboard.jsx:10` initializes `activeReports` to an empty array and never populates it. There is no own-needs list or individual-needs detail endpoint in the mounted citizen router. Submission success does not show a tracking ID.

6. **Location and verification display invented report details.** `AddLocation.jsx:16` returns a fixed Delhi point after a timer. `ReportNeed.jsx` always supplies Delhi/New Delhi and falls back to zero coordinates if route state is missing. `VerifyNeed.jsx` displays the same water-supply description and “500+ people” for every ID without fetching that report.

7. **Public accountability substitutes fabricated figures.** `Accountability.jsx:15` calls `/planner/stats`, which requires an official role. Its fallback displays fixed report counts without a visible sample-data label. It cannot satisfy the project accountability requirements.

8. **AI monitoring is not telemetry.** `backend/app/routers/ai_ops.py` returns `random.randint(...)` throughput, fixed accuracy/latency, and `15420` total processed reports. It does not query recorded pipeline activity. The UI presents these as active models.

9. **Authorization is incomplete.** Planner queries contain comments where geographic filters should be; updates also fetch by ID without jurisdiction checks. `get_current_user` does not reject suspended/pending accounts after token issuance or distinguish refresh tokens from access tokens. Public access-request validation accepts the entire `UserRole` enum, including admin, although it leaves the account pending. Restrict this to the documented requestable roles.

10. **Database setup is not reproducible from included source.** `backend/alembic/versions` contains only cached bytecode, with no migration `.py` files. The seed script imports `app.models`, which is absent, and targets the obsolete model set. It also drops tables before reseeding; it was inspected but not executed.

11. **Core integrations target nonexistent API routes.** The WhatsApp mock calls `/consent` and `/feedback`; the AI poller calls `/feedback/untriaged` and PATCH `/feedback/{id}`; PFMS/IIG demo adapters call `/integrations/sync-*`. None of these routers is registered in `backend/app/main.py` or implemented in the current router files.

12. **Deployment instructions do not match implementation.** The guide sets `JWT_SECRET`, but code reads `SECRET_KEY`. It sets `MINIO_ROOT_USER/PASSWORD` on the API, but code reads `MINIO_ACCESS_KEY/SECRET_KEY`. It claims `MINIO_SECURE=True` enables TLS, while the client hard-codes `secure=False`. `render.yaml` builds the nonexistent `frontend/web-app` path; Makefile frontend commands also use obsolete paths.

## Database and API coverage

The current ORM defines only `users`, `needs`, and `evidence`. The full-stack architecture additionally requires dedicated access requests, infrastructure stock, planned investment, projects, timeline events, citizen evidence/source metadata, audit logs, consent records, and integration-status records. Their required implementations are absent.

The mounted backend exposes health, auth, admin login/user status, citizen needs/upload/nearby, volunteer tasks/verification, planner stats/needs/status, and AI-ops metrics. It lacks the documented profile, own-request/detail, batch sync, public projects, scoped dashboard/gap, moderation, audit, consent, and integration-status capabilities. Different endpoint names alone would be acceptable if the behavior existed; these are missing behaviors as well.

## Older specification coverage

- `docs/phases.md` bootstrap: infrastructure configuration exists, but several named directories are empty/obsolete and current setup is not verified.
- Core consent/feedback API: schema remnants and test files exist; mounted endpoints and associated model implementations are absent.
- WhatsApp: mock webhook and local conversation harness exist, but depend on missing APIs. Notices are English, sessions have no expiry, and no real provider is connected.
- AI enrichment: English keyword categorization exists, but no implemented language-ID module, multilingual multi-label pipeline, enrichment endpoint, or required category test matrix was found.
- Gap support: standalone ratio and recency functions exist under `decision_support/`. They are not connected to planner endpoints. Demand intensity does not implement the documented 90-day, per-admin-unit query. No hotspot map exists.
- Accountability: seed content exists but references absent models; the public page lacks the required search and record display.
- License: Apache 2.0 license text is included.
- The broader goals for 22-language voice, IVR/SMS, mobile offline app, CSC terminals, heavy AI models, contractor performance, agency responsiveness, live government integrations, public audit trail, scaling, uptime, and performance are not demonstrated by this code.

## Explicitly deferred by the current full-stack specification

These should be labeled future work rather than counted as failures of the narrowed build scope:

- Production ASR/NLP/vision models such as IndicConformer, IndicBERT, and YOLOv8.
- Live PFMS, IIG, eSAKSHI, PMGSY GIS, CPGRAMS, e-District, CSC, and DEPA integrations.
- Kafka/Debezium streaming and Kubernetes deployment.
- Real SMS/email OTP delivery.
- A fully offline database/sync engine.

However, the current scope still requires lightweight language ID/classification, honest integration-status records, real pipeline counters, a wired fixed-code OTP flow, and a local volunteer queue with a real batch-sync API. Those substitutes are not complete either.

## Documentation problems and absent references

- `IMPLEMENTATION_SUMMARY.md` claims complete end-to-end implementation and production readiness despite the blockers above. Its native geolocation claim conflicts with the fixed-coordinate implementation. Its mocked AI-ops claim also conflicts with the root specification's requirement for real telemetry.
- `MEMORY (2).md` says frontend-only, Phase 2 complete, all screens done, and all backend routers not started in different sections. These cannot describe one coherent current state.
- Root documents refer to unsuffixed `PRD.md`, `ARCHITECTURE.md`, `DESIGN.md`, `RULES.md`, `PHASES.md`, and `MEMORY.md`; those root filenames do not exist. Similar names under `docs/` contain different specifications.
- The referenced `janvastu_proposal.md`, `JanVastu_Proposal.pdf`, and per-screen reference images were not found. The assumed existing landing page is not present as a route.
- `docs/consent-flow.md` requires anonymous consent-to-feedback linkage, while the root architecture describes user-linked consent/request records. The intended privacy model needs one reconciled specification.
- `docs/consent-flow.md` still has open items for notice wording, expiry/re-consent, and erasure handling.
- The root README uses completed-feature checkmarks for functionality not delivered in this repository, including IVR, 22-language voice, offline sync, and live integrations.
- `frontend/README.md` is still a generic Vite template. `backend/alembic/README` is a generic one-line configuration note.
- `backend/requirements.txt` and `backend/pyproject.toml` describe different dependencies; the Poetry list omits current JWT/password/storage libraries. `EmailStr` is used without an explicit `email-validator` dependency.
- An `.env.example` is included. Actual secret values were not printed or audited. This workspace has no Git repository metadata, so tracked/committed-secret status could not be assessed.

## Verification performed

- Source/document review across the files listed above.
- Frontend production build: **failed**, unresolved `recharts` import.
- Backend test collection attempted: **blocked**, Python launcher reported “No installed Python found!” No backend tests passed as part of this audit.
- Static test review: existing tests target obsolete endpoints and override `app.db.session.get_db`, while current routers use `app.db.base.get_db`. They do not establish current authentication, role-denial, geography, consent, or public-accountability correctness.
- Database migrations, seed/reset operations, external integrations, Docker startup, deployments, browser flows, and accessibility visual checks were not executed. Build output may have been generated; application source was not changed.

## Suggested completion order

1. Fix build dependencies, shared API URL/token handling, admin field/status contracts, migration source, and deployment settings.
2. Verify signup/login, approved volunteer/official access, suspension, role denials, and geographic access rules against a test PostGIS database.
3. Complete consent-aware reporting with real location, own-request tracking, evidence handling, and volunteer capture/sync.
4. Connect lightweight AI and gap calculations to recorded data; add planner filters/maps and explanations.
5. Implement public project accountability, admin governance/audit/integration status, and auditor access.
6. Finish translations, accessibility, mobile layouts, state handling, and meaningful workflow tests.
7. Reconcile the specifications and update completion claims only after each phase's exit criteria have been verified.
