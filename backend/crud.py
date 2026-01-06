# Task T012: Create CRUD operations in backend/crud.py for Task entity
# Task T037: Update CRUD operations to handle priority and tags in backend/crud.py
from sqlmodel import Session, select
from models import Task, TaskUpdate
from typing import Optional, List
import logging

def create_task(session: Session, task: Task) -> Task:
    """Create a new task"""
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_task(session: Session, task_id: int) -> Optional[Task]:
    """Get a task by ID"""
    return session.get(Task, task_id)

def get_tasks(
    session: Session,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None
) -> List[Task]:
    """Get all tasks with optional filters"""
    query = select(Task)

    # Apply filters
    if completed is not None:
        query = query.where(Task.completed == completed)
    if priority is not None:
        query = query.where(Task.priority == priority)
    if search is not None:
        query = query.where(
            (Task.title.contains(search)) | (Task.description.contains(search))
        )

    # Apply sorting
    if sort == "priority":
        query = query.order_by(Task.priority.desc())
    elif sort == "title":
        query = query.order_by(Task.title.asc())
    elif sort == "created_at":
        query = query.order_by(Task.created_at.desc())
    else:
        # Default sorting by creation date, newest first
        query = query.order_by(Task.created_at.desc())

    return session.exec(query).all()

def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Update a task"""
    db_task = session.get(Task, task_id)
    if not db_task:
        return None

    # Update fields that are provided
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    from datetime import datetime
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: int) -> bool:
    """Delete a task"""
    task = session.get(Task, task_id)
    if not task:
        return False

    session.delete(task)
    session.commit()
    return True

def toggle_task_completion(session: Session, task_id: int) -> Optional[Task]:
    """Toggle task completion status"""
    task = session.get(Task, task_id)
    if not task:
        return None

    task.completed = not task.completed
    from datetime import datetime
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task