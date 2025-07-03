@echo off
echo Starting CodeBridge Frontend on Port 3045...
echo ==========================================
echo.
cd /d "%~dp0..\frontend"
python simple_server.py
