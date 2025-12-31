print("Test 1: Python is running")

try:
    print("Test 2: Importing menu_simple...")
    from src.cli.menu_simple import prompt_text
    print("Test 3: Import successful!")
except Exception as e:
    print(f"Test 3 FAILED: {e}")
    import traceback
    traceback.print_exc()
