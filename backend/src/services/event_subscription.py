"""Event subscription capabilities for backend services."""
from typing import Callable, Dict, List, Any
from backend.src.handlers.event_handlers import EventHandler
from backend.src.services.task_event_service import TaskEventService
from backend.src.services.reminder_service import ReminderService
from backend.src.services.notification_service import NotificationService


class EventSubscriptionManager:
    """Manages event subscriptions and routing in the backend services."""

    def __init__(
        self,
        task_event_service: TaskEventService,
        reminder_service: ReminderService,
        notification_service: NotificationService
    ):
        self.task_event_service = task_event_service
        self.reminder_service = reminder_service
        self.notification_service = notification_service
        self.event_handler = EventHandler(
            task_event_service,
            reminder_service,
            notification_service
        )

        # Event subscription mapping
        self.subscriptions: Dict[str, List[Callable]] = {}

    def subscribe_to_event(self, event_type: str, handler: Callable):
        """Subscribe a handler to a specific event type."""
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []

        self.subscriptions[event_type].append(handler)

    def unsubscribe_from_event(self, event_type: str, handler: Callable):
        """Unsubscribe a handler from a specific event type."""
        if event_type in self.subscriptions and handler in self.subscriptions[event_type]:
            self.subscriptions[event_type].remove(handler)

    async def emit_event(self, event_type: str, event_data: Dict[str, Any]):
        """Emit an event to all subscribed handlers."""
        if event_type in self.subscriptions:
            for handler in self.subscriptions[event_type]:
                try:
                    await handler(event_data)
                except Exception as e:
                    print(f"Error in event handler for {event_type}: {str(e)}")

    async def process_incoming_event(self, event_type: str, event_data: Dict[str, Any]):
        """Process an incoming event through the event handler and emit to subscribers."""
        # First process with the main event handler
        await self.event_handler.handle_event(event_type, event_data)

        # Then emit to any subscribers
        await self.emit_event(event_type, event_data)

    def setup_default_subscriptions(self):
        """Set up default event subscriptions for common event types."""
        # Task created events
        self.subscribe_to_event('task_created', self.on_task_created)
        self.subscribe_to_event('task_updated', self.on_task_updated)
        self.subscribe_to_event('task_completed', self.on_task_completed)
        self.subscribe_to_event('task_deleted', self.on_task_deleted)
        self.subscribe_to_event('recurring_task_instance_created', self.on_recurring_task_instance_created)
        self.subscribe_to_event('reminder_scheduled', self.on_reminder_scheduled)
        self.subscribe_to_event('reminder_sent', self.on_reminder_sent)

    async def on_task_created(self, event_data: Dict[str, Any]):
        """Handle task created event."""
        print(f"Event subscription: Task created - {event_data.get('task_id')}")

        # Example: Create a notification for the user
        user_id = event_data.get('user_id')
        if user_id:
            await self.notification_service.send_in_app_notification(
                user_id=user_id,
                title="New Task Created",
                message=f"A new task '{event_data.get('title', 'Untitled')}' has been created.",
                notification_type="info"
            )

    async def on_task_updated(self, event_data: Dict[str, Any]):
        """Handle task updated event."""
        print(f"Event subscription: Task updated - {event_data.get('task_id')}")

        # Example: Check if reminder settings changed
        changes = event_data.get('changes', {})
        if 'reminder_enabled' in changes or 'due_date' in changes:
            # Handle reminder updates
            pass

    async def on_task_completed(self, event_data: Dict[str, Any]):
        """Handle task completed event."""
        print(f"Event subscription: Task completed - {event_data.get('task_id')}")

        # Example: Send completion notification
        user_id = event_data.get('user_id')
        if user_id:
            await self.notification_service.send_in_app_notification(
                user_id=user_id,
                title="Task Completed",
                message=f"The task '{event_data.get('title', 'Untitled')}' has been completed!",
                notification_type="success"
            )

    async def on_task_deleted(self, event_data: Dict[str, Any]):
        """Handle task deleted event."""
        print(f"Event subscription: Task deleted - {event_data.get('task_id')}")

        # Example: Cancel any related reminders
        task_id = event_data.get('task_id')
        await self.reminder_service.cancel_task_reminder(task_id)

    async def on_recurring_task_instance_created(self, event_data: Dict[str, Any]):
        """Handle recurring task instance created event."""
        print(f"Event subscription: Recurring task instance created - {event_data.get('task_id')}")

        # Example: Send notification about new recurring instance
        user_id = event_data.get('user_id')
        if user_id:
            await self.notification_service.send_in_app_notification(
                user_id=user_id,
                title="Recurring Task Instance Created",
                message=f"A new instance of your recurring task has been created.",
                notification_type="info"
            )

    async def on_reminder_scheduled(self, event_data: Dict[str, Any]):
        """Handle reminder scheduled event."""
        print(f"Event subscription: Reminder scheduled - {event_data.get('reminder_id')}")

    async def on_reminder_sent(self, event_data: Dict[str, Any]):
        """Handle reminder sent event."""
        print(f"Event subscription: Reminder sent - {event_data.get('reminder_id')}")

        # Example: Update task status or send additional notifications
        pass

    def get_subscribed_events(self) -> List[str]:
        """Get list of all event types with subscriptions."""
        return list(self.subscriptions.keys())

    def get_subscription_count(self, event_type: str) -> int:
        """Get the number of subscriptions for a specific event type."""
        return len(self.subscriptions.get(event_type, []))


# Global event subscription manager instance
_event_subscription_manager: EventSubscriptionManager = None


def get_event_subscription_manager() -> EventSubscriptionManager:
    """Get the global event subscription manager instance."""
    global _event_subscription_manager
    return _event_subscription_manager


def initialize_event_subscription_manager(
    task_event_service: TaskEventService,
    reminder_service: ReminderService,
    notification_service: NotificationService
) -> EventSubscriptionManager:
    """Initialize the global event subscription manager instance."""
    global _event_subscription_manager
    _event_subscription_manager = EventSubscriptionManager(
        task_event_service,
        reminder_service,
        notification_service
    )
    _event_subscription_manager.setup_default_subscriptions()
    return _event_subscription_manager