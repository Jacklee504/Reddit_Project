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
    reddit = praw.Reddit(
        client_id="your_client_id",
        client_secret="your_client_secret",
        user_agent="your_user_agent"
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
