# Spec: Basic Todo Features for Console App

## Overview
Build a console-based Todo app in Python that manages tasks in memory. Provide a menu-driven interface for all operations.

## Feature 1: Add Task
- Prompt user for title and description.
- Generate unique ID (incremental integer).
- Store task as dict: {'id': int, 'title': str, 'description': str, 'completed': False}.
- Add to global tasks list.
- Print confirmation.

## Feature 2: Delete Task
- List all tasks with IDs.
- Prompt for ID to delete.
- Remove if found; else error message.

## Feature 3: Update Task
- List all tasks.
- Prompt for ID.
- Prompt for new title and/or description (allow skipping).
- Update if found; else error.

## Feature 4: View Task List
- Display all tasks in a formatted table (ID, Title, Description, Status: Completed/Incomplete).
- If empty, show message.

## Feature 5: Mark as Complete
- List all tasks.
- Prompt for ID.
- Toggle completed status.
- Print updated status.

## Main Loop
- Menu options: 1. Add, 2. Delete, 3. Update, 4. View, 5. Mark Complete, 6. Exit.
- Run in loop until exit.
- Handle invalid inputs gracefully.