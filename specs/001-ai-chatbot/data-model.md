# Data Model: AI-Powered Todo Chatbot

## Entity Definitions

### Conversation
- **Purpose**: Represents a single conversation thread between user and AI assistant
- **Fields**:
  - `id`: Integer (primary key, auto-generated)
  - `user_id`: Integer (foreign key to user, or dummy for now)
  - `title`: String (summary of conversation, nullable)
  - `created_at`: DateTime (timestamp when conversation started)
  - `updated_at`: DateTime (timestamp when conversation last updated)
- **Relationships**:
  - One-to-many with Message (one conversation has many messages)
- **Validation**:
  - `user_id` must exist in users table (or be a valid dummy value)
  - `created_at` is set automatically on creation
  - `updated_at` is updated automatically on any changes

### Message
- **Purpose**: Represents an individual message within a conversation
- **Fields**:
  - `id`: Integer (primary key, auto-generated)
  - `conversation_id`: Integer (foreign key to Conversation)
  - `role`: String (either "user" or "assistant")
  - `content`: Text (the actual message content)
  - `timestamp`: DateTime (when message was created)
  - `metadata`: JSON (optional metadata for AI interactions, nullable)
- **Relationships**:
  - Many-to-one with Conversation (many messages belong to one conversation)
- **Validation**:
  - `conversation_id` must reference an existing conversation
  - `role` must be either "user" or "assistant"
  - `content` cannot be empty
  - `timestamp` is set automatically on creation

### Task (Existing from Phase 2)
- **Purpose**: Represents user tasks (existing entity, unchanged)
- **Fields**:
  - `id`: Integer (primary key, auto-generated)
  - `title`: String (required)
  - `description`: String (optional)
  - `completed`: Boolean (default False)
  - `priority`: String/Enum ("high", "medium", "low", null)
  - `tags`: Array/String (e.g., "work", "personal")
  - `created_at`, `updated_at`: DateTime (timestamps)
  - `user_id`: Integer (nullable now, required later for multi-user)

## State Transitions

### Conversation Lifecycle
- **Created**: When user starts new conversation
- **Active**: When messages are exchanged
- **Updated**: When new messages are added
- **Inactive**: When conversation is dormant (handled by cleanup process)

### Message Lifecycle
- **Created**: When user sends message or AI responds
- **Persisted**: Saved to database with timestamp
- **Retrieved**: Loaded as part of conversation history
- **Referenced**: Used for context in AI interactions

## Relationship Constraints

### Conversation-Messages
- Messages cannot exist without a conversation
- Deleting a conversation removes all associated messages
- Foreign key constraint ensures data integrity
- Cascade delete from conversation to messages

### Message-Task Interactions
- Messages reference tasks by ID when discussing specific tasks
- AI tools may create/update tasks referenced in messages
- No direct foreign key relationship between Message and Task
- Loose coupling allows flexibility in AI interactions