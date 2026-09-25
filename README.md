# CampusConnect — AI Project Teammate Finder

A full-stack student collaboration platform for finding project teammates using skills, interests, availability, experience and explainable matching.

## Stack

- Frontend: Next.js 15, React 19, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Auth: JWT + bcrypt
- Matching: weighted explainable recommendation engine
- AI: natural-language project requirement extraction with a deterministic fallback
- Collaboration: projects, teams, requests, tasks, messages

## Run with Docker

```bash
docker compose up --build
```

Frontend is intentionally run separately:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

Backend docs: http://localhost:8000/docs

## Demo accounts

Password for all seeded accounts: `password123`

- aarav@kiit.edu
- riya@kiit.edu
- kabir@kiit.edu
- ananya@kiit.edu
- dev@kiit.edu
- meera@kiit.edu

## Local backend without Docker

Set `DATABASE_URL` to a local PostgreSQL URL, install `backend/requirements.txt`, then run:

```bash
cd backend
python seed.py
uvicorn app.main:app --reload --port 8000
```

## Important production work remaining

This repository is a strong working MVP, not a finished production deployment. Before real college deployment, add email verification provider, refresh-token rotation, rate limiting, file storage, real-time WebSockets, pgvector embeddings, moderation, audit logs, database migrations (Alembic), automated CI/CD, and production secrets.
