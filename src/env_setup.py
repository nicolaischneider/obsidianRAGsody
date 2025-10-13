import os
from pathlib import Path
from dotenv import load_dotenv


def check_and_setup_env():
    """Check for required environment variables and create .env if needed."""
    load_dotenv(override=True)

    vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
    api_key = os.getenv('API_KEY')
    llm_model = os.getenv('LLM_MODEL')
    user_name = os.getenv('USER_NAME')

    env_file = Path('.env')
    needs_setup = False

    if not vault_path:
        vault_path = input("Enter path to your Obsidian vault: ").strip()
        needs_setup = True

    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
        needs_setup = True

    if not llm_model:
        print("OpenAI models: gpt-5, gpt-5-mini, gpt-4o-mini, gpt-4.1, gpt-4o")
        llm_model = input("Enter OpenAI model: ").strip()
        needs_setup = True

    if not user_name:
        user_name = input("What should we call you? ").strip()
        needs_setup = True

    if needs_setup:
        with open(env_file, 'w') as f:
            f.write(f"OBSIDIAN_VAULT_PATH={vault_path}\n")
            f.write(f"API_KEY={api_key}\n")
            f.write(f"LLM_MODEL={llm_model}\n")
            f.write(f"USER_NAME={user_name}\n")
        print(f"Configuration saved to {env_file}")

    print(f"- Using vault: {vault_path}, model: {llm_model}, hello {user_name}!\n")
    return vault_path, api_key, llm_model, user_name