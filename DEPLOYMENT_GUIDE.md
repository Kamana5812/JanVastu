# JanVastu Deployment Guide

This guide walks you through deploying the JanVastu platform using a split-stack architecture: **Vercel** for the high-performance React frontend, and **Render** for the Python/FastAPI backend and PostgreSQL database.

---

## 1. Frontend Deployment (Vercel)

Vercel is the optimal host for our React/Vite application, providing global CDN edge caching out of the box.

### Steps:
1. Push your code to a GitHub repository.
2. Log into [Vercel](https://vercel.com/) and click **Add New → Project**.
3. Import your GitHub repository.
4. **Configure Project Settings:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` or `yarn build`
   - **Output Directory:** `dist`
5. **Environment Variables:**
   - `VITE_API_BASE_URL`: Set this to your future backend URL (e.g., `https://janvastu-api.onrender.com`). You can set this as a placeholder for now and update it later once the backend is live.
6. Click **Deploy**.

> **Note:** We have already configured a `vercel.json` file in the `frontend` folder to handle React Router client-side rewrites automatically!

---

## 2. Backend Deployment (Render)

Render is perfect for our FastAPI backend because it natively supports Dockerized deployments and managed PostgreSQL databases.

### A. Deploying the PostgreSQL Database
1. Go to your [Render Dashboard](https://dashboard.render.com/) and click **New → PostgreSQL**.
2. Name it `janvastu-db`.
3. Choose the **Free** tier (or Starter if you want persistence beyond 90 days).
4. Click **Create Database**.
5. Once created, copy the **Internal Database URL**.

### B. Enabling PostGIS
Render's PostgreSQL supports PostGIS natively, but it must be enabled manually.
1. In your Render DB dashboard, click the **Connect** dropdown and connect via `psql` (or a tool like DBeaver/pgAdmin using the External URL).
2. Run the following SQL command:
   ```sql
   CREATE EXTENSION IF NOT EXISTS postgis;
   ```

### C. Deploying the FastAPI Web Service
1. In the Render Dashboard, click **New → Web Service**.
2. Connect your GitHub repository.
3. **Configure the Service:**
   - **Name:** `janvastu-api`
   - **Root Directory:** `backend`
   - **Environment:** `Docker` (Render will automatically detect the `backend/Dockerfile`).
4. **Environment Variables:**
   - `DATABASE_URL`: Paste the Internal Database URL from Step A.
   - `JWT_SECRET`: Generate a random secure string (e.g., `openssl rand -hex 32`).
   - `MINIO_ENDPOINT`: *(See storage note below)*
   - `MINIO_ROOT_USER`: *(Your storage access key)*
   - `MINIO_ROOT_PASSWORD`: *(Your storage secret key)*
5. Click **Create Web Service**.

---

## 3. Storage Architecture (Production MinIO / S3)

In our local Docker Compose environment, we run a local instance of MinIO. For production on Render/Vercel, you need a public cloud object store to handle the image evidence uploads.

Because our backend uses the standard AWS S3 SDK architecture, you can swap out the local MinIO instance for **any S3-compatible provider** without changing a single line of backend code.

### Recommended Free-Tier Storage Providers:
1. **AWS S3:** Use the AWS Free Tier. Create a bucket, enable public read access, and generate an IAM Access Key.
2. **Cloudflare R2:** 10GB free forever, zero egress fees. Extremely fast.

**To configure your backend to use them:**
Simply update your Render Web Service Environment Variables:
- `MINIO_ENDPOINT` = `s3.amazonaws.com` (or your R2 endpoint, **without** `https://`)
- `MINIO_ROOT_USER` = `Your Access Key`
- `MINIO_ROOT_PASSWORD` = `Your Secret Key`
- `MINIO_SECURE` = `True`

The backend `storage.py` logic will automatically generate secure pre-signed URLs pointing directly to your new cloud storage!

---

## 4. Final Wire-up

Once the Render backend is live, copy its public URL (e.g., `https://janvastu-api.onrender.com`). 
1. Go back to your **Vercel Project Settings → Environment Variables**.
2. Update `VITE_API_BASE_URL` to match your Render URL.
3. Trigger a redeploy on Vercel so the frontend bakes the new URL into the build.

**You are now live! 🚀**
