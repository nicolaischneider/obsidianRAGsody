# Optimal File Organizer for Obsidian Vault

from pathlib import Path
from typing import List


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

# Find the optimal folder for the new markdown file
def _find_optimal_folder(urls: List[str], markdown_content: str, vault_path: Path) -> Path:
    # TODO: Implement intelligent folder placement algorithm
    # For now, create a "generated" folder
    return vault_path / "generated"

# Save markdown content to a file in RAGsody_created folder
def save_markdown_file(markdown_content: str, urls: List[str], vault_path: str) -> str:
    vault = Path(vault_path)
    folder_path = vault / "RAGsody_created"

    filename = _generate_filename_from_title(markdown_content)

    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / filename

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return str(file_path)