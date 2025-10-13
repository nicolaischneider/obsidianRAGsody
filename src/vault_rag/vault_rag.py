# Builds the RAG (Retrieval-Augmented Generation) model for querying the vault using LlamaIndex
# This module creates a RAG system that can index all markdown files in your Obsidian vault
# and answer questions about the content using semantic search + LLM

import os
import logging
import warnings
from pathlib import Path
from typing import Optional

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore

# Disable HTTP request logging
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Suppress Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.*")

class VaultRAG:

    # Initialize RAG system for Obsidian vault processing
    def __init__(self, vault_path: str, api_key: str, llm_model: str):
        # Store the path to your Obsidian vault (where your .md files are)
        self.vault_path = Path(vault_path)
        # OpenAI API key for LLM and embedding calls
        self.api_key = api_key
        # OpenAI model to use
        self.llm_model = llm_model
        # The actual RAG index (starts as None, built later)
        self.index: Optional[VectorStoreIndex] = None
        # Set up LlamaIndex configuration
        self._setup_llama_config()

    # Configure LlamaIndex settings for OpenAI
    def _setup_llama_config(self):
        # Set up OpenAI LLM (the "brain" that generates answers)
        Settings.llm = OpenAI(
            model=self.llm_model,
            api_key=self.api_key,
            temperature=0.1  # Low temperature for more consistent answers
        )

        # Set up OpenAI embeddings (converts text to searchable vectors)
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=self.api_key
        )

    # Load documents from the Obsidian vault
    def _load_documents(self):
        # Load all markdown files from the vault
        reader = SimpleDirectoryReader(
            input_dir=str(self.vault_path),
            required_exts=[".md"],  # Only process .md files
            recursive=True  # Include subfolders
        )

        documents = reader.load_data()

        # Import here to avoid circular imports
        from rich.console import Console
        console = Console()
        console.print(f"[dim italic]Loaded {len(documents)} documents[/dim italic]")

        if len(documents) == 0:
            console.print("[red]WARNING: No documents loaded! Check your vault path.[/red]")

        return documents

    # Build the RAG index from vault documents
    def build_rag(self):
        # If already built, just return it (avoid rebuilding)
        if self.index is not None:
            return self.index

        # Load all documents from the vault
        documents = self._load_documents()

        # Build index fresh every time (no caching for now)
        self.index = VectorStoreIndex.from_documents(documents)
        return self.index

    # Query the RAG system with a question about your vault content
    def query(self, prompt: str) -> str:
        # Build RAG if not already done
        if self.index is None:
            self.build_rag()

        try:
            # Create a query engine from the index
            query_engine = self.index.as_query_engine(
                similarity_top_k=5,  # Return top 5 most relevant chunks
                response_mode="tree_summarize"
            )

            # Add instruction to format response as markdown
            markdown_prompt = f"{prompt}\n\nPlease format your response using markdown syntax (headers, lists, bold text, etc.) for better readability."

            # Query the engine and get response
            response = query_engine.query(markdown_prompt)
            response_str = str(response).strip()

            if not response_str or response_str.lower() in ['empty response', 'none', '']:
                return "No relevant information found in the vault for your query."

            return response_str

        except Exception as e:
            return f"Error querying RAG: {e}"

    # Find most similar documents to given content for folder placement
    def find_similar_documents(self, content: str, top_k: int = 3) -> list:
        """Find most similar documents and return their file paths."""
        if self.index is None:
            self.build_rag()

        try:
            # Create a retriever to get similar documents
            retriever = self.index.as_retriever(similarity_top_k=top_k)

            # Retrieve similar documents
            nodes = retriever.retrieve(content)

            # Extract file paths from the nodes
            similar_files = []
            for node in nodes:
                # The file path is stored in the node metadata
                if hasattr(node, 'metadata') and 'file_path' in node.metadata:
                    file_path = node.metadata['file_path']
                    similar_files.append(file_path)
                elif hasattr(node, 'node') and hasattr(node.node, 'metadata'):
                    file_path = node.node.metadata.get('file_path', '')
                    if file_path:
                        similar_files.append(file_path)

            return similar_files

        except Exception as e:
            print(f"Error finding similar documents: {e}")
            return []


# Global RAG instance - singleton pattern to save memory and processing
_vault_rag: Optional[VaultRAG] = None


# Initialize the global RAG instance - call this once when your app starts
def initialize_rag(vault_path: str, api_key: str, llm_model: str) -> VaultRAG:
    global _vault_rag
    if _vault_rag is None:
        # Import here to avoid circular imports
        from rich.console import Console
        console = Console()
        console.print("[dim italic]Initializing RAG system...[/dim italic]")

        _vault_rag = VaultRAG(vault_path, api_key, llm_model)
        _vault_rag.build_rag()

        console.print("[dim italic]RAG system ready![/dim italic]")
    return _vault_rag


# Simple function to query the vault once RAG is initialized
def query_vault(prompt: str) -> str:
    if _vault_rag is None:
        return "RAG system not initialized. Please run initialize_rag() first."
    return _vault_rag.query(prompt)


# Find similar documents for optimal folder placement
def find_similar_files(content: str, top_k: int = 3) -> list:
    if _vault_rag is None:
        return []
    return _vault_rag.find_similar_documents(content, top_k)