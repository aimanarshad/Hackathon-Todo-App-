# Quickstart Guide: AI-Powered Todo Chatbot

## Prerequisites

- Python 3.13+ with pip/uv
- Node.js 18+ with npm/pnpm/yarn
- Access to Google Gemini API (GEMINI_API_KEY)
- PostgreSQL-compatible database (Neon DB recommended)
- Existing Phase 1 and 2 codebase intact

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy backend environment file
cp backend/.env.example backend/.env

# Add your Gemini API key
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### 2. Backend Dependencies
```bash
cd backend
uv venv  # or use python venv if uv not available
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install google-generativeai langchain langchain-google-genai langchain-core
# Other existing dependencies remain unchanged
```

### 3. Frontend Dependencies
```bash
cd frontend
npm install  # or pnpm install / yarn install
```

### 4. Database Setup
```bash
# Run existing migrations to set up base models
cd backend
python -m alembic upgrade head
```

## New Component Installation

### 1. Backend Components
```bash
# Create required directories
mkdir -p backend/agents backend/mcp

# Create new files as specified in architecture
touch backend/conversation_models.py
touch backend/agents/gemini_agent.py
touch backend/mcp/tools.py
touch backend/routers/chat.py
```

### 2. Frontend Components
```bash
# Create chat interface directory
mkdir -p frontend/app/chat

# Create chat page
touch frontend/app/chat/page.tsx
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat`
- **Request Body**:
  ```json
  {
    "message": "string",
    "conversation_id": "integer (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "response": "string",
    "conversation_id": "integer",
    "tool_calls": "array (optional)"
  }
  ```

## Configuration

### 1. Backend Configuration
- Configure GEMINI_API_KEY in backend/.env
- Verify database connection settings
- Ensure existing task endpoints remain accessible

### 2. Frontend Configuration
- Update API URL configuration if needed
- Verify chat page routing works correctly

## Running the Application

### 1. Start Backend
```bash
cd backend
uvicorn main:app --reload
```

### 2. Start Frontend
```bash
cd frontend
npm run dev  # or pnpm dev / yarn dev
```

### 3. Access Chat Interface
- Navigate to http://localhost:3000/chat
- Start conversing with the AI assistant
- All existing functionality remains accessible at previous URLs

## Verification Steps

1. **Test Existing Functionality**: Verify Phase 1 and 2 features still work
2. **Test Chat Interface**: Send a message and verify AI response
3. **Test Task Operations**: Use natural language to add/list/complete tasks
4. **Test Conversation Persistence**: Refresh page and verify conversation history remains
5. **Test Error Handling**: Try invalid requests and verify graceful handling

## Troubleshooting

### Common Issues
- **API Key Missing**: Ensure GEMINI_API_KEY is set in backend/.env
- **Database Connection**: Verify DATABASE_URL is properly configured
- **Missing Dependencies**: Run dependency installation commands again
- **Port Conflicts**: Check if ports 8000 (backend) and 3000 (frontend) are available

### Verification Commands
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend accessibility
curl http://localhost:3000/api/health

# Verify new chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```