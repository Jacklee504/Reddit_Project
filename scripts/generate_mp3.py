import numpy as np
from scipy.io.wavfile import write
import os
from pydub import AudioSegment

def generate_sine_wave_mp3(output_path, duration=5, frequency=440, sample_rate=44100):
    """
    Generate a sine wave MP3 file.

    Args:
        output_path (str): Path to save the MP3 file.
        duration (int): Duration of the audio in seconds.
        frequency (int): Frequency of the sine wave in Hz.
        sample_rate (int): Sample rate in Hz.

    Returns:
        None
    """
    # Generate a sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Save as WAV file
    wav_path = output_path.replace('.mp3', '.wav')
    write(wav_path, sample_rate, (audio * 32767).astype(np.int16))

    # Convert WAV to MP3
    sound = AudioSegment.from_wav(wav_path)
    sound.export(output_path, format="mp3")

    # Remove the temporary WAV file
    os.remove(wav_path)

if __name__ == "__main__":
    output_path = "../tests/assets/test_voiceover.mp3"
    generate_sine_wave_mp3(output_path)
    print(f"Generated MP3 file at: {output_path}")
