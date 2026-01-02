#!/usr/bin/env python3
"""
Interactive Todo CLI Application

Launch the interactive menu-driven interface.

Usage:
    python todo_interactive.py

Or:
    python -m src.cli.interactive
"""

if __name__ == "__main__":
    from src.cli.interactive import interactive_main
    interactive_main()
