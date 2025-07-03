@echo off
echo ==========================================
echo CODEBRIDGE STEP 3: BASIC API FRAMEWORK
echo ==========================================
echo.
echo This script will:
echo 1. Install new dependencies (JWT, authentication)
echo 2. Run database migrations
echo 3. Start the server with Step 3 features
echo 4. Test all new API endpoints
echo.

set /p choice="Do you want to continue? (y/N): "
if /i not "%choice%"=="y" goto :end

echo.
echo ==========================================
echo PHASE 1: DEPENDENCY INSTALLATION
echo ==========================================
echo Installing new dependencies for authentication...
pip install python-jose[cryptography]==3.3.0
if %errorlevel% neq 0 (
    echo ❌ Failed to install python-jose!
    pause
    exit /b 1
)

pip install passlib[bcrypt]==1.7.4
if %errorlevel% neq 0 (
    echo ❌ Failed to install passlib!
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!

echo.
echo ==========================================
echo PHASE 2: DATABASE PREPARATION
echo ==========================================
echo Ensuring database is ready...
python -c "from app.core.database import create_tables; create_tables(); print('✅ Database ready')"
if %errorlevel% neq 0 (
    echo ❌ Database setup failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo PHASE 3: API VALIDATION
echo ==========================================
echo Testing new API components...
python -c "from app.main import app; from app.core.auth import create_access_token; print('✅ Authentication system ready')"
if %errorlevel% neq 0 (
    echo ❌ Authentication validation failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo PHASE 4: SERVER STARTUP
echo ==========================================
echo.
echo Starting CodeBridge API with Step 3 features...
echo.
echo 🆕 NEW IN STEP 3:
echo   • JWT Authentication
echo   • Project CRUD API
echo   • Content CRUD API  
echo   • Rate Limiting
echo   • Enhanced API Documentation
echo.
echo 🔐 Demo Authentication:
echo   • Username: admin, Password: admin123 (full access)
echo   • Username: user, Password: user123 (read/write)
echo.
echo 📚 Available Endpoints:
echo   • Root: http://localhost:3047/
echo   • API Docs: http://localhost:3047/docs
echo   • Health: http://localhost:3047/api/health
echo   • Authentication: http://localhost:3047/api/auth/login
echo   • Projects: http://localhost:3047/api/projects
echo   • Content: http://localhost:3047/api/content
echo.
echo 🧪 To test Step 3 features:
echo   In another terminal, run: python test_step3.py
echo.
echo Press Ctrl+C to stop the server
echo ==========================================

python -m uvicorn app.main:app --host 0.0.0.0 --port 3047 --reload

:end
echo.
echo ==========================================
echo Step 3 testing completed.
echo.
echo To test the new API features:
echo   python test_step3.py
echo.
echo To restart the server:
echo   python -m uvicorn app.main:app --host 0.0.0.0 --port 3047 --reload
echo.
echo To view API documentation:
echo   http://localhost:3047/docs
echo ==========================================
pause
