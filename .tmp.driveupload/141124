import streamlit as st
import subprocess
import time
import os
import streamlit.components.v1 as components
import base64
from PIL import Image
import random


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    return encoded_string

img_path = r"E:\Nahida\115467919_p0.jpg"
img_base64 = get_image_base64(img_path)

BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?q=80&w=1080" 
BLUR_RADIUS = "6px" 
MAIN_TITLE = "Embark on your audio journey with me" 

# 批处理文件的绝对路径
BAT_PATH = "E:\\pycode\\auto.bat"
BAT_PATH1 = "E:\\pycode\\auto_science.bat"

# 存放生成音频的文件夹绝对路径
AUDIO_DIR = "E:\\pycode\\otp"


if 'img_list' not in st.session_state:
    img_folder = r"E:\selected_pictures"
    valid_exts = (".jpg", ".jpeg", ".png", ".webp")
    candidate_imgs = []

    if os.path.exists(img_folder):
        for filename in os.listdir(img_folder):
            if filename.lower().endswith(valid_exts):
                full_path = os.path.join(img_folder, filename)
                try:
                    # 借助 Pillow 打开图片看看尺寸
                    with Image.open(full_path) as img:
                        w, h = img.size
                        if w < h:  # 筛选纵向图片
                            candidate_imgs.append(full_path)
                except:
                    continue 
        
        random.shuffle(candidate_imgs) 
        st.session_state.img_list = candidate_imgs
        st.session_state.img_index = 0 


# ==========================================

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

if 'show_list' not in st.session_state:
    st.session_state.show_list = False      # 控制是否展开音频列表
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = None  # 记录当前选中的音频文件路径


custom_css = f"""
<style>
    #MainMenu {{visibility: visible;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    .stApp {{ background-color: transparent; }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: url("{BACKGROUND_IMAGE}");
        background-size: cover; background-position: center; background-repeat: no-repeat;
        filter: blur({BLUR_RADIUS}); 
        z-index: -1; 
    }}

    .top-nav {{
        max-width: 800px;
        margin-left: auto;
        border-radius: 40px;
        display: flex; justify-content: flex-end; padding: 10px 50px;
        font-family: 'Helvetica Neue', sans-serif;
        backdrop-filter: blur(18px)
        
    }}
    .nav-item {{
        font-size: 25px; color: #2e7d32; font-weight: 600; cursor: pointer; transition: color 0.3s ease;
    }}
    .nav-item:hover {{ color: #81c784; }}

    .main-title {{
        font-size: 4.5rem; font-weight: 700; line-height: 1.5;
        background: linear-gradient(135deg, #2e7d32 0%, #81c784 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px; font-family: 'Helvetica Neue', sans-serif;
        animation: fadeInUp 1s ease-out;
    }}

    
    button[kind="primary"]{{
        width: 160px;
        background: linear-gradient(135deg, #a5d6a7 0%, #66bb6a 100%);
        color: white; border: none; border-radius: 40px; padding: 10px 40px;
        font-size: 18px; font-weight: bold;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 20px rgba(102, 187, 106, 0.3);
        margin-top: 10px; margin-bottom: 10px;
    }}
    button[kind="primary"]:hover{{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 25px rgba(102, 187, 106, 0.5); color: white;
    }}


    button[kind="secondary"] {{
    /* 1. 彻底隐身：没有背景，没有边框，没有阴影 */
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important; /* 去掉多余的内边距，让它像纯文本 */
    
    /* 2. 继承 me 的字体风采：大号，粗体，翠绿色 */
    font-size: 25px !important; /* 和 nav-item 保持一致的大小 */
    color: #2e7d32 !important; /* 同样的翠绿色 */
    font-weight: 600 !important;
    font-family: 'Helvetica Neue', sans-serif;
    
    /* 3. 丝滑的过渡效果 */
    transition: color 0.3s ease !important;
    cursor: pointer;
}}
    
    button[kind="secondary"]:hover {{
    color: #81c784 !important;
    background-color: transparent !important; /* 确保悬浮时也没有背景色 */
    border: none !important;
}}
    button[kind="secondary"]:focus:not(:active) {{
    border-color: transparent !important;
    color: #2e7d32 !important;
}}

    .audio-glass-box {{
        background: rgba(255, 255, 255, 0.01); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 24px; padding: 30px;
        box-shadow: 0 10px 40px rgba(129, 199, 132, 0.2); animation: fadeIn 1s ease-out;
        display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 500px;
        position: relative !important;
        top: -40px !important;
    }}

    @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: scale(0.95); }} to {{ opacity: 1; transform: scale(1); }} }}


    div[data-baseweb="select"] > div {{
        background-color: rgba(255, 255, 255, 0.4) !important; 
        border-radius: 15px !important; 
        border: 2px solid transparent !important; 
    }}
    
    
    div[data-baseweb="select"] > div:hover {{
        border: 2px solid #a5d6a7 !important; 
    }}

    
    div[data-baseweb="select"] span {{
        color: #2e7d32 !important; 
        font-weight: bold !important;
    }}

    div[data-baseweb="popover"] ul {{
        background-color: #81c784 !important; 
        border-radius: 15px !important;
        padding: 5px !important;
        overflow-y: auto !important;  
    }}

    
    ul[data-baseweb="menu"] li {{
        color: #2e7d32 !important;
        border-radius: 10px !important;
        transition: background-color 0.2s ease !important;
    }}
    ul[data-baseweb="menu"] li:hover {{
        background-color: rgba(165, 214, 167, 0.5) !important; 
    }}

    /* 改变原生音频播放器的底色 */
    audio::-webkit-media-controls-panel {{
        background-color: rgba(24, 244, 77, 0.65) !important; 
        border-radius: 20px !important; 
    }}

   
    .playing-bars {{ 
        position: absolute; 
        top: 50%; left: 50%;
        transform: translate(-50%, 40%); /* 乖乖待在正中间 */
        display: flex; align-items: flex-end; justify-content: center; 
        height: 120px; gap: 12px; 
        opacity: 0.9; /* 变成半透明的底纹，就不会喧宾夺主啦 */
        z-index: 0; /* 沉到最底下 */
    }}
    .bar {{ 
        width: 12px; background-color: #2e7d32; border-radius: 6px; 
        animation: jump 1s infinite ease-in-out; 
        animation-play-state: paused;
    }}
    .bar:nth-child(1) {{ animation-delay: 0.1s; }}
    .bar:nth-child(2) {{ animation-delay: 0.4s; }}
    .bar:nth-child(3) {{ animation-delay: 0.2s; }}
    .bar:nth-child(4) {{ animation-delay: 0.5s; }}
    .bar:nth-child(5) {{ animation-delay: 0.3s; }}
    .bar:nth-child(6) {{ animation-delay: 0.1s; }}
    .bar:nth-child(7) {{ animation-delay: 0.4s; }}
    .bar:nth-child(8) {{ animation-delay: 0.2s; }}
    .bar:nth-child(9) {{ animation-delay: 0.5s; }}
    .bar:nth-child(10) {{ animation-delay: 0.3s; }}
    .bar:nth-child(11) {{ animation-delay: 0.1s; }}
    .bar:nth-child(12) {{ animation-delay: 0.4s; }}
    .bar:nth-child(13) {{ animation-delay: 0.2s; }}
    .bar:nth-child(14) {{ animation-delay: 0.5s; }}
    .bar:nth-child(15) {{ animation-delay: 0.3s; }}
    .bar:nth-child(16) {{ animation-delay: 0.1s; }}
    .bar:nth-child(17) {{ animation-delay: 0.4s; }}
    .bar:nth-child(18) {{ animation-delay: 0.2s; }}
    @keyframes jump {{ 
        0%, 100% {{ height: 20px; }} 
        50% {{ height: 120px; }} 
    }}

    
    div.stAudio {{
        position: relative;
        margin-top: -100px !important; 
        z-index: 10; 
        padding: 0 20px;
    }}

    @keyframes slideUpFade {{
    0% {{
        opacity: 0;
        transform: translateY(30px); 
    }}
    100% {{
        opacity: 0.8; 
        transform: translateY(0); 
    }}
}}


.image-transition {{
    /* 持续 0.6 秒，缓动效果，只放一次 */
    animation: slideUpFade 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 布局与交互逻辑
# ==========================================

st.markdown('<div class="top-nav"><span class="nav-item">WHEN I REALLISE TAHT THIS IS A USELESS TOP NAVIGATION EVERYTHING HAS BEEN TOO LATE</span></div>', unsafe_allow_html=True)
st.markdown("<br><br><br>", unsafe_allow_html=True)


col_left, col_right = st.columns([1, 1.2])

# ====== 右侧区域：大标题、Start按钮 和 List按钮 ======
with col_right:
    st.markdown(f'<div class="main-title">{MAIN_TITLE}</div>', unsafe_allow_html=True)
    
    
    
    col_left1, col_right1, col_left2, col_right2 = st.columns([1, 1, 1, 1])

    
    with col_left1:
        
        
        if st.button("global", type="primary", key="btn_global"):
            with st.spinner("铃花水仙正在后台悄悄唤醒批处理流水线哦..."):
                try:
                    subprocess.run(["cmd.exe", "/c", BAT_PATH], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    st.success("启动指令发送成功啦！")
                except Exception as e:
                    st.error(f"故障啦：{e}")

        
        if st.button("List ", type="primary", key="btn_list"):
            st.session_state.show_list = not st.session_state.show_list

        if st.session_state.show_list:
            if os.path.exists(AUDIO_DIR):
                audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(('.wav', '.mp3'))]
                if audio_files:
                    audio_files.sort(reverse=True)
                    selected_file = st.selectbox("请挑选录音：", ["-- 请选择 --"] + audio_files, key="select_audio")
                    if selected_file != "-- 请选择 --":
                        st.session_state.selected_audio = os.path.join(AUDIO_DIR, selected_file)
                    else:
                        st.session_state.selected_audio = None
        
        
        

    
    with col_right1:
        
        
        
        
        
        if st.button("science", type="primary", key="btn_science"):
            with st.spinner("正在启动 Science 流水线..."):
                try:
                    subprocess.run(["cmd.exe", "/c", BAT_PATH1], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    st.success("Science 启动成功！")
                except Exception as e:
                    st.error(f"遇到麻烦了：{e}")
        
        if st.button("Change", key="btn_change_picture",type="primary"):
            if st.session_state.img_list:
        # 指针加 1，用取余运算 % 保证它到头了能回到 0，实现无限循环
             st.session_state.img_index = (st.session_state.img_index + 1) % len(st.session_state.img_list)
       
        
        
        
            

# ====== 左侧区域：音频播放器和律动条 ======



with col_left:
    rand = random.randint(0, 999999)
    image_class = f"image-transition-{st.session_state.img_index}-{rand}"
    
    if st.session_state.img_list:
        # 从记忆本子里取出当前索引对应的路径
        current_img_path = st.session_state.img_list[st.session_state.img_index]
        
        # 2. 调用你写好的转换函数，把图片变成神秘字符串
        # 记得要处理一下可能的文件读取错误哟
        try:
            dynamic_img_base64 = get_image_base64(current_img_path)
        except Exception as e:
            # 如果某张图坏掉了，就先用原来的那张保底呀
            dynamic_img_base64 = img_base64 
    else:
        # 如果文件夹里没找到纵向图，就用最开始那张 Nahida 保底
        dynamic_img_base64 = img_base64

    
    
    if st.session_state.show_list and st.session_state.selected_audio and os.path.exists(st.session_state.selected_audio):
        file_name = os.path.basename(st.session_state.selected_audio)

        image_class = f"image-transition-{st.session_state.img_index}"
        st.markdown(f'''
<div style="position: relative; width: 100%; min-height: 400px;">
    <style>
        /* 针对当前这张图的专属动画触发器 */
        .{image_class}{{
            animation: slideUpFade 0.7s ease-out both;
        }}
    </style>
            <img src="data:image/jpeg;base64,{dynamic_img_base64}" 
                    class="{image_class}"
                style="position: absolute; z-index: 0; border-radius: 20px; opacity: 0.8;top: -305px;left: 0;right:0;bottom:0;object-fit:cover;">                        
                        <div class="audio-glass-box">
                            <h4 style="color: #2e7d32; margin-bottom: -2px; position: relative; z-index: 1;top: -10px;font-size: 35px"> 正在播放选中音频</h4>
                            <div style="color: #4caf50; font-size: 14px; margin-bottom: 90px; position: relative; z-index: 1;left: -10px;">当前文件: {file_name}</div>
                            <div class="playing-bars">
                                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                                <div class="bar"></div><div class="bar"></div><div class="bar"></div>
                            </div>
                        </div>
</div>
''', unsafe_allow_html=True)
    
        
        # 紧接着就是原生的播放器
        st.audio(st.session_state.selected_audio)
        components.html("""
        <script>
        // 设定一个小闹钟，每半秒钟找找看播放器和波形条有没有加载出来
        const checkExist = setInterval(function() {
            const parentDoc = window.parent.document;
            const audioTag = parentDoc.querySelector('audio');
            const bars = parentDoc.querySelectorAll('.bar');
            
            if (audioTag && bars.length > 0) {
                clearInterval(checkExist); // 找到之后就不找啦
                
                // 定义一个动作：根据播放状态更新小条的跳动
                const updateBars = () => {
                    bars.forEach(bar => {
                        if (audioTag.paused) {
                            bar.style.animationPlayState = 'paused';
                        } else {
                            bar.style.animationPlayState = 'running';
                        }
                    });
                };
                
                // 监听播放器的各种状态变化
                audioTag.addEventListener('play', updateBars);
                audioTag.addEventListener('pause', updateBars);
                audioTag.addEventListener('ended', updateBars);
                
                // 刚加载好的时候也先检查一下状态哦
                updateBars();
            }
        }, 500); 
        </script>
        """, height=0, width=0)
    else:
        
        st.markdown(f'''
<div style="position: relative; width: 100%; min-height: 400px;">
    <style>
        /* 针对当前这张图的专属动画触发器 */
        .{image_class}{{
            animation: slideUpFade 0.7s ease-out both;
        }}
    </style>
            <img src="data:image/jpeg;base64,{dynamic_img_base64}" 
                    class="{image_class}"
                 style="position: absolute; z-index: 0; border-radius: 20px; opacity: 0.8;top: -305px;left: 0;right:0;bottom:0;object-fit:cover;">                   
                        
</div>
''', unsafe_allow_html=True)
    
    

