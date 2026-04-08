import json
import os
from pathlib import Path
from dotenv import load_dotenv

from reddit_scraper import scrape_reddit
from script_generator import generate_script
from voiceover_generator import generate_voiceover
from video_assembler import assemble_video
from content_filter import should_skip_post
from state_manager import load_processed_post_ids, mark_processed


load_dotenv()


def _is_true(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _load_mock_posts(sample_posts_path):
    with open(sample_posts_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError("Mock posts file must be a JSON array.")
    return payload


def _require_env(keys):
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


def _preflight(use_mock_data, project_root):
    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    background_video_path = project_root / "assets" / "background.mp4"
    if not background_video_path.exists():
        raise FileNotFoundError(
            f"Missing background video at {background_video_path}. Add a file before running."
        )

    _require_env(["OPENAI_API_KEY", "ELEVENLABS_API_KEY", "ELEVENLABS_VOICE_ID"])
    if not use_mock_data:
        _require_env(["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"])

    return output_dir, background_video_path


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    use_mock_data = _is_true(os.getenv("USE_MOCK_DATA", "false"))
    sample_posts_path = Path(os.getenv("SAMPLE_POSTS_PATH", str(project_root / "data" / "sample_posts.json")))
    state_path = project_root / "output" / "processed_posts.json"

    output_dir, background_video_path = _preflight(use_mock_data, project_root)
    processed_ids = load_processed_post_ids(state_path)

    print("Automation pipeline initialized.")
    print(f"Mode: {'mock data' if use_mock_data else 'reddit api'}")

    if use_mock_data:
        posts = _load_mock_posts(sample_posts_path)
    else:
        subreddits = ["AITA", "relationships"]
        posts = scrape_reddit(subreddits, limit=5)

    processed_count = 0
    skipped_count = 0

    for i, post in enumerate(posts):
        post_id = str(post.get("id") or f"mock-{i}")
        if post_id in processed_ids:
            print(f"Skipping post {post_id}: already processed.")
            skipped_count += 1
            continue

        should_skip, reason = should_skip_post(post)
        if should_skip:
            print(f"Skipping post {post_id}: {reason}.")
            skipped_count += 1
            continue

        try:
            script = generate_script(post.get("content", ""))

            voiceover = generate_voiceover(script)
            voiceover_path = output_dir / f"voiceover_{post_id}.mp3"
            with open(voiceover_path, "wb") as f:
                f.write(voiceover)

            output_video_path = output_dir / f"video_{post_id}.mp4"
            assemble_video(str(voiceover_path), str(background_video_path), str(output_video_path))

            mark_processed(state_path, post_id)
            processed_ids.add(post_id)
            processed_count += 1
            print(f"Video created successfully: {output_video_path}")
        except Exception as e:
            print(f"Error processing post {post_id}: {e}")

    print(f"Run complete. Processed: {processed_count}, Skipped: {skipped_count}, Total fetched: {len(posts)}")
