import os


DEFAULT_BANNED_KEYWORDS = [
    "suicide",
    "self-harm",
    "kill myself",
    "graphic violence",
    "hate crime",
]


def _as_int(value, fallback):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _keyword_list_from_env():
    configured = os.getenv("BANNED_KEYWORDS", "")
    if not configured.strip():
        return DEFAULT_BANNED_KEYWORDS
    return [item.strip().lower() for item in configured.split(",") if item.strip()]


def should_skip_post(post):
    """
    Returns (True, reason) when a post should be filtered out.
    """
    title = (post.get("title") or "").strip()
    content = (post.get("content") or "").strip()
    combined = f"{title}\n{content}".lower()

    if post.get("over_18"):
        return True, "nsfw"
    if not content:
        return True, "empty_content"
    if "[deleted]" in combined or "[removed]" in combined:
        return True, "deleted_or_removed"

    min_score = _as_int(os.getenv("MIN_POST_SCORE", "100"), 100)
    min_comments = _as_int(os.getenv("MIN_POST_COMMENTS", "15"), 15)
    if _as_int(post.get("score"), 0) < min_score:
        return True, "low_score"
    if _as_int(post.get("num_comments"), 0) < min_comments:
        return True, "low_comments"

    for keyword in _keyword_list_from_env():
        if keyword and keyword in combined:
            return True, f"blocked_keyword:{keyword}"

    return False, "ok"
