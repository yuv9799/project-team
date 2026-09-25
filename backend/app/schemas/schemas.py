from datetime import datetime, time
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str

class SkillInput(BaseModel):
    skill_id: int
    proficiency: float = Field(ge=0, le=1)

class InterestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class AvailabilityIn(BaseModel):
    day: int = Field(ge=0, le=6)
    start_time: time
    end_time: time

class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=180)
    description: str = Field(min_length=10)
    category: str = "Other"
    team_size: int = Field(ge=2, le=20)
    duration_weeks: int = Field(ge=1, le=52)
    weekly_hours: int = Field(ge=1, le=40)
    skill_ids: list[int] = []

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    college: str = "KIIT University"
    branch: str = "CSE"
    year: int = Field(default=2, ge=1, le=6)

class Login(BaseModel):
    email: EmailStr
    password: str

class ProfileUpdate(BaseModel):
    bio: str = ""
    branch: str | None = None
    year: int | None = Field(default=None, ge=1, le=6)
    skill_ids: list[int] | None = None
    interests: list[str] | None = None
    availability: list[AvailabilityIn] | None = None

class RequestCreate(BaseModel):
    project_id: int
    receiver_id: int
    message: str = ""

class RequestUpdate(BaseModel):
    status: str = Field(pattern="^(ACCEPTED|REJECTED)$")

class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: str = ""
    assignee_id: int | None = None
    priority: str = "MEDIUM"

class TaskUpdate(BaseModel):
    status: str = Field(pattern="^(TODO|IN_PROGRESS|REVIEW|DONE)$")

class AIProjectInput(BaseModel):
    text: str = Field(min_length=10)

class MessageCreate(BaseModel):
    project_id: int
    body: str = Field(min_length=1, max_length=2000)
