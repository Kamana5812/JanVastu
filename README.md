# JanVastu

JanVastu connects citizen requests with volunteer verification, infrastructure planning and public project records.

## Run the local demo

Requirements: Docker Desktop with Linux containers and Docker Compose.

```sh
docker compose up --build -d
```

Open http://localhost:8080. The API documentation is at http://localhost:8000/docs.

Compose runs migrations, creates a restricted API database role, and inserts **synthetic** planning contexts, requests and project records. The seed also imports 16 supplied infrastructure records with unverified claim labels and source references. Existing records are preserved. Local defaults are for demonstrations only.

Create an administrator using your own credentials:

```sh
docker compose exec -e ADMIN_EMAIL=you@example.org -e ADMIN_PASSWORD='<your-password>' api python -m app.db.bootstrap
```

Use at least 12 password characters. Open `/admin/login` directly; admin registration is not public. The demo verification code is **123456**. No SMS or email is sent.

Citizens register directly. Volunteers, officials and auditors apply and need administrator approval. Never use personal or sensitive data with demonstration OTP.

## Implemented workflows

- Password login, demo OTP login/registration/reset, refresh rotation, suspension and role checks.
- Consent-aware reporting, GPS and reverse geocoding, multilingual keyword suggestions, photos/audio/video, own-request tracking and notifications.
- Volunteer capture, browser offline drafts, retry-safe sync, and independent district verification.
- District, state and national dashboards with geographic restrictions, filters, maps, measured counts and explained gap calculations.
- Public project search, source labels, timelines, missing information and linked issue reports.
- Administrator approval, moderation, consent, audit, integration status, health, reports and manually reviewed public image derivatives.
- Auditor access to read-only logs and measured pipeline activity.
- English, Hindi and Odia interface dictionaries.
- Account erasure with retained anonymous operational history and immutable audit records.

Google sign-in is implemented for existing accounts. Enabling it requires your own Google client ID and authorized frontend origin. Identity verification follows Google's [server-side token verification](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token). It is disabled when unconfigured.

## Data and privacy

Sample requests and projects are explicitly labeled. Costs, agencies, contractors and planning indices in sample records are fictional. Gap calculations carry the label “JanVastu Analytical Indicator — not an official government metric.”

Original media stays private. An administrator must upload a separately redacted image and attest to review before it can appear on a public project. Public access also requires active account and report consent. Automatic face/name anonymization is **not** connected.

See [dataset coverage and source conflicts](docs/DATASETS.md).

## Boundaries

This is the documented hackathon build. Government integrations, live WhatsApp/IVR/SMS, production OTP delivery, speech transcription, production vision/NLP models, 22-language voice, Kafka and Kubernetes operations remain future work. Integration cards report planned or not connected. No synthetic accuracy or throughput is displayed.

This repository is not a production-readiness or legal-compliance certification.

## Development and verification

See [deployment guide](DEPLOYMENT_GUIDE.md), [implementation status](IMPLEMENTATION_SUMMARY.md), and [verification report](docs/VERIFICATION.md).

Canonical requirements: [PRD](PRD.md), [architecture](ARCHITECTURE.md), [design](DESIGN.md), [rules](RULES.md), [phases](PHASES.md). Numbered copies and older documents under `docs/` preserve earlier proposals.

License: Apache 2.0.
