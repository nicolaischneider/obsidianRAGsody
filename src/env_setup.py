import os
from pathlib import Path
from dotenv import load_dotenv


def check_and_setup_env():
    """Check for required environment variables and create .env if needed."""
    load_dotenv()

    vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
    api_key = os.getenv('API_KEY')

    env_file = Path('.env')
    needs_setup = False

    if not vault_path:
        vault_path = input("Enter path to your Obsidian vault: ").strip()
        needs_setup = True

    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
        needs_setup = True

    if needs_setup:
        with open(env_file, 'w') as f:
            f.write(f"OBSIDIAN_VAULT_PATH={vault_path}\n")
            f.write(f"API_KEY={api_key}\n")
        print(f"Configuration saved to {env_file}")

    print(f"- Using vault: {vault_path}\n")
    return vault_path, api_key