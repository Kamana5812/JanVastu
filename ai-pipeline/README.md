# Inline language pipeline

The active pipeline is `backend/app/services/ai_service.py`. It runs during report submission and records real telemetry. The old unauthenticated polling loop was removed.

`pipelines/main.py` is a compatibility CLI/import; it does not start a background service. Run its tests with the backend Python dependencies installed. Production speech, translation and vision models are future integrations.
