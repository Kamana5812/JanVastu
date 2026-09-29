> Historical copy. Current source: [PRD.md](PRD.md). Current implementation status: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md).

# JanVastu — Product Requirements Document (PRD)
**People's Infrastructure Bridge · "Har Awaaz, Har Vastu, Har Vikas"**
Scope of this PRD: the **full-stack application** — a React + Vite frontend and a real FastAPI + PostgreSQL/PostGIS backend — covering landing → role selection → auth → six role experiences. This is the working spec for implementation — read alongside `ARCHITECTURE.md`, `DESIGN.md`, `RULES.md`, `PHASES.md`, and `MEMORY.md`.

---

## 1. Product Vision

> "Every citizen development request becomes a structured signal that can contribute to evidence-based infrastructure planning."

JanVastu turns fragmented, multilingual citizen infrastructure feedback into geospatial, evidence-backed insight for policymakers, while giving citizens a place to see what happened to the money and projects already sanctioned near them.

**Core journey (all screens exist to move a user through this):**
Citizen Voice → AI Understanding → Structured Civic Demand → Geospatial Signal → Infrastructure Context → Explainable Insight → Development Action → Public Accountability.

## 2. Problem Statement
- Citizen requests live in fragmented systems (MPLADS, e-District, CPGRAMS, CSC) with no shared record.
- National infrastructure planning is top-down; nothing correlates citizen demand with existing infrastructure supply or already-planned investment.
- Citizens have no visibility into project cost, contractor, timeline, or the responsible office.
- Multilingual, low-literacy, low-connectivity populations are structurally excluded from today's feedback channels.

## 3. Users & Roles

| Role | Who | Primary need | Entry route |
|---|---|---|---|
| **Citizen** | Any resident | Report a need in their own language/medium, track it, see nearby projects | `/auth/signup/citizen` |
| **Volunteer** | Field workers / CSC operators | Capture and verify requests on behalf of citizens, often offline | `/auth/signup/volunteer` |
| **District Official** | District-level planner | See local demand vs. supply, act on recommendations | `/auth/login` → `/dashboard/district` |
| **State Planner** | State-level planner | Same, at state scope with district drill-down | `/auth/login` → `/dashboard/state` |
| **National Planner** | National-level planner | Same, at national scope | `/auth/login` → `/dashboard/national` |
| **Auditor** | Governance/transparency reviewer | Review accountability and audit data | `/auth/login` → `/audit` |
| **Admin** | Platform operator | Users, moderation, data governance, system health | `/admin/login` → `/admin` (never a public signup) |
| **Public visitor (unauthenticated)** | Anyone | Look up a project's accountability record | `/accountability` |

RBAC is a first-class requirement, not a UI convenience — see Section 8 and `ARCHITECTURE.md` §RBAC.

## 4. Functional Requirements by Screen

### 4.1 Public entry
- **Landing page** (source of truth for brand, existing — not rebuilt here).
- **Role Selection (`/auth/role`)** — "Join JanVastu" / "Choose how you want to participate." Four cards: Citizen, Volunteer, Government/Planner, Auditor, each with icon, one-line description, and CTA routing to its signup/login. Admin is never shown here. Footer link to `/auth/login`.

### 4.2 Authentication
- **Universal Login (`/auth/login`)** — two-column desktop layout (branding left, form right). Email/mobile + password, show/hide password, "Forgot password?", primary Sign In, divider, Google OAuth + OTP alternatives, link to Create Account. Must support: field validation, loading state, invalid-credential error, success redirect **by role** (Section 3 routes), OTP flow, and route protection for already-authenticated users.
- **Citizen Signup (`/auth/signup/citizen`)** — minimal fields only (name, mobile, optional email, preferred language [English/Hindi/Odia], state, district, locality, optional ward/village, password + confirm, consent checkbox). Alternative: continue with mobile OTP. On success → `/citizen`.
- **Volunteer Signup (`/auth/signup/volunteer`)** — name, mobile, email, state, district, area/organization, preferred language, relevant experience, consent. Submission does **not** grant access immediately — shows "Application Submitted / Your volunteer access request will be reviewed." Access to `/volunteer` only after a real admin approval action (an `access_requests` row moving to `approved` — see `ARCHITECTURE.md` §4).
- **Official/Planner Access (`/auth/access-request` login variant)** — official email, password, OTP/MFA, primary Sign In, secondary "Request Access" → `/auth/access-request` (name, official email, organization/department, designation, state, district, role requested, reason for access, verification info). No public official self-signup.
- **Auditor Access** — registered email, password, OTP/MFA. Auditor accounts are never self-registered; provisioning is admin-controlled (mocked as pre-seeded accounts in this phase).
- **Admin Login (`/admin/login`)** — internal-only route, never linked from public navigation. Admin email/ID, password, MFA/OTP. Must visibly show security indicators (secure connection, authorized access, audit logging enabled) and implement invalid-credential, loading, unauthorized-access, session-expiry, and account-lock/throttling states.

### 4.3 Citizen experience (`/citizen`)
- Nav: Home, Report a Need, My Requests, Nearby, Projects, Accountability, Notifications, Profile.
- Home: "How can we improve your area?" + primary "Report a Need" CTA, category grid (Water, Sanitation, Electricity, Healthcare, Education, Transport, Roads, Other), a prominent "Speak your problem" voice CTA with "Tell us what is happening in your own language."
- Report flow: input (voice/text) → attach photo/video → confirm location → a real (lightweight) AI understanding step — language ID + category classification, run server-side — producing a structured summary the citizen confirms → submit → tracking view. Every step needs a visible state (loading while the backend processes, error if submission fails, success confirmation).
- My Requests: list with status, filter/sort, empty state for first-time users.
- Nearby / Projects: map or list of nearby sanctioned/ongoing projects (seeded sample data, real query).
- Accountability: entry point into the public accountability portal, scoped to the citizen's area by default.

### 4.4 Volunteer experience (`/volunteer`)
- Nav: Dashboard, Capture Request, My Requests, Verification, Offline Queue, Sync, Notifications, Profile.
- KPIs: Requests Captured, Pending Verification, Verified Today, Sync Pending.
- Primary CTA: "Capture Citizen Request" → flow: citizen voice/text → photo → GPS → category → submit.
- Offline mode banner: "Offline — requests will sync when connectivity returns," with a mocked local queue and sync action.

### 4.5 Policymaker dashboards (District / State / National — shared architecture, different scope)
- Heading: "District Infrastructure Pulse" (state/national variants reworded to scope).
- KPIs: Citizen Demands, Verified Demands, High-Gap Areas, Active Projects, Resolved Requests, Pending Review.
- Main visualization: Demand & Infrastructure Map with toggleable layers — Citizen Demand, Infrastructure, Infrastructure Gap, Projects, Vulnerability, Investment.
- Category filter: Water, Sanitation, Electricity, Healthcare, Education, Transport, Roads, Other.
- Gap analysis panel: Demand Intensity, Infrastructure Stock, Planned Investment, JanVastu Gap Indicator — **must always carry the label "JanVastu Analytical Indicator — not an official government metric."**
- Every surfaced recommendation must be explainable on click/expand, e.g. "Why was Ward 18 surfaced?" → High citizen demand / Increasing reports / Limited infrastructure context / Planned investment context / Multiple independent signals. The AI never presents itself as making the final decision.
- State/National scope add a hierarchy selector: State → District → Block → Ward/Village, and (national only) filters for State, District, Infrastructure Category, Time Period, Project Status. No fabricated real-world statistics — all figures in this phase are clearly mock/sample data.

### 4.6 Public Accountability (`/accountability`, public, no login required)
- Heading: "See Where Public Development Is Happening."
- Search by Project, Location, Project ID, Department, Contractor.
- Project cards: name, location, department, status, progress, planned completion.
- Project detail: ID, location, department, contractor/vendor, sanctioned cost, actual cost, planned/actual start and completion, responsible agency, citizen evidence (anonymized), timeline (Sanctioned → Tendered → Awarded → Started → In Progress → Completed).
- Data source badges on every field group: Verified Source, Citizen Submitted, Government Dataset, Integrated Dataset, **Information Not Available** — missing data is always labeled as missing, never invented.
- "Report an Issue" CTA on every project detail.

### 4.7 Admin & Governance (`/admin`)
- Nav: Overview, Users, Roles & Permissions, Requests, Moderation, Data Governance, Consent, Audit Logs, Integrations, System Health, Reports.
- KPIs: Registered Users, Active Today, Requests Processed, Pending Moderation, Consent Records, System Health.
- User table: user, role, location, status, verification, last active.
- Moderation queue uses neutral labels only: "Requires Review," "Anomaly Detected," "Verification Required" — never accusatory labels, for categories like duplicate, spam, suspicious location/pattern, missing information, AI classification uncertainty.
- Data governance panel: data collection, usage, retention, access, deletion, anonymization.
- Consent center: active / withdrawn / pending consent, consent version.
- Audit log: timestamp, actor, role, action, resource, result — **append-only from the UI**, no edit/delete affordance.
- Integrations panel (PFMS, IIG, eSAKSHI, PMGSY GIS, CPGRAMS, State e-District, CSC, DEPA/consent systems) — status is always one of Connected / Not Connected / Integration Planned; **Connected only appears where a real integration exists** (none do in this phase — all show Not Connected or Integration Planned).
- System health: API, Database, Storage, Processing Queue, AI Processing, Notifications — mocked status tiles.

### 4.8 AI & Data Operations (`/admin` sub-area or standalone, admin/auditor-visible)
- Sections: Speech Processing, Language Detection, NLP Classification, Entity Extraction, Geocoding, Image Analysis, Video Processing, Deduplication, Anomaly Detection.
- Per section: model version, requests processed, processing latency, failure rate, confidence distribution, data quality, missing location, duplicate reports, anomalies — real figures computed from the actual lightweight pipeline runs (see `ARCHITECTURE.md` §3/§10), never exposing raw citizen content.

## 5. Cross-Cutting Requirements
- **Multilingual:** initial UI languages English, Hindi, Odia; all UI strings via translation keys (i18n architecture), never hard-coded, with the structure ready to add further Indian languages.
- **Accessibility:** keyboard navigation, visible focus states, accessible form labeling/errors, sufficient color contrast (see `DESIGN.md`), screen-reader-friendly status/empty/error states.
- **Every interactive element must actually work in this phase** against the real backend and database — no dead buttons, no unwired forms. Every form validates before submit.
- **States required everywhere applicable:** loading, empty, error, success, hover, focus/keyboard.
- **No fabricated data claims:** dashboards and accountability records use clearly-mock sample data; nothing is presented as a real government figure.

## 6. RBAC & Data Visibility (see `ARCHITECTURE.md` for implementation)
- Frontend role selection is **never** the real authorization mechanism — it only drives UI/UX and route guarding. Real enforcement now happens server-side: every protected API endpoint independently re-checks the caller's role from their JWT before returning data.
- Public data: public project info, public accountability records, safe/anonymized citizen evidence, public project metadata.
- Authenticated citizen: own requests, own profile, own notifications, own evidence.
- Official: authorized planning data at their scope, aggregated civic intelligence.
- Admin: governance, moderation, audit, system operations.
- Never expose: passwords, private citizen information, internal moderation notes, sensitive AI data, private administrative/security data.

## 7. Out of Scope for This Build Phase
- **A real backend and real database are now in scope** (FastAPI + PostgreSQL/PostGIS — see `ARCHITECTURE.md`), matching the "hackathon architecture" defined in the original JanVastu proposal. What remains out of scope:
  - Production-grade ASR/NLP/vision models (IndicConformer, IndicBERT, YOLOv8 fine-tunes) — replaced for now by a real but lightweight pipeline (language ID + keyword-based category classification), swappable later without an API contract change.
  - Real third-party integrations with PFMS, IIG, eSAKSHI, PMGSY GIS, CPGRAMS, State e-District, CSC, DEPA — tracked honestly via an `integrations_status` table, always `Not Connected` or `Integration Planned`.
  - Kafka/Debezium streaming and Kubernetes deployment — the proposal's own Stage 3–4 production roadmap, not this build (Docker Compose is the target here).
  - Real MFA/OTP delivery — the endpoint is real, but verification uses a fixed mock code (no SMS/email gateway).
- True offline-first storage/sync engine for the Volunteer app is still represented with a local queue on the client, synced via a real backend batch endpoint (`POST /volunteers/sync`) rather than a fully offline-capable database.

## 8. Success Criteria for This Phase
- All 16 screens in `PHASES.md` are implemented, routable, and visually consistent with the JanVastu brand (see `DESIGN.md`).
- Every form validates and every navigation action works end-to-end against the **real backend and database** — no screen silently reads from client-side mock data by the end of Phase 9.
- RBAC behaves correctly for all seven roles plus the unauthenticated public visitor, enforced independently by the backend, not just the frontend router.
- The app is usable end-to-end on mobile viewport for the Citizen and Volunteer experiences.
- No emoji-as-icon usage; no unlabeled "Connected" integration claims; no invented accountability data.
