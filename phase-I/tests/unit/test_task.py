"""Unit tests for task model and validation"""

import pytest
from src.models.task import is_valid_title, TodoError


class TestIsValidTitle:
    """Tests for is_valid_title() validation function"""

    def test_valid_title(self) -> None:
        """Test that valid titles are accepted"""
        assert is_valid_title("Buy groceries") is True
        assert is_valid_title("a") is True
        assert is_valid_title("Task with spaces") is True
        assert is_valid_title("123") is True

    def test_empty_title_invalid(self) -> None:
        """Test that empty strings are rejected"""
        assert is_valid_title("") is False

    def test_whitespace_only_title_invalid(self) -> None:
        """Test that whitespace-only strings are rejected"""
        assert is_valid_title("   ") is False
        assert is_valid_title("\t") is False
        assert is_valid_title("\n") is False
        assert is_valid_title("  \t\n  ") is False

    def test_long_title_invalid(self) -> None:
        """Test that titles over 1000 characters are rejected"""
        assert is_valid_title("a" * 1000) is True  # Exactly 1000 is valid
        assert is_valid_title("a" * 1001) is False  # 1001 is invalid

    def test_unicode_title_valid(self) -> None:
        """Test that Unicode characters are supported"""
        assert is_valid_title("📝 Buy groceries") is True
        assert is_valid_title("日本語") is True
        assert is_valid_title("Café") is True

    def test_non_string_invalid(self) -> None:
        """Test that non-string inputs are rejected"""
        assert is_valid_title(123) is False  # type: ignore
        assert is_valid_title(None) is False  # type: ignore
        assert is_valid_title([]) is False  # type: ignore
