# JanVastu project memory

## Current work — 27 September 2026

The user requested all findings in docs/IMPLEMENTATION_AUDIT.md be addressed, then requested a GitHub repository named JanVastu and a push of the current project.

Canonical current-build specifications: PRD.md, ARCHITECTURE.md, DESIGN.md, RULES.md, PHASES.md. Numbered copies and docs/ proposal specifications are historical and still need reconciliation.

## Verified

- Frontend production build passes with installed chart/map dependencies.
- Baseline and auth/governance migrations ran on isolated PostGIS database janvastu_verification.
- Six authentication/foundation integration tests passed.
- Reporting migration ran; three tests for consent, privacy, retry protection, media validation and multilingual analysis passed.
- Browser landing page inspected successfully.

## Implemented, verification pending

- Volunteer capture, IndexedDB offline queue, sync API, actual verification detail, district restrictions, independent verification and private notes.
- Migration 0004 applied in verification database. Volunteer test collection failed due to an import path; corrected to tests.test_reporting, but not rerun yet.

## Remaining

- Planner analytics/maps/gap explanations and geographic authorization.
- Public projects/accountability, full governance and auditor experiences.
- Real AI operations metrics, profile/consent management, remaining authentication options.
- Complete Hindi/Odia translations, deployment and legacy-channel reconciliation, privacy/security hardening, and end-to-end tests.
- Current frontend links to /profile and auditor /audit are placeholders pending their implementation.

## Environment

- Python .venv and frontend node_modules installed locally; excluded from Git.
- Original janvastu database was not migrated, dropped, or reset.
- Tests used the separate janvastu_verification database.
- Starting the local API was blocked by an automatic approval-review usage limit. No API server was started by that attempt.
- Frontend dev server was started on 127.0.0.1:5173.

Do not mark the remaining modules complete until their tests pass. The audit is a historical snapshot before remediation.
