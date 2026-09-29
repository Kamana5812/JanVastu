# Verification report

Run date: 29 September 2026. All database tests used the isolated `janvastu_verification` database with the restricted `janvastu_api` role. The original `janvastu` database was not reset or migrated.

## Automated checks completed

| Check | Result |
|---|---|
| Backend suite with real local MinIO enabled | 65 passed, 2 skipped on Windows |
| Audio/video signature, duration and stream-type tests inside the FFmpeg API container | 2 passed |
| Legacy pipeline and local WhatsApp adapter compatibility tests | 2 passed |
| Project/dataset/governance checks after search expansion | 7 passed |
| Frontend lint | Passed |
| Translation dictionary and literal UI-key check | 438 keys in English, Hindi and Odia |
| Frontend production build | Passed |
| Alembic migration 0008 and repeatable import | Passed; 16 supplied records |
| API Docker image build | Passed |
| Secret-pattern and tracked environment-file review | No credential files or token-pattern matches found |

The backend suite covers authentication alternatives, role denial across seven roles, geographic restrictions, refresh/suspension, consent, erasure, private/public evidence, real storage, media retries, classification, planner calculations, moderation, source badges, dataset deduplication, unknown locations and append-only audit privileges. The storage test uses actual MinIO; it is gated by `RUN_STORAGE_TESTS=1`.

A dependency deprecation warning from Starlette's test client remains. It did not fail tests. No production-provider SLA, load test or penetration test was performed.

## Browser checks

Inspected the landing page, sign-in, citizen dashboard, reporting form and imported public project detail at the in-app browser's narrow viewport. Synthetic citizen password login reached the real dashboard. Janpath's screenshot claims, conflicts and official reference rendered correctly. Hindi dataset labels were checked. Browser testing found a stale-resource race during list/detail navigation; the resource hook now ties responses to the requested path and revision.

These are targeted checks, not an exhaustive mobile-device or all-role browser certification. Microphone/GPS hardware permissions, every offline/network failure combination and real Google identity were not exercised here.

## Reproduction

Run migrations as the database owner against a database ending in `_test` or `_verification`. Provision the restricted API role, seed/import, then run `pytest -q` from `backend` using the runtime role. Enable `RUN_STORAGE_TESTS=1` and provide working MinIO settings for storage integration tests. Run FFmpeg-dependent tests in the API image when the host lacks FFmpeg.

From `frontend`: run `npm ci`, `npm run lint`, `node scripts/check-i18n.mjs`, and `npm run build`. The GitHub workflow performs database/frontend checks; live storage tests need separately configured MinIO.

## Explicit limits

Demo OTP remains 123456 without delivery. Google sign-in needs a real client configuration. Live WhatsApp/IVR/SMS, government adapters, production speech/vision and automatic anonymization are planned. Supplied screenshot claims remain unverified except the dated official observations recorded in [dataset notes](DATASETS.md). Missing coordinates/progress and conflicting costs are preserved, not filled in.
