"""Recurrence engine for handling recurring tasks."""
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from backend.src.models.task import Task
from backend.src.services.task_service import TaskService
from backend.src.dapr.dapr_client import DaprClient


class RecurrenceEngine:
    """Engine to handle recurring task creation and management."""

    def __init__(self, db_session: Session, task_service: TaskService, dapr_client: DaprClient):
        self.db_session = db_session
        self.task_service = task_service
        self.dapr_client = dapr_client

    async def process_recurring_tasks(self):
        """Process recurring tasks and create new instances as needed."""
        # Get all recurring task templates that have upcoming instances
        statement = select(Task).where(
            Task.is_recurring_template == True,
            Task.recurrence_next_instance.is_not(None),
            Task.recurrence_next_instance <= datetime.utcnow(),
            Task.recurrence_end_date.is_(None) | (Task.recurrence_end_date >= datetime.utcnow())
        )

        recurring_templates = self.db_session.exec(statement).all()

        for template_task in recurring_templates:
            await self._create_next_instance(template_task)

    async def _create_next_instance(self, template_task: Task):
        """Create the next instance of a recurring task."""
        # Calculate next occurrence based on recurrence pattern
        next_occurrence = self._calculate_next_occurrence(
            template_task.recurrence_pattern,
            template_task.recurrence_interval,
            template_task.recurrence_next_instance,
            template_task.timezone
        )

        # Check if we've reached the end date
        if (template_task.recurrence_end_date and
            next_occurrence > template_task.recurrence_end_date):
            return

        # Create new task instance
        new_task = Task(
            content=template_task.content,
            completed=False,
            user_id=template_task.user_id,
            due_date=template_task.due_date,
            reminder_enabled=template_task.reminder_enabled,
            reminder_time=template_task.reminder_time,
            recurrence_pattern=template_task.recurrence_pattern,
            recurrence_interval=template_task.recurrence_interval,
            recurrence_parent_id=template_task.id,
            timezone=template_task.timezone
        )

        # Save the new task instance
        self.db_session.add(new_task)
        self.db_session.commit()
        self.db_session.refresh(new_task)

        # Update the template's next instance date
        template_task.recurrence_next_instance = next_occurrence
        self.db_session.add(template_task)
        self.db_session.commit()

        # Publish event about the new recurring task instance
        await self.dapr_client.publish_event(
            topic_name="task-events",
            event_data={
                "event_type": "recurring_task_instance_created",
                "task_id": new_task.id,
                "template_task_id": template_task.id,
                "occurrence_date": next_occurrence.isoformat(),
                "user_id": new_task.user_id
            }
        )

    def _calculate_next_occurrence(
        self,
        pattern: str,
        interval: int,
        current_date: datetime,
        timezone: Optional[str] = "UTC"
    ) -> datetime:
        """Calculate the next occurrence based on the recurrence pattern."""
        if pattern == "daily":
            return current_date + timedelta(days=interval)
        elif pattern == "weekly":
            return current_date + timedelta(weeks=interval)
        elif pattern == "monthly":
            # For monthly, we add months (approximate)
            # In a real implementation, we'd need to handle month boundaries properly
            return current_date + timedelta(days=30 * interval)
        elif pattern == "custom":
            # For custom patterns, we could implement more complex logic
            # For now, default to weekly
            return current_date + timedelta(weeks=interval)
        else:
            # Default to daily if pattern is unknown
            return current_date + timedelta(days=1)

    async def create_recurring_task(
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
        if start_date is None:
            start_date = datetime.utcnow()

        # Create the template task
        template_task = Task(
            content=content,
            completed=False,
            user_id=user_id,
            due_date=due_date,
            reminder_enabled=reminder_enabled,
            reminder_time=reminder_time,
            recurrence_pattern=pattern_type,
            recurrence_interval=interval,
            recurrence_end_date=end_date,
            recurrence_next_instance=start_date,
            is_recurring_template=True,
            timezone=timezone
        )

        self.db_session.add(template_task)
        self.db_session.commit()
        self.db_session.refresh(template_task)

        # Publish event about the new recurring task template
        await self.dapr_client.publish_event(
            topic_name="task-events",
            event_data={
                "event_type": "recurring_task_template_created",
                "task_id": template_task.id,
                "pattern_type": pattern_type,
                "interval": interval,
                "user_id": user_id
            }
        )

        return template_task

    async def update_recurring_task(
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
        statement = select(Task).where(
            Task.id == task_id,
            Task.is_recurring_template == True
        )
        template_task = self.db_session.exec(statement).first()

        if not template_task:
            return None

        # Update fields if provided
        if content is not None:
            template_task.content = content
        if pattern_type is not None:
            template_task.recurrence_pattern = pattern_type
        if interval is not None:
            template_task.recurrence_interval = interval
        if end_date is not None:
            template_task.recurrence_end_date = end_date
        if due_date is not None:
            template_task.due_date = due_date
        if reminder_enabled is not None:
            template_task.reminder_enabled = reminder_enabled
        if reminder_time is not None:
            template_task.reminder_time = reminder_time

        self.db_session.add(template_task)
        self.db_session.commit()
        self.db_session.refresh(template_task)

        return template_task

    async def delete_recurring_task(self, task_id: int) -> bool:
        """Delete a recurring task template (stops future instances)."""
        statement = select(Task).where(
            Task.id == task_id,
            Task.is_recurring_template == True
        )
        template_task = self.db_session.exec(statement).first()

        if not template_task:
            return False

        # Mark as deleted or remove the recurrence pattern to stop future instances
        template_task.is_recurring_template = False
        template_task.recurrence_pattern = None
        template_task.recurrence_next_instance = None

        self.db_session.add(template_task)
        self.db_session.commit()

        return True