# Obsidian RAGsody

CLI tool for intelligent Obsidian vault interaction with two main features:

## Features

### 1. Vault Querying
Ask questions about your vault content using natural language.
- "What did I write about machine learning?"
- "Show me my notes on productivity"

### 2. URL to Note
Create markdown files from URLs. Files are saved to either the root or to optimal folders based on content similarity.
- "Create a note from https://example.com about AI trends"
- "Summarize this article: https://blog.example.com/post"

## Installation

```bash
pipx install git+https://github.com/nicolaischneider/obsidianRAGsody.git
obsidian-ragsody
```

Or run with uv:
```bash
uv venv
source .venv/bin/activate
uv sync
uv run python src/main.py
```

> **Warning**: On first run, you will be asked to enter 
> * your *Obsidian vault path* (eg "/Users/your_username/obsidian")
> * your *OpenAI API key*

## Tech Stack

- **[LlamaIndex](https://github.com/run-llama/llama_index)**: RAG framework for vault querying
- **[OpenAI](https://github.com/openai/openai-python)**: GPT-4o-mini for responses, text-embedding-3-small for search
- **[requests](https://github.com/psf/requests) + [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)**: Web scraping
- **[rich](https://github.com/Textualize/rich)**: Beautiful markdown rendering
- **[prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)**: Interactive CLI

## Outlook

### Future Features
- [x] **Automatic Ordering of new files**: Automatically organize newly created markdown files into appropriate folders.
- [x] **Review of files and folder path before adding to vault**: Implement a review step for new files before they are added to the vault.
- [x] **LLM Model Selection**: Select the Open AI model of your choice
- [x] **Reload RAG index after creating new notes**: Automatically update the RAG index after new notes are created.
- [ ] **Install**: Install the tool in your system for easy access

### Performance Improvements
- [ ] **Faster parsing**: Upgrade to `selectolax` for 10x faster HTML parsing
- [x] **Index caching**: Persistent RAG index storage for faster startup
- [ ] **Parallel scraping**: Concurrent URL processing for multiple links

## Requirements

- Python 3.13+
- OpenAI API key
- Obsidian vault (local folder with .md files)