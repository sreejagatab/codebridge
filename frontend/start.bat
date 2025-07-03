@echo off
echo ==========================================
echo CodeBridge Frontend Server (Port 3045)
echo ==========================================
echo.
echo Serving from: %~dp0public
echo URL: http://localhost:3045
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
cd /d "%~dp0public"
python -m http.server 3045
pause
