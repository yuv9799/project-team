from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Skill, Interest
from app.core.security import get_current_user

router = APIRouter(prefix="/api/catalog", tags=["catalog"])

@router.get("/skills")
def skills(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.scalars(select(Skill).order_by(Skill.category, Skill.name)).all()

@router.get("/interests")
def interests(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.scalars(select(Interest).order_by(Interest.name)).all()
