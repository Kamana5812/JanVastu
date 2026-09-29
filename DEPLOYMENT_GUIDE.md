# Running JanVastu

## Local demonstration

Run `docker compose up --build -d`. Frontend: http://localhost:8080. API: http://localhost:8000. MinIO console: http://localhost:9001.

The migration service uses the database owner. The API uses `janvastu_api`, which can read and append audit logs but cannot update, delete or truncate them. Audit triggers provide a second layer of protection.

Copy the root `.env.example` to `.env` to override Compose settings. Use URL-safe database passwords or percent-encode them in connection URLs. The shipped defaults are for local demos. No secret belongs in `VITE_*` variables.

## Run source directly

Install Python 3.11+, Node 24+, PostgreSQL 16/PostGIS and MinIO. Install FFmpeg/ffprobe for audio/video validation.

```sh
python -m venv .venv
# Activate the environment for your shell.
pip install -r backend/requirements.txt
cd backend
# DATABASE_URL must temporarily use the database owner.
alembic upgrade head
# Set RUNTIME_DB_PASSWORD (at least 16 characters).
python -m app.db.provision
python -m app.db.seed
# Change DATABASE_URL to the restricted runtime role.
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Copy `backend/.env.example` to `backend/.env`; configure the database, storage and signing secret. The Python settings read this file regardless of the working directory.

In another terminal:

```sh
cd frontend
npm ci
npm run dev
```

The frontend proxies `/api` to port 8000. Set `VITE_PROXY_TARGET` for a different local API port. For separate hosted origins, `VITE_API_BASE_URL` is the API origin **without** `/api/v1`.

## Tests

Create an isolated PostGIS database ending in `_test` or `_verification`. Tests refuse other database names. Run migrations and role provisioning against it, then run:

```sh
cd backend
pytest -q
cd ../frontend
node scripts/check-i18n.mjs
npm run lint
npm run build
```

Tests create synthetic rows with unique IDs and never reset an existing database. For a fresh run, create a new isolated test database and migrate it. The GitHub workflow does this automatically with a new service container.

The seed command is idempotent. It preserves existing records and adds explicit synthetic samples. Do not drop or reset a database containing user data.

## Configuration and external dependencies

- `SECRET_KEY`: random backend signing secret, at least 32 characters for production.
- `CORS_ORIGINS`: comma-separated exact frontend origins.
- `MINIO_ENDPOINT`: host and port, without a URL scheme.
- `MINIO_SECURE`: true for HTTPS storage.
- `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`: backend-only credentials.
- `GOOGLE_CLIENT_ID`: public OAuth client identifier; register the exact frontend origin with Google. Google login requires an existing approved account.
- Nominatim geocoding uses a timeout, cache and throttling. Failed lookups require the user to confirm manually supplied location; they are not presented as verified geocodes.
- OpenStreetMap map tiles require network access and carry attribution.

`APP_ENV=demo` permits the clearly labeled fixed OTP. `APP_ENV=production` rejects demo OTP and an unsafe signing secret. A real OTP delivery provider must be implemented before privileged production login is usable.

## Hosting

`render.yaml` is a demo deployment template with corrected frontend paths. Supply an externally provisioned PostGIS database, run migrations and role provisioning with its owner account, and supply the **runtime** connection URL to the API. Supply HTTPS object storage and configure CORS and the frontend API origin. The Docker API listens on port 8000.

No external hosting deployment has been performed by creating or pushing this repository.
