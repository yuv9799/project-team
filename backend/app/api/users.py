from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.db.session import get_db
from app.models.models import User, Skill, Interest, Availability
from app.core.security import get_current_user
from app.schemas.schemas import ProfileUpdate
from app.services.serializers import user_summary

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me")
def me(user=Depends(get_current_user)):
    return user_summary(user)

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    return user_summary(user)

@router.get("")
def search(q: str = "", db: Session = Depends(get_db), user=Depends(get_current_user)):
    stmt = select(User).where(User.id != user.id)
    if q:
        stmt = stmt.where(or_(User.name.ilike(f"%{q}%"), User.branch.ilike(f"%{q}%")))
    users = db.scalars(stmt.limit(50)).all()
    return [user_summary(u) for u in users]

@router.patch("/me")
def update(data: ProfileUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if data.bio is not None: user.bio = data.bio
    if data.branch is not None: user.branch = data.branch
    if data.year is not None: user.year = data.year
    if data.skill_ids is not None:
        user.skills = list(db.scalars(select(Skill).where(Skill.id.in_(data.skill_ids))).all())
    if data.interests is not None:
        existing = {i.name.lower(): i for i in db.scalars(select(Interest)).all()}
        user.interests = []
        for name in data.interests:
            key = name.strip().lower()
            if not key: continue
            obj = existing.get(key)
            if not obj:
                obj = Interest(name=name.strip()); db.add(obj); db.flush()
            user.interests.append(obj)
    if data.availability is not None:
        user.availability.clear()
        user.availability.extend([Availability(day=a.day, start_time=a.start_time, end_time=a.end_time) for a in data.availability])
    db.commit(); db.refresh(user)
    return user_summary(user)
