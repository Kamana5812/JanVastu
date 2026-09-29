> Historical copy. Current source: [DESIGN.md](DESIGN.md). Current implementation status: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md).

# JanVastu — Design System

Companion to `RULES.md` §Brand & Design. This is the single design system for the whole product — no screen invents its own.

## 1. Brand Colors

| Token | Name | Hex | Use |
|---|---|---|---|
| `--color-primary` | Deep Teal | `#176B73` | Primary brand color, headers, primary nav |
| `--color-indigo` | Indigo | `#334E9B` | Secondary brand color, links, primary buttons |
| `--color-sage` | Sage | `#6F9F87` | Supporting/tertiary accents, subtle highlights |
| `--color-sand` | Warm Sand | `#F3EFE6` | Warm background sections, cards on light backgrounds |
| `--color-bg` | Soft White | `#FAFBFC` | App background |
| `--color-accent-coral` | Coral | `#D86F5B` | Sparingly — key accents, highlight CTAs |
| `--color-accent-gold` | Golden | `#D9A441` | Sparingly — secondary accents |
| `--color-success` | Success | `#3F8F68` | Success states, positive status badges |
| `--color-warning` | Warning | `#C58A32` | Warning states, "requires review" |
| `--color-critical` | Critical | `#C65353` | Errors, critical alerts |
| `--color-info` | Information | `#4A78A8` | Informational badges/messages |

Rules: no excessive gradients, **no gradient text**, ever. These hex values are fixed — do not shift them for "brand refresh" reasons without an explicit request.

## 2. Typography
- A clean, modern sans-serif (system font stack is acceptable: `-apple-system, "Segoe UI", Roboto, "Inter", sans-serif`, or **Inter**/**Work Sans** if a webfont is added) — professional and highly legible in both Latin and Devanagari/Odia scripts.
- Scale (suggested, tokens in `tokens.css`):
  - Display / Hero: 32–40px, semi-bold
  - H1 (page heading): 28px, semi-bold
  - H2 (section heading): 20px, semi-bold
  - H3 (card/component heading): 16px, semi-bold
  - Body: 15–16px, regular
  - Caption/meta: 13px, regular
- Line height: 1.4–1.6 for body text; tighter (1.2–1.3) for headings.

## 3. Spacing
4px base unit. Scale: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px. Cards and sections use generous whitespace (minimum 16–24px internal padding) — do not crowd civic-tech UI.

## 4. Iconography
- **lucide-react only.** Never emojis as interface icons.
- Suggested mappings from the spec: Citizen → `User`/`Users`, Volunteer → `Users`, Official/Planner → `Building2`/`Landmark`, Auditor → `ShieldCheck`, Voice input → `Mic`, Location → `MapPin`, Photo → `Camera`, Video → `Video`, Notifications → `Bell`, Profile → `CircleUserRound`.
- Icon sizing consistent per context (e.g. 20px in nav, 24px in cards, 32–40px in role-selection cards).

## 5. Imagery
- Focus on **people and connection** — hands, voices, community gatherings, network/connection motifs.
- Avoid repeatedly using roads, bridges, buildings, India-map graphics, or construction imagery as the dominant visual language; these can appear sparingly as supporting icons (e.g. a category icon for "Roads"), never as hero imagery.
- Any generated supporting illustration must stay within this palette and visual language — do not introduce a new illustration style per screen.

## 6. Core Components

### Buttons
- **Primary** — solid Indigo (`#334E9B`) or Deep Teal background, white text, used for the single main action per screen.
- **Secondary** — outlined, brand-colored border and text, transparent/white background.
- **Ghost/tertiary** — text-only, used for low-emphasis actions (e.g. "Skip").
- States: default, hover (slightly darker/elevated), focus (visible outline for keyboard users), disabled (reduced opacity, no pointer), loading (inline spinner, label preserved or replaced with "Loading…").

### Cards
- Consistent radius (8–12px), consistent shadow (subtle — avoid heavy drop shadows), consistent internal padding (16–24px). Used for role-selection options, dashboard KPI tiles, project cards, request cards.

### Status Badges / Pills
- Small, rounded, colored per the status palette (success/warning/critical/information) with a label, never color alone (icon or text always accompanies color per accessibility rule).
- Used for: request status, moderation labels, data source badges, integration status, project timeline stage.

### Forms
- Labeled inputs (label always visible, not placeholder-only), inline validation messages in the Critical color, required-field indication, password visibility toggle where relevant, consistent field spacing.

### Navigation
- **Public/marketing:** top nav, matches existing landing page.
- **Auth screens:** two-column layout on desktop (branding left, form right), single column stacked on mobile.
- **Citizen/Volunteer:** mobile-first bottom or top tab nav with the screens listed in PRD §4.3/§4.4.
- **Dashboards (District/State/National/Admin/Audit):** persistent left sidebar nav with sections, collapsible on smaller viewports.

## 7. States (required everywhere applicable — see `RULES.md` §9)
- **Loading:** skeleton or spinner consistent with brand colors, never a generic gray spinner with no brand identity.
- **Empty:** friendly, on-brand message + an action where relevant (e.g. "No requests yet — Report a Need").
- **Error:** clear, non-technical message in the Critical color, with a retry action where applicable.
- **Success:** clear confirmation, Success color, auto-dismiss or explicit close.
- **Hover / Focus:** every interactive element has a visible hover state (pointer devices) and a visible focus ring (keyboard users) — never remove the default focus outline without replacing it.

## 8. Responsive Breakpoints (suggested)
- Mobile: up to 599px
- Tablet: 600–1023px
- Desktop: 1024px+
Citizen and Volunteer experiences are designed mobile-first; policymaker/admin dashboards are designed desktop-first with a usable (if denser) tablet fallback.

## 9. Accessibility
- Minimum WCAG AA contrast for all text/background combinations using the palette above — verify Warm Sand and Soft White backgrounds against text colors specifically, since light-on-light is the likeliest failure point.
- All icons paired with a text label or `aria-label`.
- All form errors announced (e.g. `aria-live` region) not just color-coded.
- Full keyboard operability for every flow, including the auth flows and the dashboard filters.
