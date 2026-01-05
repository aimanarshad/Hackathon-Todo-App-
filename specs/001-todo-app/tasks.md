# Project Tasks (BREAKDOWN): Todo In-Memory Python Console App

## Phase 1: Setup and Project Structure

### Goal
Initialize the project with proper structure, configuration files, and basic setup following the single-file approach with main.py.

### Tasks

- [x] T001 Create main.py file with proper Python shebang and imports
- [ ] T002 Create pyproject.toml with project metadata and Python 3.13+ requirement
- [ ] T003 Create README.md with project description and usage instructions
- [x] T004 Initialize global tasks list variable in main.py
- [x] T005 Create basic main() function with simple print statement to verify setup

## Phase 2: Foundational Components

### Goal
Establish the foundational data model and helper functions that will be used across all user stories.

### Tasks

- [x] T006 Implement Task data model as dictionary with id, title, description, completed fields
- [x] T007 Create function to generate unique incremental IDs for tasks
- [x] T008 Implement helper function to find task by ID in the task list
- [x] T009 Create helper function to validate task title (non-empty requirement)
- [x] T010 Implement helper function to format and display task lists in table format
- [x] T011 Create helper function to handle user input validation and error handling

## Phase 3: [US1] Add New Tasks (Priority: P1)

### Goal
Implement the core functionality to add new tasks with required title and optional description, assign unique IDs, store in memory, and confirm addition.

### Independent Test Criteria
Can be fully tested by running the application, selecting the add task option, providing a title and description, and verifying that the task appears in the list with a unique ID and uncompleted status.

### Acceptance Scenarios
1. When user selects "Add Task" and provides a title with optional description, system assigns unique ID, stores task in memory, and displays confirmation message.
2. When user provides only a title (no description), system creates task with empty description field and assigns unique ID.
3. When user tries to add a task without a title, system prompts to provide required title.

### Tasks

- [x] T012 [US1] Implement add_task() function with title and description input prompts
- [x] T013 [US1] Add validation to ensure title is provided in add_task() function
- [x] T014 [US1] Implement unique ID generation for new tasks
- [x] T015 [US1] Add new task to global task list with completed=False by default
- [x] T016 [US1] Display confirmation message with assigned ID after successful task addition
- [x] T017 [US1] Add error handling for empty title in add_task() function

## Phase 4: [US2] View and Manage Tasks (Priority: P1)

### Goal
Implement functionality to display tasks in a clear, organized format with ID, Title, Description, and Completion Status.

### Independent Test Criteria
Can be fully tested by adding tasks and then selecting the "View Task List" option to see them displayed in a readable table format.

### Acceptance Scenarios
1. When user selects "View Task List", system displays a formatted table with columns for ID, Title, Description, and Status (Completed/Incomplete).
2. When user has no tasks in list and selects "View Task List", system displays a message indicating that the list is empty.

### Tasks

- [x] T018 [US2] Implement view_tasks() function to display all tasks
- [x] T019 [US2] Create formatted table display for tasks with ID, Title, Description, Status columns
- [x] T020 [US2] Add logic to show "Completed" or "Incomplete" based on task completion status
- [x] T021 [US2] Implement empty list message when no tasks exist
- [x] T022 [US2] Add proper formatting and alignment for the task table display

## Phase 5: [US5] Navigate Menu Interface (Priority: P1)

### Goal
Implement the primary menu-driven interface with numbered options that allows users to navigate between different todo operations.

### Independent Test Criteria
Can be fully tested by using the menu system to navigate between all available options (1-6 including Exit) and verifying that invalid inputs are handled gracefully.

### Acceptance Scenarios
1. When user selects a valid menu option (1-6), system performs the corresponding action.
2. When user enters an invalid menu option, system displays an error message and prompts again.

### Tasks

- [x] T023 [US5] Implement display_menu() function to show numbered options (1-6)
- [x] T024 [US5] Create main menu loop that continuously displays options until exit
- [x] T025 [US5] Implement option selection handling for menu choices (1-6)
- [x] T026 [US5] Add proper exit functionality for option 6
- [x] T027 [US5] Implement error handling for invalid menu inputs
- [x] T028 [US5] Integrate add_task and view_tasks functions with menu options

## Phase 6: [US4] Delete Tasks (Priority: P2)

### Goal
Implement functionality to remove specific tasks by ID from the in-memory task list.

### Independent Test Criteria
Can be fully tested by adding tasks and then selecting the "Delete Task" option to remove specific tasks by ID.

### Acceptance Scenarios
1. When user selects "Delete Task" and provides a valid task ID, system removes the task from memory and confirms the deletion.
2. When user provides an invalid task ID, system displays an error message indicating the task was not found.

### Tasks

- [x] T029 [US4] Implement delete_task() function with task ID prompt
- [x] T030 [US4] Add task lookup by ID functionality in delete_task()
- [x] T031 [US4] Implement task removal from the global task list
- [x] T032 [US4] Add confirmation message after successful task deletion
- [x] T033 [US4] Add error handling for invalid task IDs in delete_task()
- [x] T034 [US4] Integrate delete_task function with menu option 2

## Phase 7: [US3] Update and Complete Tasks (Priority: P2)

### Goal
Implement functionality to update task details and toggle completion status by ID.

### Independent Test Criteria
Can be fully tested by selecting tasks by ID to update their details or toggle their completion status.

### Acceptance Scenarios
1. When user selects "Update Task" and provides a valid task ID with new title/description, system updates the specified fields and displays the updated task.
2. When user selects "Mark as Complete" and provides a valid task ID, system toggles the completion status and displays the new status.
3. When user provides an invalid task ID for update or complete, system displays an error message indicating the task was not found.

### Tasks

- [x] T035 [US3] Implement update_task() function with task ID prompt
- [x] T036 [US3] Add task lookup by ID functionality in update_task()
- [x] T037 [US3] Implement title and description update prompts in update_task()
- [x] T038 [US3] Add logic to skip updating fields if user input is empty
- [x] T039 [US3] Display updated task information after successful update
- [x] T040 [US3] Add error handling for invalid task IDs in update_task()
- [x] T041 [US3] Implement mark_complete() function with task ID prompt
- [x] T042 [US3] Add task lookup by ID functionality in mark_complete()
- [x] T043 [US3] Implement toggle logic for completion status
- [x] T044 [US3] Display new completion status after toggle
- [x] T045 [US3] Add error handling for invalid task IDs in mark_complete()
- [x] T046 [US3] Integrate update_task and mark_complete functions with menu options 3 and 5

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Implement comprehensive error handling, input validation, and edge case management to ensure the application is robust and user-friendly.

### Tasks

- [x] T047 Add input validation for non-numeric ID inputs across all functions
- [x] T048 Implement length validation for very long text inputs for titles/descriptions
- [x] T049 Add comprehensive error handling for all user inputs
- [x] T050 Implement proper formatting and user-friendly messages
- [x] T051 Add comments and documentation to all functions
- [x] T052 Test all menu options and error scenarios
- [x] T053 Perform final integration testing of all features
- [x] T054 Update README.md with complete usage instructions and examples

## Dependencies

- User Story 1 (Add Tasks) must be completed before User Story 3 and 4 can be fully tested (need tasks to update/delete)
- User Story 2 (View Tasks) is foundational for User Stories 3, 4, and 5 (need to see tasks to manage them)
- User Story 5 (Menu Interface) is required for all other user stories to be accessible

## Parallel Execution Examples

- [US1] Add Tasks and [US2] View Tasks can be developed in parallel as they operate on the same data structure
- [US4] Delete Tasks and [US3] Update/Complete Tasks can be developed in parallel as they both require task lookup functionality
- Helper functions (validation, formatting) can be developed in parallel with main features [P]

## Implementation Strategy

1. **MVP Scope**: Complete Phase 1, 2, 3, 4, and 5 to have a functional application with add/view/menu capabilities (US1, US2, US5)
2. **Incremental Delivery**: Add delete/update/complete functionality in Phase 6 and 7 (US4, US3)
3. **Polish Phase**: Complete error handling and documentation in Phase 8