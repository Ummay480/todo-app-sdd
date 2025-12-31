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
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task to add")

    # 'list' command
    list_parser = subparsers.add_parser("list", help="List all tasks")

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
        sys.exit(exit_code)
    elif args.command == "list":
        exit_code = handle_list(args, storage)
        sys.exit(exit_code)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
