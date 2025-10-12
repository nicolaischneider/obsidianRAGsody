# Orchestrates the generation and storage of markdown files in vault from various sources.

from typing import List
from pathlib import Path
from .core.website_scraper import scrape_url
from .core.page_generator import generate_markdown_from_content


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

        print(combined_markdown)  # For debugging

        # Step 3: Determine optimal folder placement
        folder_path = _determine_folder_placement(urls, all_content, vault_path)

        # Step 4: Create and save the single markdown file
        file_path = _save_markdown_file(combined_markdown, urls, folder_path)

        return f"Created combined note: {file_path}"

    except Exception as e:
        return f"Failed to process URLs: {str(e)}"


# Scrape content from a given URL
def _scrape_url_content(url: str) -> str:
    return scrape_url(url)


# Generate combined markdown summary from all URL contents using AI
def _generate_combined_markdown_summary(all_content: List[dict], prompt: str, api_key: str) -> str:
    return generate_markdown_from_content(all_content, prompt, api_key)


# Determine the best folder for the new markdown file
def _determine_folder_placement(urls: List[str], all_content: List[dict], vault_path: str) -> Path:
    # TODO: Implement intelligent folder placement algorithm
    vault = Path(vault_path)
    return vault / "generated"  # Default folder for now


# Save markdown content to a file in the specified folder
def _save_markdown_file(markdown_content: str, urls: List[str], folder_path: Path) -> str:
    # TODO: Implement file saving with proper filename generation
    #folder_path.mkdir(exist_ok=True)
    #filename = "combined_note.md"  # Placeholder filename
    #file_path = folder_path / filename

    # TODO: Actually write the file
    return ""