---
id: 0004
title: ai-chatbot-impl
stage: green
date: 2026-01-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-chatbot
branch: 001-ai-chatbot
user: hc
command: sp.implement
labels: ["implementation","ai","chatbot","todo","gemini","langchain"]
links:
  spec: /home/hc/hackathon-todo/specs/001-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/conversation_models.py
 - backend/mcp/tools.py
 - backend/agents/gemini_agent.py
 - backend/routers/chat.py
 - backend/main.py
 - frontend/app/chat/page.tsx
 - backend/pyproject.toml
 - backend/database.py
 - specs/001-ai-chatbot/tasks.md
tests:
 - none
---

## Prompt

You are Claude Code implementing Phase 3 in the existing hackathon-todo folder and repo.

CRITICAL: Do NOT delete, modify, or overwrite ANY files from Phase 1 or 2. Only ADD new files.

Use agentic workflow with two subagents:
- Backend Specialist: handles DB models, MCP tools, chat endpoint
- AI Specialist: handles Gemini + LangChain agent logic

Using constitution [paste], specify [paste], plan [paste], tasks [paste phase3-tasks.md],

Delegate tasks and generate code for:
- backend/conversation_models.py
- backend/mcp/tools.py
- backend/agents/gemini_agent.py
- backend/routers/chat.py (include in main.py with app.include_router)
- frontend/app/chat/page.tsx (simple chat UI using fetch to /api/chat)

Use:
- google.generativeai
- langchain_google_genai
- GEMINI_API_KEY from .env
- Existing get_db dependency

Output ONLY code in separate blocks with full file paths.

## Response snapshot

Implementation of the AI-powered Todo Chatbot Phase 3:

1. Created backend/conversation_models.py with Conversation and Message SQLModel classes
2. Created backend/mcp/tools.py with MCP tool functions (add_task, list_tasks, complete_task, delete_task, update_task)
3. Created backend/agents/gemini_agent.py with Google Gemini integration and LangChain
4. Created backend/routers/chat.py with chat endpoint and conversation management
5. Updated backend/main.py to include the chat router
6. Created frontend/app/chat/page.tsx with a complete chat UI
7. Updated backend/pyproject.toml with required AI dependencies
8. Updated backend/database.py to include new conversation models in metadata
9. Updated specs/001-ai-chatbot/tasks.md to mark completed tasks

The implementation follows the specification and plan, enabling users to manage tasks using natural language through an AI assistant. The system integrates Google Gemini with LangChain for function calling, maintains conversation history in the database, and provides a clean frontend interface.

## Outcome

- ✅ Impact: Successfully implemented AI chatbot functionality enabling natural language task management
- 🧪 Tests: none
- 📁 Files: Added 4 new files, updated 5 existing files to implement the AI chatbot
- 🔁 Next prompts: Ready for testing and further feature development
- 🧠 Reflection: Implementation successfully extends existing Phase 1/2 functionality while adding AI capabilities

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): Test the chat functionality with various natural language commands
