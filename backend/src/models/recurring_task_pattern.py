"""Recurring task pattern model for defining recurrence rules."""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class RecurringTaskPattern(SQLModel, table=True):
    """Represents the recurrence rules for recurring tasks."""

    __tablename__ = "recurring_task_patterns"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")  # Points to the template task
    pattern_type: str  # "daily", "weekly", "monthly", "custom"
    interval: int = Field(default=1)  # How often to repeat
    days_of_week: Optional[str] = None  # For weekly patterns (e.g., "mon,wed,fri")
    days_of_month: Optional[str] = None  # For monthly patterns (e.g., "1,15,30")
    occurrence_count: Optional[int] = None  # Max number of occurrences
    end_date: Optional[datetime] = None  # When recurrence ends
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    # task: Optional["Task"] = Relationship(back_populates="recurrence_pattern_obj")


# Indexes for better query performance
from sqlalchemy import Index

# Index on task_id for joining with tasks
Index("idx_recurring_patterns_task_id", RecurringTaskPattern.__table__.c.task_id)

# Index on pattern_type for filtering by type
Index("idx_recurring_patterns_type", RecurringTaskPattern.__table__.c.pattern_type)

# Index on end_date for finding expired patterns
Index("idx_recurring_patterns_end_date", RecurringTaskPattern.__table__.c.end_date)