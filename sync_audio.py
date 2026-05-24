import os
import shutil
import warnings
import json
import random

warnings.filterwarnings("ignore")


SOURCE_FOLDER = r"E:\pycode\otp" 

TEXT_FOLDER = r"E:\pycode\text_data"

TARGET_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio") 

PICTURE_FOLDER = r"E:\selected_pictures"

def sync_newest_audio():

    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
        print(f"已新建目标文件夹：{TARGET_FOLDER}")

    print("正在清空旧音频文件...")
    for filename in os.listdir(TARGET_FOLDER):
        file_path = os.path.join(TARGET_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"清理文件 {filename} 时发生了错误：{e}")

    print("挑选背景图片...")
    bg_ext = ".png" # 默认
    if os.path.exists(PICTURE_FOLDER):
        pics = [f for f in os.listdir(PICTURE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if pics:
            chosen_pic = random.choice(pics)
            bg_ext = os.path.splitext(chosen_pic)[1]
            pic_source = os.path.join(PICTURE_FOLDER, chosen_pic)
            pic_target = os.path.join(TARGET_FOLDER, f"background{bg_ext}")
            try:
                shutil.copy2(pic_source, pic_target)
                print(f"已选中背景图：{chosen_pic}")
            except Exception as e:
                print(f"复制背景图时发生了错误：{e}")
        else:
            print("没在图库里找到合适的图片喵！")
    else:
        print(f"图片文件夹不存在：{PICTURE_FOLDER}")

    print(f"在从源文件夹抓取音频：{SOURCE_FOLDER}...")
    valid_files = []
    if os.path.exists(SOURCE_FOLDER):
        for filename in os.listdir(SOURCE_FOLDER):
            if filename.lower().endswith(('.wav', '.mp3')): # 兼容 mp3
                full_path = os.path.join(SOURCE_FOLDER, filename)
                valid_files.append(full_path)
    
    file_count_to_copy = min(5, len(valid_files))

    if file_count_to_copy == 0:
        print("源文件夹里没有可以搬运的音频")
        return

    newest_files = sorted(valid_files, key=os.path.getmtime, reverse=True)[:file_count_to_copy]

    print(f"发现最新的音频 {len(newest_files)} 首，开始搬运并整合简介...")
    audio_data_list = []
    
    title_text = [
        "这是第一个标题",
        "一共有五个标题",
        "标题的数目并非六，亦非四",
        "六是多了，四是少了",
        "五是第三个质数，但是三并非标题的数目"
    ]

    for i, file_path in enumerate(newest_files):
        _, ext = os.path.splitext(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        new_filename = f"{i+1}{ext}" 
        target_path = os.path.join(TARGET_FOLDER, new_filename)
        
        json_source_path = os.path.join(TEXT_FOLDER, f"{base_name}.json")
        summary_text = "这是一段非常精彩的播报，但由于时空乱流，主播好像忘记写简介了喵~"
        original_text = "由于时空乱流，原文数据丢失在虚空中了喵..."
        
        if os.path.exists(json_source_path):
            try:
                with open(json_source_path, 'r', encoding='utf-8') as f:
                    data_dict = json.load(f)
                    summary_text = data_dict.get("summary", summary_text)
                    original_text = data_dict.get("original", original_text)
            except Exception as e:
                print(f"⚠️ 读取数据 {base_name}.json 失败：{e}")
        else:
            txt_source_path = os.path.join(SOURCE_FOLDER, f"{base_name}.txt")
            if os.path.exists(txt_source_path):
                try:
                    with open(txt_source_path, 'r', encoding='utf-8') as f:
                        summary_text = f.read().strip()
                except Exception as e:
                    pass

        try:
            shutil.copy2(file_path, target_path) 
            print(f"✅ 已将 {os.path.basename(file_path)} 搬运为 {new_filename}")
            
            display_date = base_name
            if len(base_name) >= 8 and base_name[:8].isdigit():
                display_date = f"{base_name[:4]}-{base_name[4:6]}-{base_name[6:8]}"
            
            current_title = title_text[i] if i < len(title_text) else f"资讯集锦 {i+1}"
            
            audio_data_list.append({
                "id": i + 1,
                "title": f"{current_title} #{base_name[-4:] if len(base_name) > 4 else base_name}",
                "audio": f"audio/{new_filename}",
                "summary": summary_text,
                "original": original_text,
                "date": display_date
            })
            
        except Exception as e:
            print(f"💥 搬运文件 {new_filename} 时发生了错误：{e}")

    data_js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.js")
    try:
        js_content = f"const audioData = {json.dumps(audio_data_list, ensure_ascii=False, indent=4)};\n"
        js_content += f"const siteConfig = {{ background: 'audio/background{bg_ext}' }};\n"
        
        with open(data_js_path, "w", encoding="utf-8") as f:
            f.write(js_content)
        print("已成功生成 data.js 配置文件！")
    except Exception as e:
        print(f"生成 data.js 时发生了错误：{e}")

    print("\n==============================================")
    print("文件夹整理完毕啦！")
    print("请重新打开或刷新你的 index.html 网页吧喵！")
    print("==============================================")

if __name__ == "__main__":
    sync_newest_audio()