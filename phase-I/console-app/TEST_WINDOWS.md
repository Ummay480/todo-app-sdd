# Windows Testing Instructions

## Quick Test (Run in PowerShell)

```powershell
# Navigate to project
cd D:\aidd\todo-app

# Pull latest changes
git pull

# Test 1: Verify files exist
ls src/cli/__main__.py
ls src/cli/interactive.py
ls src/cli/menu_simple.py

# Test 2: Run the interactive menu
python -m src.cli.interactive
```

## Expected Behavior

When you run `python -m src.cli.interactive`, you should see:

1. Welcome banner with ASCII art
2. Main menu with 10 options
3. A prompt: `👉 Select an option (1-10, undo, or exit):`

## Test Sequence

1. Type `1` and press Enter (Add todo)
2. Enter title: `Test task`
3. When asked for priority, type `3` and press Enter (High)
4. Enter category: `Work`
5. Skip due date (just press Enter)
6. Skip tags (just press Enter)
7. You should see: `✓ Todo added "Test task" (ID: 5)`
8. Press Enter to continue
9. Type `2` and press Enter (List all todos)
10. You should see all 5 tasks in a table
11. Type `exit` and press Enter

## If It Still Doesn't Work

Run this diagnostic:

```powershell
python -c "from src.cli.interactive import interactive_main; print('Import OK')"
```

If this prints "Import OK", the issue is with the interactive loop waiting for input.

## Alternative: Direct Python Execution

```powershell
python src/cli/interactive.py
```

This should also work as interactive.py has `if __name__ == "__main__"` guard.
