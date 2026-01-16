from typing import Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_session
from models import Task  # Assuming existing Task model from Phase 2
from conversation_models import Conversation, Message
from fastapi import Depends


def get_db():
    """Wrapper for getting database session for tools"""
    for session in get_session():
        yield session


class AddTaskInput(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[str] = None


class AddTaskTool(BaseTool):
    name: str = "add_task"
    description: str = "Add a new task"
    args_schema: type = AddTaskInput

    def _run(self, title: str, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[str] = None):
        db: Session = next(get_db())
        try:
            task = Task(
                title=title,
                description=description,
                completed=False,
                priority=priority,
                tags=tags
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            return f"Task '{task.title}' added successfully with ID {task.id}"
        except Exception as e:
            db.rollback()
            return f"Error adding task: {str(e)}"
        finally:
            db.close()

    def _arun(self, title: str, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[str] = None):
        raise NotImplementedError("Async not implemented")


class ListTasksInput(BaseModel):
    completed: Optional[bool] = None
    priority: Optional[str] = None


class ListTasksTool(BaseTool):
    name: str = "list_tasks"
    description: str = "List all tasks or filter by completion status or priority"
    args_schema: type = ListTasksInput

    def _run(self, completed: Optional[bool] = None, priority: Optional[str] = None):
        db: Session = next(get_db())
        try:
            query = db.query(Task)

            if completed is not None:
                query = query.filter(Task.completed == completed)
            if priority is not None:
                query = query.filter(Task.priority == priority)

            tasks = query.all()

            if not tasks:
                return "No tasks found."

            task_list = []
            for task in tasks:
                status = "completed" if task.completed else "pending"
                task_info = f"- ID: {task.id}, Title: {task.title}, Status: {status}"
                if task.priority:
                    task_info += f", Priority: {task.priority}"
                if task.description:
                    task_info += f", Description: {task.description}"
                task_list.append(task_info)

            return "\n".join(task_list)
        except Exception as e:
            return f"Error listing tasks: {str(e)}"
        finally:
            db.close()

    def _arun(self, completed: Optional[bool] = None, priority: Optional[str] = None):
        raise NotImplementedError("Async not implemented")


class CompleteTaskInput(BaseModel):
    task_id: int


class CompleteTaskTool(BaseTool):
    name: str = "complete_task"
    description: str = "Mark a task as completed by ID"
    args_schema: type = CompleteTaskInput

    def _run(self, task_id: int):
        db: Session = next(get_db())
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return f"Task with ID {task_id} not found."

            if task.completed:
                return f"Task '{task.title}' is already completed."

            task.completed = True
            db.commit()
            db.refresh(task)
            return f"Task '{task.title}' marked as completed."
        except Exception as e:
            db.rollback()
            return f"Error completing task: {str(e)}"
        finally:
            db.close()

    def _arun(self, task_id: int):
        raise NotImplementedError("Async not implemented")


class DeleteTaskInput(BaseModel):
    task_id: int


class DeleteTaskTool(BaseTool):
    name: str = "delete_task"
    description: str = "Delete a task by ID"
    args_schema: type = DeleteTaskInput

    def _run(self, task_id: int):
        db: Session = next(get_db())
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return f"Task with ID {task_id} not found."

            title = task.title
            db.delete(task)
            db.commit()
            return f"Task '{title}' deleted successfully."
        except Exception as e:
            db.rollback()
            return f"Error deleting task: {str(e)}"
        finally:
            db.close()

    def _arun(self, task_id: int):
        raise NotImplementedError("Async not implemented")


class UpdateTaskInput(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None


class UpdateTaskTool(BaseTool):
    name: str = "update_task"
    description: str = "Update a task by ID with any combination of fields"
    args_schema: type = UpdateTaskInput

    def _run(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
             completed: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[str] = None):
        db: Session = next(get_db())
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                return f"Task with ID {task_id} not found."

            updates = []
            if title is not None:
                task.title = title
                updates.append(f"title to '{title}'")
            if description is not None:
                task.description = description
                updates.append(f"description to '{description}'")
            if completed is not None:
                task.completed = completed
                updates.append(f"completion status to {completed}")
            if priority is not None:
                task.priority = priority
                updates.append(f"priority to '{priority}'")
            if tags is not None:
                task.tags = tags
                updates.append(f"tags to '{tags}'")

            if not updates:
                return "No updates provided."

            db.commit()
            db.refresh(task)
            return f"Task '{task.title}' updated: {', '.join(updates)}."
        except Exception as e:
            db.rollback()
            return f"Error updating task: {str(e)}"
        finally:
            db.close()

    def _arun(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
              completed: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[str] = None):
        raise NotImplementedError("Async not implemented")


# Initialize all tools
def get_all_tools():
    return [
        AddTaskTool(),
        ListTasksTool(),
        CompleteTaskTool(),
        DeleteTaskTool(),
        UpdateTaskTool()
    ]