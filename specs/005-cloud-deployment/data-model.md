# Data Model: Phase 5 Advanced Cloud Deployment

## Overview

This data model extends the existing Task model from Phase 2 with additional fields and patterns for recurring tasks and due date reminders, while maintaining backward compatibility.

## Extended Task Model

### Task (Extended from Phase 2)

```python
class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Phase 3 additions (AI Chatbot)
    user_id: Optional[int] = None

    # Phase 5 additions (Advanced Features)
    due_date: Optional[datetime] = None
    reminder_enabled: bool = False
    reminder_time: Optional[datetime] = None  # When the reminder should trigger
    recurrence_pattern: Optional[str] = None  # "daily", "weekly", "monthly", "custom"
    recurrence_interval: Optional[int] = 1    # How often to repeat (e.g., every 2 weeks)
    recurrence_end_date: Optional[datetime] = None  # When recurrence stops
    recurrence_parent_id: Optional[int] = None  # For recurring instances, points to original
    recurrence_next_instance: Optional[datetime] = None  # When next instance should be created
    is_recurring_template: bool = False  # Whether this task is a template for recurrence
    timezone: Optional[str] = "UTC"  # User's timezone for scheduling
```

## New Supporting Models

### RecurringTaskPattern

Represents the recurrence rules for recurring tasks.

```python
class RecurringTaskPattern(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")  # Points to the template task
    pattern_type: str  # "daily", "weekly", "monthly", "custom"
    interval: int = 1  # How often to repeat
    days_of_week: Optional[str] = None  # For weekly patterns (e.g., "mon,wed,fri")
    days_of_month: Optional[str] = None  # For monthly patterns (e.g., "1,15,30")
    occurrence_count: Optional[int] = None  # Max number of occurrences
    end_date: Optional[datetime] = None  # When recurrence ends
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Optional["Task"] = Relationship(back_populates="recurrence_pattern_obj")
```

### Reminder

Manages reminder scheduling and delivery status.

```python
class Reminder(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    scheduled_time: datetime  # When the reminder should fire
    sent_time: Optional[datetime] = None  # When it was actually sent
    delivery_status: str = "pending"  # "pending", "sent", "failed", "cancelled"
    delivery_attempts: int = 0
    last_delivery_attempt: Optional[datetime] = None
    reminder_type: str = "due_date"  # "due_date", "custom", "recurring"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Optional["Task"] = Relationship(back_populates="reminders")
```

### TaskEvent

Captures events related to tasks for the event-driven architecture.

```python
class TaskEvent(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    event_type: str  # "task_created", "task_updated", "task_completed", "task_deleted", "reminder_sent"
    task_id: int = Field(foreign_key="task.id")
    event_data: dict  # JSON payload with event details
    event_timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: Optional[str] = None  # For tracing related events
    causation_id: Optional[str] = None  # Which event caused this event
    processed_by: Optional[str] = None  # Which service processed this event
    processed_at: Optional[datetime] = None

    # Relationships
    task: Optional["Task"] = Relationship(back_populates="events")
```

## Kafka Topic Schemas

### task-events Topic
```json
{
  "event_type": "task_created|task_updated|task_completed|task_deleted|reminder_sent",
  "task_id": 123,
  "timestamp": "2023-12-01T10:00:00Z",
  "correlation_id": "uuid",
  "causation_id": "uuid",
  "payload": {
    "task_content": "Do something",
    "due_date": "2023-12-05T10:00:00Z",
    "user_id": 456
  }
}
```

### reminders Topic
```json
{
  "reminder_id": 789,
  "task_id": 123,
  "scheduled_time": "2023-12-01T09:00:00Z",
  "reminder_type": "due_date|recurring",
  "user_id": 456,
  "delivery_method": "email|push|notification"
}
```

### task-updates Topic
```json
{
  "task_id": 123,
  "action": "created|updated|completed|deleted",
  "timestamp": "2023-12-01T10:00:00Z",
  "changes": {
    "field": "value_before -> value_after"
  },
  "user_id": 456
}
```

## Dapr State Store Keys

The following keys will be used in the Dapr state store for managing application state:

- `recurrence_engine:last_processed:{timestamp}` - Track last time recurrence was processed
- `reminders_engine:last_processed:{timestamp}` - Track last time reminders were processed
- `task_stats:user_{user_id}:completed_today` - User's daily completion stats
- `health_check:dapr_components:status` - Health status of Dapr components

## Validation Rules

1. **Due Date Validation**: Due date must be in the future
2. **Recurrence Pattern Validation**: Recurrence patterns must be valid and have appropriate intervals
3. **Reminder Timing**: Reminder time must be before the due date
4. **Timezone Handling**: All timestamps stored in UTC with user timezone preference stored separately
5. **Task Relationships**: Recurring instances must reference valid templates
6. **Event Consistency**: Events must have proper causation/correlation chains

## State Transitions

### Task State Transitions
- `pending` → `completed` (when marked complete)
- `pending` → `deleted` (when deleted)
- `completed` → `pending` (when unmarked)

### Reminder State Transitions
- `pending` → `sent` (when successfully delivered)
- `pending` → `failed` (when delivery fails)
- `pending` → `cancelled` (when associated task is deleted/completed)

## Backward Compatibility

- All new fields are optional to maintain compatibility with existing data
- Existing API endpoints continue to function unchanged
- New functionality is additive only
- Old task records without new fields work seamlessly