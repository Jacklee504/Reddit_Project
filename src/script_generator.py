import os
# Required dependencies
import openai

def generate_script(post_content):
    """
    Generate a script from Reddit post content using OpenAI API.

    Args:
        post_content (str): Content of the Reddit post.

    Returns:
        str: Generated script.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Transform Reddit posts into engaging 45-60 second video scripts with a hook in the first 3 seconds."},
            {"role": "user", "content": post_content}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content
