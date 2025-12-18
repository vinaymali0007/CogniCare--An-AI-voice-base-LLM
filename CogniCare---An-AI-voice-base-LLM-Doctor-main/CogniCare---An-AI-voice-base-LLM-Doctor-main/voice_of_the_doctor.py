import os
import subprocess
from gtts import gTTS
from dotenv import load_dotenv
load_dotenv()

# --- ElevenLabs Imports ---
# Make sure you have the latest elevenlabs library: pip install elevenlabs
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice # Needed for the new API format's 'voice' parameter
import elevenlabs # For elevenlabs.save

# --- API Keys ---
# IMPORTANT: Check your .env file for the exact name.
# Using ELEVENLABS_API_KEY (all caps, underscore) is standard.
ELEVENLABS_API_KEY = os.environ.get("Elevenlabs_APIkey") 
# If your .env uses "Elevenlabs_APIkey", change it here to match or update your .env
# ELEVENLABS_API_KEY = os.environ.get("Elevenlabs_APIkey")


# --- gTTS Old Function ---
def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)




# --- ElevenLabs Old Function (API Format Modified) ---
def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    # --- MODIFIED API CALL FORMAT ---
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="pqHfZKP75CvOlQylNhV4", # Convert voice ID string to Voice object
        model_id="eleven_multilingual_v2", # 'model' parameter becomes 'model_id'
        output_format="mp3_22050_32", # 'output_format' remains the same
    )
    # --- END MODIFIED API CALL ---
    elevenlabs.save(audio, output_filepath)

# Test call for the old function (kept as per your structure)
#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

# --- Playback Imports ---
import platform
import logging # Already imported at top, but keeping for clarity of original section

# --- Logging Configuration (if not already at the top) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# --- gTTS Function with Playback ---
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    ffmpeg_path = r"C:\ffmpeg-2025-07-28-git-dc8e753f32-full_build\bin"
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True) # Added check=True
        elif os_name == "Windows":  # Windows
            # --- MODIFIED: Use ffplay for MP3 playback on Windows ---
            # Make sure FFMPEG_PATH (or ffmpeg_path) is defined at the top of your script.
            ffplay_exe_path = os.path.join(ffmpeg_path, "ffplay.exe") 
            if not os.path.exists(ffplay_exe_path):
                print(f"Error: ffplay.exe not found at {ffplay_exe_path}. Cannot play MP3.")
                return # Exit the function if ffplay is not found
            subprocess.run([ffplay_exe_path, '-nodisp', '-autoexit', output_filepath], check=True)
            # --- END MODIFIED ---
        elif os_name == "Linux":  # Linux
            # 'aplay' is typically for WAV. Consider 'mpg123' or 'ffplay' for MP3.
            subprocess.run(['aplay', output_filepath], check=True) # Added check=True
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Test call for the function. Output filename is "elevenlabs_testing.mp3".
# Note: This will overwrite any ElevenLabs output file with the same name.
#text_to_speech_with_gtts(input_text, output_filepath="elevenlabs_testing.mp3")
# --- ElevenLabs Function with Playback (API Format Modified) ---
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    # --- API CALL FORMAT (as fixed in previous turns) ---
    audio = client.text_to_speech.convert(
        text=input_text,
        # Using the specific voice_id you provided.
        # Note: If your SDK is very old, it might expect 'voice' instead of 'voice_id'.
        # However, for recent SDKs (v1.x.x+), voice=Voice(voice_id="ID") is standard.
        voice_id="pqHfZKP75CvOlQylNhV4",
        model_id="eleven_multilingual_v2",
        output_format="mp3_22050_32",
    )
    # --- END API CALL ---
    elevenlabs.save(audio, output_filepath)
    ffmpeg_path = r"C:\ffmpeg-2025-07-28-git-dc8e753f32-full_build\bin"
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True) # Added check=True for robustness
        elif os_name == "Windows":  # Windows
            # --- MODIFIED: Use ffplay for MP3 playback on Windows ---
            # Ensure ffmpeg_path (containing ffplay.exe) is defined globally in your script.
            ffplay_path = os.path.join(ffmpeg_path, "ffplay.exe") 
            subprocess.run([ffplay_path, '-nodisp', '-autoexit', output_filepath], check=True)
            # --- END MODIFIED ---
        elif os_name == "Linux":  # Linux
            # 'aplay' is typically for WAV. For MP3, 'mpg123' or 'ffplay' is better.
            # Keeping original for now, but consider installing 'mpg123' or using ffplay.
            subprocess.run(['aplay', output_filepath], check=True) # Added check=True
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        # Use logging.error for better error handling consistent with your other code
        print(f"An error occurred while trying to play the audio: {e}") # Keeping print as per your original snippet

#input_text = "Hi this is AI with Hassan!"
# Test call for the function (kept as per your snippet)
#text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")