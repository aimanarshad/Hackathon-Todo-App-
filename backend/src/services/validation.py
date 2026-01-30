"""Validation functions for recurring tasks and reminders."""
from datetime import datetime
from typing import Optional
from pydantic import ValidationError
from backend.models import Task


def validate_recurrence_pattern(pattern_type: str) -> bool:
    """Validate recurrence pattern type."""
    valid_patterns = {"daily", "weekly", "monthly", "custom"}
    return pattern_type.lower() in valid_patterns


def validate_recurrence_interval(interval: int) -> bool:
    """Validate recurrence interval is positive."""
    return isinstance(interval, int) and interval > 0


def validate_due_date(due_date: Optional[datetime]) -> bool:
    """Validate due date is in the future."""
    if due_date is None:
        return True
    return due_date > datetime.utcnow()


def validate_reminder_time(reminder_time: Optional[datetime], due_date: Optional[datetime]) -> bool:
    """Validate reminder time is before due date."""
    if reminder_time is None:
        return True
    if due_date is None:
        return True
    return reminder_time < due_date


def validate_timezone(timezone: str) -> bool:
    """Validate timezone string."""
    import zoneinfo
    try:
        zoneinfo.ZoneInfo(timezone)
        return True
    except Exception:
        return False


def validate_recurring_task_fields(
    content: str,
    pattern_type: str,
    interval: int,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    due_date: Optional[datetime],
    reminder_time: Optional[datetime],
    timezone: str
) -> dict:
    """Validate all fields for a recurring task."""
    errors = []

    # Validate content
    if not content or len(content.strip()) == 0:
        errors.append("Content is required")

    # Validate pattern type
    if not validate_recurrence_pattern(pattern_type):
        errors.append(f"Invalid recurrence pattern. Must be one of: daily, weekly, monthly, custom")

    # Validate interval
    if not validate_recurrence_interval(interval):
        errors.append("Recurrence interval must be a positive integer")

    # Validate dates
    if start_date and start_date < datetime.utcnow():
        errors.append("Start date must be in the future")

    if end_date and start_date and end_date < start_date:
        errors.append("End date must be after start date")

    if not validate_due_date(due_date):
        errors.append("Due date must be in the future")

    if not validate_reminder_time(reminder_time, due_date):
        errors.append("Reminder time must be before due date")

    # Validate timezone
    if not validate_timezone(timezone):
        errors.append(f"Invalid timezone: {timezone}")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def validate_reminder_fields(
    task_id: int,
    scheduled_time: datetime,
    reminder_type: str
) -> dict:
    """Validate fields for a reminder."""
    errors = []

    # Validate task ID
    if not isinstance(task_id, int) or task_id <= 0:
        errors.append("Task ID must be a positive integer")

    # Validate scheduled time
    if scheduled_time < datetime.utcnow():
        errors.append("Scheduled time must be in the future")

    # Validate reminder type
    valid_types = {"due_date", "custom", "recurring"}
    if reminder_type not in valid_types:
        errors.append(f"Invalid reminder type. Must be one of: {', '.join(valid_types)}")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def validate_task_update_fields(task_update_data: dict) -> dict:
    """Validate fields in a task update request."""
    errors = []

    # Validate recurrence fields if present
    if "recurrence_pattern" in task_update_data:
        pattern = task_update_data["recurrence_pattern"]
        if pattern and not validate_recurrence_pattern(pattern):
            errors.append(f"Invalid recurrence pattern: {pattern}")

    if "recurrence_interval" in task_update_data:
        interval = task_update_data["recurrence_interval"]
        if interval and not validate_recurrence_interval(interval):
            errors.append("Recurrence interval must be a positive integer")

    if "due_date" in task_update_data:
        due_date = task_update_data["due_date"]
        if due_date and not validate_due_date(due_date):
            errors.append("Due date must be in the future")

    if "reminder_time" in task_update_data and "due_date" in task_update_data:
        reminder_time = task_update_data["reminder_time"]
        due_date = task_update_data["due_date"]
        if reminder_time and due_date and not validate_reminder_time(reminder_time, due_date):
            errors.append("Reminder time must be before due date")

    if "timezone" in task_update_data:
        timezone = task_update_data["timezone"]
        if timezone and not validate_timezone(timezone):
            errors.append(f"Invalid timezone: {timezone}")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def validate_task_creation(task_data: dict) -> dict:
    """Validate fields for creating a new task."""
    errors = []

    # Validate required fields
    if "title" not in task_data or not task_data["title"]:
        errors.append("Title is required")

    # Validate optional fields
    if "recurrence_pattern" in task_data and task_data["recurrence_pattern"]:
        pattern = task_data["recurrence_pattern"]
        if not validate_recurrence_pattern(pattern):
            errors.append(f"Invalid recurrence pattern: {pattern}")

    if "recurrence_interval" in task_data and task_data["recurrence_interval"]:
        interval = task_data["recurrence_interval"]
        if not validate_recurrence_interval(interval):
            errors.append("Recurrence interval must be a positive integer")

    if "due_date" in task_data and task_data["due_date"]:
        due_date_str = task_data["due_date"]
        try:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            if not validate_due_date(due_date):
                errors.append("Due date must be in the future")
        except ValueError:
            errors.append("Invalid date format for due_date")

    if "timezone" in task_data and task_data["timezone"]:
        timezone = task_data["timezone"]
        if not validate_timezone(timezone):
            errors.append(f"Invalid timezone: {timezone}")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }