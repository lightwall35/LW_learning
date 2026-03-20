import warnings
warnings.filterwarnings("ignore")
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

# ================= 1. 获取新闻 =================
rss_url = "https://abcnews.go.com/abcnews/internationalheadlines"
news_feed = feedparser.parse(rss_url)
article_list=[]

if len(news_feed.entries) == 0:
    print("没有找到新闻喵！")
    exit()

for i in range(0,5):
    target_url = news_feed.entries[i].link  
    
    print("\nnews-please正在提取纯净正文")


    article = NewsPlease.from_url(target_url)
    clean_text = re.sub(r'^.{0,80}?--\s*', '', article.maintext)
    clean_text = clean_text.replace("U.S.", "US").replace("U.K.", "UK")
    article_list.append(clean_text)

result = "\n\n\nThe next:\n\n\n".join(article_list)


print(result)
print(" 新闻提取成功，准备配音...")
start_time = time.perf_counter()
# ================= 2. 准备配音参数 =================
data = {
    "text": result,                   
    "text_lang": "en",                          
    "ref_audio_path": r"D:\GPT-SoVITS-v2pro-20250604-nvidia50\nahida等11个文件\nahida\v1\推理音频\新鲜感，就是来源于生活中的小小仪式哦。.wav",  # 【修复】加了 r 防止路径错乱
    "prompt_text": "新鲜感，就是来源于生活中的小小仪式哦。",            
    "prompt_lang": "zh",            
    "top_k": 5,                   
    "top_p": 1,                   
    "temperature": 1,             
    "text_split_method": "cut5",  
    "batch_size": 1,              
    "batch_threshold": 0.75,      
    "split_bucket": True,         
    "speed_factor": 1.0,          
    "fragment_interval": 0.3,     
    "seed": -1,                   
    "parallel_infer": True,         
    "repetition_penalty": 1.35,   
    "sample_steps": 32,           
    "super_sampling": False,      
    "streaming_mode": False,      
    "overlap_length": 2,          
    "min_chunk_length": 16,
}

# ================= 3. 发送给 GPT-SoVITS =================

print("正在生成音频，因为是长新闻，可能需要稍等片刻...")
response = requests.post("http://127.0.0.1:9880/tts", json=data)


if response.status_code != 200:
    raise Exception(f"请求 GPT-SoVITS 出现错误: 状态码 {response.status_code}, 信息: {response.text}")

# ================= 4. 保存音频 =================
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
end_time = time.perf_counter()
elapsed_time = end_time - start_time


overlayed_audio.export(full_path, format="wav")
print(f"工作全部完成啦！一共花掉了 {elapsed_time:.4f} 秒呢")

