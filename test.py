import sys
import time
import io
from pydub import AudioSegment 
import random
import os
import math

bgm_folder = r"E:\music"
candidate_bgms = []
valid_exts = (".mp3", ".wav", ".m4a", ".flac", ".ogg")




if os.path.exists(bgm_folder):
    for filename in os.listdir(bgm_folder):
        if filename.endswith(valid_exts):
            candidate_bgms.append(os.path.join(bgm_folder, filename))
#if candidate_bgms:
 #   random.shuffle(candidate_bgms)

special_rules = {
    "罗辑": 10.0,   
    "Eyes of Irumyuui": 6.2727, 
    "Adventure Through the Light": 6.2727 ,
    "Nature Sequence. 6th Layer": 6.2727 ,
    "old stories": 6.2727 ,
    "Reg & his Interference Unit": 6.2727,
    "Sufjan Stevens - Death with Dignity": 6.2727,
    "Tomorrowland": 6.2727,
    "undertale": 6.2727,
    "where dream rest": 6.2727, 
    "深渊的琴槌": 6.2727,          
    
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



for bgm in candidate_bgms:
    print(bgm)
total_count = len(candidate_bgms)
unique_count = len(set(candidate_bgms)) # set 会自动去除完全一样的重复项

print("\n" + "="*30)
print(f"列表里一共有 {total_count} 首歌呢！")
print(f"其中不重复的真实歌曲有 {unique_count} 首呀！")