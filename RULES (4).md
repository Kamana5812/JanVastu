# JanVastu — Non-Negotiable Rules

These rules override convenience or a coding agent's default instincts. If a change would violate one of these, stop and flag it rather than proceeding.

## Brand & Design
1. The **landing page is the source of truth** for branding, logo, colors, typography, visual language, navigation, tone, spacing, buttons, and components. Every new screen must look like it belongs to the same product.
2. A **reference image**, where supplied for a specific screen, is the source of truth for **that screen's layout, content hierarchy, and component arrangement** — analyze and reproduce it (layout, spacing, hierarchy, card proportions, navigation, button styles, icon placement, colors, borders, shadows, responsive behavior), adapting only where literal reproduction would be unusable.
3. **Never** change the brand colors (see `DESIGN.md` for exact hex values). No gradients beyond what's specified; **no gradient text**.
4. **Never** use emojis as interface icons. Use `lucide-react` (or another professional SVG icon library) exclusively.
5. **Never** introduce a second design system, a competing component library, or Tailwind (unless the existing project already requires it, which it does not today).
6. Visual identity emphasizes **people, voice, community, connectivity, civic intelligence, development, transparency** — not literal infrastructure imagery. Avoid repeatedly using roads, bridges, buildings, India-map graphics, or construction imagery as the visual language.
7. Maintain a clean civic-tech, modern public-service aesthetic: generous whitespace, professional typography, accessible contrast, consistent buttons/cards/status badges across every screen.

## Functionality
8. Do not ship a static visual. **Every button that should navigate must actually navigate. Every form must validate.** Every dashboard interaction is backed by real data from the database (seeded sample data where a real third-party source isn't connected yet — see §12/§25).
9. Implement the required states everywhere they apply: loading, empty, error, success, hover, and keyboard-accessible focus.
10. Keep the AI pipeline and third-party integration seams swappable (see `ARCHITECTURE.md` §1/§7) — the lightweight real pipeline and stubbed integrations must be replaceable later without changing the API contract.
11. **Do not modify unrelated pages** when implementing a requested screen.

## Data Integrity
12. **Never invent or fabricate data.** Dashboards, gap indicators, and accountability records must be clearly sample/mock data in this phase — never presented as real government figures.
13. Every JanVastu-computed indicator (e.g. the Demand-Supply Gap Indicator) must carry the visible label **"JanVastu Analytical Indicator — not an official government metric."**
14. Accountability records must show a **data source badge** on every field group (Verified Source / Citizen Submitted / Government Dataset / Integrated Dataset / **Information Not Available**) — missing data is always labeled as missing, never filled in or guessed.
15. Integration status (Admin → Integrations) must only ever show **Connected** where a real integration genuinely exists. In this phase, that means every integration shows **Not Connected** or **Integration Planned** — never Connected.
16. AI must never be presented as making the final decision. Every recommendation is explainable and framed as decision support (see PRD §4.5's "Why was Ward 18 surfaced?" pattern).
17. Moderation/anomaly labels must stay neutral and factual ("Requires Review," "Anomaly Detected," "Verification Required") — never accusatory labels like "offender" or "poor performer."

## Access & Security
18. **Admin must never be presented as a normal public signup option.** Only a discreet internal access route (`/admin/login`), never linked from public navigation.
19. Official/Planner and Auditor accounts are never self-registered via open signup — only through the access-request/approval flow or admin provisioning.
20. Volunteer signup never grants immediate privileged access — it produces a pending application; access is only enabled after (mocked) approval.
21. **Frontend role selection is never the actual authorization mechanism.** It drives routing/UX only. Real enforcement lives in the backend: every protected endpoint independently re-checks the caller's role from their JWT (see `ARCHITECTURE.md` §5). A frontend-only guard is never sufficient — if a backend route lacks its own role check, that is a bug, not an acceptable shortcut.
22. Never expose in the UI or client state: passwords, private citizen information, internal moderation notes, sensitive AI/model internals, private administrative data, or security configuration details.
23. Audit logs are **append-only, enforced at the database level** — the API's database role has no `UPDATE`/`DELETE` grant on `audit_logs`, and no edit or delete affordance is ever built in the UI or the API.
24. **Passwords are always hashed** (`bcrypt`/`passlib`) — never logged, never stored, never returned in any API response, even to the account's own owner.
25. **Seeded/sample data used for demos (infrastructure stock, planned investment, sample projects, sample citizens) must be clearly synthetic** — no real person's real complaint, real government contractor, or real cost figure is ever inserted into the database and presented as if factual.
26. **Secrets never leave the backend.** Database credentials, JWT signing secrets, and storage credentials live only in backend environment variables, never in frontend code, `VITE_*` env vars, or client-visible responses.

## Internationalization
27. Initial languages are English, Hindi, and Odia; architecture must support 22+ Indian languages later. **Never hard-code UI text** — every string goes through the translation-key system from the first screen built.

## Process
28. Work in the phased order defined in `PHASES.md`. Confirm completion of a phase's frontend **and** backend deliverables (or get explicit sign-off) before starting the next one — do not jump ahead or batch multiple phases silently.
29. When a rule in this file and a convenience elsewhere in the codebase conflict, this file wins.
