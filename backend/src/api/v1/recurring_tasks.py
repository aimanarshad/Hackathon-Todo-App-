"""API endpoints for recurring tasks."""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlmodel import Session
from backend.models import Task, TaskUpdate
from backend.src.database import get_session
from backend.src.services.recurring_task_service import RecurringTaskService
from backend.src.tasks.recurrence_engine import RecurrenceEngine
from backend.src.dapr.dapr_client import DaprClient
from backend.src.dapr.task_event_producer import TaskEventProducer


router = APIRouter(prefix="/recurring", tags=["recurring-tasks"])


def get_recurring_task_service(session: Session = Depends(get_session)):
    """Get recurring task service with dependencies."""
    dapr_client = DaprClient()
    recurrence_engine = RecurrenceEngine(session, None, dapr_client)  # We'll mock the task service for now
    event_producer = TaskEventProducer(dapr_client.client)

    # Create a minimal task service mock for the recurrence engine
    class MockTaskService:
        pass

    recurrence_engine.task_service = MockTaskService()
    return RecurringTaskService(session, recurrence_engine)


@router.post("/", response_model=Task)
async def create_recurring_task(
    task_data: dict,
    recurring_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """Create a new recurring task template."""
    try:
        content = task_data.get("content", "")
        user_id = task_data.get("user_id")
        pattern_type = task_data.get("recurrence_pattern", "daily")
        interval = task_data.get("recurrence_interval", 1)
        start_date_str = task_data.get("start_date")
        end_date_str = task_data.get("recurrence_end_date")
        due_date_str = task_data.get("due_date")
        reminder_enabled = task_data.get("reminder_enabled", False)
        reminder_time_str = task_data.get("reminder_time")
        timezone = task_data.get("timezone", "UTC")

        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None
        due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
        reminder_time = datetime.fromisoformat(reminder_time_str) if reminder_time_str else None

        task = recurring_service.create_recurring_task(
            content=content,
            user_id=user_id,
            pattern_type=pattern_type,
            interval=interval,
            start_date=start_date,
            end_date=end_date,
            due_date=due_date,
            reminder_enabled=reminder_enabled,
            reminder_time=reminder_time,
            timezone=timezone
        )

        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=dict)
async def get_recurring_task(
    task_id: int,
    recurring_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """Get details of a recurring task template."""
    task = recurring_service.get_recurring_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Recurring task not found")

    # Get instances of this recurring task
    instances = recurring_service.get_recurring_task_instances(task_id)

    return {
        "id": task.id,
        "content": task.title,
        "completed": task.completed,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
        "due_date": task.due_date,
        "recurrence_pattern": task.recurrence_pattern,
        "recurrence_interval": task.recurrence_interval,
        "recurrence_end_date": task.recurrence_end_date,
        "recurrence_next_instance": task.recurrence_next_instance,
        "is_recurring_template": task.is_recurring_template,
        "reminder_enabled": task.reminder_enabled,
        "reminder_time": task.reminder_time,
        "timezone": task.timezone,
        "instances": [
            {
                "id": instance.id,
                "content": instance.title,
                "original_task_id": instance.recurrence_parent_id,
                "instance_date": instance.created_at,
                "completed": instance.completed
            } for instance in instances
        ]
    }


@router.put("/{task_id}", response_model=Task)
async def update_recurring_task(
    task_id: int,
    task_update: TaskUpdate,
    recurring_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """Update a recurring task template."""
    # Convert TaskUpdate fields to parameters for the service
    updated_task = recurring_service.update_recurring_task(
        task_id=task_id,
        content=task_update.title,
        pattern_type=task_update.recurrence_pattern,
        interval=task_update.recurrence_interval,
        end_date=task_update.recurrence_end_date,
        due_date=task_update.due_date,
        reminder_enabled=task_update.reminder_enabled,
        reminder_time=task_update.reminder_time
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Recurring task not found")

    return updated_task


@router.delete("/{task_id}")
async def delete_recurring_task(
    task_id: int,
    recurring_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """Delete a recurring task template (stops future instances from being created)."""
    success = recurring_service.delete_recurring_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recurring task not found")

    return {"message": "Recurring task deleted successfully"}


@router.get("/user/{user_id}", response_model=List[Task])
async def get_recurring_tasks_for_user(
    user_id: int,
    recurring_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """Get all recurring task templates for a specific user."""
    return recurring_service.get_recurring_tasks_for_user(user_id)


@router.get("/upcoming/{user_id}", response_model=List[Task])
async def get_upcoming_recurring_tasks(
    user_id: int,
    recurring_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """Get recurring tasks that have upcoming instances."""
    return recurring_service.get_upcoming_recurring_tasks(user_id)


@router.post("/process")
async def process_recurring_tasks(
    recurring_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """Process recurring tasks and create new instances as needed."""
    await recurring_service.process_recurring_tasks()
    return {"message": "Recurring tasks processed successfully"}