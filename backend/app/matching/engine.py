from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import User, Project, user_skills, project_skills
from sqlalchemy import select

WEIGHTS = {"skills": .40, "interests": .20, "availability": .15, "experience": .15, "role": .10}

def overlap_hours(a, b):
    total = 0
    for x in a:
        for y in b:
            if x.day != y.day: continue
            start = max(x.start_time, y.start_time)
            end = min(x.end_time, y.end_time)
            if end > start:
                total += (datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)).seconds / 3600
    return total

def project_skill_map(db, project):
    rows = db.execute(select(project_skills.c.skill_id, project_skills.c.required_proficiency).where(project_skills.c.project_id == project.id)).all()
    return {r.skill_id: r.required_proficiency for r in rows}

def candidate_score(db: Session, project: Project, candidate: User):
    req = project_skill_map(db, project)
    if req:
        cand = {s.id: .5 for s in candidate.skills}
        skill_score = sum(min(cand.get(k, 0) / max(v, .01), 1) for k, v in req.items()) / len(req)
    else:
        skill_score = .5
    owner = project.owner
    pi = {i.name.lower() for i in getattr(owner, 'interests', [])}
    ci = {i.name.lower() for i in candidate.interests}
    interest_score = len(pi & ci) / max(1, len(pi | ci))
    availability = min(overlap_hours(owner.availability, candidate.availability) / max(project.weekly_hours, 1), 1)
    experience_score = min(len(candidate.projects) / 3, 1)
    role_score = 1 if candidate.id != owner.id else 0
    total = 100 * (WEIGHTS['skills']*skill_score + WEIGHTS['interests']*interest_score + WEIGHTS['availability']*availability + WEIGHTS['experience']*experience_score + WEIGHTS['role']*role_score)
    reasons = []
    if skill_score >= .7: reasons.append("strong skill coverage")
    if interest_score > 0: reasons.append("shared interests")
    if availability >= .6: reasons.append("good availability overlap")
    if experience_score >= .66: reasons.append("relevant project experience")
    return round(total), reasons

def recommend(db: Session, project: Project, limit=10):
    users = db.scalars(select(User).where(User.id != project.owner_id)).all()
    scored = []
    for u in users:
        score, reasons = candidate_score(db, project, u)
        scored.append({"user": u, "score": score, "reasons": reasons})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:limit]
