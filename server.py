import os
import random
import json
import subprocess
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

img_folder = r"E:\selected_pictures"
AUDIO_DIR = r"E:\pycode\otp"
BAT_PATH = r"E:\pycode\auto.bat"
BAT_PATH1 = r"E:\pycode\auto_science.bat"
BAT_PATH2 = r"E:\pycode\webui_request.bat"

# Cache list
cached_fg = []
cached_bg = []
is_cached = False

def init_images():
    global cached_fg, cached_bg, is_cached
    if is_cached:
        return
    valid_exts = (".jpg", ".jpeg", ".png", ".webp")
    fg = []
    bg = []
    if os.path.exists(img_folder):
        for filename in os.listdir(img_folder):
            if filename.lower().endswith(valid_exts):
                full_path = os.path.join(img_folder, filename)
                try:
                    with Image.open(full_path) as img:
                        w, h = img.size
                        if w < h:
                            fg.append(full_path)
                        else:
                            bg.append(full_path)
                except:
                    pass
    random.shuffle(fg)
    random.shuffle(bg)
    special_url = "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?q=80&w=1080"
    bg.insert(0, special_url)
    
    if not fg:
        fg.append(r"E:\Nahida\115467919_p0.jpg")
        
    cached_fg = fg
    cached_bg = bg
    is_cached = True

@app.on_event("startup")
def startup_event():
    print("API Server initializing images...")
    init_images()

@app.get("/")
def serve_index():
    path = "index.html"
    if not os.path.exists(path):
        return HTMLResponse(content="<h1>index.html not found! Make sure it's in the same directory as server.py</h1>", status_code=404)
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/init_data")
def get_init_data():
    return {
        "fg_list": cached_fg,
        "bg_list": cached_bg
    }

@app.get("/api/audio_list")
def get_audio_list():
    if os.path.exists(AUDIO_DIR):
        audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(('.wav', '.mp3'))]
        audio_files.sort(reverse=True)
        return {"audios": audio_files}
    return {"audios": []}

@app.get("/api/file")
def serve_file(path: str):
    if not os.path.exists(path):
        return JSONResponse({"error": "File not found"}, status_code=404)
    return FileResponse(path)

@app.post("/api/run_bat")
def run_bat(bat_type: str):
    try:
        if bat_type == "global":
            subprocess.Popen(["cmd.exe", "/c", BAT_PATH], creationflags=subprocess.CREATE_NO_WINDOW)
            return {"status": "success", "msg": "Global batch task started in background."}
        elif bat_type == "science":
            subprocess.Popen(["cmd.exe", "/c", BAT_PATH1], creationflags=subprocess.CREATE_NO_WINDOW)
            return {"status": "success", "msg": "Science batch task started in background."}
        else:
            return JSONResponse({"error": "Unknown bat type"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

class SynthPayload(BaseModel):
    sovits_payload: dict
    if_music: str

@app.post("/api/synth")
def synth(payload: SynthPayload):
    try:
        data_to_send = {
            "sovits_payload": payload.sovits_payload,
            "if_music": payload.if_music
        }
        json_save_path = r"E:\pycode\transfer_data.json"
        with open(json_save_path, "w", encoding="utf-8") as f:
            json.dump(data_to_send, f, ensure_ascii=False, indent=4)
            
        subprocess.Popen(["cmd.exe", "/c", BAT_PATH2], creationflags=subprocess.CREATE_NO_WINDOW)
        return {"status": "success", "msg": "Synthesis task dispatched!"}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
