# AI caller for OpenAI API interactions
import openai

# Call OpenAI API with a given prompt
def call_openai_api(prompt: str, api_key: str, llm_model: str) -> str:
    try:
        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3  # Lower temperature for more consistent output
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating content: {str(e)}"