@echo off
echo Starting FastAPI Server and WebUI...

cd /d E:\pycode

start "FastAPI Server" cmd /k "python server.py"

timeout /t 3 /nobreak >nul

start http://127.0.0.1:8000

echo.
echo Startup complete! You can close this window.
pause
