@echo off
echo ==========================================
echo CODEBRIDGE FULL SYSTEM TEST & RUN
echo ==========================================
echo.
echo This script will:
echo 1. Install dependencies
echo 2. Run comprehensive validation
echo 3. Initialize the database
echo 4. Start the server
echo 5. Test all endpoints
echo.

set /p choice="Do you want to continue? (y/N): "
if /i not "%choice%"=="y" goto :end

echo.
echo ==========================================
echo PHASE 1: DEPENDENCY INSTALLATION
echo ==========================================
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Dependency installation failed!
    pause
    exit /b 1
)

pip install requests
if %errorlevel% neq 0 (
    echo ❌ Failed to install requests!
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!

echo.
echo ==========================================
echo PHASE 2: SYSTEM VALIDATION
echo ==========================================

echo.
echo Testing imports...
python -c "from app.main import app; from app.core.config import settings; print(f'✅ Core imports OK - {settings.APP_NAME} v{settings.VERSION}')"
if %errorlevel% neq 0 (
    echo ❌ Import validation failed!
    pause
    exit /b 1
)

echo.
echo Testing database setup...
python -c "from app.core.database import create_tables; create_tables(); print('✅ Database tables created')"
if %errorlevel% neq 0 (
    echo ❌ Database setup failed!
    pause
    exit /b 1
)

echo.
echo Seeding database...
python -c "from app.core.database import SessionLocal; from app.services.database_service import seed_database, get_database_stats; db = SessionLocal(); seed_database(db); stats = get_database_stats(db); print(f'✅ Database seeded - {stats.get(\"total_projects\", 0)} projects, {stats.get(\"total_content\", 0)} content items'); db.close()"
if %errorlevel% neq 0 (
    echo ❌ Database seeding failed!
    pause
    exit /b 1
)

echo.
echo ✅ System validation completed successfully!

echo.
echo ==========================================
echo PHASE 3: SERVER STARTUP
echo ==========================================
echo.
echo Starting CodeBridge server...
echo.
echo Available endpoints:
echo - Root: http://localhost:3047/
echo - Health: http://localhost:3047/api/health
echo - Database Health: http://localhost:3047/api/health/database
echo - API Documentation: http://localhost:3047/docs
echo.
echo 🔗 In another terminal, run: python test_endpoints.py
echo    to test all endpoints while the server is running.
echo.
echo Press Ctrl+C to stop the server
echo ==========================================

python -m uvicorn app.main:app --host 0.0.0.0 --port 3047 --reload

:end
echo.
echo ==========================================
echo System testing completed.
echo.
echo To run endpoint tests:
echo   python test_endpoints.py
echo.
echo To restart the server:
echo   start_server.bat
echo.
echo To run validation:
echo   python validate_steps_1_2.py
echo ==========================================
pause
