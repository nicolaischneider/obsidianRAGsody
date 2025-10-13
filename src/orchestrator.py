from prompt_toolkit import prompt
from rich.console import Console
from rich.markdown import Markdown
from .env_setup import check_and_setup_env
from .request_interpreter import interpret_request, RagVaultRequest, GenerateNewMarkdownRequest
from .vault_rag.vault_rag import initialize_rag, query_vault
from .generate_md.generate_md_orchestrator import generate_markdown_from_urls
from .input_analyzer import analyze_input, InputAction

# Setup environment and initialize RAG system
def _setup_and_initialize(console: Console) -> tuple[str, str, str, str]:
    vault_path, api_key, llm_model, user_name = check_and_setup_env()
    initialize_rag(vault_path, api_key, llm_model)
    return vault_path, api_key, llm_model, user_name

# Handle vault RAG query requests
def _handle_rag_query(console: Console, request: RagVaultRequest) -> None:
    console.print("\n[dim italic]Searching vault...[/dim italic]\n")
    answer = query_vault(request.prompt)
    markdown = Markdown(answer)
    console.print(markdown)
    console.print()

# Handle URL-to-markdown generation requests
def _handle_markdown_generation(console: Console, request: GenerateNewMarkdownRequest, vault_path: str, api_key: str, llm_model: str) -> None:
    console.print("\n[dim italic]Generating markdown from URLs...[/dim italic]\n")

    result_data = generate_markdown_from_urls(
        urls=request.urls,
        prompt=request.prompt,
        vault_path=vault_path,
        api_key=api_key,
        llm_model=llm_model
    )

    if isinstance(result_data, dict) and result_data.get("success"):
        markdown = Markdown(result_data['markdown_content'])
        console.print(markdown)
        console.print("\n[dim]------[/dim]")
        console.print(f"Created new note:\n{result_data['file_path']}\n")
    else:
        error_msg = result_data.get("error", str(result_data))
        console.print(f"\nError: {error_msg}\n")

# Main CLI orchestrator that handles the interactive loop.
def run_cli():
    console = Console()

    # Welcome message
    welcome_md = "# Welcome to Obsidian RAGsody\n"
    console.print(Markdown(welcome_md))
    console.print("- Type 'quit' or 'exit' to quit.")

    # Setup and initialization
    vault_path, api_key, llm_model, user_name = _setup_and_initialize(console)

    # Interactive prompt loop
    while True:
        try:
            console.print(Markdown("---"))
            user_input = prompt(f"{user_name}: ")

            # Analyze input for special commands
            action = analyze_input(user_input, console)

            match action:
                # User requested to quit
                case InputAction.QUIT:
                    print(f"\nBye, {user_name}!")
                    break

                # User input was handled (e.g., help command)
                case InputAction.HANDLED:
                    continue

                # Continue to interpret the input
                case InputAction.CONTINUE:
                    result = interpret_request(user_input)

                    if isinstance(result, RagVaultRequest):
                        _handle_rag_query(console, result)
                    elif isinstance(result, GenerateNewMarkdownRequest):
                        _handle_markdown_generation(console, result, vault_path, api_key, llm_model)
                    else:
                        console.print("[red]Unknown request type[/red]")

        except (KeyboardInterrupt, EOFError):
            console.print(f"\nBye, {user_name}!")
            break