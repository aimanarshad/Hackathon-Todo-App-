# OpenAPI Contract: Phase 2 Full-Stack Todo Web App

## Task API Specification

### GET /tasks
**Description**: Retrieve all tasks with optional filtering and sorting

**Parameters**:
- `completed` (boolean, optional): Filter by completion status
- `priority` (string, optional): Filter by priority level (high, medium, low)
- `search` (string, optional): Search keyword for title/description
- `sort` (string, optional): Sort by field (created_at, priority, title)

**Response**:
- 200: Array of Task objects
```json
[
  {
    "id": 1,
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "tags": "work,personal",
    "created_at": "2026-01-06T14:30:00Z",
    "updated_at": "2026-01-06T14:30:00Z",
    "user_id": null
  }
]
```

### POST /tasks
**Description**: Create a new task

**Request Body**:
```json
{
  "title": "New task",
  "description": "Task description",
  "priority": "medium",
  "tags": "work,personal"
}
```

**Response**:
- 201: Created Task object
```json
{
  "id": 1,
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "priority": "medium",
  "tags": "work,personal",
  "created_at": "2026-01-06T14:30:00Z",
  "updated_at": "2026-01-06T14:30:00Z",
  "user_id": null
}
```

### GET /tasks/{id}
**Description**: Retrieve a specific task by ID

**Path Parameters**:
- `id` (integer): Task ID

**Response**:
- 200: Task object
- 404: Task not found

### PUT /tasks/{id}
**Description**: Update a specific task by ID

**Path Parameters**:
- `id` (integer): Task ID

**Request Body**:
```json
{
  "title": "Updated task",
  "description": "Updated description",
  "completed": true,
  "priority": "high",
  "tags": "work,urgent"
}
```

**Response**:
- 200: Updated Task object
- 404: Task not found

### DELETE /tasks/{id}
**Description**: Delete a specific task by ID

**Path Parameters**:
- `id` (integer): Task ID

**Response**:
- 204: No content (success)
- 404: Task not found

### PATCH /tasks/{id}/complete
**Description**: Toggle completion status of a specific task

**Path Parameters**:
- `id` (integer): Task ID

**Response**:
- 200: Updated Task object
- 404: Task not found