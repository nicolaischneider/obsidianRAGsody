# Page Generator for given data as markdown

from typing import List
from .ai_caller import call_openai_api

# Generate markdown content from scraped URLs using OpenAI
def generate_markdown_from_content(all_content: List[dict], prompt: str, api_key: str, llm_model: str) -> str:
    # Prepare the content for the AI prompt
    content_text = _prepare_content_for_ai(all_content)

    # Create the AI prompt
    ai_prompt = _create_ai_prompt(content_text, prompt)

    # Call OpenAI to generate markdown
    response = call_openai_api(ai_prompt, api_key, llm_model)

    # Clean the response to extract only markdown content
    cleaned_response = _extract_markdown_content(response)

    return cleaned_response

# Prepare scraped content for AI processing
def _prepare_content_for_ai(all_content: List[dict]) -> str:
    prepared_content = []

    for i, item in enumerate(all_content, 1):
        url = item["url"]
        content = item["content"]

        section = f"=== Source {i}: {url} ===\n{content}\n"
        prepared_content.append(section)

    return "\n".join(prepared_content)

# Create the prompt for OpenAI
def _create_ai_prompt(content_text: str, user_prompt: str) -> str:
    system_prompt = f"""I have fetched content from the given URLs. The content can be found below.
    {content_text}
    Based on this content and the following request: "{user_prompt}"
    Create a markdown document. Use proper markdown formatting including headers, lists, bold text, links, etc. Return ONLY the markdown content without any introduction or explanation."""
    return system_prompt

# Extract markdown content from AI response, removing outer code blocks
def _extract_markdown_content(response: str) -> str:
    cleaned = response.strip()

    # Look for ```markdown anywhere in the response (not just at start)
    markdown_start = cleaned.find('```markdown')
    if markdown_start != -1:
        # Find the closing ``` after the ```markdown
        content_start = markdown_start + 11  # length of '```markdown'
        end_marker = cleaned.find('```', content_start)
        if end_marker != -1:
            # Extract content between ```markdown and closing ```
            cleaned = cleaned[content_start:end_marker].strip()
            return cleaned

    # Check if response starts with markdown code blocks
    if cleaned.startswith('```markdown'):
        # Find the last closing ``` (working backwards)
        end_marker = cleaned.rfind('```')
        if end_marker > 11:  # More than just the opening ```markdown
            # Extract content between ```markdown and the last closing ```
            cleaned = cleaned[11:end_marker].strip()

    elif cleaned.startswith('```'):
        # Handle case where it's just ``` without markdown
        end_marker = cleaned.rfind('```')
        if end_marker > 3:
            cleaned = cleaned[3:end_marker].strip()

    return cleaned