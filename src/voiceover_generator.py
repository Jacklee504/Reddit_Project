import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_voiceover(script_text, voice_id=None):
    """
    Generate a voiceover from the script text using ElevenLabs API.

    Args:
        script_text (str): The script to convert into voiceover.
        voice_id (str | None): ElevenLabs voice ID. Falls back to ELEVENLABS_VOICE_ID.

    Returns:
        bytes: Audio file content in MP3 format.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    resolved_voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID")
    if not api_key:
        raise ValueError("Missing ELEVENLABS_API_KEY environment variable.")
    if not resolved_voice_id:
        raise ValueError("Missing voice ID. Set ELEVENLABS_VOICE_ID or pass voice_id.")

    api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{resolved_voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json"
    }

    payload = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(api_url, json=payload, headers=headers, timeout=60)

    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Voiceover generation failed: {response.text}")
