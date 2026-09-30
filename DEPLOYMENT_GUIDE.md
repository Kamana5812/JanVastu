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

### Vercel frontend

Import the repository with root directory `frontend`, framework Vite, build command `npm run build`, and output directory `dist`. Set `VITE_API_BASE_URL` to the Render service origin and redeploy after changing it. The SPA rewrite is included in `frontend/vercel.json`.

The frontend is published at https://janvastu.vercel.app. Backend connection and live verification are still in progress.

### Render API with Neon database and private storage

`render.yaml` provisions only the free Docker API. In the Render form use root directory `backend`, Dockerfile `./Dockerfile`, build context `.`, command `python -m app.hosted_start`, and health check `/api/v1/health`.

Create a dedicated Neon PostgreSQL database with PostGIS support and a private `janvastu-media` bucket. Set these backend environment variables:

- `JANVASTU_OWNER_DATABASE_URL`: direct (non-pooled) database owner connection, preserving the SSL parameters.
- `SECRET_KEY`: a generated random signing secret, at least 32 characters.
- `APP_ENV=demo`, `MOCK_OTP_ENABLED=true` for the labeled hackathon demo.
- `CORS_ORIGINS` and `FRONTEND_URL`: `https://janvastu.vercel.app`.
- `MINIO_ENDPOINT`: the host from Neon's `AWS_ENDPOINT_URL_S3`, without `https://`.
- `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY`: Neon's storage credentials.
- `MINIO_REGION`: Neon's `AWS_REGION` (this project uses `us-east-2`).
- `MINIO_BUCKET=janvastu-media`, `MINIO_SECURE=true`.

On startup, `app.hosted_start` migrates the database, provisions the restricted `janvastu_api` role, and imports idempotent demo/dataset seeds. It then replaces itself with the API process, using the restricted connection and removing the owner connection from that process's environment. Render retains the owner setting for future migrations; keep dashboard access limited. The runtime password is derived from `SECRET_KEY`; rotating the signing secret also rotates that database password on the next startup.

Never put database or storage credentials in Git or Vercel frontend variables. Keep the bucket private; evidence access is authorized by the API. Free hosting has usage limits and Render can sleep while idle. No paid database or AWS resources are required for this setup.
