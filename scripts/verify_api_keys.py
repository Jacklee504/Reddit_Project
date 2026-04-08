import os
import praw
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify PRAW (Reddit) API Key
try:
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="api_key_verification"
    )
    reddit.user.me()  # Attempt to fetch the authenticated user
    print("PRAW API Key: Verified")
except Exception as e:
    print(f"PRAW API Key: Verification failed - {e}")

# Verify OpenAI API Key
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.list()  # Attempt to list available models
    print("OpenAI API Key: Verified")
except Exception as e:
    print(f"OpenAI API Key: Verification failed - {e}")

# Add additional API key verifications here if needed

print("API Key verification completed.")
