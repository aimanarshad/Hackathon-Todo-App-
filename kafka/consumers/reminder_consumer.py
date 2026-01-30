"""Kafka consumer for reminder events."""
import asyncio
import json
from typing import Dict, Any
from dapr.ext.grpc import App
from dapr.clients import DaprClient


class ReminderConsumer:
    """Consumer for handling reminder events from Kafka via Dapr pubsub."""

    def __init__(self):
        self.app = App()
        self.dapr_client = DaprClient()

    def setup_routes(self):
        """Set up Dapr pubsub routes for consuming reminder events."""
        # Subscribe to reminders topic specifically for reminder processing
        @self.app.subscribe(pubsub_name='pubsub', topic='reminders')
        async def handle_reminder_events(event_data: Dict[str, Any]):
            return await self.process_reminder_event(event_data)

    async def process_reminder_event(self, event_data: Dict[str, Any]):
        """Process events from the reminders topic."""
        try:
            event_type = event_data.get('event_type')
            reminder_id = event_data.get('reminder_id')
            task_id = event_data.get('task_id')
            user_id = event_data.get('user_id')

            print(f"Processing reminder event: {event_type} for reminder {reminder_id}, task {task_id}")

            if event_type == 'reminder_scheduled':
                await self.handle_reminder_scheduled(event_data)
            elif event_type == 'reminder_sent':
                await self.handle_reminder_sent(event_data)
            else:
                print(f"Unknown reminder event type: {event_type}")

            return {'status': 'SUCCESS'}

        except Exception as e:
            print(f"Error processing reminder event: {str(e)}")
            return {'status': 'RETRY'}

    async def handle_reminder_scheduled(self, event_data: Dict[str, Any]):
        """Handle reminder scheduled event."""
        scheduled_time = event_data.get('scheduled_time')
        print(f"Reminder scheduled for task {event_data.get('task_id')} at {scheduled_time}")

        # In a real implementation, you might register the reminder with a scheduler
        # or update the reminder status in the database

        # For now, just log the event
        pass

    async def handle_reminder_sent(self, event_data: Dict[str, Any]):
        """Handle reminder sent event."""
        print(f"Reminder sent for task {event_data.get('task_id')}")

        # In a real implementation, you might update the reminder status in the database
        # or trigger follow-up actions

        # For now, just log the event
        pass

    def start_server(self):
        """Start the Dapr gRPC server to listen for reminder events."""
        print("Starting Dapr reminder event consumer server...")
        self.setup_routes()
        # Note: This would typically run indefinitely
        # In practice, you'd run this as part of your application lifecycle
        pass


# Example usage
if __name__ == '__main__':
    consumer = ReminderConsumer()
    consumer.start_server()

    # Keep the server running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down reminder consumer...")