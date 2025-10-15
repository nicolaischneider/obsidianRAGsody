from rich.console import Console
from rich.markdown import Markdown
from typing import List
from pathlib import Path
from .core.website_scraper import scrape_url
from .core.page_generator import generate_markdown_from_content
from .core.optimal_file_organizer import save_markdown_file

def _print_md_to_console(markdown_content: str, file_path: str) -> None:
    console = Console()
    markdown = Markdown(markdown_content)
    console.print(markdown)
    console.print("\n[dim]------[/dim]")
    console.print(f"Created new note:\n{file_path}\n")

# Main function to process URLs and create markdown files in the vault
def generate_markdown_from_urls(urls: List[str], prompt: str, vault_path: str, api_key: str, llm_model: str) -> str:

    try:
        # Step 1: Scrape content from all URLs
        all_content = []
        for url in urls:
            content = _scrape_url_content(url)
            all_content.append({"url": url, "content": content})

        # Step 2: Generate combined markdown summary using AI
        markdown_file = _generate_combined_markdown_summary(all_content, prompt, api_key, llm_model)

        # Step 3: Create and save the single markdown file with optimal placement
        file_path = save_markdown_file(markdown_file, urls, vault_path)

        # Step 4: Print the generated markdown to console
        _print_md_to_console(markdown_file, file_path)

        return {
            "success": True,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Scrape content from a given URL
def _scrape_url_content(url: str) -> str:
    return scrape_url(url)


# Generate combined markdown summary from all URL contents using AI
def _generate_combined_markdown_summary(all_content: List[dict], prompt: str, api_key: str, llm_model: str) -> str:
    return generate_markdown_from_content(all_content, prompt, api_key, llm_model)


