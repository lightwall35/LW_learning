import os
import shutil
import warnings

# 忽略不必要的错误提示
warnings.filterwarnings("ignore")

# ==========================================
# 铃花水仙的管家配置 (请根据实际路径修改喵)
# ==========================================
# 你的 GPT-SoVITS 输出音频的文件夹路径
SOURCE_FOLDER = r"E:\pycode\otp" 

# 你的专属小站用于存放展示音频的路径
TARGET_FOLDER =os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio") 

def sync_newest_audio():
    print("🌟 铃花水仙播报：正在整理 audio 文件夹，确保只有最新的五首声音喵...")

    # 1. 确保目标文件夹存在，不存在就新建一个
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print(f"✅ 已新建目标文件夹：{TARGET_FOLDER}")

    # 2. 清空目标文件夹里的所有旧文件，确保始终只有5首
    print("🧹 正在清空旧音频文件...")
    for filename in os.listdir(TARGET_FOLDER):
        file_path = os.path.join(TARGET_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"💥 清理文件 {filename} 时发生了错误：{e}")

    # 3. 获取源文件夹中所有的 WAV 文件
    print(f"📂 正在从源文件夹抓取音频：{SOURCE_FOLDER}...")
    valid_files = []
    if os.path.exists(SOURCE_FOLDER):
        for filename in os.listdir(SOURCE_FOLDER):
            if filename.lower().endswith(('.wav', '.mp3')): # 兼容 mp3
                full_path = os.path.join(SOURCE_FOLDER, filename)
                valid_files.append(full_path)
    
    # 4. 如果文件数量不足5个，有什么就抓什么
    file_count_to_copy = min(5, len(valid_files))

    # 5. 安全检查：如果没有任何音频，就直接结束
    if file_count_to_copy == 0:
        print("❌ 铃花水仙播报：哎呀，源文件夹里没有可以搬运的音频呀！")
        return

    # 6. 【关键动作】按文件最后修改时间排序，拿到最新的文件
    # 这一步会把最老的音频从选择列表中剔除掉，确保刚好5首喵。
    newest_files = sorted(valid_files, key=os.path.getmtime, reverse=True)[:file_count_to_copy]

    # 7. 开始搬运并按 1.wav 到 5.wav 重新命名
    print(f"🚚 发现最新的音频 {len(newest_files)} 首，开始搬运并改名喵...")
    for i, file_path in enumerate(newest_files):
        # 聪明地提取文件原本的后缀名（比如 .mp3）
        _, ext = os.path.splitext(file_path)
        new_filename = f"{i+1}{ext}" 
        
        target_path = os.path.join(TARGET_FOLDER, new_filename)
        try:
            shutil.copy2(file_path, target_path) 
            print(f"✅ 已将 {os.path.basename(file_path)} 搬运并改名为 {new_filename}")
        except Exception as e:
            print(f"💥 搬运文件 {new_filename} 时发生了错误：{e}")

    print("\n==============================================")
    print("🎉 铃花水仙播报：audio 文件夹整理完毕啦！")
    print("🎉 请重新打开或刷新你的 index.html 网页吧喵！")
    print("==============================================")

if __name__ == "__main__":
    sync_newest_audio()