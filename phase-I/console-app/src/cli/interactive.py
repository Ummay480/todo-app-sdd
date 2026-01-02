"""Interactive menu-driven interface for Todo CLI"""

import sys
from typing import NoReturn
from src.lib.storage import TaskStorage
from src.services.task_service import TaskService
from src.models.task import TaskPriority
from src.cli.menu_simple import prompt_text, prompt_list


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_menu() -> None:
    """Display the main menu."""
    print_header("📋 TODO APP - MAIN MENU")
    print()
    print("  1️⃣  Add todo")
    print("  2️⃣  List all todos")
    print("  3️⃣  Search todos")
    print("  4️⃣  Filter by category")
    print("  5️⃣  Filter by tags")
    print("  6️⃣  Advanced filters")
    print("  7️⃣  Complete todo")
    print("  8️⃣  Update todo")
    print("  9️⃣  Delete todo")
    print("  🔟 Statistics")
    print("  ↩️  Undo last action")
    print("  ❌ Exit")
    print()


def interactive_add(storage: TaskStorage, service: TaskService) -> None:
    """Interactive task addition with prompts."""
    print_header("➕ ADD NEW TODO")
    print()

    # Required: Title
    title = prompt_text("Enter todo title")
    if not title:
        print("❌ Title cannot be empty")
        input("\nPress Enter to continue...")
        return

    # Optional: Priority
    priority_choices = ["Low", "Medium", "High", "Critical", "None (skip)"]
    priority_choice = prompt_list("Select priority", priority_choices, default="Medium")
    priority: TaskPriority | None = None
    if priority_choice != "None (skip)":
        priority = priority_choice  # type: ignore

    # Optional: Category
    category = prompt_text("Enter category", optional=True) or None

    # Optional: Due date
    due_date = prompt_text("Enter due date (YYYY-MM-DD)", optional=True) or None

    # Optional: Tags
    tags_input = prompt_text("Enter tags (comma-separated)", optional=True)
    tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None

    # Add task
    result = service.add_task(
        title,
        category=category,
        tags=tags,
        priority=priority,
        due_date=due_date
    )

    if result["success"]:
        task = result["task"]
        print(f"\n✓ Todo added \"{task['title']}\" (ID: {task['id']})")
        if result.get("warning"):
            print(f"  ⚠ {result['warning']}")
    else:
        print(f"\n❌ Error: {result['error']}")

    input("\nPress Enter to continue...")


def interactive_list(storage: TaskStorage) -> None:
    """Display all todos in formatted table."""
    print_header("📋 LIST ALL TODOS")
    print()

    tasks = storage.get_all_tasks()

    if not tasks:
        print("  No todos found. Add one to get started!")
        return

    # Print table header
    print(f"{'ID':<4} | {'✓':<2} | {'Title':<30} | {'Priority':<8} | {'Due Date':<12} | {'Category':<15}")
    print("-" * 90)

    # Print each task
    for task in tasks:
        task_id = str(task["id"])
        status_icon = "✓" if task["status"] == "completed" else "○"
        title = task["title"][:28] + ".." if len(task["title"]) > 30 else task["title"]
        priority = task.get("priority", "")[:8] if task.get("priority") else "-"
        due_date = task.get("due_date", "")[:12] if task.get("due_date") else "-"
        category = task.get("category", "")[:13] + ".." if task.get("category") and len(task.get("category", "")) > 15 else task.get("category", "-")

        print(f"{task_id:<4} | {status_icon:<2} | {title:<30} | {priority:<8} | {due_date:<12} | {category:<15}")

        # Show tags if present
        if task.get("tags"):
            tags_str = ", ".join(task["tags"])
            print(f"       Tags: {tags_str}")

    # Print summary
    completed = sum(1 for t in tasks if t["status"] == "completed")
    print()
    print(f"Total: {len(tasks)} todos ({completed} completed)")


def interactive_statistics(storage: TaskStorage) -> None:
    """Display statistics screen."""
    print_header("📊 STATISTICS")
    print()

    tasks = storage.get_all_tasks()

    if not tasks:
        print("  No data to show yet. Add some todos!")
        return

    # Basic stats
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "completed")
    pending = total - completed
    completion_rate = (completed / total * 100) if total > 0 else 0

    print(f"  📝 Total Todos:        {total}")
    print(f"  ✅ Completed:          {completed}")
    print(f"  ⏳ Pending:            {pending}")
    print(f"  📈 Completion Rate:    {completion_rate:.1f}%")
    print()

    # By category
    categories = {}
    for task in tasks:
        cat = task.get("category", "Uncategorized")
        categories[cat] = categories.get(cat, 0) + 1

    if categories:
        print("  By Category:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"    • {cat}: {count}")
        print()

    # By priority
    priorities = {}
    for task in tasks:
        pri = task.get("priority", "None")
        priorities[pri] = priorities.get(pri, 0) + 1

    if priorities:
        print("  By Priority:")
        for pri, count in sorted(priorities.items(), key=lambda x: -x[1]):
            print(f"    • {pri}: {count}")
        print()

    # By status
    print(f"  By Status:")
    print(f"    • Pending: {pending}")
    print(f"    • Completed: {completed}")


def interactive_filter_category(storage: TaskStorage) -> None:
    """Filter todos by category."""
    category = prompt_text("Enter category to filter")
    if not category:
        input("\nPress Enter to continue...")
        return

    print_header(f"📁 FILTER: Category = {category}")
    print()

    tasks = storage.filter_tasks(category=category)

    if not tasks:
        print(f"  No todos found in category '{category}'")
        input("\nPress Enter to continue...")
        return

    for task in tasks:
        status_icon = "✓" if task["status"] == "completed" else "○"
        print(f"  {status_icon} [{task['id']}] {task['title']}")
        if task.get("tags"):
            print(f"       Tags: {', '.join(task['tags'])}")

    print(f"\n  Total: {len(tasks)} todos")
    input("\nPress Enter to continue...")


def interactive_filter_tags(storage: TaskStorage) -> None:
    """Filter todos by tag."""
    tag = prompt_text("Enter tag to filter")
    if not tag:
        input("\nPress Enter to continue...")
        return

    print_header(f"🏷️ FILTER: Tag = {tag}")
    print()

    tasks = storage.filter_tasks(tag=tag)

    if not tasks:
        print(f"  No todos found with tag '{tag}'")
        input("\nPress Enter to continue...")
        return

    for task in tasks:
        status_icon = "✓" if task["status"] == "completed" else "○"
        category = task.get("category", "None")
        print(f"  {status_icon} [{task['id']}] {task['title']} | Category: {category}")

    print(f"\n  Total: {len(tasks)} todos")
    input("\nPress Enter to continue...")


def interactive_search(storage: TaskStorage) -> None:
    """Search todos by keyword."""
    keyword = prompt_text("Enter search keyword")
    if not keyword:
        input("\nPress Enter to continue...")
        return

    print_header(f"🔍 SEARCH: \"{keyword}\"")
    print()

    tasks = storage.get_all_tasks()
    keyword_lower = keyword.lower()

    # Search in title, category, and tags
    results = []
    for task in tasks:
        if keyword_lower in task["title"].lower():
            results.append(task)
        elif task.get("category") and keyword_lower in task["category"].lower():
            results.append(task)
        elif any(keyword_lower in tag.lower() for tag in task.get("tags", [])):
            if task not in results:
                results.append(task)

    if not results:
        print(f"  No todos found matching '{keyword}'")
        return

    for task in results:
        status_icon = "✓" if task["status"] == "completed" else "○"
        print(f"  {status_icon} [{task['id']}] {task['title']}")
        meta = []
        if task.get("category"):
            meta.append(f"Category: {task['category']}")
        if task.get("tags"):
            meta.append(f"Tags: {', '.join(task['tags'])}")
        if meta:
            print(f"       {' | '.join(meta)}")

    print(f"\n  Total: {len(results)} todos found")


def interactive_main() -> NoReturn:
    """Main interactive menu loop."""
    storage = TaskStorage()
    service = TaskService(storage)

    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 22 + "TODO CLI APPLICATION" + " " * 26 + "║")
    print("║" + " " * 18 + "Interactive Menu Mode" + " " * 29 + "║")
    print("╚" + "=" * 68 + "╝")

    while True:
        print_menu()

        choice = input("👉 Select an option (1-10, undo, or exit): ").strip().lower()

        if choice == "1" or choice == "add":
            interactive_add(storage, service)

        elif choice == "2" or choice == "list":
            interactive_list(storage)

        elif choice == "3" or choice == "search":
            interactive_search(storage)

        elif choice == "4" or choice == "category":
            interactive_filter_category(storage)

        elif choice == "5" or choice == "tags" or choice == "tag":
            interactive_filter_tags(storage)

        elif choice == "6" or choice == "filter" or choice == "filters":
            print_header("🔧 ADVANCED FILTERS")
            print()
            status = prompt_text("Filter by status (pending/completed)", optional=True) or None
            category = prompt_text("Filter by category", optional=True) or None
            tag = prompt_text("Filter by tag", optional=True) or None

            if status or category or tag:
                tasks = storage.filter_tasks(status=status, category=category, tag=tag)
                print(f"\n  Found {len(tasks)} todos")
                for task in tasks:
                    status_icon = "✓" if task["status"] == "completed" else "○"
                    print(f"  {status_icon} [{task['id']}] {task['title']}")
            else:
                print("  No filters applied")

        elif choice == "7" or choice == "complete":
            task_id = prompt_text("Enter task ID to complete")
            if task_id.isdigit():
                task = storage.get_task_by_id(int(task_id))
                if task:
                    storage.update_task(int(task_id), status="completed")
                    print(f"\n✅ Task {task_id} marked as completed")
                else:
                    print(f"\n❌ Task {task_id} not found")

        elif choice == "8" or choice == "update":
            task_id = prompt_text("Enter task ID to update")
            if task_id.isdigit():
                task = storage.get_task_by_id(int(task_id))
                if task:
                    new_title = prompt_text("Enter new title")
                    if new_title:
                        storage.update_task(int(task_id), title=new_title)
                        print(f"\n✅ Task {task_id} updated")
                else:
                    print(f"\n❌ Task {task_id} not found")

        elif choice == "9" or choice == "delete":
            task_id = prompt_text("Enter task ID to delete")
            if task_id.isdigit():
                task = storage.get_task_by_id(int(task_id))
                if task:
                    storage.delete_task(int(task_id))
                    print(f"\n✅ Task {task_id} deleted")
                else:
                    print(f"\n❌ Task {task_id} not found")

        elif choice == "10" or choice == "stats" or choice == "statistics":
            interactive_statistics(storage)

        elif choice == "undo":
            print("\n⚠️  Undo feature coming soon!")

        elif choice == "exit" or choice == "quit" or choice == "q":
            print("\n👋 Goodbye! Your todos are saved in tasks.json\n")
            sys.exit(0)

        else:
            print(f"\n❌ Invalid option: {choice}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    interactive_main()
