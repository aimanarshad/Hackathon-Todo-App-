---
id: 1
title: Implement Todo App
stage: tasks
date_iso: 2026-01-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-app
branch: 001-todo-app
user: user
command: sp.implement
labels:
  - implementation
  - python
  - todo-app

links:
  spec: specs/001-todo-app/spec.md
  plan: specs/001-todo-app/plan.md
  tasks: specs/001-todo-app/tasks.md
  ticket: null
  adr: null
  pr: null

files_yaml:
  - main.py

tests_yaml:
  - functional testing
  - menu navigation
  - task operations

outcome: Complete implementation of Todo In-Memory Python Console App with all 5 features
evaluation: Application implements all required features and meets specification requirements
---

# Prompt

You are Claude Code, implementing the Hackathon II Phase 1: Todo In-Memory Python Console App. Follow the Spec-Kit Plus workflow. Using the project tasks (paste the content of tasks.md here), plan (paste plan.md), specification (paste specify.md), and constitution (paste constitution.md), generate the Python code for the entire app. Implement only what the tasks authorize. Reference Task IDs in code comments.

Project Details:
- Output complete code for src/main.py.
- Use Python 3.13+ features if beneficial.
- Include comments linking to tasks, e.g., # [Task]: T-001 [From]: speckit.specify §1.
- Structure: Modular functions, main loop, in-memory list.
- Test mentally for correctness; handle edges like empty list, invalid IDs.

Output only the Python code, wrapped in ```python ... ```.

# Response

Implemented the complete Todo In-Memory Python Console App with all required functionality:

- Global in-memory task list storage
- 5 core features: Add, Delete, Update, View, Mark Complete
- Menu-driven interface with numbered options (1-6)
- Task data model with id, title, description, completed fields
- Comprehensive error handling for invalid inputs
- Formatted table display for tasks
- Unique ID generation for tasks
- Input validation for required fields
- Proper exit functionality

The implementation follows all tasks from the task breakdown and includes task ID references in comments. The application is fully functional and meets all requirements from the specification.