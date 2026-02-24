import feedparser
import requests
from newsplease import NewsPlease
import os
from datetime import datetime

# ================= 1. 获取新闻 =================
rss_url = "https://abcnews.go.com/abcnews/internationalheadlines"
news_feed = feedparser.parse(rss_url)
article_list=[]

if len(news_feed.entries) == 0:
    print("没有找到新闻喵！")
    exit()

for i in range(0,3):
    target_url = news_feed.entries[i].link  
    
    print("\nnews-please正在提取纯净正文")


    article = NewsPlease.from_url(target_url)
    article_list.append(article.maintext)

result = "\n\n\nThe next:\n\n\n".join(article_list)


print("✅ 新闻提取成功，准备配音...")
print(result)
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
# 【修复】将 json=data 移到了双引号外面
print("🚀 正在生成音频，因为是长新闻，可能需要稍等片刻...")
response = requests.post("http://127.0.0.1:9880/tts", json=data)

# 【修复】正确的状态码检查方法
if response.status_code != 200:
    raise Exception(f"请求 GPT-SoVITS 出现错误: 状态码 {response.status_code}, 信息: {response.text}")

# ================= 4. 保存音频 =================
save_folder = r"E:\pycode\otp"
time_str = datetime.now().strftime("%Y%m%d%H%M%S")
full_path = os.path.join(save_folder, f"{time_str}.wav")

with open(full_path, "wb") as f:
    f.write(response.content)

