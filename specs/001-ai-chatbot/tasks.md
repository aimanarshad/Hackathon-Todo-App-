# Phase 3 Tasks: Atomic Breakdown

**Feature**: AI-Powered Todo Chatbot
**Branch**: 001-ai-chatbot
**Input**: `/specs/001-ai-chatbot/plan.md`, `/specs/001-ai-chatbot/spec.md`, `/specs/001-ai-chatbot/data-model.md`

## Phase 1: Setup Tasks

- [x] T001 Create required backend directories: backend/agents, backend/mcp
- [x] T002 Install new dependencies: google-generativeai, langchain, langchain-google-genai, langchain-core
- [x] T003 Create frontend chat directory: frontend/app/chat

## Phase 2: Foundational Tasks

- [x] T004 [P] Create Conversation and Message models in backend/conversation_models.py
- [x] T005 [P] Create MCP tools module in backend/mcp/tools.py with add_task function
- [x] T006 [P] Create MCP tools with list_tasks function in backend/mcp/tools.py
- [x] T007 [P] Create MCP tools with complete_task function in backend/mcp/tools.py
- [x] T008 [P] Create MCP tools with delete_task function in backend/mcp/tools.py
- [x] T009 [P] Create MCP tools with update_task function in backend/mcp/tools.py
- [x] T010 Update database migration to include conversation models

## Phase 3: User Story 1 - Natural Language Task Management (P1)

- [x] T011 [P] [US1] Create Gemini agent module in backend/agents/gemini_agent.py
- [x] T012 [P] [US1] Bind MCP tools to Gemini agent for function calling
- [x] T013 [US1] Create chat router in backend/routers/chat.py
- [x] T014 [US1] Implement POST /api/chat endpoint with conversation history
- [x] T015 [US1] Add conversation state management to chat endpoint
- [x] T016 [US1] Create frontend chat page in frontend/app/chat/page.tsx
- [x] T017 [US1] Implement chat UI with message display and input
- [x] T018 [US1] Connect frontend to backend chat API
- [x] T019 [US1] Test basic task operations via natural language

## Phase 4: User Story 2 - Persistent Conversation Context (P2)

- [ ] T020 [P] [US2] Enhance conversation model with title generation
- [ ] T021 [US2] Implement conversation context retrieval in agent
- [ ] T022 [US2] Add message history tracking in conversation flow
- [ ] T023 [US2] Implement context-aware task identification
- [ ] T024 [US2] Test conversation continuity across multiple exchanges
- [ ] T025 [US2] Add conversation context to frontend display

## Phase 5: User Story 3 - Friendly and Helpful Interaction (P3)

- [ ] T026 [P] [US3] Enhance agent response formatting with friendly messages
- [ ] T027 [US3] Implement ambiguity resolution in agent
- [ ] T028 [US3] Add error handling with helpful feedback
- [ ] T029 [US3] Create action confirmation responses
- [ ] T030 [US3] Test user experience with friendly interactions

## Phase 6: Testing & Quality Assurance

- [ ] T031 [P] Create backend unit tests for conversation models
- [ ] T032 [P] Create backend unit tests for MCP tools
- [ ] T033 Create integration tests for chat endpoint
- [ ] T034 Create frontend component tests for chat UI
- [ ] T035 Run end-to-end tests for all 5 basic task operations
- [ ] T036 Verify 90% accuracy in natural language interpretation
- [ ] T037 Test response time is under 3 seconds for 95% of requests

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T038 Add error handling and logging to chat endpoint
- [ ] T039 Update README with chatbot usage instructions
- [ ] T040 Add environment variable validation for GEMINI_API_KEY
- [ ] T041 Optimize conversation history loading for performance
- [ ] T042 Ensure all Phase 1 and 2 functionality remains intact
- [ ] T043 Document the new API endpoints in OpenAPI format

## Dependencies

- **User Story 2** depends on: **User Story 1** (requires basic chat functionality)
- **User Story 3** depends on: **User Story 1** (requires basic response mechanism)

## Parallel Execution Opportunities

- **T004-T009**: Model and tool creation can run in parallel
- **T011-T012**: Agent creation and tool binding can run in parallel with UI work
- **T016-T017**: Frontend implementation can run in parallel with backend API
- **T031-T032**: Backend tests can run in parallel with frontend tests

## Implementation Strategy

**MVP Scope**: Complete User Story 1 (Natural Language Task Management) which provides core functionality allowing users to manage tasks via natural language.

**Incremental Delivery**:
1. Setup foundational models and tools (Tasks T001-T010)
2. Implement basic chat functionality (Tasks T011-T019) - MVP
3. Add conversation context (Tasks T020-T025)
4. Enhance user experience (Tasks T026-T030)
5. Add testing and polish (Tasks T031-T043)