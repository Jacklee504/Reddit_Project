from moviepy.editor import *

def assemble_video(voiceover_path, background_video_path, output_path):
    """
    Assemble a video using a voiceover and background footage.

    Args:
        voiceover_path (str): Path to the voiceover MP3 file.
        background_video_path (str): Path to the background video file.
        output_path (str): Path to save the assembled video.

    Returns:
        None
    """
    # Load voiceover and background video
    voiceover = AudioFileClip(voiceover_path)
    background_video = VideoFileClip(background_video_path)

    # Set the duration of the background video to match the voiceover
    background_video = background_video.set_duration(voiceover.duration)

    # Set the voiceover as the audio of the video
    final_video = background_video.set_audio(voiceover)

    # Write the final video to the output path
    final_video.write_videofile(output_path, codec="libx264", fps=30)
