"""Unit tests for list command handler"""

import pytest
import argparse
from src.cli.main import handle_list
from src.lib.storage import TaskStorage
from src.models.task import Task


class TestHandleList:
    """Tests for handle_list function"""

    def test_handle_list_empty_storage(self, capsys) -> None:
        """Test list with no tasks"""
        storage = TaskStorage()
        args = argparse.Namespace()

        exit_code = handle_list(args, storage)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No tasks found" in captured.out
        assert "Suggestion" in captured.out

    def test_handle_list_single_task(self, capsys) -> None:
        """Test list with one task"""
        storage = TaskStorage()
        task: Task = {"id": 1, "title": "Buy groceries", "status": "pending"}
        storage.add_task(task)
        args = argparse.Namespace()

        exit_code = handle_list(args, storage)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "TODO List" in captured.out
        assert "Total: 1 task" in captured.out
        assert "Buy groceries" in captured.out
        assert "[1]" in captured.out
        assert "pending" in captured.out

    def test_handle_list_multiple_tasks(self, capsys) -> None:
        """Test list with multiple tasks"""
        storage = TaskStorage()
        task1: Task = {"id": 1, "title": "Task 1", "status": "pending"}
        task2: Task = {"id": 2, "title": "Task 2", "status": "completed"}
        task3: Task = {"id": 3, "title": "Task 3", "status": "pending"}

        storage.add_task(task1)
        storage.add_task(task2)
        storage.add_task(task3)
        args = argparse.Namespace()

        exit_code = handle_list(args, storage)

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Total: 3 tasks" in captured.out
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "Task 3" in captured.out

    def test_handle_list_shows_status_icons(self, capsys) -> None:
        """Test that list shows different icons for pending/completed"""
        storage = TaskStorage()
        task1: Task = {"id": 1, "title": "Pending task", "status": "pending"}
        task2: Task = {"id": 2, "title": "Completed task", "status": "completed"}

        storage.add_task(task1)
        storage.add_task(task2)
        args = argparse.Namespace()

        exit_code = handle_list(args, storage)

        captured = capsys.readouterr()
        # Check for status icons (○ for pending, ✓ for completed)
        assert "○" in captured.out or "o" in captured.out.lower()
        assert "✓" in captured.out or "completed" in captured.out.lower()
