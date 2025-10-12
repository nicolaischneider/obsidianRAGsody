# Orchestrates the generation and storage of markdown files in vault from various sources.

from typing import List
from pathlib import Path
from .core.website_scraper import scrape_url
from .core.page_generator import generate_markdown_from_content
from .core.optimal_file_organizer import save_markdown_file


# Main function to process URLs and create markdown files in the vault
def generate_markdown_from_urls(urls: List[str], prompt: str, vault_path: str, api_key: str) -> str:

    try:
        # Step 1: Scrape content from all URLs
        all_content = []
        for url in urls:
            content = _scrape_url_content(url)
            all_content.append({"url": url, "content": content})

        # Step 2: Generate combined markdown summary using AI
        combined_markdown = _generate_combined_markdown_summary(all_content, prompt, api_key)

        # Step 3: Create and save the single markdown file with optimal placement
        file_path = save_markdown_file(combined_markdown, urls, vault_path)

        return {
            "success": True,
            "file_path": file_path,
            "markdown_content": combined_markdown
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
def _generate_combined_markdown_summary(all_content: List[dict], prompt: str, api_key: str) -> str:
    return generate_markdown_from_content(all_content, prompt, api_key)


