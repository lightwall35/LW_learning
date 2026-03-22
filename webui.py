import streamlit as st
import subprocess
import time
import os
import streamlit.components.v1 as components
import base64
from PIL import Image
import random
import requests
import json


def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    return encoded_string

img_path = r"E:\Nahida\115467919_p0.jpg"
img_base64 = get_image_base64(img_path)

BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?q=80&w=1080" 
BLUR_RADIUS = "6px" 
MAIN_TITLE = "Embark on your audio journey with me" 


BAT_PATH = "E:\\pycode\\auto.bat"
BAT_PATH1 = "E:\\pycode\\auto_science.bat"
BAT_PATH2 = "E:\\pycode\\webui_request.bat"

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
                
                    with Image.open(full_path) as img:
                        w, h = img.size
                        if w < h:  
                            candidate_imgs.append(full_path)
                except:
                    continue 
        
        random.shuffle(candidate_imgs) 
        st.session_state.img_list = candidate_imgs
        st.session_state.img_index = 0 


# ==========================================

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

if 'show_list' not in st.session_state:
    st.session_state.show_list = False      
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = None  


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
    
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important; 
    
    
    font-size: 45px !important; 
    color: #2e7d32 !important; 
    font-weight: 600 !important;
    font-family: 'Helvetica Neue', sans-serif;
    
    
    transition: color 0.3s ease !important;
    cursor: pointer;
}}
    
    button[kind="secondary"]:hover {{
    color: #81c784 !important;
    background-color: transparent !important; 
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

    @keyframes slideInLeftScript {{
        0% {{ transform: translateX(-50px); opacity: 0; }}
        100% {{transform: translateX(0); opacity: 1; }}
    }}

    
    .slide-in-box {{
        animation: slideInLeftScript 0.6s ease-out;
    }}
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

    
    audio::-webkit-media-controls-panel {{
        background-color: rgba(24, 244, 77, 0.65) !important; 
        border-radius: 20px !important; 
    }}

   
    .playing-bars {{ 
        position: absolute; 
        top: 50%; left: 50%;
        transform: translate(-50%, 40%); 
        display: flex; align-items: flex-end; justify-content: center; 
        height: 120px; gap: 12px; 
        opacity: 0.9; 
        z-index: 0; 
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
    
     animation: slideUpFade 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}}


    div.stTextArea [data-baseweb="textarea"],
    div.stTextArea [data-baseweb="base-input"] {{
        background-color: transparent !important;
    }}

    div.stTextArea [data-baseweb="textarea"] {{
        animation: slideInLeftScript 0.6s ease-out !important;
        animation: slideInLeftScript 0.6s ease-out;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
        z-index: 60 !important;
    }}

    div.stTextArea [data-baseweb="textarea"]:focus-within {{
        animation: slideInLeftScript 0.6s ease-out !important;
        border-color: rgba(165, 214, 167, 0.8) !important;
        box-shadow: 0 0 15px rgba(165, 214, 167, 0.2) !important;
        background-color: transparent !important;
    }}

    div.stTextArea textarea {{
        animation: slideInLeftScript 0.6s ease-out !important;
        background-color: transparent !important;
        color: #2e7d32 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        top: -100px !important; 
    }}

    
    div.stTextArea textarea::placeholder {{
        color: rgba(46, 125, 50, 0.5) !important;
    }}

    div.stSlider label {{
        color: #2e7d32 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }}

    

    div.stSlider [data-baseweb="slider"] > div > div {{
        height: -8px !important;       /* 原本是 4px，你可以把它改得更粗，比如 10px 哟 */
        border-radius: 4px !important; /* 让变粗的轨道两端依然保持圆润 */
    }}

    /* 4. 修改滑块下方显示的具体数值文字颜色 */
    div.stSlider [data-testid="stTickBar"] {{
        color: #4caf50 !important;
    }}

    div[data-testid="stWidgetLabel"] p,
    label p {{
        color: #2e7d32 !important; /* 清新的翠绿色 */
        font-size: 16px !important; /* 把字号放大一点 */
        font-weight: 600 !important; /* 微微加粗，看得更清楚 */
    }}

    /* 2. 把 Toggle 开关整体按比例放大 */
    div[data-testid="stToggle"] {{
        transform: scale(3) !important; /* 整个开关放大 1.2 倍 */
        
    }}

    

    

    
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 布局与交互逻辑
# ==========================================
if 'page_now' not in st.session_state:
       st.session_state.page_now = 'main'

if st.session_state.page_now == 'main':
    col_1,col_2= st.columns([10, 1])
    with col_2:
        if st.button("me", key="btn_me", type="secondary"):
            st.session_state.page_now = 'me'
            st.rerun()
    st.markdown('<div class="top-nav"><span class="nav-item">WHEN I REALLISE TAHT THIS IS A USELESS TOP NAVIGATION EVERYTHING HAS BEEN TOO LATE</span></div>', unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)


    col_left, col_right = st.columns([1, 1.2])

    
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
            
                 st.session_state.img_index = (st.session_state.img_index + 1) % len(st.session_state.img_list)
        
            
            
        
    with col_left:
        rand = random.randint(0, 999999)
        image_class = f"image-transition-{st.session_state.img_index}-{rand}"
        
        if st.session_state.img_list:
            
            current_img_path = st.session_state.img_list[st.session_state.img_index]
            
            
            try:
                dynamic_img_base64 = get_image_base64(current_img_path)
            except Exception as e:
                dynamic_img_base64 = img_base64 
        else:
            dynamic_img_base64 = img_base64

        
        
        if st.session_state.show_list and st.session_state.selected_audio and os.path.exists(st.session_state.selected_audio):
            file_name = os.path.basename(st.session_state.selected_audio)

            image_class = f"image-transition-{st.session_state.img_index}"
            st.markdown(f'''
    <div style="position: relative; width: 100%; min-height: 400px;">
        <style>
            .{image_class}{{
                animation: slideUpFade 0.7s ease-out both;
            }}
        </style>
                <img src="data:image/jpeg;base64,{dynamic_img_base64}" 
                        class="{image_class}"
                    style="position: absolute; z-index: 0; border-radius: 20px; opacity: 0.8;top: -360px;left: 0;right:0;bottom:0;object-fit:cover;">                        
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
        
            
            st.audio(st.session_state.selected_audio)
            components.html("""
            <script>
            const checkExist = setInterval(function() {
                const parentDoc = window.parent.document;
                const audioTag = parentDoc.querySelector('audio');
                const bars = parentDoc.querySelectorAll('.bar');
                
                if (audioTag && bars.length > 0) {
                    clearInterval(checkExist); 
                    
    
                    const updateBars = () => {
                        bars.forEach(bar => {
                            if (audioTag.paused) {
                                bar.style.animationPlayState = 'paused';
                            } else {
                                bar.style.animationPlayState = 'running';
                            }
                        });
                    };
                    
                    
                    audioTag.addEventListener('play', updateBars);
                    audioTag.addEventListener('pause', updateBars);
                    audioTag.addEventListener('ended', updateBars);
                    
                    
                    updateBars();
                }
            }, 500); 
            </script>
            """, height=0, width=0)
        else:
            
            st.markdown(f'''
    <div style="position: relative; width: 100%; min-height: 400px;">
        <style>
            .{image_class}{{
                animation: slideUpFade 0.7s ease-out both;
            }}
        </style>
                <img src="data:image/jpeg;base64,{dynamic_img_base64}" 
                        class="{image_class}"
                    style="position: absolute; z-index: 0; border-radius: 20px; opacity: 0.8;top: -360px;left: 0;right:0;bottom:0;object-fit:cover;">                   
                            
    </div>
        ''', unsafe_allow_html=True)
if st.session_state.page_now == 'me':
    
    col_A, col_B = st.columns([1.2, 1])
    

    with col_B:
        col_1,col_2= st.columns([3.5, 1])
        with col_2:
            if st.button("main", key="btn_me", type="secondary"):
                st.session_state.page_now = 'main'
                st.rerun()   
        st.markdown("<h4 style='color: #2e7d32;'>参数设置</h4>", unsafe_allow_html=True) 
        text_lang = st.selectbox("文本语言", ["zh", "en", "ja", "yue"], key="lang_select")
        seed = st.slider("seed", -1, 99999, 99999, key="seed_slider")
        raw = 99998-seed
        
        col_k,col_l = st.columns([1,1])
        
        with col_k:
            top_k = st.slider("top_k", 0, 20, 5, key="top_k_slider")
            top_p = st.slider("top_p", 0.0, 1.0, 1.0, key="top_p_slider")
            temperature = st.slider("temperature", 0.1, 2.0, 1.0, key="temp_slider")
            batch_size = st.slider("batch_size", 1, 8, 1, key="batch_size_slider")
            batch_threshold = st.slider("batch_threshold", 0.0, 1.0, 0.75, key="batch_threshold_slider") 
            text_split_method = st.segmented_control("文本切分方式", options=["cut5", "cut10", "cut20", "none"],default="cut5",key="split_method_control")
        with col_l:      
            speed_factor = st.slider("speed_factor", 0.5, 2.0   , 1.0, key="speed_factor_slider")
            fragment_interval = st.slider("fragment_interval", 0.0, 1.0, 0.3, key="fragment_interval_slider")
            repetition_penalty = st.slider("repetition_penalty", 1.0, 2.0, 1.35, key="repetition_penalty_slider")
            sample_steps = st.slider("sample_steps", 1, 64, 32, key="sample_steps_slider")
            min_chunk_length = st.slider("min_chunk_length", 1, 64, 16, key="min_chunk_length_slider")
            background_music = st.segmented_control("背景音乐", options=["off", "on"], default="on", key="bgm_control")
        col_q,col_w,col_e,col_r = st.columns([1,1,1,1])
        with col_q:
            split_bucket = st.toggle("split_bucket", key="split_bucket_toggle")
        with col_w:
            parallel_infer = st.toggle("parallel_infer", key="parallel_infer_toggle")
        with col_e:
            super_sampling = st.toggle("super_sampling", key="super_sampling_toggle")
        with col_r:
            streaming_mode = st.toggle("streaming_mode", key="streaming_mode_toggle")
        overlap_length = st.slider("overlap_length", 0, 10, 2, key="overlap_length_slider")
    
    with col_A:
        
        text = user_text_area = st.text_area(
        label="这是一个圆角矩形：",
        placeholder="",
        height=650,  
        key="my_glass_textarea"
        )
        col_z, col_x, col_c = st.columns([1, 1, 1])
        with col_z:
            if st.button("合成", type="primary", use_container_width=True):
                if not text:
                    st.warning("木有文字(>_<)")
                else:
                    with st.spinner("正在发送合成请求..."):
                        try:
                            
                            api_url = "http://127.0.0.1:9880/" 
                            
                            payload = {
                                "text": text,                   
                                "text_lang": text_lang,                          
                                "ref_audio_path": r"D:\GPT-SoVITS-v2pro-20250604-nvidia50\nahida等11个文件\nahida\v1\推理音频\新鲜感，就是来源于生活中的小小仪式哦。.wav",  
                                "prompt_text": "新鲜感，就是来源于生活中的小小仪式哦。",            
                                "prompt_lang": "zh",            
                                "top_k": top_k,                   
                                "top_p": top_p,                   
                                "temperature": temperature,             
                                "text_split_method": text_split_method,  
                                "batch_size": batch_size,              
                                "batch_threshold": batch_threshold,      
                                "split_bucket": split_bucket,      
                                "speed_factor": speed_factor,          
                                "fragment_interval": fragment_interval,     
                                "seed": raw,                   
                                "parallel_infer": parallel_infer,         
                                "repetition_penalty": repetition_penalty,   
                                "sample_steps": sample_steps,           
                                "super_sampling": super_sampling,      
                                "streaming_mode": streaming_mode,      
                                "overlap_length": overlap_length,          
                                "min_chunk_length": min_chunk_length,
                            }
                            
                            if_music = background_music
                            data_to_send = {
                                    "sovits_payload": payload,
                                    "if_music": if_music
                                }
                            with open("transfer_data.json", "w", encoding="utf-8") as f:
                                json.dump(data_to_send, f, ensure_ascii=False, indent=4)
                            subprocess.run(["cmd.exe", "/c", BAT_PATH2], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        except Exception as e:
                            st.error(f"连接 API 的时候遇到了一点小麻烦：{e}")
