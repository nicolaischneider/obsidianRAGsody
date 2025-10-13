from enum import Enum
from rich.console import Console
from rich.markdown import Markdown


class InputAction(Enum):
    QUIT = "quit"
    CONTINUE = "continue"
    HANDLED = "handled"


def analyze_input(user_input: str, console: Console) -> InputAction:
    """Analyze input and return appropriate action."""
    cmd = user_input.lower().strip()

    if cmd in ['quit', 'exit']:
        return InputAction.QUIT
    elif cmd in ['help', '?']:
        _handle_help(console)
        return InputAction.HANDLED

    return InputAction.CONTINUE


def _handle_help(console: Console) -> None:
    help_md = """
## Commands
- `help` - Show this help
- `quit`, `exit` - Exit
- Ask questions about your vault content
- Ask to generate markdown nodes and include the URLs you wish the LLM to create the nodes from.
"""
    console.print(Markdown(help_md))