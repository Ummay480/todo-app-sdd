#!/usr/bin/env python3
"""Test script to verify interactive menu works"""

import sys
print("="*70)
print("TESTING INTERACTIVE MENU")
print("="*70)

try:
    print("\n1. Testing imports...")
    from src.cli.interactive import interactive_main, print_menu
    print("   ✓ Imports successful")

    print("\n2. Testing print_menu()...")
    print_menu()
    print("   ✓ Menu displayed")

    print("\n3. Testing storage...")
    from src.lib.storage import TaskStorage
    storage = TaskStorage()
    tasks = storage.get_all_tasks()
    print(f"   ✓ Storage working ({len(tasks)} tasks)")

    print("\n4. All components working!")
    print("\nTo run the full interactive menu:")
    print("   python -m src.cli.interactive")
    print("\nNote: The menu will wait for your input.")
    print("      Type 'exit' to quit.")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
