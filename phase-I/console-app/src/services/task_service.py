"""Business logic for task operations"""

from typing import Dict, Any, Optional
from src.lib.storage import TaskStorage
from src.models.task import Task, is_valid_title, create_task, TaskPriority


class TaskService:
    """Service layer for task operations.

    Handles business logic for task management including validation,
    duplicate detection, and coordination with storage layer.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize service with storage backend.

        Args:
            storage: TaskStorage instance for persistence
        """
        self._storage = storage

    def add_task(
        self,
        title: str,
        category: str | None = None,
        tags: list[str] | None = None,
        priority: TaskPriority | None = None,
        due_date: str | None = None
    ) -> Dict[str, Any]:
        """Add a new task with the given title, category, and tags.

        Validates the title, checks for duplicates, and creates a new task
        with auto-generated ID and default "pending" status.

        Args:
            title: The task title to add
            category: Optional category for organization
            tags: Optional list of tags

        Returns:
            Dictionary with:
                - success (bool): True if task created, False if validation failed
                - task (Task): The created task (if success=True)
                - warning (str): Warning message if duplicate detected (if success=True)
                - error (str): Error message if validation failed (if success=False)

        Examples:
            >>> service.add_task("Buy groceries", category="personal", tags=["shopping"])
            {'success': True, 'task': {...}, 'warning': None}

            >>> service.add_task("")
            {'success': False, 'error': 'Task title cannot be empty'}
        """
        # Validate title
        if not is_valid_title(title):
            if not title or not title.strip():
                return {
                    "success": False,
                    "error": "Task title cannot be empty",
                }
            elif len(title) > 1000:
                return {
                    "success": False,
                    "error": "Task title exceeds maximum length (1000 characters)",
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid task title",
                }

        # Check for duplicates
        has_duplicate = self._storage.has_duplicate(title)
        warning: Optional[str] = None
        if has_duplicate:
            # Find the existing task ID for the warning message
            existing_tasks = self._storage.get_all_tasks()
            existing_id = next(
                task["id"] for task in existing_tasks if task["title"] == title
            )
            warning = (
                f"A task with this title already exists (ID: {existing_id})"
            )

        # Create new task with all fields
        task_id = self._storage.generate_id()
        task = create_task(
            task_id=task_id,
            title=title,
            status="pending",
            category=category,
            tags=tags,
            priority=priority,
            due_date=due_date
        )

        # Add to storage
        self._storage.add_task(task)

        return {
            "success": True,
            "task": task,
            "warning": warning,
        }
