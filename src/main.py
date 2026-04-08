# Entry point for the automation pipeline

from reddit_scraper import scrape_reddit
from script_generator import generate_script
from voiceover_generator import generate_voiceover
from video_assembler import assemble_video

if __name__ == "__main__":
    print("Automation pipeline initialized.")

    # Step 1: Scrape Reddit for top posts
    subreddits = ["AITA", "relationships"]
    posts = scrape_reddit(subreddits, limit=5)

    for i, post in enumerate(posts):
        try:
            # Step 2: Generate script from post content
            script = generate_script(post["content"])

            # Step 3: Generate voiceover from script
            voiceover = generate_voiceover(script)
            voiceover_path = f"output/voiceover_{i}.mp3"
            with open(voiceover_path, "wb") as f:
                f.write(voiceover)

            # Step 4: Assemble video
            background_video_path = "assets/background.mp4"  # Replace with actual path
            output_video_path = f"output/video_{i}.mp4"
            assemble_video(voiceover_path, background_video_path, output_video_path)

            print(f"Video {i} created successfully: {output_video_path}")
        except Exception as e:
            print(f"Error processing post {i}: {e}")
