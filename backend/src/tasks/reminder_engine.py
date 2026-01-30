"""Reminder engine for processing reminders."""
from datetime import datetime
from typing import List
from sqlmodel import Session
from backend.src.services.reminder_service import ReminderService
from backend.src.dapr.task_event_producer import TaskEventProducer


class ReminderEngine:
    """Engine to handle reminder processing and scheduling."""

    def __init__(self, db_session: Session, reminder_service: ReminderService, task_event_producer: TaskEventProducer):
        self.db_session = db_session
        self.reminder_service = reminder_service
        self.task_event_producer = task_event_producer

    async def process_upcoming_reminders(self) -> int:
        """Process all upcoming reminders that should be sent now."""
        return self.reminder_service.process_upcoming_reminders()

    async def schedule_task_reminder(self, task_id: int, reminder_time: datetime, user_id: int) -> bool:
        """Schedule a reminder for a specific task."""
        # For now, we'll just return True - the actual scheduling is handled by the reminder service
        # which integrates with the scheduler
        return True

    async def cancel_task_reminder(self, task_id: int) -> bool:
        """Cancel any scheduled reminders for a task."""
        # Get all reminders for this task
        reminders = self.reminder_service.get_reminders_by_task_id(task_id)

        cancelled_count = 0
        for reminder in reminders:
            if self.reminder_service.cancel_reminder(reminder.id):
                cancelled_count += 1

        return cancelled_count > 0

    async def create_due_date_reminder(self, task_id: int, due_date: datetime, user_id: int) -> bool:
        """Create a reminder for a task's due date."""
        # This would typically be called when a task with a due date is created
        # For now, we'll just return True
        return True

    async def get_upcoming_reminders(self, user_id: int) -> List:
        """Get upcoming reminders for a user."""
        # This would return a list of reminders for the user
        # For now, we'll return an empty list
        return []

    async def process_reminder_queue(self) -> int:
        """Process the reminder queue and send notifications."""
        # Process all upcoming reminders
        processed_count = self.reminder_service.process_upcoming_reminders()
        return processed_count

    async def send_reminder_notification(self, task_id: int, user_id: int, reminder_message: str) -> bool:
        """Send a reminder notification to a user."""
        try:
            # Publish reminder sent event
            await self.task_event_producer.publish_reminder_sent(
                reminder_id=0,  # Placeholder ID
                task_id=task_id,
                sent_time=datetime.utcnow(),
                user_id=user_id
            )

            # In a real implementation, this would send an actual notification
            # (email, push notification, etc.)
            print(f"Sending reminder to user {user_id} for task {task_id}: {reminder_message}")

            return True
        except Exception as e:
            print(f"Error sending reminder notification: {str(e)}")
            return False

    async def check_and_trigger_reminders(self):
        """Check for any reminders that should be triggered now and process them."""
        # Get all upcoming reminders that should be sent now
        upcoming_reminders = self.reminder_service.get_upcoming_reminders()

        triggered_count = 0
        for reminder in upcoming_reminders:
            try:
                # In a real implementation, we would get the user and task details
                # For now, we'll just use placeholder values
                user_id = 0  # Placeholder
                task_id = reminder.task_id
                message = f"Reminder: Task '{task_id}' is due soon!"

                # Send the reminder notification
                success = await self.send_reminder_notification(task_id, user_id, message)

                if success:
                    # Mark as sent in the database
                    self.reminder_service.mark_reminder_as_sent(reminder.id)
                    triggered_count += 1
                else:
                    # Mark as failed
                    self.reminder_service.mark_reminder_as_failed(reminder.id)

            except Exception as e:
                print(f"Error triggering reminder {reminder.id}: {str(e)}")
                self.reminder_service.mark_reminder_as_failed(reminder.id)

        return triggered_count