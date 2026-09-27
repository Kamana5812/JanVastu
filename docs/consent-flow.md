# JanVastu — Citizen Consent Flow

**Last Updated**: 2025

This flow governs how consent is captured before any citizen feedback is recorded, in compliance with the DPDP Act 2023 and the platform's Citizen Sovereignty principle (see `rules.md §1`).

## Flow Steps

1. **Citizen initiates contact** (IVR / mobile app / WhatsApp)
2. **System plays/displays consent notice** in the citizen's local language
3. **Citizen provides consent** — voice "yes", tap, or OTP confirmation
4. **Consent recorded** with timestamp, purpose, and language
5. **Consent ID linked to feedback** — the consent record is *never* linked to citizen identity, only to the feedback item via an opaque `consent_id`
6. **Citizen** proceeds to submit their feedback (voice, text, photo, or video)

## Design Notes

- The `consent_id` is the *only* link between a feedback item and the fact that consent was given — it must not be traceable back to a phone number, name, or other citizen identifier once anonymization runs at ingestion (see `architecture.md §1.7` and `rules.md` anonymization requirements).
- Consent notices must be available in all 22+ supported languages before that language's collection channel goes live.
- Every consent capture event must be immutable and auditable (append-only log), per the platform's Transparency and Accountability principles.

## Open Items

- [ ] Define exact consent notice copy per language (legal + UX sign-off required)
- [ ] Define consent expiry / re-consent policy, if any
- [ ] Define erasure request handling in relation to already-anonymized feedback (DPDP right-to-erasure vs. anonymization tension — needs governance decision)
