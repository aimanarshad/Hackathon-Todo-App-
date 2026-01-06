# Task T011: Create Pydantic schemas in backend/schemas.py for request/response validation
# Task T036: Update Task schemas to include priority and tags validation in backend/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    priority: Optional[str] = None  # "high", "medium", "low"
    tags: Optional[str] = ""  # comma-separated

class TaskCreate(TaskBase):
    title: str  # Required for creation

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True