if not "%1"=="minimized" start "" /min "%~f0" minimized & exit
set "SCRIPT_DIR=D:\GPT-SoVITS-v2pro-20250604-nvidia50\GPT-SoVITS-v2pro-20250604-nvidia50"
cd /d "%SCRIPT_DIR%"
set "PATH=%SCRIPT_DIR%\runtime;%PATH%"
"%SCRIPT_DIR%\runtime\python.exe" -I "%SCRIPT_DIR%\webui.py" zh_CN
pause
