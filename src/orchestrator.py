from prompt_toolkit import prompt
from rich.console import Console
from rich.markdown import Markdown
from .env_setup import check_and_setup_env
from .request_interpreter import interpret_request, RagVaultRequest, GenerateNewMarkdownRequest
from .vault_rag.vault_rag import initialize_rag, query_vault
from .generate_md.generate_md_orchestrator import generate_markdown_from_urls

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

            # Case 1: User requests to perform a RAG query
            if isinstance(result, RagVaultRequest):
                console.print("\nSearching vault...")
                answer = query_vault(result.prompt)

                # Render the markdown response with rich
                markdown = Markdown(answer)
                console.print(markdown)
                console.print()

            # Case 2: User requests to generate new markdown content
            elif isinstance(result, GenerateNewMarkdownRequest):
                console.print("\nGenerating markdown from URLs...")
                result_data = generate_markdown_from_urls(
                    urls=result.urls,
                    prompt=result.prompt,
                    vault_path=vault_path,
                    api_key=api_key
                )

                if isinstance(result_data, dict) and result_data.get("success"):
                    # Print success message
                    console.print(f"\nCreated new note: {result_data['file_path']}")

                    # Render the generated markdown
                    markdown = Markdown(result_data['markdown_content'])
                    console.print(markdown)
                    console.print()
                else:
                    # Handle error case
                    error_msg = result_data.get("error", str(result_data))
                    console.print(f"\nError: {error_msg}\n")

            # Unknown request type
            else:
                console.print("Unknown request type")

        except KeyboardInterrupt:
            console.print("\nBye, Dude!")
            break

        except EOFError:
            console.print("\nBye, Dude!")
            break