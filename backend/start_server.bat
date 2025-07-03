@echo off
echo Starting CodeBridge Backend Server (Step 2 Complete)
echo ===================================================

REM Step 1: Install any missing dependencies
echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1
pip install requests > nul 2>&1

REM Step 2: Initialize database if needed
echo Initializing database...
python -c "from app.core.database import create_tables; create_tables(); print('Database ready')" 2>nul

REM Step 3: Seed database
echo Seeding database...
python -c "from app.core.database import SessionLocal; from app.services.database_service import seed_database; db = SessionLocal(); seed_database(db); db.close(); print('Database seeded')" 2>nul

REM Step 4: Start the FastAPI server
echo Starting server on http://localhost:3047
echo.
echo Available endpoints:
echo - Root: http://localhost:3047/
echo - Health: http://localhost:3047/api/health
echo - Database Health: http://localhost:3047/api/health/database
echo - API Documentation: http://localhost:3047/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 3047 --reload
