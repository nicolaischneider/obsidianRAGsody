from prompt_toolkit import prompt
from rich.console import Console
from rich.markdown import Markdown
from .env_setup import check_and_setup_env
from .request_interpreter import interpret_request, RagVaultRequest, GenerateNewMarkdownRequest
from .vault_rag.vault_rag import initialize_rag, query_vault

# Main CLI orchestrator that handles the interactive loop.
def run_cli():
    # Create rich console for markdown rendering
    console = Console()

    # Styled welcome message
    console.print("\n[bold]Welcome to [purple]Obsidian[/purple] [green]RAG[/green]sody![/bold]")
    console.print("- Type 'quit' or 'exit' to quit.")

    # Check environment setup first
    vault_path, api_key = check_and_setup_env()

    # Initialize RAG system
    initialize_rag(vault_path, api_key)

    # Start the interactive prompt loop
    while True:
        try:
            # Get user input
            user_input = prompt("obsidian-ragsody> ")

            # Handle exit commands
            if user_input.lower() in ['quit', 'exit']:
                print("\nBye, Dude!")
                break

            # Interpret the request
            result = interpret_request(user_input)

            # Process the interpreted request

            # User requests to perform a RAG query
            if isinstance(result, RagVaultRequest):
                console.print("\nSearching vault...")
                answer = query_vault(result.prompt)

                # Render the markdown response with rich
                markdown = Markdown(answer)
                console.print(markdown)
                console.print()
            
            # User requests to generate new markdown content
            elif isinstance(result, GenerateNewMarkdownRequest):
                print(f"Generate Markdown: {result.prompt}")
                print(f"URLs found: {result.urls}")
                # TODO: Call markdown generator

            # Unknown request type
            else:
                print("Unknown request type")

        except KeyboardInterrupt:
            print("\nBye, Dude!")
            break

        except EOFError:
            print("\nBye, Dude!")
            break