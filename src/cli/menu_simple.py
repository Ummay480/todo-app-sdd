"""Simple text-based menu navigation (cross-platform fallback)"""

from typing import List


def prompt_text(message: str, optional: bool = False) -> str:
    """Prompt for text input.

    Args:
        message: Prompt message
        optional: Whether the input is optional

    Returns:
        User input string
    """
    suffix = " (optional)" if optional else ""
    value = input(f"? {message}{suffix}: ").strip()
    return value


def prompt_list(message: str, choices: List[str], default: str = "") -> str:
    """Prompt for selection from a numbered list.

    Args:
        message: Prompt message
        choices: List of choices
        default: Default choice

    Returns:
        Selected choice
    """
    print(f"\n? {message}")
    default_idx = choices.index(default) if default in choices else 0

    for i, choice in enumerate(choices, 1):
        marker = "➤" if choice == default else " "
        print(f"  {marker} {i}. {choice}")

    while True:
        response = input(f"\nSelect (1-{len(choices)}) [default: {default_idx + 1}]: ").strip()

        if not response:
            return choices[default_idx]

        if response.isdigit() and 1 <= int(response) <= len(choices):
            return choices[int(response) - 1]

        print(f"❌ Invalid choice. Please enter a number between 1 and {len(choices)}")


def confirm(message: str, default: bool = False) -> bool:
    """Prompt for yes/no confirmation.

    Args:
        message: Prompt message
        default: Default value

    Returns:
        True for yes, False for no
    """
    default_str = "Y/n" if default else "y/N"
    response = input(f"? {message} ({default_str}): ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']
