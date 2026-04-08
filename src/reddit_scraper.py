import praw
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_reddit(subreddits, limit=10):
    """
    Scrape top posts from specified subreddits.

    Args:
        subreddits (list): List of subreddit names to scrape.
        limit (int): Number of posts to fetch per subreddit.

    Returns:
        list: List of top posts with title and content.
    """
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not client_id or not client_secret or not user_agent:
        raise ValueError(
            "Missing Reddit credentials. Set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT."
        )

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    posts = []
    for subreddit in subreddits:
        subreddit_obj = reddit.subreddit(subreddit)
        for submission in subreddit_obj.top(limit=limit):
            posts.append({
                "title": submission.title,
                "content": submission.selftext
            })

    return posts
