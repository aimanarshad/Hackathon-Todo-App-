---
id: 0002
title: ai-chatbot
stage: plan
date: 2026-01-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-ai-chatbot
branch: 001-ai-chatbot
user: hc
command: sp.plan
labels: ["ai","chatbot","architecture","plan","todo","gemini","langchain"]
links:
  spec: /home/hc/hackathon-todo/specs/001-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-ai-chatbot/plan.md
 - specs/001-ai-chatbot/research.md
 - specs/001-ai-chatbot/data-model.md
 - specs/001-ai-chatbot/quickstart.md
 - specs/001-ai-chatbot/contracts/chat-api.yaml
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Using constitution  and specify

Generate specs/phase3-plan.md.

IMPORTANT: Same folder/repo. Do NOT delete or modify any previous work.

Plan:
- Architecture: Existing Next.js frontend + FastAPI backend + Gemini agent + MCP tools.
- New backend structure:
  - conversation_models.py (SQLModel models)
  - mcp/tools.py (tool functions using existing CRUD or DB)
  - agents/gemini_agent.py (LangChain chain with Gemini and tool binding)
  - routers/chat.py (stateless chat endpoint)
- Integration: Reuse existing Task model and Neon DB.
- Frontend: Add /app/chat/page.tsx with chat UI calling /api/chat.
- Stateless design: all conversation state in DB.

Suggest subagents: Backend Specialist, AI Agent Specialist.

Output ONLY the Markdown for phase3-plan.md.
Start with # Phase 3 Plan: Architecture & Implementation Strategy

## Response snapshot

# Phase 3 Plan: Architecture & Implementation Strategy

**Branch**: `001-ai-chatbot` | **Date**: 2026-01-14 | **Spec**: /home/hc/hackathon-todo/specs/001-ai-chatbot/spec.md
**Input**: Feature specification from `/specs/001-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered todo chatbot that allows users to manage tasks using natural language. The system integrates Google Gemini with LangChain for function calling, leveraging existing FastAPI backend and Next.js frontend while maintaining all Phase 1 and 2 functionality. The architecture includes new conversation and message models for state management, MCP tools for task operations, and a stateless chat endpoint.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Next.js 14+, google-generativeai, langchain, langchain-google-genai, langchain-core
**Storage**: Neon Serverless PostgreSQL (reuse existing connection)
**Testing**: pytest (backend), Jest/RTL (frontend)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (full-stack)
**Performance Goals**: <3 second response time for 95% of requests, 90% accuracy in natural language interpretation
**Constraints**: Maintain backward compatibility with existing Phase 1 and 2 functionality, secure API key handling, stateless endpoint design
**Scale/Scope**: Single user conversations with conversation history persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Spec-Driven Development Only**: Plan follows spec-driven approach with Claude-generated implementation
- ✅ **Iterative Evolution**: Builds on existing Phase 1 and 2 foundation without breaking changes
- ✅ **Clean Architecture**: Clear separation between backend (data/business logic) and frontend (presentation)
- ✅ **Simplicity & Extensibility**: Minimal components with design for future phases (Kubernetes, advanced AI features)
- ✅ **User-Centric**: Focuses on intuitive natural language interaction
- ✅ **Monorepo Structure**: Maintains single repository with organized folder structure
- ✅ **Backward Compatibility**: Preserves all existing functionality from Phases 1 and 2
- ✅ **Phase 3 Specific Principles**: Implements conversational AI, Gemini integration, MCP tools, stateless design
- ✅ **Security**: API keys properly secured, no exposure to frontend
- ✅ **Data Persistence**: Conversation state stored reliably in database

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── agents/              # Gemini + LangChain agent logic
│   └── gemini_agent.py  # LangChain chain with Gemini and tool binding
├── mcp/                 # MCP tool functions
│   └── tools.py         # Tool functions using existing CRUD or DB
├── models/              # Existing models preserved
├── conversation_models.py # SQLModel models for Conversation and Message
├── routers/
│   ├── tasks.py         # Existing tasks router (preserved)
│   └── chat.py          # New chat endpoint router
└── main.py              # Existing FastAPI app (preserved)

frontend/
├── app/
│   ├── chat/            # New chat interface
│   │   └── page.tsx     # Chat UI calling /api/chat
│   └── tasks/           # Existing tasks interface (preserved)
└── components/          # Existing components (preserved)
```

**Structure Decision**: Web application structure selected with clear separation between backend API layer and frontend presentation layer. New AI components integrated into existing architecture without modifying existing functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional dependencies | AI functionality requires Gemini/LangChain integration | Existing architecture insufficient for natural language processing |
| New database models | Conversation state management required for chat functionality | Existing Task model alone cannot handle conversation context |
| MCP tools layer | Function calling architecture needed for safe AI interactions | Direct AI-to-database access would be less secure and harder to maintain |

## Additional Files Created

In addition to the plan.md file, the following supporting files were created as part of the planning process:

- **research.md**: Details on technology choices and architectural patterns
- **data-model.md**: Comprehensive data model definitions for new entities
- **quickstart.md**: Setup and configuration instructions
- **contracts/**: API contract definitions (chat-api.yaml)
- **Agent context updated**: Added new technologies to CLAUDE.md

## Subagents Suggested

- **Backend Specialist**: Focuses on FastAPI, SQLModel, and database integration
- **AI Agent Specialist**: Specializes in LangChain, Google Gemini integration, and tool calling

## Implementation Strategy

The plan follows a phased approach:
1. **Phase 0**: Research and technology selection (completed in research.md)
2. **Phase 1**: Data modeling and API contract design (completed in data-model.md and contracts/)
3. **Phase 2**: Task breakdown for implementation (to be created in tasks.md via /sp.tasks)

This approach ensures all constitutional requirements are met while providing a clear path for implementation.

## Outcome

- ✅ Impact: Comprehensive architecture plan created for AI-powered todo chatbot
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.yaml
- 🔁 Next prompts: Generate tasks with /sp.tasks for implementation
- 🧠 Reflection: Plan balances innovation with backward compatibility, following constitutional principles

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): Begin task breakdown for implementation
