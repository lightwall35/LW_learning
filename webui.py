import streamlit as st
import subprocess
import os
import streamlit.components.v1 as components
import base64
from PIL import Image
import random
import json
import mimetypes

# ==========================================
# 辅助函数：将本地图片文件编码为 base64 格式
# 作用：用于支持动态修改 CSS 和 HTML 中的内嵌图片展示
# ==========================================
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    return encoded_string

# ==========================================
# 辅助函数：切换当前横屏背景图片流的索引
# 作用：绑定在配置页面的“背景图片”按钮的回调事件上，用于来回切换网页全局模糊图
# ==========================================
def change_bg_index():
    if st.session_state.get("img_list_for_background"):
        current_len = len(st.session_state.img_list_for_background)
        st.session_state.img_index_for_background = (st.session_state.img_index_for_background + 1) % current_len

# ==========================================
# 全局硬编码变量初始化
# ==========================================
# 作用：硬编码一张默认的前景角色图片路径以及将其转化为 base64 代码备用
img_path = r"E:\Nahida\115467919_p0.jpg"
img_base64 = get_image_base64(img_path)

# 作用：全局默认网页毛玻璃图与模糊度的初始设定
BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?q=80&w=1080" 
BLUR_RADIUS = "6px" 
MAIN_TITLE = "Embark on your audio journey with me" 

# 作用：设置核心批处理外部命令和存放本地录音目录的文件路径
BAT_PATH = "E:\\pycode\\auto.bat"
BAT_PATH1 = "E:\\pycode\\auto_science.bat"
BAT_PATH2 = "E:\\pycode\\webui_request.bat"
AUDIO_DIR = "E:\\pycode\\otp"

# ==========================================
# 核心状态 (Session State) 变量：图片池加载并初始化
# 作用：它会自动扫描你电脑上的目标文件夹，聪明地把竖向图选作前景图片，横向图塞入背景池
# ==========================================
if 'img_list' not in st.session_state:
    img_folder = r"E:\selected_pictures"
    valid_exts = (".jpg", ".jpeg", ".png", ".webp")
    candidate_imgs = []
    candidate_imgs_for_background = []
    if os.path.exists(img_folder):
        for filename in os.listdir(img_folder):
            if filename.lower().endswith(valid_exts):
                full_path = os.path.join(img_folder, filename)
                try:
                    with Image.open(full_path) as img:
                        w, h = img.size
                        if w < h:  
                            candidate_imgs.append(full_path)
                        else:
                            candidate_imgs_for_background.append(full_path)
                except:
                    continue 
        # 打乱图片加载的预设顺序以提供新鲜感
        random.shuffle(candidate_imgs) 
        st.session_state.img_list = candidate_imgs
        st.session_state.img_index = 0 
        random.shuffle(candidate_imgs_for_background) 
        # 额外塞入一张特别指定的高清网络风景图作为兜底背景
        special_url = "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?q=80&w=1080"
        candidate_imgs_for_background.insert(0, special_url)
        st.session_state.img_list_for_background = candidate_imgs_for_background
        st.session_state.img_index_for_background = 0 

# ==========================================
# 动态计算和应用当前的网页毛玻璃背景
# 作用：如果当前指针落在本地图片上，会将它转换为能让浏览器直接读取的协议内嵌数据
# ==========================================
if st.session_state.get("img_list_for_background"):
    current_bg_index = st.session_state.img_index_for_background
    current_bg_path = st.session_state.img_list_for_background[current_bg_index]
    if current_bg_path.startswith("http"):
        BACKGROUND_IMAGE = current_bg_path
    else:
        bg_base64 = get_image_base64(current_bg_path)
        mime_type, _ = mimetypes.guess_type(current_bg_path)
        if not mime_type:
            mime_type = "image/jpeg"
        BACKGROUND_IMAGE = f"data:{mime_type};base64,{bg_base64}"
        BLUR_RADIUS = "6px" 

# ==========================================
# 基础页面全局设置与会话组件设定
# 作用：收起烦人的侧边栏并使页面铺满、初始化选中的音频列表参数
# ==========================================
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
if 'show_list' not in st.session_state:
    st.session_state.show_list = False      
if 'selected_audio' not in st.session_state:
    st.session_state.selected_audio = None  

# ==========================================
# CSS 注射库：全站深度样式覆写重制
# 作用：接管 Streamlit 自带的老土样式，更换为毛玻璃晶体质感的视觉特效！
# ==========================================
custom_css = f"""
<style>
    /* 【隐藏原生控件】
       作用：隐藏了 Streamlit 原生带有的右上角三个点菜单以及底部的“Made with Streamlit”标识
       应用场景：使得整个 WEBUI 脱离 Streamlit 的模版感，变得更加清爽 */
    #MainMenu {{visibility: visible;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* 【超大背景底色】
       作用：为页面打底建立一张带有模糊滤镜的巨幅海报作为全屏背景图
       应用场景：页面全局根节点。使用刚刚在上面生成的动态 BACKGROUND_IMAGE */
    .stApp {{ background-color: transparent; }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-image: url("{BACKGROUND_IMAGE}");
        background-size: cover; background-position: center; background-repeat: no-repeat;
        filter: blur({BLUR_RADIUS}); 
        z-index: -1; 
        transition: background-image 0.5s ease-in-out;
    }}

    /* 【主页顶部导航栏】
       作用：制作了一个带有文字跑马灯的浅浮层玻璃栏
       应用场景：下文中被包裹于主页区域 (<div class="top-nav">) 中起装饰性提示作用 */
    .top-nav {{
        max-width: 800px;
        margin-left: auto;
        border-radius: 40px;
        display: flex; justify-content: flex-end; padding: 10px 50px;
        font-family: 'Helvetica Neue', sans-serif;
        backdrop-filter: blur(18px);
    }}
    .nav-item {{
        font-size: 25px; color: #2e7d32; font-weight: 600; cursor: pointer; transition: color 0.3s ease;
    }}
    .nav-item:hover {{ color: #81c784; }}

    /* 【页面炫彩主标语】
       作用：为页面提供了一句可以从下向上浮现渐入的绿意渐变色大字作为 Slogan
       应用场景：在下方的 main 主页 st.markdown("<div class='main-title'>Embark on your...") 中调用 */
    .main-title {{
        font-size: 4.5rem; font-weight: 700; line-height: 1.5;
        background: linear-gradient(135deg, #2e7d32 0%, #81c784 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px; font-family: 'Helvetica Neue', sans-serif;
        animation: fadeInUp 1s ease-out;
    }}
    
    /* 【核心主力按钮强化设计（Primary）】
       作用：将丑陋的默认方形按钮覆写成了薄荷渐变特效椭圆按钮，并且在鼠标经过时会微幅上扬提亮！
       应用场景：整个页面只要带有 type="primary" 属性的按钮（比如：List, Science, 合成等）全部受到其恩惠！ */
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

    /* 【纯粹字符链接按钮（Secondary）】
       作用：褪去了按钮原有框体的一切元素，让它看起来只是一段可以点击、具有交互反馈的粗体字符而已
       应用场景：页面顶端用来在 main 与 me 之间切换的文字跳转枢纽 (type="secondary")！ */
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
    button[kind="secondary"]:hover {{ color: #81c784 !important; background-color: transparent !important; border: none !important; }}
    button[kind="secondary"]:focus:not(:active) {{ border-color: transparent !important; color: #2e7d32 !important; }}

    /* 【高透毛玻璃播放图窗】
       作用：通过极其强大的 -webkit-backdrop-filter 实现一个将下层图像进行超强模糊扭曲的透色框体展示区域
       应用场景：当你在点击音频播放的时候，浮现于前景大图前方的 `<div class="audio-glass-box">` 面板 */
    .audio-glass-box {{
        background: rgba(255, 255, 255, 0.01); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 24px; padding: 30px;
        box-shadow: 0 10px 40px rgba(129, 199, 132, 0.2); animation: fadeIn 1s ease-out;
        display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 500px;
        position: relative !important;
        top: -40px !important;
    }}

    /* 【关键帧动效库（Keyframes）】
       作用：收录了浮动淡入淡出、左侧切入弹出等一系列炫彩的位移公式！
       应用场景：为按钮、标语和图片入场赋予灵魂，供上文下文各个元素的 animation 里直接被调用 */
    @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: scale(0.95); }} to {{ opacity: 1; transform: scale(1); }} }}
    @keyframes slideInLeftScript {{ 0% {{ transform: translateX(-50px); opacity: 0; }} 100% {{transform: translateX(0); opacity: 1; }} }}

    /* 【浮空透明下拉选择器】
       作用：将普通的白底黑字选单强行魔改成带浅绿框线的高透菜单框并赋予高亮选定指示
       应用场景：影响你选了 List 按钮之后，弹出的那个用来筛选本地历史音频框体的 st.selectbox 样式 */
    div[data-baseweb="select"] > div {{
        background-color: rgba(255, 255, 255, 0.4) !important; 
        border-radius: 15px !important; 
        border: 2px solid transparent !important; 
    }}
    div[data-baseweb="select"] > div:hover {{ border: 2px solid #a5d6a7 !important; }}
    div[data-baseweb="select"] span {{ color: #2e7d32 !important; font-weight: bold !important; }}
    div[data-baseweb="popover"] ul {{ background-color: #81c784 !important; border-radius: 15px !important; padding: 5px !important; overflow-y: auto !important;  }}
    ul[data-baseweb="menu"] li {{ color: #2e7d32 !important; border-radius: 10px !important; transition: background-color 0.2s ease !important; }}
    ul[data-baseweb="menu"] li:hover {{ background-color: rgba(165, 214, 167, 0.5) !important;  }}

    /* 【魔幻翠绿音频轨道条】
       作用：入侵并修改了 Chrome 浏览器等 Webkit 内核专属的音频控件媒体条底层面板（-webkit-media-controls-panel）
       应用场景：强行让你呼出的 st.audio() 音乐条从传统的灰色条子变成了通体绿色的大胶囊！ */
    audio::-webkit-media-controls-panel {{
        background-color: rgba(24, 244, 77, 0.65) !important; 
        border-radius: 20px !important; 
    }}

    /* 【随音乐起舞的波浪光谱】
       作用：用高度复杂的 CSS 手写了 18 个条形小格子，设定不同的 animation-delay 错开时间以模拟声音柱群跳动！
       应用场景：嵌套在 audio-glass-box 里的 <div class="playing-bars">，它会在你播放音乐时起舞。 */
    .playing-bars {{ 
        position: absolute; 
        top: 50%; left: 50%;
        transform: translate(-50%, 40%); 
        display: flex; align-items: flex-end; justify-content: center; 
        height: 120px; gap: 12px; 
        opacity: 0.9; 
        z-index: 0; 
    }}
    .bar {{ width: 12px; background-color: #2e7d32; border-radius: 6px; animation: jump 1s infinite ease-in-out; animation-play-state: paused; }}
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
    @keyframes jump {{ 0%, 100% {{ height: 20px; }} 50% {{ height: 120px; }} }}

    /* 【音频控件上提防挡】
       作用：粗暴但有效地将音频条相对其默认位置向上强行偏移了 100px 放置
       应用场景：直接影响代码中的 st.audio 元素防止它沉底被吞并 */
    div.stAudio {{ position: relative; margin-top: -100px !important; z-index: 10; padding: 0 20px; }}

    /* 【前景魔术相框（平滑淡入淡出改良版）】
       作用：为页面纵向人物预览图构建一个稳定的静态图层
       应用场景：在这个相框内，我们将会在后台悄悄动态注入 background-image，从而实现跨图平稳渐变过渡效果！ */
    .foreground-magic-layer {{
        position: absolute; z-index: 0; border-radius: 20px; opacity: 0.8;
        top: -360px; left: 0;
        width: 100%; aspect-ratio: 1 / 1.5;
        background-size: cover; background-position: center; background-repeat: no-repeat;
        transition: background-image 0.5s ease-in-out;
    }}

    /* 【透明晶体输入文本域】
       作用：抹掉 Streamlit 富文本框沉重的底色，套上了具有强烈透镜感、圆角打磨及获得焦点悬浮高亮的质感
       应用场景：直接接管 me 页面的核心模块——也就是那个承载文字输入的巨大 st.text_area 框体输入面板 */
    div.stTextArea [data-baseweb="textarea"],
    div.stTextArea [data-baseweb="base-input"] {{ background-color: transparent !important; }}
    div.stTextArea [data-baseweb="textarea"] {{
        animation: slideInLeftScript 0.6s ease-out !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
        z-index: 60 !important;
    }}
    div.stTextArea [data-baseweb="textarea"]:focus-within {{
        border-color: rgba(165, 214, 167, 0.8) !important;
        box-shadow: 0 0 15px rgba(165, 214, 167, 0.2) !important;
    }}
    div.stTextArea textarea {{ color: #2e7d32 !important; font-weight: 500 !important; line-height: 1.6 !important; top: -100px !important; }}
    div.stTextArea textarea::placeholder {{ color: rgba(46, 125, 50, 0.5) !important; }}

    /* 【参数滑块组件的绿色革命】
       作用：放大滑轨体积达到厚实的 10px，并将提示小字及轨道上的各项数值强行涂绿以融入绿意森林感的设计里
       应用场景：主要在 me 参数配置页面中影响着十个左右如 top_k / top_p 这类的 st.slider 进度拖动条 */
    div.stSlider label {{ color: #2e7d32 !important; font-weight: 600 !important; font-size: 16px !important; }}
    div.stSlider [data-baseweb="slider"] > div > div {{ height: 10px !important; border-radius: 4px !important; }}
    div.stSlider [data-testid="stTickBar"] {{ color: #4caf50 !important; }}

    /* 【全局文本 Label 组件统一样式】
       作用：把很多组件（例如下拉框、开关）默认提示字的灰色基调替换为了生机盎然的清脆绿
       应用场景：用于包裹各类 widget 之上的 <label> 原件 */
    div[data-testid="stWidgetLabel"] p, label p {{ color: #2e7d32 !important; font-size: 16px !important; font-weight: 600 !important; }}

    /* 【大号夸张的 Toggle 开关按钮】
       作用：通过 scale(3) 极其直接地将原组件在长宽比例上等比放大 3 倍
       应用场景：控制 me 底部那一长列类似 parallel_infer 等等的 st.toggle 开关以方便点击盲操 */
    div[data-testid="stToggle"] {{ transform: scale(3) !important; }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 页面路由与主逻辑区分配
# 作用：充当路由器的角色让系统默认落地于 "main" 并根据状态在各页面间切换
# ==========================================
if 'page_now' not in st.session_state:
       st.session_state.page_now = 'main'

# ----------------- MAIN (主页音频欣赏页面区) -----------------
# 作用：展示目前已生成的音频、查看精美视觉人物壁纸插图的地方
if st.session_state.page_now == 'main':
    # 控制右上角进行 me 配置页面跳转的区域及一行跑马灯提示语
    col_1,col_2= st.columns([10, 1])
    with col_2:
        if st.button("me", key="btn_me", type="secondary"):
            st.session_state.page_now = 'me'
            st.rerun()
    st.markdown('<div class="top-nav"><span class="nav-item">WHEN I REALLISE TAHT THIS IS A USELESS TOP NAVIGATION EVERYTHING HAS BEEN TOO LATE</span></div>', unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # 切分页面显示：左边用来展示动态图像与音频面板，右边用来排布按钮并控制行为
    col_left, col_right = st.columns([1, 1.2])

    # ===== 右侧面板：主要任务栏与外部调度按钮区 =====
    with col_right:
        st.markdown(f'<div class="main-title">{MAIN_TITLE}</div>', unsafe_allow_html=True)
        # 作用：排版技巧 —— 刻意布置并遗失后两个空列以使这俩列表项始终受挤压偏左展示
        col_left1, col_right1, col_left2, col_right2 = st.columns([1, 1, 1, 1])
        
        # 内部列 1：启动自动流程大批处理 / 收放历史录音文件框
        with col_left1:
            if st.button("global", type="primary", key="btn_global"):
                with st.spinner("悄悄唤醒批处理流水线"):
                    try:
                        subprocess.run(["cmd.exe", "/c", BAT_PATH], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        st.success("启动指令发送成功")
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
                        # 将挑选好的本地音频录入全局状态便于播放
                        if selected_file != "-- 请选择 --":
                            st.session_state.selected_audio = os.path.join(AUDIO_DIR, selected_file)
                        else:
                            st.session_state.selected_audio = None

        # 内部列 2：触发额外的 science 推理任务 / 循环切换主屏幕显示的插图大壁纸
        with col_right1:
            if st.button("science", type="primary", key="btn_science"):
                with st.spinner("正在启动 Science 批处理文件..."):
                    try:
                        subprocess.run(["cmd.exe", "/c", BAT_PATH1], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        st.success("Science 启动成功")
                    except Exception as e:
                        st.error(f"遇到麻烦了：{e}")
            if st.button("Change", key="btn_change_picture",type="primary"):
                if st.session_state.img_list:
                    st.session_state.img_index = (st.session_state.img_index + 1) % len(st.session_state.img_list)
        
    # ===== 左侧面板：画廊壁纸及交互式音乐动态波形大屏幕区 =====
    with col_left:
        # 将被选中的竖屏前景图片解析出 base64 代码准备压入 HTML 展示
        if st.session_state.img_list:
            current_img_path = st.session_state.img_list[st.session_state.img_index]
            try:
                dynamic_img_base64 = get_image_base64(current_img_path)
            except Exception as e:
                dynamic_img_base64 = img_base64 
        else:
            dynamic_img_base64 = img_base64

        # 核心解法：分离“会变的图片流”与“固定的 DOM 容器”
        # 这里单独负责抛出动态 CSS 样式，通知浏览器更换底层 .foreground-magic-layer 相框里的壁纸
        st.markdown(f'''
            <style>
                .foreground-magic-layer {{
                    background-image: url('data:image/jpeg;base64,{dynamic_img_base64}');
                }}
            </style>
        ''', unsafe_allow_html=True)

        # 情况 A：如果当前用户开启录音列表，并选中了合法的录音路径，则召唤动态图谱播放器！
        if st.session_state.show_list and st.session_state.selected_audio and os.path.exists(st.session_state.selected_audio):
            file_name = os.path.basename(st.session_state.selected_audio)
            
            # 使用原生 HTML 代码组装固定相框、毛玻璃浮板以及 CSS 琴键动画棒阵列
            # 特别注意：只要 file_name 不变，下方这段 HTML 字符就是严丝合缝一致的！
            # 浏览器一旦发现 div 没被销毁重建，就会触发通过 `<style>` 更新 `background-image` 的 0.5秒渐变 transition！
            st.markdown(f'''
    <div style="position: relative; width: 100%; min-height: 400px;">
        <div class="foreground-magic-layer"></div>                       
        <div class="audio-glass-box">
            <h4 style="color: #2e7d32; margin-bottom: -2px; position: relative; z-index: 1;top: -10px;font-size: 35px"> 正在播放选中音频</h4>
            <div style="color: #4caf50; font-size: 14px; margin-bottom: 90px; position: relative; z-index: 1;left: -10px;">当前文件: {file_name}</div>
            <div class="playing-bars">
                <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
                <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
                <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
            </div>
        </div>
    </div>
            ''', unsafe_allow_html=True)
            
            # 引入音乐播放元件
            st.audio(st.session_state.selected_audio)
            
            # 高级黑魔法：通过嵌入微型的 JavaScript 定时器侦听 audio 属性来联动动画律动
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
                            if (audioTag.paused) { bar.style.animationPlayState = 'paused'; } 
                            else { bar.style.animationPlayState = 'running'; }
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
            
        # 情况 B：不处于播放面板展示状态时，安静地仅显示静态相框图层即可
        else:
            st.markdown(f'''
    <div style="position: relative; width: 100%; min-height: 400px;">
        <div class="foreground-magic-layer"></div>                   
    </div>
            ''', unsafe_allow_html=True)


# ----------------- ME (详细配置选项面板区) -----------------
# 作用：作为 GPT-SoVITS 语音合成核心的中枢发源地调整合成细节的地方
if st.session_state.page_now == 'me':
    # 以大约 1.2:1 的权重分配大文本输入框和密密麻麻繁多的模型数值滑块
    col_A, col_B = st.columns([1.2, 1])
    
    # ===== 页面右侧参数设置台 =====
    with col_B:
        # 配置界面也有返回逻辑的退出枢纽
        col_1,col_2= st.columns([3.5, 1])
        with col_2:
            if st.button("main", key="btn_me", type="secondary"):
                st.session_state.page_now = 'main'
                st.rerun()   

        st.markdown("<h4 style='color: #2e7d32;'>参数设置</h4>", unsafe_allow_html=True) 
        
        # 作用：核心配置基础信息（语种、种子号等）
        text_lang = st.selectbox("文本语言", ["zh", "en", "ja", "yue"], key="lang_select")
        seed = st.slider("seed", -1, 99999, 99999, key="seed_slider")
        raw = 99998-seed
        
        # 作用：运用对分列的布局对密集繁琐地 SoVITS TTS 相关高级控制超参进行展示调整
        col_k,col_l = st.columns([1,1])
        with col_k:
            top_k = st.slider("top_k", 0, 20, 5, key="top_k_slider")
            top_p = st.slider("top_p", 0.0, 1.0, 1.0, key="top_p_slider")
            temperature = st.slider("temperature", 0.1, 2.0, 1.0, key="temp_slider")
            batch_size = st.slider("batch_size", 1, 8, 1, key="batch_size_slider")
            batch_threshold = st.slider("batch_threshold", 0.0, 1.0, 0.75, key="batch_threshold_slider") 
            text_split_method = st.segmented_control("文本切分方式", options=["cut5", "cut10", "cut20", "none"],default="cut5",key="split_method_control")
        with col_l:      
            speed_factor = st.slider("speed_factor", 0.5, 2.0, 1.0, key="speed_factor_slider")
            fragment_interval = st.slider("fragment_interval", 0.0, 1.0, 0.3, key="fragment_interval_slider")
            repetition_penalty = st.slider("repetition_penalty", 1.0, 2.0, 1.35, key="repetition_penalty_slider")
            sample_steps = st.slider("sample_steps", 1, 64, 32, key="sample_steps_slider")
            min_chunk_length = st.slider("min_chunk_length", 1, 64, 16, key="min_chunk_length_slider")
            background_music = st.segmented_control("背景音乐", options=["off", "on"], default="on", key="bgm_control")
            
        # 作用：平铺展示底部的实验性及进阶性 Toggle 拨动控制开关
        col_q,col_w,col_e,col_r = st.columns([1,1,1,1])
        with col_q: split_bucket = st.toggle("split_bucket", key="split_bucket_toggle")
        with col_w: parallel_infer = st.toggle("parallel_infer", key="parallel_infer_toggle")
        with col_e: super_sampling = st.toggle("super_sampling", key="super_sampling_toggle")
        with col_r: streaming_mode = st.toggle("streaming_mode", key="streaming_mode_toggle") # 注：流式输出目前处于关停警告状态
        overlap_length = st.slider("overlap_length", 0, 10, 2, key="overlap_length_slider")
    
    # ===== 页面左侧：长文输入合成区及最终提交按钮面板 =====
    with col_A:
        # 作用：抓取用户输入将准备转化为语音的长篇故事或者小说数据
        text = st.text_area(
            label="这是一个圆角矩形：",
            placeholder="",
            height=650,  
            key="my_glass_textarea"
        )
        col_z, col_x, col_c = st.columns([1, 1, 1])
        with col_z:
            # 作用：全流程的点火中心。收集上面所有调整过的表盘数据并写入 JSON 交给后台请求器处理！
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
                                "ref_audio_path": r"D:\GPT-SoVITS-v2pro-20250604-nvidia50\参考音频\先否定一些不可行的方案，会让即将提出要施行的计划变得更有分量，这可是教令院因论派中非常主流的观点。.wav",  
                                "prompt_text": "先否定一些不可行的方案，会让即将提出要施行的计划变得更有分量，这可是教令院因论派中非常主流的观点。",            
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
                            # 数据持久化并呼出 bat 执行外包的请求脚本
                            json_save_path = r"E:\pycode\transfer_data.json"
                            with open(json_save_path, "w", encoding="utf-8") as f:
                                json.dump(data_to_send, f, ensure_ascii=False, indent=4)
                            subprocess.run(["cmd.exe", "/c", BAT_PATH2], check=True)
                        except Exception as e:
                            st.error(f"连接 API 的时候遇到了一点小麻烦：{e}")
        
        with col_x:
            # 作用：点击后执行 change_bg_index 后台函数，切换整体全局毛玻璃后的壁纸图
            st.button("背景图片", key="btn_change_picture", type="primary", on_click=change_bg_index)
