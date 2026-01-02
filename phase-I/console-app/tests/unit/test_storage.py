"""Unit tests for task storage"""

import pytest
from src.lib.storage import TaskStorage
from src.models.task import Task


class TestTaskStorage:
    """Tests for TaskStorage class"""

    def test_add_task(self) -> None:
        """Test adding a task to storage"""
        storage = TaskStorage()
        task: Task = {"id": 1, "title": "Test task", "status": "pending"}
        storage.add_task(task)

        all_tasks = storage.get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0]["title"] == "Test task"

    def test_generate_sequential_ids(self) -> None:
        """Test that IDs are generated sequentially"""
        storage = TaskStorage()
        assert storage.generate_id() == 1
        assert storage.generate_id() == 2
        assert storage.generate_id() == 3

    def test_get_all_tasks_empty(self) -> None:
        """Test get_all_tasks on empty storage"""
        storage = TaskStorage()
        assert storage.get_all_tasks() == []

    def test_get_all_tasks_multiple(self) -> None:
        """Test get_all_tasks with multiple tasks"""
        storage = TaskStorage()
        task1: Task = {"id": 1, "title": "Task 1", "status": "pending"}
        task2: Task = {"id": 2, "title": "Task 2", "status": "pending"}

        storage.add_task(task1)
        storage.add_task(task2)

        all_tasks = storage.get_all_tasks()
        assert len(all_tasks) == 2
        assert all_tasks[0]["title"] == "Task 1"
        assert all_tasks[1]["title"] == "Task 2"

    def test_has_duplicate_true(self) -> None:
        """Test has_duplicate returns True when duplicate exists"""
        storage = TaskStorage()
        task: Task = {"id": 1, "title": "Buy groceries", "status": "pending"}
        storage.add_task(task)

        assert storage.has_duplicate("Buy groceries") is True

    def test_has_duplicate_false(self) -> None:
        """Test has_duplicate returns False when no duplicate exists"""
        storage = TaskStorage()
        task: Task = {"id": 1, "title": "Buy groceries", "status": "pending"}
        storage.add_task(task)

        assert storage.has_duplicate("Write code") is False

    def test_has_duplicate_case_sensitive(self) -> None:
        """Test that duplicate detection is case-sensitive"""
        storage = TaskStorage()
        task: Task = {"id": 1, "title": "Buy Groceries", "status": "pending"}
        storage.add_task(task)

        assert storage.has_duplicate("Buy Groceries") is True
        assert storage.has_duplicate("buy groceries") is False
