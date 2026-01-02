"""Unit tests for task service"""

import pytest
from src.services.task_service import TaskService
from src.lib.storage import TaskStorage


class TestTaskService:
    """Tests for TaskService class"""

    def test_add_task_valid_title(self) -> None:
        """Test adding a task with a valid title"""
        storage = TaskStorage()
        service = TaskService(storage)

        result = service.add_task("Buy groceries")

        assert result["success"] is True
        assert result["task"]["title"] == "Buy groceries"
        assert result["task"]["status"] == "pending"
        assert result["task"]["id"] == 1
        assert result.get("warning") is None

    def test_add_task_empty_title(self) -> None:
        """Test that empty titles are rejected"""
        storage = TaskStorage()
        service = TaskService(storage)

        result = service.add_task("")

        assert result["success"] is False
        assert "error" in result
        assert "empty" in result["error"].lower()

    def test_add_task_whitespace_only(self) -> None:
        """Test that whitespace-only titles are rejected"""
        storage = TaskStorage()
        service = TaskService(storage)

        result = service.add_task("   ")

        assert result["success"] is False
        assert "error" in result

    def test_add_task_duplicate_warning(self) -> None:
        """Test that duplicate titles trigger a warning"""
        storage = TaskStorage()
        service = TaskService(storage)

        # Add first task
        result1 = service.add_task("Buy groceries")
        assert result1["success"] is True
        assert result1.get("warning") is None

        # Add duplicate task
        result2 = service.add_task("Buy groceries")
        assert result2["success"] is True
        assert result2["warning"] is not None
        assert "already exists" in result2["warning"]
        assert result2["task"]["id"] == 2  # New task created with new ID

    def test_add_task_long_title(self) -> None:
        """Test that titles over 1000 characters are rejected"""
        storage = TaskStorage()
        service = TaskService(storage)

        long_title = "a" * 1001
        result = service.add_task(long_title)

        assert result["success"] is False
        assert "error" in result

    def test_add_multiple_tasks(self) -> None:
        """Test adding multiple tasks sequentially"""
        storage = TaskStorage()
        service = TaskService(storage)

        result1 = service.add_task("Task 1")
        result2 = service.add_task("Task 2")
        result3 = service.add_task("Task 3")

        assert result1["task"]["id"] == 1
        assert result2["task"]["id"] == 2
        assert result3["task"]["id"] == 3
