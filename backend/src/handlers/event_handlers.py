"""Event handlers for processing task events."""
from typing import Dict, Any
from backend.src.services.task_event_service import TaskEventService
from backend.src.services.reminder_service import ReminderService
from backend.src.services.notification_service import NotificationService


class EventHandler:
    """Handles different types of events in the system."""

    def __init__(
        self,
        task_event_service: TaskEventService,
        reminder_service: ReminderService,
        notification_service: NotificationService
    ):
        self.task_event_service = task_event_service
        self.reminder_service = reminder_service
        self.notification_service = notification_service

    async def handle_task_created(self, event_data: Dict[str, Any]):
        """Handle task created event."""
        print(f"Handling task created event: {event_data}")

        # If the task has a due date and reminder is enabled, create a reminder
        task_id = event_data.get('task_id')
        user_id = event_data.get('user_id')
        due_date = event_data.get('due_date')
        reminder_enabled = event_data.get('reminder_enabled', False)
        reminder_time = event_data.get('reminder_time')

        if reminder_enabled and due_date and reminder_time:
            # Create a reminder for the task
            await self.reminder_service.create_reminder(
                task_id=task_id,
                scheduled_time=reminder_time,
                reminder_type="due_date",
                user_id=user_id
            )

    async def handle_task_updated(self, event_data: Dict[str, Any]):
        """Handle task updated event."""
        print(f"Handling task updated event: {event_data}")

        # Check if due date or reminder settings changed
        task_id = event_data.get('task_id')
        changes = event_data.get('changes', {})

        # If due date or reminder settings were updated, handle accordingly
        if 'due_date' in changes or 'reminder_enabled' in changes or 'reminder_time' in changes:
            # Cancel existing reminders and create new ones if needed
            await self.reminder_service.cancel_task_reminder(task_id)

            # If new due date and reminder settings exist, create new reminder
            due_date = event_data.get('due_date')
            reminder_enabled = event_data.get('reminder_enabled', False)
            reminder_time = event_data.get('reminder_time')

            if reminder_enabled and due_date and reminder_time:
                await self.reminder_service.create_reminder(
                    task_id=task_id,
                    scheduled_time=reminder_time,
                    reminder_type="due_date",
                    user_id=event_data.get('user_id')
                )

    async def handle_task_completed(self, event_data: Dict[str, Any]):
        """Handle task completed event."""
        print(f"Handling task completed event: {event_data}")

        # Cancel any scheduled reminders for this task
        task_id = event_data.get('task_id')
        await self.reminder_service.cancel_task_reminder(task_id)

    async def handle_task_deleted(self, event_data: Dict[str, Any]):
        """Handle task deleted event."""
        print(f"Handling task deleted event: {event_data}")

        # Cancel any scheduled reminders for this task
        task_id = event_data.get('task_id')
        await self.reminder_service.cancel_task_reminder(task_id)

    async def handle_recurring_task_instance_created(self, event_data: Dict[str, Any]):
        """Handle recurring task instance created event."""
        print(f"Handling recurring task instance created event: {event_data}")

        task_id = event_data.get('task_id')
        template_task_id = event_data.get('template_task_id')
        user_id = event_data.get('user_id')

        # If the template task had reminders enabled, create a reminder for the new instance
        # This would require fetching the template task details
        # For now, just log the event

    async def handle_reminder_scheduled(self, event_data: Dict[str, Any]):
        """Handle reminder scheduled event."""
        print(f"Handling reminder scheduled event: {event_data}")

    async def handle_reminder_sent(self, event_data: Dict[str, Any]):
        """Handle reminder sent event."""
        print(f"Handling reminder sent event: {event_data}")

        task_id = event_data.get('task_id')
        user_id = event_data.get('user_id')
        reminder_message = event_data.get('message', 'Task reminder')

        # Send notification to the user
        if user_id:
            await self.notification_service.send_task_reminder_notification(
                user_id=user_id,
                task_id=task_id,
                task_title=event_data.get('task_title', 'Untitled Task'),
                reminder_time=event_data.get('reminder_time', ''),
                delivery_method=event_data.get('delivery_method', 'email')
            )

    async def handle_event(self, event_type: str, event_data: Dict[str, Any]):
        """Route events to appropriate handlers."""
        handler_map = {
            'task_created': self.handle_task_created,
            'task_updated': self.handle_task_updated,
            'task_completed': self.handle_task_completed,
            'task_deleted': self.handle_task_deleted,
            'recurring_task_instance_created': self.handle_recurring_task_instance_created,
            'reminder_scheduled': self.handle_reminder_scheduled,
            'reminder_sent': self.handle_reminder_sent,
        }

        handler = handler_map.get(event_type)
        if handler:
            await handler(event_data)
        else:
            print(f"No handler found for event type: {event_type}")

    async def process_task_event(self, event_data: Dict[str, Any]):
        """Process a task event from the event-driven architecture."""
        event_type = event_data.get('event_type')
        if not event_type:
            print("No event type found in event data")
            return

        await self.handle_event(event_type, event_data)

        # Create a record of the event processing
        task_event = self.task_event_service.create_task_event(
            event_type=event_type,
            task_id=event_data.get('task_id', 0),
            event_data=event_data
        )

        return task_event