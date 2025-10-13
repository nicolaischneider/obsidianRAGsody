# Obsidian RAGsody

CLI tool for intelligent Obsidian vault interaction with two main features:

## Features

### 1. Vault Querying
Ask questions about your vault content using natural language.
- "What did I write about machine learning?"
- "Show me my notes on productivity"

### 2. URL to Note
Create markdown files from URLs. Files saved to `RAGsody_created/` folder.
- "Create a note from https://example.com about AI trends"
- "Summarize this article: https://blog.example.com/post"

## Setup

### First Time Setup

```bash
uv venv
source .venv/bin/activate
uv init
uv add llama-index-core llama-index-llms-openai llama-index-embeddings-openai
uv add prompt-toolkit python-dotenv requests beautifulsoup4 rich
uv run python main.py
```

### Load

```bash
source .venv/bin/activate
uv run python main.py
```

On first run, enter your *Obsidian vault path* and *OpenAI API key*.

## Tech Stack

- **[LlamaIndex](https://github.com/run-llama/llama_index)**: RAG framework for vault querying
- **[OpenAI](https://github.com/openai/openai-python)**: GPT-4o-mini for responses, text-embedding-3-small for search
- **[requests](https://github.com/psf/requests) + [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)**: Web scraping
- **[rich](https://github.com/Textualize/rich)**: Beautiful markdown rendering
- **[prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)**: Interactive CLI

## Outlook

### Future Features
- [ ] **Automatic Ordering of new files**: Automatically organize newly created markdown files into appropriate folders.
- [ ] **Review of files before adding to vault**: Implement a review step for new files before they are added to the vault.
- [ ] **LLM Model Selection**: Select the Open AI model of your choice
- [ ] **Install**: Install the tool in your system for easy access

### Performance Improvements
- [ ] **Faster parsing**: Upgrade to `selectolax` for 10x faster HTML parsing
- [ ] **Index caching**: Persistent RAG index storage for faster startup
- [ ] **Parallel scraping**: Concurrent URL processing for multiple links