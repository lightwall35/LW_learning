import requests

# ================= 1. 遥控换装：切换纳西妲模型 (使用 GET 明信片) =================
print("🔄 正在给 API 发送明信片，要求换上草神大人的模型...")

gpt_path = r"D:\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\GPT_weights_v4\纳西妲_ZH-e10.ckpt"
sovits_path = r"D:\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50\SoVITS_weights_v4\纳西妲_ZH_e10_s1400_l32.pth"

# 步骤 A：换 GPT 模型
# 使用 params 参数，Python 会自动帮你把路径拼接成文档里那种 ?weights_path=xxx 的格式
res_gpt = requests.get("http://127.0.0.1:9880/set_gpt_weights", params={"weights_path": gpt_path})
if res_gpt.status_code == 200:
    print("✅ GPT 情感模型切换成功！")
else:
    print(f"❌ GPT 模型切换失败: {res_gpt.text}")

# 步骤 B：换 SoVITS 模型
res_sovits = requests.get("http://127.0.0.1:9880/set_sovits_weights", params={"weights_path": sovits_path})
if res_sovits.status_code == 200:
    print("✅ SoVITS 音色模型切换成功！")
else:
    print(f"❌ SoVITS 模型切换失败: {res_sovits.text}")


# ================= 2. 爬取新闻并在下面拼接 POST 请求 =================
# ... 这里放你用 news-please 提取新闻的代码 ...

# ================= 3. 发送配音请求 (使用 POST 大包裹) =================
# print("🚀 正在用 POST 发送长篇大论给纳西妲配音...")
# data = { ... } # 填好文档里要求的参数
# response = requests.post("http://127.0.0.1:9880/tts", json=data) # 注意 endpoint 变成了 /tts