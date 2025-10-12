import warnings

# Suppress all warnings before importing anything else
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*validate_default.*")

from src.orchestrator import run_cli

def main():
    run_cli()

if __name__ == "__main__":
    main()
