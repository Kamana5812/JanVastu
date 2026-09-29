# JanVastu implementation status

Updated 29 September 2026. This describes the hackathon build and its remaining production boundaries.

## Included

- Seven roles with database-backed authentication, approval, suspension, refresh rotation and server-side geographic access checks.
- Citizen reporting, consent, category suggestions, image/audio/video evidence, location, own-request tracking and notifications.
- Volunteer capture, persistent browser draft queue, retry-safe synchronization and independent district verification.
- District/state/national planning, filters, map layers and explained gap indicators calculated from recorded requests and labeled sample context.
- Public project search and detail, field source labels, timeline and manually reviewed public image derivatives.
- Administrator approvals, moderation, users, consent, immutable audit records, health, reports and integration status. Auditors have read-only access.
- Measured language/category pipeline activity. Missing accuracy is shown as unavailable.
- Account consent withdrawal and erasure; anonymous operational records and append-only audit history remain.
- English, Hindi and Odia dictionaries; responsive components and accessible form labels.
- Docker API and frontend builds, migrations, restricted database role, repeatable seed/import and GitHub verification workflow.
- Six synthetic projects and 16 supplied Bhubaneswar infrastructure records. Screenshot observations, conflicting values and official field references remain distinct. See [dataset notes](docs/DATASETS.md).

## Verification

See [verification report](docs/VERIFICATION.md) for executed checks and limitations. Implementation is not proof that every browser/device combination has passed.

## Production work outside this build

Live SMS/email OTP, WhatsApp/IVR delivery, government connectors, production ASR/vision, automatic anonymization, 22-language voice, Kafka/Debezium and Kubernetes operations remain planned. Google sign-in requires a configured client ID; a live Google account flow has not been verified here. Demo OTP must not protect production data.

Source verification is incomplete for supplied screenshot claims. Exact coordinates, current progress, precise completion dates and cost classifications are intentionally absent where unknown.
