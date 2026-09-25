from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import Message, TeamMember
from app.core.security import get_current_user
from app.schemas.schemas import MessageCreate

router=APIRouter(prefix="/api/messages", tags=["messages"])

@router.get("/{project_id}")
def list_messages(project_id:int, db:Session=Depends(get_db), user=Depends(get_current_user)):
    if not db.scalar(select(TeamMember).where(TeamMember.project_id==project_id, TeamMember.user_id==user.id)): raise HTTPException(403,"Not a team member")
    return [{"id":m.id,"sender_id":m.sender_id,"body":m.body,"created_at":m.created_at.isoformat()} for m in db.scalars(select(Message).where(Message.project_id==project_id).order_by(Message.created_at)).all()]

@router.post("")
def send(data:MessageCreate, db:Session=Depends(get_db), user=Depends(get_current_user)):
    if not db.scalar(select(TeamMember).where(TeamMember.project_id==data.project_id, TeamMember.user_id==user.id)): raise HTTPException(403,"Not a team member")
    m=Message(project_id=data.project_id,sender_id=user.id,body=data.body); db.add(m); db.commit(); db.refresh(m)
    return {"id":m.id,"sender_id":m.sender_id,"body":m.body,"created_at":m.created_at.isoformat()}
