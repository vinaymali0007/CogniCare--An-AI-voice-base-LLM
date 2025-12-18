import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os 

ffmpeg_path = r"C:\ffmpeg-2025-07-28-git-dc8e753f32-full_build\bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def record_audio (file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

audio_filepath="patient_voice_test_for_patient.mp3"
#record_audio(file_path=audio_filepath)

from groq import Groq

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.environ.get("Groq_APIkey")
stt_model_name="whisper-large-v3"
def transcribe_with_groq(stt_model_name: str, audio_filepath: str, GROQ_API_KEY: str):
    """
    Transcribes an audio file using the specified Groq STT model,
    incorporating the file handling and response_format from your standalone code.

    Args:
        stt_model_name (str): The name of the Groq STT model (e.g., "whisper-large-v3").
        audio_filepath (str): The path to the audio file to transcribe.
        api_key (str): Your Groq API key.

    Returns:
        str: The transcribed text.
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    # --- MODIFIED FILE HANDLING AND PARAMETERS ---
    # Use os.path.basename(audio_filepath) for the filename in the tuple
    # Read the file content into memory
    with open(audio_filepath, "rb") as file_obj:
        file_content = file_obj.read()
        transcription = client.audio.transcriptions.create(
            file=(os.path.basename(audio_filepath), file_content), # File as tuple (filename, bytes)
            model=stt_model_name,
            response_format="verbose_json", # Explicitly set verbose_json
            language="en" # Keep language parameter as it was in your function
        )
    # --- END MODIFIED ---

    return transcription.text