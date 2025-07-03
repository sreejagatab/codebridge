@echo off
echo ==========================================
echo Starting CodeBridge Full Stack Application
echo ==========================================
echo.
echo [1/3] Starting Backend Server (Port 3047)...
start "CodeBridge Backend" cmd /k "cd /d %~dp0 && uvicorn app.main:app --host 0.0.0.0 --port 3047 --reload"

echo.
echo [2/3] Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo.
echo [3/3] Starting Frontend Server (Port 3045)...
start "CodeBridge Frontend" cmd /k "cd /d %~dp0..\frontend && start.bat"

echo.
echo ==========================================
echo CodeBridge Application Started!
echo ==========================================
echo Backend:  http://localhost:3047
echo Frontend: http://localhost:3045
echo API Docs: http://localhost:3047/docs
echo Health:   http://localhost:3047/api/health
echo ==========================================
echo.
pause
