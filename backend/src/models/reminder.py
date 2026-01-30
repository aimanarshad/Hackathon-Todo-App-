"""Reminder model for task reminders."""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Reminder(SQLModel, table=True):
    """Manages reminder scheduling and delivery status."""

    __tablename__ = "reminders"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    scheduled_time: datetime  # When the reminder should fire
    sent_time: Optional[datetime] = None  # When it was actually sent
    delivery_status: str = Field(default="pending")  # "pending", "sent", "failed", "cancelled"
    delivery_attempts: int = Field(default=0)
    last_delivery_attempt: Optional[datetime] = None
    reminder_type: str = Field(default="due_date")  # "due_date", "custom", "recurring"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    # task: Optional["Task"] = Relationship(back_populates="reminders")


# Indexes for better query performance
from sqlalchemy import Index

# Index on scheduled_time for querying upcoming reminders
Index("idx_reminders_scheduled_time", Reminder.__table__.c.scheduled_time)

# Index on delivery_status for filtering by status
Index("idx_reminders_delivery_status", Reminder.__table__.c.delivery_status)

# Index on task_id for joining with tasks
Index("idx_reminders_task_id", Reminder.__table__.c.task_id)

# Composite index for common query patterns
Index("idx_reminders_status_scheduled", Reminder.__table__.c.delivery_status, Reminder.__table__.c.scheduled_time)