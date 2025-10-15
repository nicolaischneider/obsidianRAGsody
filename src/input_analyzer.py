import os
from pathlib import Path
from enum import Enum
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv


class InputAction(Enum):
    QUIT = "quit"
    CONTINUE = "continue"
    HANDLED = "handled"
    CONFIG_UPDATED = "config_updated"


def analyze_input(user_input: str, console: Console) -> InputAction:
    """Analyze input and return appropriate action."""
    cmd = user_input.lower().strip()

    if cmd in ["quit", "exit"]:
        return InputAction.QUIT
    elif cmd in ["help", "?"]:
        _handle_help(console)
        return InputAction.HANDLED
    elif cmd in ["config"]:
        config_updated = _handle_config(console)
        return InputAction.CONFIG_UPDATED if config_updated else InputAction.HANDLED

    return InputAction.CONTINUE


def _handle_help(console: Console) -> None:
    help_md = """
## Commands
- `help` - Show this help
- `config` - Change settings
- `quit`, `exit` - Exit
- Ask questions about your vault content
- Ask to generate markdown nodes and include the URLs you wish the LLM to create the nodes from.
"""
    console.print(Markdown(help_md))


def _handle_config(console: Console) -> bool:
    console.print("\nWhat config would you like to change?")
    console.print("1. Vault path")
    console.print("2. API key")
    console.print("3. LLM model")
    console.print("4. User name")

    choice = input("\nEnter number (1-4): ").strip()

    env_file = Path(".env")
    if not env_file.exists():
        console.print("[red]No .env file found[/red]")
        return

    # Read existing settings
    settings = {}
    with open(env_file, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                settings[key] = value

    # Handle user choice
    if choice == "1":
        new_value = input("Enter path to your Obsidian vault: ").strip()
        if new_value:
            settings["OBSIDIAN_VAULT_PATH"] = new_value
    elif choice == "2":
        new_value = input("Enter your OpenAI API key: ").strip()
        if new_value:
            settings["API_KEY"] = new_value
    elif choice == "3":
        console.print("OpenAI models: gpt-5, gpt-5-mini, gpt-4o-mini, gpt-4.1, gpt-4o")
        new_value = input("Enter OpenAI model: ").strip()
        if new_value:
            settings["LLM_MODEL"] = new_value
    elif choice == "4":
        new_value = input("What should we call you? ").strip()
        if new_value:
            settings["USER_NAME"] = new_value
    else:
        console.print("Invalid choice")
        return False

    # Write updated settings
    with open(env_file, "w") as f:
        for key, value in settings.items():
            f.write(f"{key}={value}\n")

    console.print("[green]Setting updated![/green]")
    return True
