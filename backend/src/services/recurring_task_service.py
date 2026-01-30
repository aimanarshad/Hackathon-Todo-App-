"""Service for managing recurring tasks."""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from backend.models import Task
from backend.src.models.recurring_task_pattern import RecurringTaskPattern
from backend.src.tasks.recurrence_engine import RecurrenceEngine


class RecurringTaskService:
    """Service for managing recurring tasks and their patterns."""

    def __init__(
        self,
        db_session: Session,
        recurrence_engine: RecurrenceEngine
    ):
        self.db_session = db_session
        self.recurrence_engine = recurrence_engine

    def create_recurring_task(
        self,
        content: str,
        user_id: int,
        pattern_type: str,
        interval: int = 1,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        due_date: Optional[datetime] = None,
        reminder_enabled: bool = False,
        reminder_time: Optional[datetime] = None,
        timezone: str = "UTC"
    ) -> Task:
        """Create a new recurring task template."""
        return self.recurrence_engine.create_recurring_task(
            content=content,
            user_id=user_id,
            pattern_type=pattern_type,
            interval=interval,
            start_date=start_date,
            end_date=end_date,
            due_date=due_date,
            reminder_enabled=reminder_enabled,
            reminder_time=reminder_time,
            timezone=timezone
        )

    def get_recurring_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a recurring task template by its ID."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.is_recurring_template == True
        )
        return self.db_session.exec(statement).first()

    def get_recurring_tasks_for_user(self, user_id: int) -> List[Task]:
        """Get all recurring task templates for a specific user."""
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.is_recurring_template == True
        )
        return self.db_session.exec(statement).all()

    def get_recurring_task_instances(self, template_task_id: int) -> List[Task]:
        """Get all instances of a recurring task template."""
        statement = select(Task).where(
            Task.recurrence_parent_id == template_task_id
        ).order_by(Task.created_at.desc())
        return self.db_session.exec(statement).all()

    def update_recurring_task(
        self,
        task_id: int,
        content: Optional[str] = None,
        pattern_type: Optional[str] = None,
        interval: Optional[int] = None,
        end_date: Optional[datetime] = None,
        due_date: Optional[datetime] = None,
        reminder_enabled: Optional[bool] = None,
        reminder_time: Optional[datetime] = None
    ) -> Optional[Task]:
        """Update a recurring task template."""
        return self.recurrence_engine.update_recurring_task(
            task_id=task_id,
            content=content,
            pattern_type=pattern_type,
            interval=interval,
            end_date=end_date,
            due_date=due_date,
            reminder_enabled=reminder_enabled,
            reminder_time=reminder_time
        )

    def delete_recurring_task(self, task_id: int) -> bool:
        """Delete a recurring task template (stops future instances)."""
        return self.recurrence_engine.delete_recurring_task(task_id)

    def process_recurring_tasks(self):
        """Process recurring tasks and create new instances as needed."""
        return self.recurrence_engine.process_recurring_tasks()

    def get_upcoming_recurring_tasks(self, user_id: int) -> List[Task]:
        """Get recurring tasks that have upcoming instances."""
        statement = select(Task).where(
            Task.user_id == user_id,
            Task.is_recurring_template == True,
            Task.recurrence_next_instance.is_not(None),
            Task.recurrence_next_instance <= datetime.utcnow() + timedelta(days=7),  # Next week
            (Task.recurrence_end_date.is_(None)) | (Task.recurrence_end_date >= datetime.utcnow())
        ).order_by(Task.recurrence_next_instance.asc())
        return self.db_session.exec(statement).all()

    def get_recurring_task_pattern(self, task_id: int) -> Optional[RecurringTaskPattern]:
        """Get the recurrence pattern for a recurring task."""
        statement = select(RecurringTaskPattern).where(
            RecurringTaskPattern.task_id == task_id
        )
        return self.db_session.exec(statement).first()

    def create_recurring_task_pattern(
        self,
        task_id: int,
        pattern_type: str,
        interval: int = 1,
        days_of_week: Optional[str] = None,
        days_of_month: Optional[str] = None,
        occurrence_count: Optional[int] = None,
        end_date: Optional[datetime] = None
    ) -> RecurringTaskPattern:
        """Create a recurrence pattern for a task."""
        pattern = RecurringTaskPattern(
            task_id=task_id,
            pattern_type=pattern_type,
            interval=interval,
            days_of_week=days_of_week,
            days_of_month=days_of_month,
            occurrence_count=occurrence_count,
            end_date=end_date
        )

        self.db_session.add(pattern)
        self.db_session.commit()
        self.db_session.refresh(pattern)

        return pattern

    def update_recurring_task_pattern(
        self,
        task_id: int,
        pattern_type: Optional[str] = None,
        interval: Optional[int] = None,
        days_of_week: Optional[str] = None,
        days_of_month: Optional[str] = None,
        occurrence_count: Optional[int] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[RecurringTaskPattern]:
        """Update a recurrence pattern for a task."""
        statement = select(RecurringTaskPattern).where(
            RecurringTaskPattern.task_id == task_id
        )
        pattern = self.db_session.exec(statement).first()

        if not pattern:
            return None

        if pattern_type is not None:
            pattern.pattern_type = pattern_type
        if interval is not None:
            pattern.interval = interval
        if days_of_week is not None:
            pattern.days_of_week = days_of_week
        if days_of_month is not None:
            pattern.days_of_month = days_of_month
        if occurrence_count is not None:
            pattern.occurrence_count = occurrence_count
        if end_date is not None:
            pattern.end_date = end_date

        self.db_session.add(pattern)
        self.db_session.commit()
        self.db_session.refresh(pattern)

        return pattern