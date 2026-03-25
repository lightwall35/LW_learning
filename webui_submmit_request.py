import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import feedparser
import requests
from newsplease import NewsPlease
import os
from datetime import datetime
import re
import time
import io
from pydub import AudioSegment 
import random
import math
import json

json_file_path = r"E:\pycode\transfer_data.json"


received_payload = None
if_music = False

with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    received_payload = data.get("sovits_payload")
    if_music = data.get("if_music")



response = requests.post("http://127.0.0.1:9880/tts", json=received_payload)
if response.status_code == 200:
    if if_music:
        virtual_file = io.BytesIO(response.content)
        silence = AudioSegment.silent(duration=2000)
        audio = AudioSegment.from_file(virtual_file, format="wav")


        bgm_folder = r"E:\music"
        candidate_bgms = []
        valid_exts = (".mp3", ".wav", ".m4a", ".flac", ".ogg")
        if os.path.exists(bgm_folder):
            for filename in os.listdir(bgm_folder):
                if filename.endswith(valid_exts):
                    candidate_bgms.append(os.path.join(bgm_folder, filename))
        target_length = len(audio) + 4000

        special_rules = {
            "罗辑": 4.2727,   
            "Eyes of Irumyuui": 4.2727, 
            "Adventure Through the Light": 4.2727 ,
            "Nature Sequence. 6th Layer": 6.2727 ,
            "old stories": 4.2727 ,
            "Reg & his Interference Unit": 4.2727,
            "Sufjan Stevens - Death with Dignity": 6.2727,
            "Tomorrowland": 6.2727,
            "undertale": 4.2727,
            "where dream rest": 4.2727, 
            "深渊的琴槌": 4.2727,  
            "星茶会": 4.2727        
            
        }
        scored_bgms = []
        for path in candidate_bgms:
            filename = os.path.basename(path)
            current_value = 1.0
            for keyword, value in special_rules.items():
                if keyword in filename:
                    current_value = value
                    break

            r = random.random()
            if r == 0:
                r = 0.00001
            score = math.pow(r, 1.0 / current_value)

            scored_bgms.append((score, path))

        scored_bgms.sort(key=lambda x: x[0], reverse=True)

        candidate_bgms = [item[1] for item in scored_bgms]
            
        audio_bgm =  AudioSegment.from_file(candidate_bgms[0])

        current_bgm_index = 1
        while len(audio_bgm) < target_length:
            if candidate_bgms:
                random_path = candidate_bgms[current_bgm_index]
                next_bgm = AudioSegment.from_file(random_path)
                audio_bgm = audio_bgm + silence + next_bgm
                current_bgm_index += 1       
            else:
                audio_bgm = audio_bgm + silence + audio_bgm

        audio_bgm = audio_bgm - 9
        audio_bgm = audio_bgm[:target_length].fade_out(4000)
        overlayed_audio = audio_bgm.overlay(audio, position=0)
        save_folder = r"E:\pycode\otp"
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        full_path = os.path.join(save_folder, f"{time_str}.wav")




        overlayed_audio.export(full_path, format="wav")
    else:
        save_folder = r"E:\pycode\otp"
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        full_path = os.path.join(save_folder, f"{time_str}.wav")
        with open(full_path, "wb") as f:
            f.write(response.content)
else:
    print("=======================================")
    print(f"糟糕！API 拒绝了请求，状态码：{response.status_code}")
    print(f"接口的报错详情是：{response.text}")
    print("=======================================")






