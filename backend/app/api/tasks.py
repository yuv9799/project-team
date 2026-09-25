from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import Task, TeamMember
from app.core.security import get_current_user
from app.schemas.schemas import TaskCreate, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/{project_id}")
def list_tasks(project_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not db.scalar(select(TeamMember).where(TeamMember.project_id==project_id, TeamMember.user_id==user.id)): raise HTTPException(403, "Not a team member")
    return [{"id": t.id, "title": t.title, "description": t.description, "status": t.status, "priority": t.priority, "assignee_id": t.assignee_id} for t in db.scalars(select(Task).where(Task.project_id==project_id)).all()]

@router.post("")
def create_task(data: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not db.scalar(select(TeamMember).where(TeamMember.project_id==data.project_id, TeamMember.user_id==user.id)): raise HTTPException(403, "Not a team member")
    t=Task(**data.model_dump()); db.add(t); db.commit(); db.refresh(t)
    return {"id": t.id, "title": t.title, "status": t.status}

@router.patch("/{task_id}")
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t=db.get(Task, task_id)
    if not t or not db.scalar(select(TeamMember).where(TeamMember.project_id==t.project_id, TeamMember.user_id==user.id)): raise HTTPException(404, "Task not found")
    t.status=data.status; db.commit(); return {"status": t.status}
