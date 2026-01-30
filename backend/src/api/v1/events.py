"""API endpoints for server-sent events."""
import asyncio
from typing import AsyncGenerator
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/events", tags=["events"])


# Store for client connections (in production, you'd use Redis or similar)
clients = set()


@router.get("/task-stream", response_class=StreamingResponse)
async def task_stream(request: Request):
    """Server-sent events endpoint for real-time task updates."""

    async def event_generator():
        # Register client
        client_id = id(request)
        clients.add(client_id)

        try:
            # Send initial connection event
            yield f"data: {\"event\": \"connection_established\", \"message\": \"Connected to task stream\"}\n\n"

            # Simulate sending events
            counter = 0
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break

                # Simulate task events
                task_events = [
                    {"event_type": "task_created", "task_id": counter, "timestamp": "2024-01-01T10:00:00Z", "user_id": 1},
                    {"event_type": "task_updated", "task_id": counter-1, "timestamp": "2024-01-01T10:05:00Z", "user_id": 1, "changes": {"completed": True}},
                ]

                for event in task_events:
                    if await request.is_disconnected():
                        break

                    yield f"data: {str(event).replace('\'', '\"')}\n\n"
                    await asyncio.sleep(5)  # Send event every 5 seconds

                counter += 1

        except Exception as e:
            print(f"Error in event generator: {str(e)}")
        finally:
            # Unregister client
            if client_id in clients:
                clients.remove(client_id)

    return StreamingResponse(event_generator(), media_type="text/plain")


@router.get("/health")
async def events_health():
    """Health check for events endpoint."""
    return {
        "status": "healthy",
        "active_connections": len(clients)
    }


@router.get("/broadcast-test")
async def broadcast_test():
    """Test endpoint to simulate broadcasting an event."""
    # This would normally broadcast to all connected clients
    # For now, just return a test response
    return {
        "message": "Broadcast test initiated",
        "active_connections": len(clients),
        "timestamp": "2024-01-01T10:00:00Z"
    }