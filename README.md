# Obsidian RAGsody

A powerful CLI tool for intelligent interaction with your Obsidian vault. Ask questions about your notes using natural language and get AI-powered answers based on your vault content.

## Features

### 1. Vault Querying (✅ Working)
Ask questions about your Obsidian vault content using LlamaIndex and OpenAI. The system:
- Indexes all markdown files in your vault
- Uses semantic search to find relevant content
- Generates contextual answers using GPT-4o-mini

**Example queries:**
- "What did I write about machine learning?"
- "Show me my notes on productivity"
- "What are my thoughts on Python?"

### 2. URL to Note (🚧 Coming Soon)
Create markdown files from URLs with smart folder placement.

## How It Works

1. **Startup**: Indexes all `.md` files in your Obsidian vault using LlamaIndex
2. **Query Processing**: Analyzes your input to determine if you want to query existing content or create new content
3. **Semantic Search**: Finds relevant content using OpenAI embeddings
4. **AI Response**: Generates comprehensive answers using GPT-4o-mini

## Setup

```bash
# Install dependencies
uv venv
uv add llama-index-core llama-index-llms-openai llama-index-embeddings-openai llama-index-readers-file
uv add prompt-toolkit python-dotenv

# Run the tool
uv run python main.py
```

## Configuration

On first run, you'll be prompted to enter:
- **Obsidian Vault Path**: Path to your Obsidian vault directory
- **OpenAI API Key**: Your OpenAI API key for LLM and embeddings

These are saved in a `.env` file for future use.

## Tech Stack

- **Python 3.10+**
- **LlamaIndex**: RAG framework for document indexing and querying
- **OpenAI**: GPT-4o-mini for responses, text-embedding-3-small for search
- **prompt-toolkit**: Interactive CLI interface