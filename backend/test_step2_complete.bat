@echo off
echo Step 2 Database Foundation Validation
echo ====================================

echo.
echo 1. Installing dependencies...
pip install aiosqlite
if %errorlevel% neq 0 (
    echo Failed to install aiosqlite
    pause
    exit /b 1
)

echo.
echo 2. Creating database tables...
python -c "from app.core.database import create_tables; create_tables(); print('Tables created successfully')"
if %errorlevel% neq 0 (
    echo Failed to create tables
    pause
    exit /b 1
)

echo.
echo 3. Running simple database test...
python simple_db_test.py
if %errorlevel% neq 0 (
    echo Simple database test failed
    pause
    exit /b 1
)

echo.
echo 4. Running comprehensive Step 2 tests...
python test_step2.py
if %errorlevel% neq 0 (
    echo Step 2 tests failed
    pause
    exit /b 1
)

echo.
echo 5. Starting server to test health endpoints...
start "CodeBridge Backend" python -m uvicorn app.main:app --host 0.0.0.0 --port 3047 --reload

echo.
echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo.
echo 6. Testing health endpoints...
curl -f http://localhost:3047/api/health/simple
echo.
curl -f http://localhost:3047/api/health/database
echo.

echo.
echo ====================================
echo Step 2 Database Foundation Complete!
echo ====================================
echo.
echo Available endpoints:
echo - Health: http://localhost:3047/api/health
echo - Database Health: http://localhost:3047/api/health/database
echo - API Docs: http://localhost:3047/docs
echo.
echo Press any key to continue...
pause > nul
