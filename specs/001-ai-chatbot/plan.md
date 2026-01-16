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
