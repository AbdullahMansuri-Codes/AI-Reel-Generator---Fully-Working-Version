import os
from test_to_audio import text_to_speech_file
import subprocess
import time

BASE_PATH = r"C:\Users\Admin\Downloads\Code With Harry VidSnap IAS\VidSnap AI\User_Uploads"
DONE_FILE = r"C:\Users\Admin\Downloads\Code With Harry VidSnap IAS\done.txt"


def text_to_audio(folder):
    try:
        file_path = os.path.join(BASE_PATH, folder, "description.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        print(text, folder)
        print(f"Text-To-Folder:{folder}")
        # Pass full path here
        text_to_speech_file(text=text, folder=os.path.join(BASE_PATH, folder))

    except FileNotFoundError:
        print(f"Missing description.txt in {folder}")



def create_reel(folder):
    print(f"Create-Reel:{folder}")
    output_dir = os.path.join("static", "reels")
    os.makedirs(output_dir, exist_ok=True)   # <-- create folder if missing

    output_file = os.path.join(output_dir, f"{folder}.mp4")

    command = f'''ffmpeg -f concat -safe 0 -i "C:/Users/Admin/Downloads/Code With Harry VidSnap IAS/VidSnap AI/User_Uploads/{folder}/input.txt" -i "C:/Users/Admin/Downloads/Code With Harry VidSnap IAS/VidSnap AI/User_Uploads/{folder}/audio.mp3" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p "{output_file}"'''
    
import os
import subprocess
from test_to_audio import text_to_speech_file

# Use relative paths for portability
BASE_PATH = os.path.join(os.path.dirname(__file__), 'User_Uploads')
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
REELS_FOLDER = os.path.join(STATIC_FOLDER, 'reels')


def text_to_audio(folder):
    try:
        file_path = os.path.join(BASE_PATH, folder, "description.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        print(text, folder)
        print(f"Text-To-Folder:{folder}")
        # Pass full path here
        text_to_speech_file(text=text, folder=os.path.join(BASE_PATH, folder))

    except FileNotFoundError:
        print(f"Missing description.txt in {folder}")



def create_reel(folder):
    print(f"Create-Reel:{folder}")
    output_dir = REELS_FOLDER
    os.makedirs(output_dir, exist_ok=True)   # <-- create folder if missing

    output_file = os.path.join(output_dir, f"{folder}.mp4")
    
    input_txt_path = os.path.join(BASE_PATH, folder, 'input.txt')
    audio_mp3_path = os.path.join(BASE_PATH, folder, 'audio.mp3')

    command = f'''ffmpeg -f concat -safe 0 -i "{input_txt_path}" -i "{audio_mp3_path}" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p "{output_file}"'''
    
    subprocess.run(command, shell=True, check=True)
