from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import Project, Skill, TeamMember, CollaborationRequest, Notification, User
from app.core.security import get_current_user
from app.schemas.schemas import ProjectCreate, RequestCreate, RequestUpdate
from app.matching.engine import recommend

router = APIRouter(prefix="/api/projects", tags=["projects"])

def serialize(p):
    return {"id": p.id, "name": p.name, "description": p.description, "category": p.category, "team_size": p.team_size, "duration_weeks": p.duration_weeks, "weekly_hours": p.weekly_hours, "status": p.status, "owner": {"id": p.owner.id, "name": p.owner.name}, "skills": [{"id": s.id, "name": s.name, "category": s.category} for s in p.skills], "members": [{"user_id": m.user_id, "name": m.user.name, "role": m.role} for m in p.members]}

@router.post("")
def create(data: ProjectCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    skills = list(db.scalars(select(Skill).where(Skill.id.in_(data.skill_ids))).all()) if data.skill_ids else []
    p = Project(owner_id=user.id, name=data.name, description=data.description, category=data.category, team_size=data.team_size, duration_weeks=data.duration_weeks, weekly_hours=data.weekly_hours, skills=skills)
    db.add(p); db.flush(); db.add(TeamMember(project_id=p.id, user_id=user.id, role="Project Lead")); db.commit(); db.refresh(p)
    return serialize(p)

@router.get("")
def list_projects(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return [serialize(p) for p in db.scalars(select(Project).order_by(Project.created_at.desc())).all()]

@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.get(Project, project_id)
    if not p: raise HTTPException(404, "Project not found")
    return serialize(p)

@router.get("/{project_id}/recommendations")
def recommendations(project_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.get(Project, project_id)
    if not p: raise HTTPException(404, "Project not found")
    return [{"user": {"id": x["user"].id, "name": x["user"].name, "branch": x["user"].branch, "year": x["user"].year, "skills": [s.name for s in x["user"].skills], "interests": [i.name for i in x["user"].interests]}, "score": x["score"], "reasons": x["reasons"]} for x in recommend(db, p)]

@router.post("/requests")
def request_team(data: RequestCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    p = db.get(Project, data.project_id); receiver = db.get(User, data.receiver_id)
    if not p or not receiver: raise HTTPException(404, "Project or user not found")
    existing = db.scalar(select(CollaborationRequest).where(CollaborationRequest.project_id==p.id, CollaborationRequest.sender_id==user.id, CollaborationRequest.receiver_id==receiver.id, CollaborationRequest.status=="PENDING"))
    if existing: raise HTTPException(409, "Request already pending")
    req = CollaborationRequest(project_id=p.id, sender_id=user.id, receiver_id=receiver.id, message=data.message)
    db.add(req); db.add(Notification(user_id=receiver.id, title="New collaboration request", body=f"{user.name} invited you to {p.name}")); db.commit()
    return {"id": req.id, "status": req.status}

@router.get("/requests/mine")
def requests(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = db.scalars(select(CollaborationRequest).where((CollaborationRequest.receiver_id==user.id) | (CollaborationRequest.sender_id==user.id)).order_by(CollaborationRequest.created_at.desc())).all()
    return [{"id": r.id, "project_id": r.project_id, "sender_id": r.sender_id, "receiver_id": r.receiver_id, "status": r.status, "message": r.message} for r in rows]

@router.patch("/requests/{request_id}")
def update_request(request_id: int, data: RequestUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    r = db.get(CollaborationRequest, request_id)
    if not r or r.receiver_id != user.id: raise HTTPException(404, "Request not found")
    r.status = data.status
    if data.status == "ACCEPTED":
        exists = db.scalar(select(TeamMember).where(TeamMember.project_id==r.project_id, TeamMember.user_id==user.id))
        if not exists: db.add(TeamMember(project_id=r.project_id, user_id=user.id, role="Member"))
        db.add(Notification(user_id=r.sender_id, title="Collaboration accepted", body="Your project invitation was accepted."))
    db.commit()
    return {"status": r.status}
