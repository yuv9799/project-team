from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.api import auth, users, skills, projects, tasks, ai, messages
from app.models import models

Base.metadata.create_all(bind=engine)
app=FastAPI(title="CampusConnect API", version="1.0.0")

raw_origins = [x.strip() for x in settings.cors_origins.split(',') if x.strip()]
if "*" in raw_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=raw_origins if raw_origins else ["http://localhost:3000"],
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth.router); app.include_router(users.router); app.include_router(skills.router); app.include_router(projects.router); app.include_router(tasks.router); app.include_router(ai.router); app.include_router(messages.router)

@app.get("/health")
def health(): return {"status":"ok"}

