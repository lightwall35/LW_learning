import feedparser
from newsplease import NewsPlease

# ================= 1. 侦察兵出动（获取最新精确 URL） =================
print("1. 正在通过 RSS 寻找最新头条...")
rss_url = "https://abcnews.go.com/abcnews/internationalheadlines"
news_feed = feedparser.parse(rss_url)

if len(news_feed.entries) == 0:
    print("没有找到新闻喵！")
    exit()

# 直接拿到最新第一条新闻的精确网址！
target_url = news_feed.entries[0].link  
print(f"🎯 侦察兵锁定目标网址：{target_url}")

# ================= 2. 主攻手出动（剥离纯净正文） =================
print("\n2. news-please 正在施展魔法，提取纯净正文...")

# 直接把刚才侦察到的网址喂给它！
article = NewsPlease.from_url(target_url)

print("\n✅ 提取成功！直接为你展示前 300 个字符：")
print("==================================================")
print(article.maintext)
print("==================================================")

# 接下来，只需要把 article.maintext 传给你的 GPT-SoVITS 接口就行啦！