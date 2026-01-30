"""Service for managing task reminders."""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlmodel import Session, select
from backend.models import Task
from backend.src.models.reminder import Reminder
from backend.src.dapr.task_event_producer import TaskEventProducer
from backend.src.tasks.scheduler import get_scheduler


class ReminderService:
    """Service for managing task reminders."""

    def __init__(self, db_session: Session, task_event_producer: TaskEventProducer):
        self.db_session = db_session
        self.task_event_producer = task_event_producer

    def create_reminder(
        self,
        task_id: int,
        scheduled_time: datetime,
        reminder_type: str = "due_date",
        user_id: Optional[int] = None
    ) -> Reminder:
        """Create a new reminder."""
        reminder = Reminder(
            task_id=task_id,
            scheduled_time=scheduled_time,
            reminder_type=reminder_type,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db_session.add(reminder)
        self.db_session.commit()
        self.db_session.refresh(reminder)

        # Schedule the reminder using the scheduler
        scheduler = get_scheduler()
        if scheduler:
            scheduler.schedule_reminder(scheduled_time, task_id, user_id or 0)

        # Publish reminder scheduled event
        # Note: We use asyncio.run here to run the async method in a sync context
        import asyncio
        asyncio.run(
            self.task_event_producer.publish_reminder_scheduled(
                reminder_id=reminder.id,
                task_id=task_id,
                scheduled_time=scheduled_time,
                user_id=user_id or 0
            )
        )

        return reminder

    def get_reminder_by_id(self, reminder_id: int) -> Optional[Reminder]:
        """Get a reminder by its ID."""
        statement = select(Reminder).where(Reminder.id == reminder_id)
        return self.db_session.exec(statement).first()

    def get_reminders_by_task_id(self, task_id: int) -> List[Reminder]:
        """Get all reminders for a specific task."""
        statement = select(Reminder).where(Reminder.task_id == task_id)
        return self.db_session.exec(statement).all()

    def get_upcoming_reminders(self, limit: int = 100) -> List[Reminder]:
        """Get all upcoming reminders."""
        statement = select(Reminder).where(
            Reminder.scheduled_time >= datetime.utcnow(),
            Reminder.delivery_status == "pending"
        ).order_by(Reminder.scheduled_time.asc()).limit(limit)
        return self.db_session.exec(statement).all()

    def get_reminders_by_user(self, user_id: int) -> List[Reminder]:
        """Get all reminders for a specific user."""
        # Join with Task table to filter by user
        statement = select(Reminder).join(Task).where(
            Task.user_id == user_id,
            Reminder.delivery_status == "pending"
        ).order_by(Reminder.scheduled_time.asc())
        return self.db_session.exec(statement).all()

    def cancel_reminder(self, reminder_id: int) -> bool:
        """Cancel a scheduled reminder."""
        statement = select(Reminder).where(Reminder.id == reminder_id)
        reminder = self.db_session.exec(statement).first()

        if not reminder:
            return False

        reminder.delivery_status = "cancelled"
        reminder.updated_at = datetime.utcnow()

        self.db_session.add(reminder)
        self.db_session.commit()

        return True

    def mark_reminder_as_sent(self, reminder_id: int) -> bool:
        """Mark a reminder as sent."""
        statement = select(Reminder).where(Reminder.id == reminder_id)
        reminder = self.db_session.exec(statement).first()

        if not reminder:
            return False

        reminder.delivery_status = "sent"
        reminder.sent_time = datetime.utcnow()
        reminder.updated_at = datetime.utcnow()

        self.db_session.add(reminder)
        self.db_session.commit()

        return True

    def mark_reminder_as_failed(self, reminder_id: int) -> bool:
        """Mark a reminder as failed."""
        statement = select(Reminder).where(Reminder.id == reminder_id)
        reminder = self.db_session.exec(statement).first()

        if not reminder:
            return False

        reminder.delivery_status = "failed"
        reminder.last_delivery_attempt = datetime.utcnow()
        reminder.delivery_attempts += 1
        reminder.updated_at = datetime.utcnow()

        self.db_session.add(reminder)
        self.db_session.commit()

        return True

    def create_due_date_reminder(self, task: Task) -> Optional[Reminder]:
        """Create a reminder for a task's due date."""
        if not task.due_date or not task.reminder_enabled or not task.reminder_time:
            return None

        return self.create_reminder(
            task_id=task.id,
            scheduled_time=task.reminder_time,
            reminder_type="due_date",
            user_id=task.user_id
        )

    def create_recurring_task_reminder(self, task: Task) -> Optional[Reminder]:
        """Create a reminder for a recurring task."""
        if not task.due_date or not task.reminder_enabled or not task.reminder_time:
            return None

        return self.create_reminder(
            task_id=task.id,
            scheduled_time=task.reminder_time,
            reminder_type="recurring",
            user_id=task.user_id
        )

    def process_upcoming_reminders(self) -> int:
        """Process all upcoming reminders that should be sent now."""
        now = datetime.utcnow()

        # Get all reminders that should be sent now
        statement = select(Reminder).where(
            Reminder.scheduled_time <= now,
            Reminder.delivery_status == "pending"
        )
        reminders_to_process = self.db_session.exec(statement).all()

        processed_count = 0
        for reminder in reminders_to_process:
            try:
                # Mark as sent
                self.mark_reminder_as_sent(reminder.id)

                # Publish reminder sent event
                import asyncio
                asyncio.run(
                    self.task_event_producer.publish_reminder_sent(
                        reminder_id=reminder.id,
                        task_id=reminder.task_id,
                        sent_time=datetime.utcnow(),
                        user_id=0  # TODO: Get user ID from task
                    )
                )

                processed_count += 1
            except Exception as e:
                print(f"Error processing reminder {reminder.id}: {str(e)}")
                self.mark_reminder_as_failed(reminder.id)

        return processed_count

    def get_overdue_reminders(self, minutes_threshold: int = 5) -> List[Reminder]:
        """Get reminders that are overdue by the specified threshold."""
        threshold_time = datetime.utcnow() - timedelta(minutes=minutes_threshold)

        statement = select(Reminder).where(
            Reminder.scheduled_time <= threshold_time,
            Reminder.delivery_status == "pending"
        )
        return self.db_session.exec(statement).all()

    def reschedule_failed_reminder(self, reminder_id: int, new_time: datetime) -> bool:
        """Reschedule a failed reminder for a new time."""
        statement = select(Reminder).where(Reminder.id == reminder_id)
        reminder = self.db_session.exec(statement).first()

        if not reminder:
            return False

        # Reset the reminder to pending with new time
        reminder.scheduled_time = new_time
        reminder.delivery_status = "pending"
        reminder.updated_at = datetime.utcnow()

        self.db_session.add(reminder)
        self.db_session.commit()

        # Reschedule in the scheduler
        scheduler = get_scheduler()
        if scheduler:
            scheduler.schedule_reminder(new_time, reminder.task_id, 0)  # TODO: Get user ID

        return True