@echo off
echo ==========================================
echo CodeBridge System Test & Startup
echo ==========================================

echo.
echo 1. Installing dependencies...
pip install requests > nul 2>&1

echo.
echo 2. Running import tests...
python -c "from app.main import app; print('✅ FastAPI app import successful')"
if %errorlevel% neq 0 (
    echo ❌ Import test failed
    goto :error
)

echo.
echo 3. Testing database setup...
python -c "from app.core.database import create_tables; create_tables(); print('✅ Database tables created')"
if %errorlevel% neq 0 (
    echo ❌ Database setup failed
    goto :error
)

echo.
echo 4. Running database seeding...
python -c "from app.core.database import SessionLocal; from app.services.database_service import seed_database; db = SessionLocal(); seed_database(db); db.close(); print('✅ Database seeded')"
if %errorlevel% neq 0 (
    echo ❌ Database seeding failed
    goto :error
)

echo.
echo 5. Testing configuration...
python -c "from app.core.config import settings; print(f'✅ Configuration OK - {settings.APP_NAME} v{settings.VERSION} on port {settings.PORT}')"
if %errorlevel% neq 0 (
    echo ❌ Configuration test failed
    goto :error
)

echo.
echo ==========================================
echo ✅ ALL TESTS PASSED!
echo ==========================================
echo.
echo Starting CodeBridge server...
echo.
echo Available endpoints:
echo - Root: http://localhost:3047/
echo - Health: http://localhost:3047/api/health
echo - Database Health: http://localhost:3047/api/health/database
echo - API Docs: http://localhost:3047/docs
echo.
echo Press Ctrl+C to stop the server
echo ==========================================

python start_system.py

goto :end

:error
echo.
echo ==========================================
echo ❌ TESTS FAILED
echo ==========================================
echo Please check the errors above and fix them.
pause
exit /b 1

:end
echo.
echo Server stopped.
pause
