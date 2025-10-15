from rich.console import Console
from rich.markdown import Markdown
from typing import List
from pathlib import Path
from prompt_toolkit import prompt
from .core.website_scraper import scrape_url
from .core.page_generator import generate_markdown_from_content, _extract_markdown_content
from .core.optimal_file_organizer import save_markdown_file
from .core.ai_caller import call_openai_api

# Main function to process URLs and create markdown files in the vault
def generate_markdown_from_urls(urls: List[str], prompt: str, vault_path: str, api_key: str, llm_model: str) -> str:

    try:
        # Step 1: Scrape content from all URLs
        all_content = []
        for url in urls:
            content = scrape_url(url)
            all_content.append({"url": url, "content": content})

        # Step 2: Generate combined markdown summary using AI
        markdown_file = generate_markdown_from_content(all_content, prompt, api_key, llm_model)

        # Step 2.5: Get user approval and iterate if needed
        final_markdown = _get_user_approval_for_markdown(markdown_file, api_key, llm_model)

        # Step 3: Create and save the single markdown file with optimal placement
        file_path = save_markdown_file(final_markdown, urls, vault_path)

        # Step 4: Print the generated markdown to console
        _print_md_to_console(final_markdown, file_path)

        return {
            "success": True,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Get user approval for generated markdown and iterate if needed
def _get_user_approval_for_markdown(markdown_content: str, api_key: str, llm_model: str) -> str:
    console = Console()
    current_markdown = markdown_content

    while True:
        # Show the current markdown to the user
        console.print("\n[dim italic]Generated markdown:[/dim italic]\n")
        markdown_display = Markdown(current_markdown)
        console.print(markdown_display)
        console.print("\n[dim]------[/dim]\n")

        # Ask for user approval
        user_input = prompt("Are you satisfied with this markdown? (y/yes to approve, or provide feedback): ").strip().lower()

        # If user approves, return the current markdown
        if user_input in ['y', 'yes']:
            return current_markdown

        # Otherwise, user provided feedback - ask AI to revise
        console.print("\n[dim italic]Revising markdown based on your feedback...[/dim italic]\n")

        revision_prompt = f"""You created a markdown document for a user, however they have some comments. Please adhere accordingly: {user_input}
        The following is the markdown you created, please adjust:
        {current_markdown}"""

        # Get revised markdown from AI
        revised_response = call_openai_api(revision_prompt, api_key, llm_model)

        # Extract markdown content using existing function
        current_markdown = _extract_markdown_content(revised_response)

def _print_md_to_console(markdown_content: str, file_path: str) -> None:
    console = Console()
    markdown = Markdown(markdown_content)
    console.print(markdown)
    console.print("\n[dim]------[/dim]")
    console.print(f"Created new note:\n{file_path}\n")