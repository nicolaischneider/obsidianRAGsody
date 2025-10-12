# Interprets user requests and routes them to the appropriate handlers.

import re
from enum import Enum
from typing import List, Union
from dataclasses import dataclass


class RequestType(Enum):
    RAG_VAULT = "rag_vault"
    GENERATE_NEW_MARKDOWN = "generate_new_markdown"


@dataclass
class RagVaultRequest:
    prompt: str


@dataclass
class GenerateNewMarkdownRequest:
    prompt: str
    urls: List[str]


RequestResult = Union[RagVaultRequest, GenerateNewMarkdownRequest]


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text using regex."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)


def interpret_request(user_input: str) -> RequestResult:
    """
    Analyze user input and determine if they want to:
    1. Query existing vault (RAG)
    2. Generate new markdown from URLs
    """
    urls = extract_urls(user_input)

    if urls:
        return GenerateNewMarkdownRequest(prompt=user_input, urls=urls)
    else:
        return RagVaultRequest(prompt=user_input)