# Task T009: Create Task model in backend/models.py following SQLModel specification
# Task T035: Update Task model to properly handle priority field validation in backend/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str
    description: str = ""
    completed: bool = False
    priority: Optional[str] = None  # "high", "medium", "low"
    tags: Optional[str] = ""  # comma-separated
    user_id: Optional[int] = None  # For future multi-user support

class Task(TaskBase, table=True):
    """
    Task model representing a single todo item with attributes for title,
    description, completion status, priority, tags, and timestamps.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None