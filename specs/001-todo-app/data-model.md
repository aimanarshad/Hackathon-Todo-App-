# Data Model: Todo In-Memory Python Console App

## Task Entity

### Structure
```python
{
    'id': int,           # Unique identifier for the task
    'title': str,        # Required title of the task
    'description': str,  # Optional description of the task (can be empty string)
    'completed': bool    # Boolean indicating completion status
}
```

### Fields
- **id**: Integer, unique across all tasks, auto-generated as incremental value
- **title**: String, required field, cannot be empty
- **description**: String, optional field, defaults to empty string if not provided
- **completed**: Boolean, indicates whether task is completed (True) or incomplete (False), defaults to False

### Validation Rules
- ID must be unique within the task list
- Title must not be empty or None
- ID must be a positive integer
- Completed field must be boolean

### State Transitions
- New task: `completed = False` (default)
- Mark complete: `completed = True`
- Mark incomplete: `completed = False`

## Task List

### Structure
- Collection type: List of Task entities
- Storage: In-memory only (Python list)
- Access: By ID for operations (search through list)
- Persistence: None (lost when application exits)

### Operations
- Add: Append new Task to list
- Read: Find Task by ID in list
- Update: Find Task by ID and modify fields
- Delete: Remove Task by ID from list
- List: Return all Tasks in list