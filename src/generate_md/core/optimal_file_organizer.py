# Optimal File Organizer for Obsidian Vault

from pathlib import Path
from typing import List
from ...vault_rag.vault_rag import find_similar_files


# Generate filename from markdown title (first line)
def _generate_filename_from_title(markdown_content: str) -> str:
    lines = markdown_content.strip().split('\n')

    if not lines:
        return "untitled.md"

    first_line = lines[0].strip()

    # Check if first line is a markdown header
    if first_line.startswith('#'):
        # Remove the # and any extra spaces
        title = first_line.lstrip('#').strip()
    else:
        # Use first line as is
        title = first_line

    # Convert to filename: lowercase, replace spaces with underscores, remove special chars
    filename = title.lower()
    filename = filename.replace(' ', '_')

    # Remove special characters, keep only alphanumeric, underscores, and hyphens
    filename = ''.join(c for c in filename if c.isalnum() or c in '_-')

    # Ensure it's not empty
    if not filename:
        filename = "untitled"

    return f"{filename}.md"

# Find the optimal folder for the new markdown file using RAG similarity
def find_optimal_folder(markdown_content: str, vault_path: str) -> str:
    vault = Path(vault_path)

    # Use RAG to find most similar existing files
    similar_files = find_similar_files(markdown_content, top_k=3)

    if similar_files:
        # Take the first (most similar) file and get its directory
        most_similar_file = Path(similar_files[0])
        optimal_folder = most_similar_file.parent

        # Make sure the folder exists and is within the vault
        if optimal_folder.exists() and str(optimal_folder).startswith(str(vault)):
            return str(optimal_folder)

    # Fallback to RAGsody_created if no similar files found or path issues
    return str(vault / "RAGsody_created")

# Save markdown content to a specific folder
def save_markdown_to_folder(markdown_content: str, folder_path: str) -> str:
    folder = Path(folder_path)
    filename = _generate_filename_from_title(markdown_content)

    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / filename

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return str(file_path)