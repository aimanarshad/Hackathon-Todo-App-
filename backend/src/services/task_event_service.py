"""Service for managing task events in the event-driven architecture."""
from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from backend.models import Task
from backend.src.models.task_event import TaskEvent


class TaskEventService:
    """Service for managing task events."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task_event(
        self,
        event_type: str,
        task_id: int,
        event_data: dict,
        correlation_id: Optional[str] = None,
        causation_id: Optional[str] = None
    ) -> TaskEvent:
        """Create a new task event."""
        task_event = TaskEvent(
            event_type=event_type,
            task_id=task_id,
            event_data=event_data,
            event_timestamp=datetime.utcnow(),
            correlation_id=correlation_id,
            causation_id=causation_id
        )

        self.db_session.add(task_event)
        self.db_session.commit()
        self.db_session.refresh(task_event)

        return task_event

    def get_events_by_task_id(self, task_id: int) -> List[TaskEvent]:
        """Get all events for a specific task."""
        statement = select(TaskEvent).where(TaskEvent.task_id == task_id)
        return self.db_session.exec(statement).all()

    def get_events_by_type(self, event_type: str) -> List[TaskEvent]:
        """Get all events of a specific type."""
        statement = select(TaskEvent).where(TaskEvent.event_type == event_type)
        return self.db_session.exec(statement).all()

    def get_events_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[TaskEvent]:
        """Get events within a specific time range."""
        statement = select(TaskEvent).where(
            TaskEvent.event_timestamp >= start_time,
            TaskEvent.event_timestamp <= end_time
        )
        return self.db_session.exec(statement).all()

    def mark_event_as_processed(
        self,
        event_id: int,
        processor_name: str
    ) -> Optional[TaskEvent]:
        """Mark an event as processed by a specific service."""
        statement = select(TaskEvent).where(TaskEvent.id == event_id)
        task_event = self.db_session.exec(statement).first()

        if not task_event:
            return None

        task_event.processed_by = processor_name
        task_event.processed_at = datetime.utcnow()

        self.db_session.add(task_event)
        self.db_session.commit()
        self.db_session.refresh(task_event)

        return task_event

    def get_unprocessed_events(self, processor_name: str) -> List[TaskEvent]:
        """Get events that haven't been processed by a specific processor."""
        statement = select(TaskEvent).where(
            (TaskEvent.processed_by.is_(None)) |
            (TaskEvent.processed_by != processor_name)
        )
        return self.db_session.exec(statement).all()

    def create_task_created_event(self, task: Task) -> TaskEvent:
        """Create an event for when a task is created."""
        event_data = {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": task.user_id,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "reminder_enabled": task.reminder_enabled,
            "recurrence_pattern": task.recurrence_pattern
        }

        return self.create_task_event(
            event_type="task_created",
            task_id=task.id,
            event_data=event_data
        )

    def create_task_updated_event(self, task: Task, changes: dict) -> TaskEvent:
        """Create an event for when a task is updated."""
        event_data = {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "user_id": task.user_id,
            "changes": changes,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "reminder_enabled": task.reminder_enabled,
            "recurrence_pattern": task.recurrence_pattern
        }

        return self.create_task_event(
            event_type="task_updated",
            task_id=task.id,
            event_data=event_data
        )

    def create_task_completed_event(self, task: Task) -> TaskEvent:
        """Create an event for when a task is completed."""
        event_data = {
            "task_id": task.id,
            "title": task.title,
            "completed": task.completed,
            "user_id": task.user_id
        }

        return self.create_task_event(
            event_type="task_completed",
            task_id=task.id,
            event_data=event_data
        )

    def create_task_deleted_event(self, task_id: int, user_id: Optional[int] = None) -> TaskEvent:
        """Create an event for when a task is deleted."""
        event_data = {
            "task_id": task_id,
            "user_id": user_id
        }

        return self.create_task_event(
            event_type="task_deleted",
            task_id=task_id,
            event_data=event_data
        )

    def create_recurring_task_instance_event(
        self,
        task_id: int,
        template_task_id: int,
        user_id: Optional[int] = None
    ) -> TaskEvent:
        """Create an event for when a recurring task instance is created."""
        event_data = {
            "task_id": task_id,
            "template_task_id": template_task_id,
            "user_id": user_id
        }

        return self.create_task_event(
            event_type="recurring_task_instance_created",
            task_id=task_id,
            event_data=event_data
        )

    def create_reminder_scheduled_event(
        self,
        task_id: int,
        reminder_id: int,
        scheduled_time: datetime,
        user_id: Optional[int] = None
    ) -> TaskEvent:
        """Create an event for when a reminder is scheduled."""
        event_data = {
            "task_id": task_id,
            "reminder_id": reminder_id,
            "scheduled_time": scheduled_time.isoformat(),
            "user_id": user_id
        }

        return self.create_task_event(
            event_type="reminder_scheduled",
            task_id=task_id,
            event_data=event_data
        )