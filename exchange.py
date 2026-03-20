import os
from pydub import AudioSegment

target_dir = r"E:\pycode\otp"

for filename in os.listdir(target_dir):
    if filename.endswith(".wav"):
        file_path = os.path.join(target_dir, filename)
        try:
            audio = AudioSegment.from_wav(file_path)
            audio.export(file_path.replace(".wav", ".mp3"), format="mp3", bitrate="128k")
            os.remove(file_path)
        except Exception:
            pass