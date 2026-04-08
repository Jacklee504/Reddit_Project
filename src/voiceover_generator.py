import requests

def generate_voiceover(script_text):
    """
    Generate a voiceover from the script text using ElevenLabs API.

    Args:
        script_text (str): The script to convert into voiceover.

    Returns:
        bytes: Audio file content in MP3 format.
    """
    api_url = "https://api.elevenlabs.io/v1/text-to-speech"
    api_key = "your_elevenlabs_api_key"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": script_text,
        "voice": "default",
        "format": "mp3"
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Voiceover generation failed: {response.text}")
