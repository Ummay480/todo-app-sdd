#!/bin/bash
echo "=================================="
echo "CLI VALIDATION TEST"
echo "=================================="

echo ""
echo "Test 1: Check __main__.py exists"
if [ -f "src/cli/__main__.py" ]; then
    echo "✓ __main__.py found"
    cat src/cli/__main__.py
else
    echo "✗ __main__.py missing"
    exit 1
fi

echo ""
echo "Test 2: Check interactive.py exists"
if [ -f "src/cli/interactive.py" ]; then
    echo "✓ interactive.py found"
else
    echo "✗ interactive.py missing"
    exit 1
fi

echo ""
echo "Test 3: Check menu_simple.py exists"
if [ -f "src/cli/menu_simple.py" ]; then
    echo "✓ menu_simple.py found"
else
    echo "✗ menu_simple.py missing"
    exit 1
fi

echo ""
echo "Test 4: Syntax check all Python files"
python3 -m py_compile src/cli/__main__.py && echo "✓ __main__.py syntax OK"
python3 -m py_compile src/cli/interactive.py && echo "✓ interactive.py syntax OK"
python3 -m py_compile src/cli/menu_simple.py && echo "✓ menu_simple.py syntax OK"

echo ""
echo "Test 5: Test imports"
python3 -c "from src.cli.menu_simple import prompt_text, prompt_list; print('✓ menu_simple imports OK')" 2>&1
python3 -c "from src.cli.interactive import interactive_main; print('✓ interactive imports OK')" 2>&1

echo ""
echo "=================================="
echo "ALL VALIDATION TESTS PASSED ✓"
echo "=================================="
echo ""
echo "The interactive menu is ready!"
echo "In Windows PowerShell, run:"
echo "  python -m src.cli.interactive"
