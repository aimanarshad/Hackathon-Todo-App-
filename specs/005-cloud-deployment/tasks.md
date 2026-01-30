---
description: "Task list for Phase 5 Advanced Cloud Deployment implementation"
---

# Tasks: Phase 5 Advanced Cloud Deployment

**Input**: Design documents from `/specs/005-cloud-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure for Phase 5 per implementation plan
- [ ] T002 [P] Set up Dapr configuration files in dapr/config.yaml and dapr/components/
- [ ] T003 [P] Create Kafka configuration files in kafka/topics/ and kafka/consumers/
- [ ] T004 Create Dockerfiles for backend and frontend in docker/
- [ ] T005 Update Helm charts in charts/todo-app/ with Dapr sidecar configurations

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Extend existing Task model with Phase 5 fields in backend/models.py
- [x] T007 Create RecurringTaskPattern model in backend/src/models/recurring_task_pattern.py
- [x] T008 Create Reminder model in backend/src/models/reminder.py
- [x] T009 Create TaskEvent model in backend/src/models/task_event.py
- [x] T010 [P] Set up Dapr pubsub component for Kafka in dapr/components/pubsub.yaml
- [x] T011 [P] Set up Dapr statestore component for PostgreSQL in dapr/components/statestore.yaml
- [x] T012 [P] Set up Dapr secretstore component in dapr/components/secretstore.yaml
- [x] T013 [P] Set up Dapr jobs component configuration in dapr/components/jobs.yaml
- [x] T014 Update database migration scripts to include new model fields in backend/migrations/add_phase5_fields.py
- [x] T015 Configure Kafka topics for task-events, reminders, and task-updates in kafka/topics/
- [x] T016 Set up Dapr services integration in backend/src/dapr/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Recurring Tasks Management (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks that automatically repeat on a daily or weekly schedule, allowing them to set up routine activities without manually recreating them each time they're due.

**Independent Test**: Can be fully tested by creating a recurring task with daily/weekly frequency and verifying it appears in the task list on scheduled days, delivering predictable routine task automation.

### Implementation for User Story 1

- [x] T017 [P] [US1] Create RecurrenceEngine service in backend/src/tasks/recurrence_engine.py
- [x] T018 [P] [US1] Create RecurringTaskService in backend/src/services/recurring_task_service.py
- [x] T019 [US1] Add recurring task API endpoints to backend/src/api/v1/recurring_tasks.py
- [x] T020 [US1] Implement recurring task validation logic in backend/src/services/validation.py
- [x] T021 [US1] Create recurring task scheduler in backend/src/tasks/scheduler.py
- [x] T022 [US1] Update existing TaskService to handle recurring instances in backend/src/services/task_service.py
- [x] T023 [US1] Add recurring task endpoints to FastAPI app in backend/main.py
- [x] T024 [US1] Create frontend components for recurring task creation in frontend/src/components/RecurringTaskForm.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Due Date Reminders (Priority: P1)

**Goal**: Users can set due dates for tasks and receive timely reminders through an automated notification system, helping them stay organized and meet deadlines effectively.

**Independent Test**: Can be fully tested by setting due dates on tasks and verifying that reminder notifications are delivered at the specified times, delivering proactive deadline awareness.

### Implementation for User Story 2

- [x] T025 [P] [US2] Create ReminderService in backend/src/services/reminder_service.py
- [x] T026 [P] [US2] Create ReminderEngine for scheduling in backend/src/tasks/reminder_engine.py
- [x] T027 [US2] Add reminder API endpoints to backend/src/api/v1/reminders.py
- [x] T028 [US2] Create Kafka producer for reminder events in backend/src/dapr/task_event_producer.py
- [x] T029 [US2] Create Kafka consumer for reminder processing in kafka/consumers/task_update_consumer.py
- [x] T030 [US2] Implement notification delivery mechanism in backend/src/services/notification_service.py
- [x] T031 [US2] Add reminder endpoints to FastAPI app in backend/main.py
- [x] T032 [US2] Create frontend components for reminder management in frontend/src/components/ReminderSettings.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Event-Driven Task Updates (Priority: P2)

**Goal**: The system processes task-related events asynchronously through an event-driven architecture, enabling scalable and reliable updates that can trigger multiple downstream actions without blocking user operations.

**Independent Test**: Can be fully tested by performing task operations and verifying that events are published to Kafka topics and consumed by interested services, delivering decoupled and scalable processing.

### Implementation for User Story 3

- [x] T033 [P] [US3] Create TaskEventService in backend/src/services/task_event_service.py
- [x] T034 [P] [US3] Create Kafka producer for task events in backend/src/dapr/task_event_producer.py
- [x] T035 [US3] Create Kafka consumer for task updates in kafka/consumers/task_update_consumer.py
- [x] T036 [US3] Implement event publishing logic in existing task operations in backend/src/services/task_service.py
- [x] T037 [US3] Add event subscription capabilities to backend services in backend/src/services/event_subscription.py
- [x] T038 [US3] Create event processing handlers in backend/src/handlers/event_handlers.py
- [x] T039 [US3] Add server-sent events endpoint for real-time updates in backend/src/api/v1/events.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Cloud-Based Task Management (Priority: P1)

**Goal**: Users can access their tasks seamlessly through a cloud-deployed application that provides high availability, scalability, and resilience compared to local deployments.

**Independent Test**: Can be fully tested by accessing the application through cloud endpoints and verifying all functionality works identically to local deployment, delivering production-ready availability.

### Implementation for User Story 4

- [x] T040 [P] [US4] Update Helm charts for Dapr integration in charts/todo-app/templates/
- [x] T041 [P] [US4] Create Oracle OKE deployment scripts in scripts/deploy-oke.sh
- [x] T042 [US4] Create GitHub Actions workflow for CI/CD in .github/workflows/deploy-oke.yml
- [x] T043 [US4] Add monitoring manifests for Prometheus in monitoring/prometheus/prometheus.yml
- [x] T044 [US4] Create Grafana dashboard for application metrics in monitoring/grafana/dashboards/todo-app.json
- [x] T045 [US4] Update Dockerfiles for production deployment in docker/
- [x] T046 [US4] Configure health checks and readiness probes in Helm charts
- [x] T047 [US4] Set up kubectl-ai commands for cloud deployment in scripts/kubectl-ai-commands.sh

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T048 [P] Update documentation in docs/README.md for Phase 5 features
- [x] T049 Update quickstart guide in specs/005-cloud-deployment/quickstart.md with new features
- [ ] T050 Add integration tests for all new features in backend/tests/integration/
- [x] T051 [P] Update frontend to support new recurring tasks and reminder UI in frontend/src/pages/
- [ ] T052 Security hardening for new API endpoints in backend/src/middleware/
- [ ] T053 Performance optimization for event processing in backend/src/tasks/
- [x] T054 Run quickstart validation to ensure all features work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - Integrates with all previous stories

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create RecurrenceEngine service in backend/src/tasks/recurrence_engine.py"
Task: "Create RecurringTaskService in backend/src/services/recurring_task_service.py"

# Launch frontend and API together:
Task: "Add recurring task API endpoints to backend/src/api/v1/recurring_tasks.py"
Task: "Create frontend components for recurring task creation in frontend/src/components/RecurringTaskForm.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Recurring Tasks)
   - Developer B: User Story 2 (Reminders)
   - Developer C: User Story 3 (Event-driven)
   - Developer D: User Story 4 (Cloud Deployment)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence