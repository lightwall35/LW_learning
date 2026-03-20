@echo off
chcp 65001 >nul

echo ==============================================
echo                     START
echo ==============================================
echo.

echo 唤醒 GPT-SoVITS api
netstat -ano | find "9880" | find "LISTENING" >nul

if %errorlevel% equ 0 (
    echo api正在运行，跳过启动步骤啦
    goto api_ready
)

echo  API 还没醒，开始唤醒...
cd /d D:\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50
start /min "" .\runtime\python api_v2.py -a 127.0.0.1 -p 9880

:check_port
timeout /t 1 >nul
netstat -ano | find "9880" | find "LISTENING" >nul
if %errorlevel% neq 0 (
    goto check_port
)
echo api 正在待命

:api_ready
echo.
echo 开始抓取新闻并发送配音请求...
C:\Users\minec\miniconda3\envs\tts_env\python.exe "E:\pycode\default copy.py"

for %%f in (E:\pycode\otp\*.wav) do (
    ffmpeg -i "%%f" -b:a 128k "%%~dpnf.mp3" && del "%%f"
)
echo.
echo ==============================================
echo                      END
echo ==============================================
pause