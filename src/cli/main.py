"""CLI entry point for Todo application"""

import sys
import argparse
from typing import NoReturn
from src.lib.storage import TaskStorage
from src.services.task_service import TaskService


def handle_list(args: argparse.Namespace, storage: TaskStorage) -> int:
    """Handle the 'list' command.

    Args:
        args: Parsed command-line arguments
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success)
    """
    tasks = storage.get_all_tasks()

    if not tasks:
        print("No tasks found.")
        print('Suggestion: Add a task with: todo add "Your task title"')
        return 0

    # Display header
    print("\nTODO List")
    print("=" * 50)
    print(f"Total: {len(tasks)} task{'s' if len(tasks) != 1 else ''}\n")

    # Display each task
    for task in tasks:
        status_icon = "○" if task["status"] == "pending" else "✓"
        print(f"  {status_icon} [{task['id']}] {task['title']}")
        print(f"      Status: {task['status']}")
        print()

    return 0


def handle_complete(args: argparse.Namespace, storage: TaskStorage) -> int:
    """Handle the 'complete' command.

    Args:
        args: Parsed command-line arguments
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task_id = args.id
    task = storage.get_task_by_id(task_id)

    if not task:
        print(f"ERROR: Task with ID {task_id} not found")
        print(f"Suggestion: Use 'todo list' to see all tasks")
        print("Code: TASK_NOT_FOUND")
        return 1

    if task["status"] == "completed":
        print(f"⚠ Task {task_id} is already completed")
        print(f"  [{task_id}] {task['title']}")
        return 0

    # Update status
    storage.update_task(task_id, status="completed")
    print(f"✓ Task completed: \"{task['title']}\" (ID: {task_id})")
    return 0


def handle_delete(args: argparse.Namespace, storage: TaskStorage) -> int:
    """Handle the 'delete' command.

    Args:
        args: Parsed command-line arguments
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task_id = args.id
    task = storage.get_task_by_id(task_id)

    if not task:
        print(f"ERROR: Task with ID {task_id} not found")
        print(f"Suggestion: Use 'todo list' to see all tasks")
        print("Code: TASK_NOT_FOUND")
        return 1

    # Delete task
    storage.delete_task(task_id)
    print(f"✓ Task deleted: \"{task['title']}\" (ID: {task_id})")
    return 0


def handle_update(args: argparse.Namespace, storage: TaskStorage) -> int:
    """Handle the 'update' command.

    Args:
        args: Parsed command-line arguments
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    from src.models.task import is_valid_title

    task_id = args.id
    new_title = args.title

    # Validate new title
    if not is_valid_title(new_title):
        if not new_title or not new_title.strip():
            print("ERROR: Task title cannot be empty")
            print('Suggestion: Provide a non-empty title')
            print("Code: EMPTY_TITLE")
        elif len(new_title) > 1000:
            print("ERROR: Task title exceeds maximum length (1000 characters)")
            print("Suggestion: Shorten your title to 1000 characters or less")
            print("Code: TITLE_TOO_LONG")
        else:
            print("ERROR: Invalid task title")
            print("Code: INVALID_TITLE")
        return 1

    task = storage.get_task_by_id(task_id)

    if not task:
        print(f"ERROR: Task with ID {task_id} not found")
        print(f"Suggestion: Use 'todo list' to see all tasks")
        print("Code: TASK_NOT_FOUND")
        return 1

    old_title = task["title"]

    # Update title
    storage.update_task(task_id, title=new_title)
    print(f"✓ Task updated (ID: {task_id})")
    print(f"  Old: \"{old_title}\"")
    print(f"  New: \"{new_title}\"")
    return 0


def handle_add(args: argparse.Namespace, service: TaskService) -> int:
    """Handle the 'add' command.

    Args:
        args: Parsed command-line arguments
        service: TaskService instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    title = args.title

    # Add task via service
    result = service.add_task(title)

    if result["success"]:
        # Success case
        task = result["task"]
        warning = result.get("warning")

        if warning:
            # Duplicate detected
            print(f"⚠ Task added: \"{task['title']}\" (ID: {task['id']})")
            print(f"  Note: {warning}")
        else:
            # Normal success
            print(f"✓ Task added: \"{task['title']}\" (ID: {task['id']})")

        return 0
    else:
        # Error case
        error = result["error"]
        print(f"ERROR: {error}")

        # Provide helpful suggestions
        if "empty" in error.lower():
            print('Suggestion: Provide a non-empty title, e.g., todo add "Buy groceries"')
            print("Code: EMPTY_TITLE")
        elif "exceeds maximum length" in error.lower():
            print("Suggestion: Shorten your title to 1000 characters or less")
            print("Code: TITLE_TOO_LONG")
        else:
            print("Suggestion: Ensure your title is valid")
            print("Code: INVALID_TITLE")

        return 1


def main() -> NoReturn:
    """Main CLI entry point.

    Parses arguments and dispatches to appropriate command handler.
    """
    # Create parser
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple CLI todo application",
    )

    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task to add")

    # 'list' command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # 'complete' command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", type=int, help="ID of the task to complete")

    # 'delete' command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")

    # 'update' command
    update_parser = subparsers.add_parser("update", help="Update a task's title")
    update_parser.add_argument("id", type=int, help="ID of the task to update")
    update_parser.add_argument("title", type=str, help="New title for the task")

    # Parse arguments
    args = parser.parse_args()

    # Check if a command was provided
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize storage and service
    storage = TaskStorage()
    service = TaskService(storage)

    # Dispatch to command handler
    if args.command == "add":
        exit_code = handle_add(args, service)
    elif args.command == "list":
        exit_code = handle_list(args, storage)
    elif args.command == "complete":
        exit_code = handle_complete(args, storage)
    elif args.command == "delete":
        exit_code = handle_delete(args, storage)
    elif args.command == "update":
        exit_code = handle_update(args, storage)
    else:
        parser.print_help()
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
