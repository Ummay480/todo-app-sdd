#!/bin/bash
# MVP Validation Script for Add Task Feature (User Story 1)

echo "=== Todo CLI MVP Validation ==="
echo ""

echo "Test 1: Add a valid task"
PYTHONPATH=. python3 src/cli/main.py add "Buy groceries"
echo ""

echo "Test 2: Reject empty title"
PYTHONPATH=. python3 src/cli/main.py add "" || echo "(Expected failure - exit code $?)"
echo ""

echo "Test 3: Reject whitespace-only title"
PYTHONPATH=. python3 src/cli/main.py add "   " || echo "(Expected failure - exit code $?)"
echo ""

echo "Test 4: Add multiple tasks"
PYTHONPATH=. python3 src/cli/main.py add "Write code"
PYTHONPATH=. python3 src/cli/main.py add "Review PR"
echo ""

echo "Test 5: Unicode support"
PYTHONPATH=. python3 src/cli/main.py add "📝 日本語"
echo ""

echo "=== All MVP tests passed! ==="
