"""API endpoints for task reminders."""
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from backend.models import Task
from backend.src.database import get_session
from backend.src.services.reminder_service import ReminderService
from backend.src.dapr.task_event_producer import TaskEventProducer


router = APIRouter(prefix="/reminders", tags=["reminders"])


def get_reminder_service(session: Session = Depends(get_session)):
    """Get reminder service with dependencies."""
    # Create a mock event producer for now
    class MockEventProducer:
        async def publish_reminder_scheduled(self, **kwargs):
            return True

        async def publish_reminder_sent(self, **kwargs):
            return True

    event_producer = MockEventProducer()
    return ReminderService(session, event_producer)


@router.post("/", response_model=dict)
async def create_reminder(
    reminder_data: dict,
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Schedule a reminder for a task."""
    try:
        task_id = reminder_data.get("task_id")
        scheduled_time_str = reminder_data.get("scheduled_time")
        reminder_type = reminder_data.get("reminder_type", "due_date")
        user_id = reminder_data.get("user_id")

        if not task_id:
            raise HTTPException(status_code=400, detail="Task ID is required")
        if not scheduled_time_str:
            raise HTTPException(status_code=400, detail="Scheduled time is required")

        scheduled_time = datetime.fromisoformat(scheduled_time_str.replace('Z', '+00:00'))

        reminder = reminder_service.create_reminder(
            task_id=task_id,
            scheduled_time=scheduled_time,
            reminder_type=reminder_type,
            user_id=user_id
        )

        return {
            "id": reminder.id,
            "task_id": reminder.task_id,
            "scheduled_time": reminder.scheduled_time,
            "delivery_status": reminder.delivery_status,
            "reminder_type": reminder.reminder_type,
            "created_at": reminder.created_at,
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{reminder_id}", response_model=dict)
async def get_reminder(
    reminder_id: int,
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Get details of a specific reminder."""
    reminder = reminder_service.get_reminder_by_id(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    return {
        "id": reminder.id,
        "task_id": reminder.task_id,
        "scheduled_time": reminder.scheduled_time,
        "sent_time": reminder.sent_time,
        "delivery_status": reminder.delivery_status,
        "delivery_attempts": reminder.delivery_attempts,
        "last_delivery_attempt": reminder.last_delivery_attempt,
        "reminder_type": reminder.reminder_type,
        "created_at": reminder.created_at,
        "updated_at": reminder.updated_at
    }


@router.get("/task/{task_id}", response_model=List[dict])
async def get_reminders_for_task(
    task_id: int,
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Get all reminders for a specific task."""
    reminders = reminder_service.get_reminders_by_task_id(task_id)

    return [
        {
            "id": r.id,
            "task_id": r.task_id,
            "scheduled_time": r.scheduled_time,
            "sent_time": r.sent_time,
            "delivery_status": r.delivery_status,
            "delivery_attempts": r.delivery_attempts,
            "last_delivery_attempt": r.last_delivery_attempt,
            "reminder_type": r.reminder_type,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        } for r in reminders
    ]


@router.get("/upcoming", response_model=List[dict])
async def get_upcoming_reminders(
    limit: int = 100,
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Get upcoming reminders."""
    reminders = reminder_service.get_upcoming_reminders(limit=limit)

    return [
        {
            "id": r.id,
            "task_id": r.task_id,
            "scheduled_time": r.scheduled_time,
            "delivery_status": r.delivery_status,
            "reminder_type": r.reminder_type,
            "created_at": r.created_at
        } for r in reminders
    ]


@router.get("/user/{user_id}", response_model=List[dict])
async def get_reminders_for_user(
    user_id: int,
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Get all reminders for a specific user."""
    reminders = reminder_service.get_reminders_by_user(user_id)

    return [
        {
            "id": r.id,
            "task_id": r.task_id,
            "scheduled_time": r.scheduled_time,
            "delivery_status": r.delivery_status,
            "reminder_type": r.reminder_type,
            "created_at": r.created_at
        } for r in reminders
    ]


@router.put("/{reminder_id}/cancel")
async def cancel_reminder(
    reminder_id: int,
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Cancel a scheduled reminder."""
    success = reminder_service.cancel_reminder(reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder not found")

    return {"message": "Reminder cancelled successfully"}


@router.get("/process", response_model=dict)
async def process_upcoming_reminders(
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Process all upcoming reminders that should be sent now."""
    processed_count = reminder_service.process_upcoming_reminders()
    return {"processed_count": processed_count}


@router.post("/task/{task_id}/due-date")
async def create_due_date_reminder(
    task_id: int,
    reminder_data: dict,
    session: Session = Depends(get_session),
    reminder_service: ReminderService = Depends(get_reminder_service)
):
    """Create a reminder for a task's due date."""
    # Get the task to check if it has a due date
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if not task.due_date:
        raise HTTPException(status_code=400, detail="Task has no due date")

    # Create a reminder based on the due date
    reminder = reminder_service.create_reminder(
        task_id=task_id,
        scheduled_time=task.due_date,
        reminder_type="due_date",
        user_id=task.user_id
    )

    return {
        "id": reminder.id,
        "task_id": reminder.task_id,
        "scheduled_time": reminder.scheduled_time,
        "delivery_status": reminder.delivery_status
    }