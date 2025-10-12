# Website Scraper for extracting information from web pages

import requests
from bs4 import BeautifulSoup
from typing import Optional


# Scrape and extract clean text content from a URL
def scrape_url(url: str) -> str:
    try:
        # Send GET request with headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title = _extract_title(soup)

        # Extract main content
        content = _extract_main_content(soup)

        # Combine title and content
        full_content = f"Title: {title}\n\n{content}"

        return full_content.strip()

    except Exception as e:
        return f"Error scraping {url}: {str(e)}"


# Extract page title
def _extract_title(soup: BeautifulSoup) -> str:
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()
    return "No title found"


# Extract main content from the page
def _extract_main_content(soup: BeautifulSoup) -> str:
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
        script.decompose()

    # Try to find main content areas first
    main_content = _find_main_content_area(soup)

    if main_content:
        text = main_content.get_text()
    else:
        # Fallback to body text
        text = soup.get_text()

    # Clean up the text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    return text


# Try to find the main content area of the page
def _find_main_content_area(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    # Common selectors for main content
    content_selectors = [
        'main',
        'article',
        '[role="main"]',
        '.content',
        '.post-content',
        '.entry-content',
        '.article-content',
        '#content',
        '#main-content'
    ]

    for selector in content_selectors:
        element = soup.select_one(selector)
        if element:
            return element

    return None