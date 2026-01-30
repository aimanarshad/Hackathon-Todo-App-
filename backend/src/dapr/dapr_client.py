"""Dapr client wrapper for interacting with Dapr sidecar."""
import json
from typing import Dict, Any, Optional
from dapr.clients import DaprClient as DaprSidecarClient


class DaprClient:
    """Wrapper for Dapr client to provide simplified event publishing."""

    def __init__(self):
        self.client = DaprSidecarClient()

    async def publish_event(self, topic_name: str, event_data: Dict[str, Any]) -> bool:
        """Publish an event to a Dapr pubsub topic."""
        try:
            # Add metadata for correlation
            event_data["timestamp"] = self._get_current_timestamp()
            event_data["correlation_id"] = self._generate_correlation_id()

            # Publish to Dapr pubsub
            with self.client as c:
                c.publish_event(
                    pubsub_name="pubsub",  # This should match the Dapr component name
                    topic_name=topic_name,
                    data=json.dumps(event_data),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing event to {topic_name}: {str(e)}")
            return False

    async def save_state(self, store_name: str, key: str, value: Any) -> bool:
        """Save state to Dapr state store."""
        try:
            with self.client as c:
                c.save_state(store_name, key, json.dumps(value))
            return True
        except Exception as e:
            print(f"Error saving state to {store_name} with key {key}: {str(e)}")
            return False

    async def get_state(self, store_name: str, key: str) -> Optional[Any]:
        """Get state from Dapr state store."""
        try:
            with self.client as c:
                response = c.get_state(store_name, key)
                if response.data:
                    return json.loads(response.data.decode('utf-8'))
            return None
        except Exception as e:
            print(f"Error getting state from {store_name} with key {key}: {str(e)}")
            return None

    async def delete_state(self, store_name: str, key: str) -> bool:
        """Delete state from Dapr state store."""
        try:
            with self.client as c:
                c.delete_state(store_name, key)
            return True
        except Exception as e:
            print(f"Error deleting state from {store_name} with key {key}: {str(e)}")
            return False

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def _generate_correlation_id(self) -> str:
        """Generate a correlation ID for tracking events."""
        import uuid
        return str(uuid.uuid4())

    def close(self):
        """Close the Dapr client connection."""
        self.client.close()