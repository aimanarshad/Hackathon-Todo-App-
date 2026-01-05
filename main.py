#!/usr/bin/env python3
"""
Todo In-Memory Python Console App
A command-line todo application that stores tasks in memory.
"""

# [Task]: T004 [From]: speckit.specify §2.1
# Global tasks list variable
tasks = []

# [Task]: T007 [From]: speckit.specify §2.2
# Function to generate unique incremental IDs for tasks
def generate_unique_id():
    """Generate a unique ID for a new task."""
    if not tasks:
        return 1
    # Find the highest ID and add 1
    max_id = max(task['id'] for task in tasks)
    return max_id + 1

# [Task]: T008 [From]: speckit.specify §2.3
# Helper function to find task by ID in the task list
def find_task_by_id(task_id):
    """
    Find a task by its ID in the global task list.

    Args:
        task_id (int): The ID of the task to find

    Returns:
        dict or None: The task if found, None otherwise
    """
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# [Task]: T009 [From]: speckit.specify §2.4
# Helper function to validate task title (non-empty requirement)
def validate_task_title(title):
    """
    Validate that the task title is not empty.

    Args:
        title (str): The title to validate

    Returns:
        bool: True if valid, False otherwise
    """
    return title is not None and title.strip() != ""

# [Task]: T010 [From]: speckit.specify §2.5
# Helper function to format and display task lists in table format
def display_tasks_table():
    """Display all tasks in a formatted table."""
    if not tasks:
        print("\nNo tasks found.")
        return

    # Calculate column widths
    id_width = max(4, len("ID"))
    title_width = max(10, len("Title"))
    desc_width = max(15, len("Description"))
    status_width = max(10, len("Status"))

    for task in tasks:
        id_width = max(id_width, len(str(task['id'])))
        title_width = max(title_width, len(task['title']))
        desc_width = max(desc_width, len(task['description']))

    # Print header
    print(f"\n{'ID':<{id_width}} | {'Title':<{title_width}} | {'Description':<{desc_width}} | {'Status':<{status_width}}")
    print("-" * (id_width + title_width + desc_width + status_width + 8))

    # Print tasks
    for task in tasks:
        status = "Completed" if task['completed'] else "Incomplete"
        print(f"{task['id']:<{id_width}} | {task['title']:<{title_width}} | {task['description']:<{desc_width}} | {status:<{status_width}}")

# [Task]: T011 [From]: speckit.specify §2.6
# Helper function to handle user input validation and error handling
def get_valid_task_id():
    """
    Get a valid task ID from user input with error handling.

    Returns:
        int or None: The task ID if valid, None if invalid input
    """
    try:
        task_id = int(input("Enter task ID: "))
        return task_id
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return None

def get_user_input(prompt, required=True):
    """
    Get user input with validation.

    Args:
        prompt (str): The prompt to display
        required (bool): Whether the input is required

    Returns:
        str: The user input
    """
    user_input = input(prompt)
    if required and not validate_task_title(user_input):
        print("Error: Input cannot be empty.")
        return None
    return user_input

# [Task]: T012, T013, T014, T015, T016, T017 [From]: speckit.specify §3
# Implement add_task() function with validation and error handling
def add_task():
    """Add a new task with required title and optional description."""
    print("\n--- Add New Task ---")

    # Get title (required)
    title = get_user_input("Enter task title (required): ", required=True)
    if title is None:
        return  # Error message already displayed

    # Get description (optional)
    description = get_user_input("Enter task description (optional): ", required=False)
    if description is None:
        description = ""

    # Generate unique ID
    task_id = generate_unique_id()

    # Create new task
    new_task = {
        'id': task_id,
        'title': title.strip(),
        'description': description.strip(),
        'completed': False
    }

    # Add to global task list
    tasks.append(new_task)

    # Display confirmation with assigned ID
    print(f"Task added successfully with ID: {task_id}")

# [Task]: T018, T019, T020, T021, T022 [From]: speckit.specify §4
# Implement view_tasks() function with formatted display
def view_tasks():
    """Display all tasks in a formatted table."""
    print("\n--- View Task List ---")
    display_tasks_table()

# [Task]: T023 [From]: speckit.specify §5.1
# Implement display_menu() function to show numbered options (1-6)
def display_menu():
    """Display the main menu with numbered options."""
    print("\n" + "="*40)
    print("TODO APPLICATION")
    print("="*40)
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Update Task")
    print("4. View Task List")
    print("5. Mark as Complete")
    print("6. Exit")
    print("="*40)

# [Task]: T029, T030, T031, T032, T033 [From]: speckit.specify §6
# Implement delete_task() function with validation and error handling
def delete_task():
    """Delete a task by its ID."""
    print("\n--- Delete Task ---")

    if not tasks:
        print("No tasks to delete.")
        return

    display_tasks_table()

    task_id = get_valid_task_id()
    if task_id is None:
        return  # Error message already displayed

    task = find_task_by_id(task_id)
    if task:
        tasks.remove(task)
        print(f"Task with ID {task_id} deleted successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")

# [Task]: T035, T036, T037, T038, T039, T040 [From]: speckit.specify §7
# Implement update_task() function with validation and error handling
def update_task():
    """Update a task's title and/or description by its ID."""
    print("\n--- Update Task ---")

    if not tasks:
        print("No tasks to update.")
        return

    display_tasks_table()

    task_id = get_valid_task_id()
    if task_id is None:
        return  # Error message already displayed

    task = find_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Get new title (optional - press Enter to skip)
    new_title = input(f"Enter new title (current: '{task['title']}') or press Enter to skip: ")
    if new_title.strip():  # Only update if not empty
        if validate_task_title(new_title):
            task['title'] = new_title.strip()
        else:
            print("Error: Title cannot be empty.")
            return
    else:
        print("Title unchanged.")

    # Get new description (optional - press Enter to skip)
    new_description = input(f"Enter new description (current: '{task['description']}') or press Enter to skip: ")
    if new_description.strip():  # Only update if not empty
        task['description'] = new_description.strip()
    else:
        print("Description unchanged.")

    print(f"Task with ID {task_id} updated successfully.")
    print(f"Updated task: ID={task['id']}, Title='{task['title']}', Description='{task['description']}', Completed={task['completed']}")

# [Task]: T041, T042, T043, T044, T045 [From]: speckit.specify §7
# Implement mark_complete() function with validation and error handling
def mark_complete():
    """Toggle the completion status of a task by its ID."""
    print("\n--- Mark Task as Complete/Incomplete ---")

    if not tasks:
        print("No tasks to mark.")
        return

    display_tasks_table()

    task_id = get_valid_task_id()
    if task_id is None:
        return  # Error message already displayed

    task = find_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Toggle the completion status
    task['completed'] = not task['completed']

    status = "Completed" if task['completed'] else "Incomplete"
    print(f"Task with ID {task_id} marked as {status}.")

# [Task]: T024, T025, T026, T027, T028 [From]: speckit.specify §5
# Main menu loop that handles user selections
def main_menu_loop():
    """Main menu loop that continuously displays options until exit."""
    while True:
        display_menu()

        try:
            choice = input("Select an option (1-6): ").strip()

            if choice == '1':
                add_task()
            elif choice == '2':
                delete_task()
            elif choice == '3':
                update_task()
            elif choice == '4':
                view_tasks()
            elif choice == '5':
                mark_complete()
            elif choice == '6':
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Error: Invalid option. Please select a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# [Task]: T005 [From]: speckit.specify §1.5
# Basic main() function with implementation
def main():
    """Main function to run the todo application."""
    print("Welcome to the Todo Application!")
    main_menu_loop()

if __name__ == "__main__":
    main()
