"""Kafka producer for task events using Dapr pubsub."""
import json
from typing import Dict, Any
from dapr.clients import DaprClient as DaprSidecarClient


class TaskEventProducer:
    """Producer for publishing task-related events to Kafka via Dapr pubsub."""

    def __init__(self, dapr_client: DaprSidecarClient):
        self.dapr_client = dapr_client

    async def publish_task_created(self, task_id: int, user_id: int, content: str, due_date=None):
        """Publish a task created event."""
        event_data = {
            "event_type": "task_created",
            "task_id": task_id,
            "user_id": user_id,
            "content": content,
            "due_date": due_date.isoformat() if due_date else None,
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("task-events", event_data)

    async def publish_task_updated(self, task_id: int, user_id: int, changes: Dict[str, Any]):
        """Publish a task updated event."""
        event_data = {
            "event_type": "task_updated",
            "task_id": task_id,
            "user_id": user_id,
            "changes": changes,
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("task-events", event_data)

    async def publish_task_completed(self, task_id: int, user_id: int):
        """Publish a task completed event."""
        event_data = {
            "event_type": "task_completed",
            "task_id": task_id,
            "user_id": user_id,
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("task-events", event_data)

    async def publish_task_deleted(self, task_id: int, user_id: int):
        """Publish a task deleted event."""
        event_data = {
            "event_type": "task_deleted",
            "task_id": task_id,
            "user_id": user_id,
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("task-events", event_data)

    async def publish_recurring_task_instance_created(self, task_id: int, template_task_id: int, user_id: int):
        """Publish a recurring task instance created event."""
        event_data = {
            "event_type": "recurring_task_instance_created",
            "task_id": task_id,
            "template_task_id": template_task_id,
            "user_id": user_id,
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("task-events", event_data)

    async def publish_reminder_scheduled(self, reminder_id: int, task_id: int, scheduled_time, user_id: int):
        """Publish a reminder scheduled event."""
        event_data = {
            "event_type": "reminder_scheduled",
            "reminder_id": reminder_id,
            "task_id": task_id,
            "scheduled_time": scheduled_time.isoformat() if scheduled_time else None,
            "user_id": user_id,
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("reminders", event_data)

    async def publish_reminder_sent(self, reminder_id: int, task_id: int, sent_time, user_id: int):
        """Publish a reminder sent event."""
        event_data = {
            "event_type": "reminder_sent",
            "reminder_id": reminder_id,
            "task_id": task_id,
            "sent_time": sent_time.isoformat() if sent_time else None,
            "user_id": user_id,
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("reminders", event_data)

    async def publish_task_update_notification(self, task_id: int, action: str, user_id: int, changes: Dict[str, Any] = None):
        """Publish a task update notification to the task-updates topic."""
        event_data = {
            "event_type": "task_update_notification",
            "task_id": task_id,
            "action": action,
            "user_id": user_id,
            "changes": changes or {},
            "timestamp": self._get_current_timestamp()
        }

        return await self._publish_event("task-updates", event_data)

    async def _publish_event(self, topic_name: str, event_data: Dict[str, Any]) -> bool:
        """Internal method to publish an event to the specified topic."""
        try:
            # Add correlation and causation IDs
            event_data["correlation_id"] = self._generate_correlation_id()

            # Publish to Dapr pubsub
            self.dapr_client.publish_event(
                pubsub_name="pubsub",  # This should match the Dapr component name
                topic_name=topic_name,
                data=json.dumps(event_data),
                data_content_type='application/json'
            )

            return True
        except Exception as e:
            print(f"Error publishing event to {topic_name}: {str(e)}")
            return False

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def _generate_correlation_id(self) -> str:
        """Generate a correlation ID for tracking events."""
        import uuid
        return str(uuid.uuid4())