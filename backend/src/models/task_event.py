"""Task event model for event-driven architecture."""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, JSON


class TaskEvent(SQLModel, table=True):
    """Captures events related to tasks for the event-driven architecture."""

    __tablename__ = "task_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(sa_column=Column("event_type", nullable=False))  # "task_created", "task_updated", "task_completed", "task_deleted", "reminder_sent"
    task_id: int = Field(foreign_key="task.id")
    event_data: Dict[str, Any] = Field(sa_column=Column("event_data", JSON, nullable=False))  # JSON payload with event details
    event_timestamp: datetime = Field(sa_column=Column("event_timestamp", DateTime(timezone=True), nullable=False, default=datetime.utcnow))
    correlation_id: Optional[str] = Field(sa_column=Column("correlation_id", nullable=True))  # For tracing related events
    causation_id: Optional[str] = Field(sa_column=Column("causation_id", nullable=True))  # Which event caused this event
    processed_by: Optional[str] = Field(sa_column=Column("processed_by", nullable=True))  # Which service processed this event
    processed_at: Optional[datetime] = Field(sa_column=Column("processed_at", DateTime(timezone=True), nullable=True))

    # Relationships
    # task: Optional["Task"] = Relationship(back_populates="events")


# Indexes for better query performance
from sqlalchemy import Index

# Index on event_type for filtering by event type
Index("idx_task_events_event_type", TaskEvent.__table__.c.event_type)

# Index on task_id for joining with tasks
Index("idx_task_events_task_id", TaskEvent.__table__.c.task_id)

# Index on event_timestamp for time-based queries
Index("idx_task_events_timestamp", TaskEvent.__table__.c.event_timestamp)

# Composite index for common query patterns
Index("idx_task_events_type_timestamp", TaskEvent.__table__.c.event_type, TaskEvent.__table__.c.event_timestamp)