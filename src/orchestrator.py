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

    # Styled welcome message as markdown title
    welcome_md = "# Welcome to Obsidian RAGsody\n"
    console.print(Markdown(welcome_md))
    console.print("- Type 'quit' or 'exit' to quit.")

    # Check environment setup first
    vault_path, api_key, llm_model, user_name = check_and_setup_env()

    # Initialize RAG system
    initialize_rag(vault_path, api_key, llm_model)

    # Add markdown separator
    separator_md = "---"

    # Start the interactive prompt loop
    while True:
        try:
            # Get user input with chat-like prompt
            console.print(Markdown(separator_md))
            user_input = prompt(f"{user_name}: ")

            # Handle exit commands
            if user_input.lower() in ['quit', 'exit']:
                print(f"\nBye, {user_name}!")
                break

            # Interpret the request
            result = interpret_request(user_input)

            # Process the interpreted request

            # Case 1: User requests to perform a RAG query
            if isinstance(result, RagVaultRequest):
                console.print("\n[dim italic]Searching vault...[/dim italic]\n")
                answer = query_vault(result.prompt)

                # Render the markdown response with rich
                markdown = Markdown(answer)
                console.print(markdown)
                console.print()

            # Case 2: User requests to generate new markdown content
            elif isinstance(result, GenerateNewMarkdownRequest):
                console.print("\n[dim italic]Generating markdown from URLs...[/dim italic]\n")

                # Generate markdown and save to vault
                result_data = generate_markdown_from_urls(
                    urls=result.urls,
                    prompt=result.prompt,
                    vault_path=vault_path,
                    api_key=api_key,
                    llm_model=llm_model
                )

                # Handle success result
                if isinstance(result_data, dict) and result_data.get("success"):

                    # Render the generated markdown
                    markdown = Markdown(result_data['markdown_content'])
                    console.print(markdown)
                    console.print()
                    
                    # Print success message
                    console.print("\n[dim]------[/dim]")
                    console.print(f"Created new note:\n{result_data['file_path']}\n")
                
                # Handle failure case
                else:
                    # Handle error case
                    error_msg = result_data.get("error", str(result_data))
                    console.print(f"\nError: {error_msg}\n")

            # Unknown request type
            else:
                console.print("[red]Unknown request type[/red]")

        except KeyboardInterrupt:
            console.print(f"\nBye, {user_name}!")
            break

        except EOFError:
            console.print(f"\nBye, {user_name}!")
            break