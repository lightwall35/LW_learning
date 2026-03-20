import feedparser
from newsplease import NewsPlease


print("1. 正在通过 RSS 寻找最新头条...")
rss_url = "https://abcnews.go.com/abcnews/internationalheadlines"
news_feed = feedparser.parse(rss_url)
article_list=[]

if len(news_feed.entries) == 0:
    print("没有找到新闻喵！")
    exit()


for i in range(0,3):
    target_url = news_feed.entries[i].link  
    print(f"锁定目标网址：{target_url}")


    print("\nnews-please正在提取纯净正文")


    article = NewsPlease.from_url(target_url)
    article_list.append(article.maintext)

result = "\n\n\nThe next:\n\n\n".join(article_list)
print("\n✅ 提取成功")
print("==================================================")
print(result)
print("==================================================")
# 把合并好的超级长文，写进本地硬盘里慢慢看！
with open("3篇大新闻合体.txt", "w", encoding="utf-8") as f:
    f.write(result)

