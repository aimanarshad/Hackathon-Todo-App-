# Quickstart: Todo In-Memory Python Console App

## Prerequisites
- Python 3.13+ installed
- UV package manager installed

## Setup
1. Clone or navigate to the project directory
2. Install dependencies: `uv sync` (or `pip install -r requirements.txt` if using pip)
3. Run the application: `python main.py`

## Usage
1. Execute `python main.py` to start the application
2. The menu-driven interface will display 6 options:
   - Option 1: Add Task
   - Option 2: Delete Task
   - Option 3: Update Task
   - Option 4: View Task List
   - Option 5: Mark as Complete
   - Option 6: Exit
3. Select an option by entering the corresponding number
4. Follow the prompts to perform the desired operation

## Example Workflow
1. Start the application
2. Select "1" to add a task
3. Enter a title (required) and description (optional)
4. Select "4" to view your task list
5. Select "5" to mark a task as complete
6. Select "6" to exit the application

## Notes
- All data is stored in memory only and will be lost when the application exits
- Task IDs are auto-generated as incremental integers
- The application handles invalid inputs gracefully with error messages