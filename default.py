import feedparser
import requests
from newsplease import NewsPlease

# ================= 1. 获取新闻 =================
rss_url = "https://abcnews.go.com/abcnews/internationalheadlines"
news_feed = feedparser.parse(rss_url)

if len(news_feed.entries) == 0:
    print("没有找到新闻喵！")
    exit()

target_url = news_feed.entries[0].link
print(f"🎯 正在提取新闻网址：{target_url}")
article = NewsPlease.from_url(target_url)

print("✅ 新闻提取成功，正在召唤纳西妲准备配音...")

# ================= 2. 准备配音参数 =================
data = {
    "text": article.maintext,                   # 【修复】去掉了双引号，传入真实的新闻内容
    "text_lang": "en",                          # 【修复】补上了双引号
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
with open("success.wav", "wb") as f:
    f.write(response.content)

