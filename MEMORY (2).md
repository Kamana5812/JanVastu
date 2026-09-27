# JanVastu — Project Memory

Living context file for whoever (or whichever coding agent) picks this project up next. Update this file at the end of every work session — it is the fastest way back into the project's current state. Read alongside `PRD.md`, `ARCHITECTURE.md`, `DESIGN.md`, `RULES.md`, `PHASES.md`.

## Project Identity
- **Product:** JanVastu — People's Infrastructure Bridge. Tagline: "Har Awaaz, Har Vastu, Har Vikas."
- **What it is:** a multilingual civic-intelligence frontend that turns citizen infrastructure requests into geospatial, evidence-backed insight for policymakers, plus a public accountability portal.
- **Context:** built for the "Build with AI: Code for Communities — Second Edition" hackathon (Track 1, AI for Digital Public Infrastructure & Governance, BRICS Innovation theme). See the full hackathon research/proposal (`janvastu_proposal.md` / `JanVastu_Proposal.pdf`) for the product and policy background this UI implements.
- **This repo's scope:** frontend only, React + Vite, mock data throughout, architecture ready for a real backend/AI layer later.

## Current Status
- **Phase:** Phase 2 (Authentication) — Complete. Frontend forms and backend APIs for all roles are wired.
- **Next action:** Run the alembic migrations and proceed to Phase 3 (Citizen Module).

## Screen / Route Inventory

| # | Screen | Route | Phase | Status |
|---|---|---|---|---|
| 1 | Role Selection | `/auth/role` | 1 | Done |
| 2 | Login | `/auth/login` | 2 | Done |
| 3 | Citizen Signup | `/auth/signup/citizen` | 2 | Done |
| 4 | Volunteer Signup | `/auth/signup/volunteer` | 2 | Done |
| 5 | Official Access + Request | `/auth/access-request` | 2 | Done |
| 6 | Auditor Access | `/auth/login` (auditor variant) | 2 | Done |
| 7 | Admin Login | `/admin/login` | 2 | Done |
| 8 | Citizen Dashboard | `/citizen` | 3 | Done |
| 9 | Volunteer Dashboard | `/volunteer` | 4 | Done |
| 10 | District Dashboard | `/dashboard/district` | 5 | Done |
| 11 | State Dashboard | `/dashboard/state` | 5 | Done |
| 12 | National Dashboard | `/dashboard/national` | 5 | Done |
| 13 | Public Accountability | `/accountability` | 6 | Done |
| 14 | Admin & Governance | `/admin` | 7 | Done |
| 15 | AI & Data Operations | (admin sub-area) | 8 | Done |
| 16 | Cross-cutting polish (a11y, i18n, responsive, RBAC audit) | — | 9 | Done |

Update the Status column as each screen is built (Not started → In progress → Done) — this table is the single source of truth for "where are we."

## Key Decisions Log
- **Real backend and database added** (this was a mock-only frontend plan initially) — FastAPI + PostgreSQL/PostGIS, Docker Compose for local dev, real JWT auth with server-side RBAC enforcement, MinIO for media storage, OpenStreetMap Nominatim for real geocoding. This matches the "hackathon architecture" tier from the original JanVastu proposal. Kafka/Debezium/Kubernetes remain that same proposal's Stage 3–4 production roadmap — explicitly not part of this build (`ARCHITECTURE.md` §11).
- **AI pipeline is real but lightweight for this phase** — language ID + keyword-based category classification, not production ASR/NLP/vision models — behind an interface designed to swap in IndicConformer/IndicBERT/YOLOv8 later without changing the API contract.
- **No Tailwind** — plain CSS/CSS Modules per explicit spec instruction (`RULES.md` §5).
- **No external frontend state library** — Context + hooks only; the app talks to one real backend, so no heavier client store is justified (`ARCHITECTURE.md` §1).
- **lucide-react** is the icon library — no emoji icons anywhere (`RULES.md` §4).
- **Admin is never publicly reachable** — `/admin/login` is not linked from any public nav (`RULES.md` §18).
- **All integrations show Not Connected/Planned, never Connected**, until a real integration exists (`RULES.md` §15).
- **JanVastu Gap Indicator always carries its disclosure label** — never presented as an official government metric (`RULES.md` §13).
- Same source-truth split as the research phase: **landing page = brand source of truth; reference image = per-screen layout source of truth** — carried over from the original UI-implementation instructions.

## Open Questions / Pending Decisions
- Whether the coding agent building this is Claude Code, Antigravity, or another tool — doesn't change these docs, but affects how phases get executed/confirmed.
- Where the Postgres/MinIO instances actually run for the hackathon demo itself (local machine via Docker Compose vs. a free-tier cloud host) — architecture supports either, deployment target not yet chosen.
- Final choice of webfont (system stack vs. Inter/Work Sans) — currently left open in `DESIGN.md` §2.
- Whether the branding name in market is staying "JanVastu" or reconciling with the earlier "PRAGATI-AI" concept logged for the same hackathon — noted previously, still unresolved as of this writing.

## Backend API Inventory (see `ARCHITECTURE.md` §3 for full detail)
| Router | Status |
|---|---|
| `auth` (signup/login/access-request/OTP) | Not started |
| `users` | Not started |
| `requests` (citizen/volunteer demand records) | Not started |
| `volunteers` (offline sync) | Not started |
| `projects` (public accountability) | Not started |
| `dashboard` (district/state/national + gap engine) | Not started |
| `admin` (users, moderation, audit logs, consent, integrations) | Not started |
| `ai_ops` (pipeline metrics) | Not started |

## How to Resume Work
1. Re-read this file's **Current Status** and **Screen/Route Inventory** first.
2. Open `PHASES.md`, find the first "Not started" phase, and treat its exit criteria as the definition of done for the session.
3. Cross-check any new screen against `RULES.md` before writing code — it's short and catches the most common regressions (emoji icons, fabricated data, Admin exposed publicly, etc.).
4. At the end of the session, update the Status column above and append any new decisions to the **Key Decisions Log**.
