"""Simple arrow-key menu navigation using ANSI escape codes"""

import sys
from typing import List

# Platform-specific imports
if sys.platform == 'win32':
    import msvcrt
else:
    import tty
    import termios


def get_key() -> str:
    """Get a single keypress from stdin.

    Returns:
        String representing the key pressed
    """
    if sys.platform == 'win32':
        # Windows implementation
        if msvcrt.kbhit():
            ch = msvcrt.getch()

            # Handle special keys (arrow keys start with 0xe0 or 0x00)
            if ch in (b'\xe0', b'\x00'):
                ch2 = msvcrt.getch()
                if ch2 == b'H':  # Up arrow
                    return 'up'
                elif ch2 == b'P':  # Down arrow
                    return 'down'
                elif ch2 == b'M':  # Right arrow
                    return 'right'
                elif ch2 == b'K':  # Left arrow
                    return 'left'
            elif ch == b'\r':  # Enter
                return 'enter'
            elif ch == b'\x03':  # Ctrl+C
                return 'ctrl_c'

            return ch.decode('utf-8', errors='ignore')
        return ''
    else:
        # Unix implementation
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

            # Handle escape sequences (arrow keys)
            if ch == '\x1b':
                ch = sys.stdin.read(2)
                if ch == '[A':
                    return 'up'
                elif ch == '[B':
                    return 'down'
                elif ch == '[C':
                    return 'right'
                elif ch == '[D':
                    return 'left'
            elif ch == '\r' or ch == '\n':
                return 'enter'
            elif ch == '\x03':  # Ctrl+C
                return 'ctrl_c'

            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def select_from_list(message: str, choices: List[str], default: int = 0) -> str:
    """Display an interactive menu with arrow-key navigation.

    Args:
        message: Question/prompt to display
        choices: List of menu options
        default: Index of default selection

    Returns:
        Selected choice string
    """
    current = default

    while True:
        # Clear screen and move cursor to top
        print('\033[2J\033[H', end='')

        # Print question
        print(f"\n? {message} (use arrow keys)\n")

        # Print choices with cursor indicator
        for idx, choice in enumerate(choices):
            if idx == current:
                print(f"  \033[36m❯ {choice}\033[0m")  # Cyan with cursor
            else:
                print(f"    {choice}")

        # Print help text
        print("\n  [↑/↓: Navigate  Enter: Select  Ctrl+C: Cancel]")

        # Get key input
        key = get_key()

        if key == 'up' and current > 0:
            current -= 1
        elif key == 'down' and current < len(choices) - 1:
            current += 1
        elif key == 'enter':
            # Clear screen
            print('\033[2J\033[H', end='')
            return choices[current]
        elif key == 'ctrl_c':
            print('\033[2J\033[H', end='')
            print("\n❌ Cancelled\n")
            sys.exit(0)


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
    """Prompt for selection from a list with arrow-key navigation.

    Args:
        message: Prompt message
        choices: List of choices
        default: Default choice

    Returns:
        Selected choice
    """
    default_idx = 0
    if default and default in choices:
        default_idx = choices.index(default)

    return select_from_list(message, choices, default_idx)


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
