# Data Model: Phase 2 Full-Stack Todo Web App

## Task Entity

**Fields**:
- `id`: Integer, Primary Key, Auto-generated
- `title`: String (required), Task title/description
- `description`: String (optional), Detailed task description
- `completed`: Boolean, Default False, Completion status
- `priority`: String (optional), Values: "high", "medium", "low"
- `tags`: String (optional), Comma-separated tags
- `created_at`: DateTime, Auto-generated, Timestamp of creation
- `updated_at`: DateTime, Auto-generated, Timestamp of last update
- `user_id`: Integer (optional), For future multi-user support

**Validation Rules**:
- `title` must not be empty
- `priority` must be one of "high", "medium", "low" if provided
- `tags` must be comma-separated if provided
- `created_at` and `updated_at` automatically managed

**Relationships**:
- No relationships in Phase 2 (will add user relationship in Phase 3)

## State Transitions

**Task Completion**:
- `completed: false` → `completed: true` (when marked complete)
- `completed: true` → `completed: false` (when marked incomplete)

**Task Updates**:
- Any field except `id` and `created_at` can be updated
- `updated_at` automatically updated on any change

## API Contract

**GET /tasks** - Retrieve all tasks with optional filters
- Query parameters: `completed`, `priority`, `search`, `sort`
- Response: Array of Task objects

**POST /tasks** - Create a new task
- Request body: Task object (without id, created_at, updated_at)
- Response: Created Task object

**GET /tasks/{id}** - Retrieve a specific task
- Path parameter: task id
- Response: Task object

**PUT /tasks/{id}** - Update a specific task
- Path parameter: task id
- Request body: Task object
- Response: Updated Task object

**DELETE /tasks/{id}** - Delete a specific task
- Path parameter: task id
- Response: Empty

**PATCH /tasks/{id}/complete** - Toggle task completion status
- Path parameter: task id
- Response: Updated Task object