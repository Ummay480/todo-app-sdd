"""File-based persistent storage for Todo tasks"""

import json
import os
from typing import List
from src.models.task import Task


class TaskStorage:
    """Manages persistent storage of tasks in a JSON file.

    This class provides CRUD operations for tasks with automatic file persistence.
    All operations are deterministic and tasks persist across CLI runs.
    """

    def __init__(self, filename: str = "tasks.json") -> None:
        """Initialize task storage with file persistence.

        Args:
            filename: Path to JSON file for storing tasks (default: tasks.json)
        """
        self._filename = filename
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self._load()

    def generate_id(self) -> int:
        """Generate next unique task ID.

        IDs are auto-incremented starting from 1, ensuring deterministic
        behavior across runs with the same operation sequence.

        Returns:
            Next available task ID
        """
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def _load(self) -> None:
        """Load tasks from JSON file.

        Reads tasks from the file and determines the next available ID.
        Creates an empty file if it doesn't exist.
        """
        if os.path.exists(self._filename):
            try:
                with open(self._filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._tasks = data.get("tasks", [])
                    # Use stored next_id if available, otherwise calculate from tasks
                    self._next_id = data.get("next_id")
                    if self._next_id is None:
                        if self._tasks:
                            max_id = max(task["id"] for task in self._tasks)
                            self._next_id = max_id + 1
                        else:
                            self._next_id = 1
            except (json.JSONDecodeError, KeyError):
                # If file is corrupted, start fresh
                self._tasks = []
                self._next_id = 1
        else:
            # Create empty file
            self._save()

    def _save(self) -> None:
        """Save tasks to JSON file.

        Writes all tasks to the file in a deterministic format.
        """
        data = {
            "tasks": self._tasks,
            "next_id": self._next_id
        }
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_task(self, task: Task) -> None:
        """Add a task to storage and save to file.

        Args:
            task: Task dictionary with id, title, and status fields
        """
        self._tasks.append(task)
        self._save()

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from storage.

        Returns:
            List of all tasks in storage
        """
        return self._tasks.copy()

    def has_duplicate(self, title: str) -> bool:
        """Check if a task with the given title already exists.

        Uses case-sensitive exact string matching for deterministic behavior.

        Args:
            title: Title to check for duplicates

        Returns:
            True if a task with this title exists, False otherwise
        """
        return any(task["title"] == title for task in self._tasks)

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task if found, None otherwise
        """
        for task in self._tasks:
            if task["id"] == task_id:
                return task
        return None

    def update_task(self, task_id: int, **updates) -> bool:
        """Update a task's fields and save to file.

        Args:
            task_id: The ID of the task to update
            **updates: Field names and new values

        Returns:
            True if task was found and updated, False otherwise
        """
        for task in self._tasks:
            if task["id"] == task_id:
                for key, value in updates.items():
                    if key in task:
                        task[key] = value  # type: ignore
                self._save()
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID and save to file.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        for i, task in enumerate(self._tasks):
            if task["id"] == task_id:
                self._tasks.pop(i)
                self._save()
                return True
        return False

    def filter_tasks(
        self,
        status: str | None = None,
        category: str | None = None,
        tag: str | None = None
    ) -> list[Task]:
        """Filter tasks by status, category, or tag.

        Args:
            status: Filter by status (pending/completed)
            category: Filter by category
            tag: Filter by tag (matches if tag is in task's tags list)

        Returns:
            List of tasks matching all specified filters
        """
        filtered = self._tasks.copy()

        if status:
            filtered = [t for t in filtered if t.get("status") == status]

        if category:
            filtered = [t for t in filtered if t.get("category") == category]

        if tag:
            filtered = [t for t in filtered if tag in t.get("tags", [])]

        return filtered
