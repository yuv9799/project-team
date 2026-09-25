# 🚀 Deployment Guide: CampusConnect

This guide explains how to deploy **CampusConnect** using free-tier cloud services:
- **Backend & Database**: [Render](https://render.com) (or [Railway](https://railway.app) / [Fly.io](https://fly.io) + [Neon](https://neon.tech))
- **Frontend**: [Vercel](https://vercel.com)

---

## Architecture Overview

```
┌────────────────────────────────┐
│   Vercel (Next.js Frontend)    │  URL: https://campus-connect.vercel.app
└───────────────┬────────────────┘
                │ NEXT_PUBLIC_API_URL
                ▼
┌────────────────────────────────┐
│   Render (FastAPI Backend)     │  URL: https://campus-connect-api.onrender.com
└───────────────┬────────────────┘
                │ DATABASE_URL
                ▼
┌────────────────────────────────┐
│   PostgreSQL Database          │  (Render Postgres / Neon / Supabase)
└────────────────────────────────┘
```

---

## Step 1: Deploy Database & Backend (Render)

### Option A: Using Render Blueprint (Fastest)

1. Push this repository to GitHub: `https://github.com/yuv9799/project-team`.
2. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** → **Blueprint**.
3. Connect your repository `yuv9799/project-team`.
4. Render will detect `render.yaml` and automatically provision:
   - **PostgreSQL Database** (`campus-connect-db`)
   - **FastAPI Web Service** (`campus-connect-api` built from `./backend/Dockerfile`)
5. Click **Apply**.
6. Once deployed, note down your backend URL: e.g., `https://campus-connect-api.onrender.com`.

### Option B: Manual Setup on Render

1. **Create PostgreSQL Database**:
   - In Render, click **New +** → **PostgreSQL Database**.
   - Name: `campus-connect-db`, Database: `campus_connect`, User: `campus`.
   - Copy the **Internal Connection String** (or External Connection String).

2. **Create Web Service**:
   - In Render, click **New +** → **Web Service**.
   - Connect your GitHub repository.
   - **Root Directory**: `backend`
   - **Environment**: `Docker` (or `Python 3` with Build: `pip install -r requirements.txt`, Start: `python seed.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`)
   - Add Environment Variables:
     - `DATABASE_URL`: *(Your PostgreSQL connection string)*
     - `JWT_SECRET`: *(A random 32+ character secret)*
     - `ACCESS_TOKEN_MINUTES`: `10080`
     - `CORS_ORIGINS`: `http://localhost:3000,https://*.vercel.app`
3. Click **Deploy Web Service**.

---

## Step 2: Deploy Frontend (Vercel)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) and click **Add New...** → **Project**.
2. Import your GitHub repository `yuv9799/project-team`.
3. In **Project Configuration**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Click *Edit* and select `frontend` (or `campus-connect/frontend` depending on repository root structure).
4. In **Environment Variables**:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://campus-connect-api.onrender.com` *(Replace with your actual Render backend URL)*
5. Click **Deploy**.

---

## Step 3: Verify Deployment

1. Visit your Vercel URL (e.g., `https://campus-connect.vercel.app`).
2. Test signing in with one of the pre-seeded demo accounts:
   - **Email**: `aarav@kiit.edu`
   - **Password**: `password123`
3. Visit the backend health check endpoint: `https://campus-connect-api.onrender.com/health` (should return `{"status":"ok"}`).
4. Backend Swagger documentation: `https://campus-connect-api.onrender.com/docs`.
