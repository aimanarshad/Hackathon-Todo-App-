# Task T013: Create API router for tasks in backend/routers/tasks.py with all required endpoints
# Task T020: Implement GET /tasks endpoint in backend with basic listing functionality
# Task T021: Implement POST /tasks endpoint in backend for task creation
# Task T022: Implement GET /tasks/{id} endpoint in backend for retrieving single task
# Task T023: Implement PUT /tasks/{id} endpoint in backend for task updates
# Task T024: Implement DELETE /tasks/{id} endpoint in backend for task deletion
# Task T025: Implement PATCH /tasks/{id}/complete endpoint in backend for toggling completion
# Task T042: Update API endpoints to handle priority and tags properly
# Task T047: Update GET /tasks endpoint to support filtering by completion status
# Task T048: Update GET /tasks endpoint to support filtering by priority
# Task T049: Update GET /tasks endpoint to support search by keyword
# Task T050: Update GET /tasks endpoint to support sorting by various criteria
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Optional, List
from database import get_session
from models import Task, TaskUpdate
import schemas
import crud
from database import create_db_and_tables
import logging

router = APIRouter()

@router.on_event("startup")
def on_startup():
    create_db_and_tables()

@router.get("/", response_model=List[schemas.TaskResponse])
def list_tasks(
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, description="Filter by priority level"),
    search: Optional[str] = Query(None, description="Search keyword for title/description"),
    sort: Optional[str] = Query(None, description="Sort by field (created_at, priority, title)")
):
    """Get all tasks with optional filtering and sorting"""
    # Task T047: Update GET /tasks endpoint to support filtering by completion status
    # Task T048: Update GET /tasks endpoint to support filtering by priority
    # Task T049: Update GET /tasks endpoint to support search by keyword
    # Task T050: Update GET /tasks endpoint to support sorting by various criteria
    tasks = crud.get_tasks(
        session=session,
        completed=completed,
        priority=priority,
        search=search,
        sort=sort
    )
    return tasks

@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, session: Session = Depends(get_session)):
    """Create a new task"""
    # Task T032: Add server-side validation for task title in backend
    if not task.title or task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Task title cannot be empty")

    # Task T043: Add validation for priority values (high, medium, low) in backend
    if task.priority and task.priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Priority must be one of: high, medium, low")

    # Task T044: Add validation for tags format (comma-separated) in backend
    if task.tags and not isinstance(task.tags, str):
        raise HTTPException(status_code=400, detail="Tags must be a string")

    db_task = Task.from_orm(task) if hasattr(Task, 'from_orm') else Task.model_validate(task)
    db_task = crud.create_task(session, db_task)
    return db_task


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID"""
    task = crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, session: Session = Depends(get_session)):
    """Update a specific task by ID"""
    # Task T043: Add validation for priority values (high, medium, low) in backend
    if task_update.priority and task_update.priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Priority must be one of: high, medium, low")

    # Task T044: Add validation for tags format (comma-separated) in backend
    if task_update.tags and not isinstance(task_update.tags, str):
        raise HTTPException(status_code=400, detail="Tags must be a string")

    updated_task = crud.update_task(session, task_id, TaskUpdate.model_validate(task_update))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a specific task by ID"""
    success = crud.delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.patch("/{task_id}/complete", response_model=schemas.TaskResponse)
def toggle_task_completion(task_id: int, session: Session = Depends(get_session)):
    """Toggle completion status of a specific task"""
    task = crud.toggle_task_completion(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task















