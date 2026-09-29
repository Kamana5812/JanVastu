# JanVastu project memory

Updated 29 September 2026.

## User scope

Complete the documented hackathon workflows, reconcile documentation, publish to the private GitHub repo JanVastu, and include the three supplied infrastructure screenshots as data. Repo: https://github.com/Kamana5812/JanVastu (main). Initial published commit: 76f6e7c. Subsequent work is described in IMPLEMENTATION_SUMMARY.md and docs/VERIFICATION.md.

## Implemented and checked

Authentication/approval for seven roles, reporting and media, volunteer queue/verification, planning, public accountability, admin/governance/audit, profile/consent/erasure, measured pipeline operations, English/Hindi/Odia dictionaries, Docker deployment and CI. Backend suite: 65 passed, two host skips; both media tests passed in the API container. Legacy tests: two passed. Frontend lint, 438-key translations and build pass. A browser-discovered list/detail data-shape race was fixed in useResource.

16 infrastructure records, 21 observations and 5 source definitions are stored in backend/app/data/bhubaneswar.json. Images 1/2 repeat. Conflicts remain visible. Jaydev flyover/expressway are linked components with potentially shared budget. PIB ring-road approved cost and Parliament's dated Janpath figure have field-specific official references. All remaining screenshot claims are unverified. No invented GPS/progress or dates. Migration 0008 permits unknown project coordinates/progress. Import is idempotent and preserves existing records.

## Local verification environment

Only janvastu_verification was migrated through 0008. Original janvastu database/volumes remain intact. API container janvastu-verification-api listens on 127.0.0.1:58000; frontend preview on 127.0.0.1:5173 uses it. Existing janvastu-postgres-1 and janvastu-minio-1 supply the verification services. Runtime config files .env.verification and .env.containerverification are ignored. Do not print their secrets. verification_setup rotates the runtime password, so rerunning it requires refreshing the container environment.

## Scope boundaries

Live provider credentials/delivery, production speech/vision, government integrations, Kafka and Kubernetes are outside this build. Full all-device/all-role visual QA remains incomplete; targeted browser inspection and backend role tests are recorded. Never call screenshot observations official facts or claim production readiness. Current documentation replaces historical numbered proposals; RULES.md includes sample and supplied-source badge extensions.
