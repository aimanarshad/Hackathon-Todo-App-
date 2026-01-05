# Todo In-Memory Python Console App

A command-line todo application that stores tasks in memory with no persistence.

## Features

1. **Add Task**: Prompt for title (required) and description (optional), generate unique ID, store in memory, print confirmation.
2. **Delete Task**: List tasks, prompt for ID, remove if found, else error.
3. **Update Task**: List tasks, prompt for ID, allow updating title and/or description (skip if empty), print updated.
4. **View Task List**: Display formatted table (ID, Title, Description, Status: Completed/Incomplete), or message if empty.
5. **Mark as Complete**: List tasks, prompt for ID, toggle completion, print new status.

## Usage

Run the application with Python 3.13+:

```bash
python main.py
```

The application provides a menu-driven interface with the following options:
- 1. Add Task
- 2. Delete Task
- 3. Update Task
- 4. View Task List
- 5. Mark as Complete
- 6. Exit

## Data Model

Each task is stored as a dictionary with the following structure:
```python
{
    'id': int,           # Unique identifier for the task
    'title': str,        # Required title of the task
    'description': str,  # Optional description of the task (can be empty string)
    'completed': bool    # Boolean indicating completion status
}
```

## Architecture

- Single-file application in `main.py`
- In-memory storage using a global list
- Modular functions for each feature
- Menu-driven interface with error handling# Hackathon-Todo-App-
