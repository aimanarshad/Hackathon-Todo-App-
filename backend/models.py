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
    Extended for Phase 5 with recurring tasks, due dates, and reminders.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Phase 5 additions (Advanced Features)
    due_date: Optional[datetime] = None
    reminder_enabled: bool = False
    reminder_time: Optional[datetime] = None  # When the reminder should trigger
    recurrence_pattern: Optional[str] = None  # "daily", "weekly", "monthly", "custom"
    recurrence_interval: Optional[int] = 1    # How often to repeat (e.g., every 2 weeks)
    recurrence_end_date: Optional[datetime] = None  # When recurrence stops
    recurrence_parent_id: Optional[int] = None  # For recurring instances, points to original
    recurrence_next_instance: Optional[datetime] = None  # When next instance should be created
    is_recurring_template: bool = False  # Whether this task is a template for recurrence
    timezone: Optional[str] = "UTC"  # User's timezone for scheduling

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    # Phase 5 fields for updates
    due_date: Optional[datetime] = None
    reminder_enabled: Optional[bool] = None
    reminder_time: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    recurrence_end_date: Optional[datetime] = None
    recurrence_parent_id: Optional[int] = None
    recurrence_next_instance: Optional[datetime] = None
    is_recurring_template: Optional[bool] = None
    timezone: Optional[str] = None