@echo off
echo Starting PostgreSQL database...
docker-compose up -d postgres

if %errorlevel% neq 0 (
    echo Failed to start PostgreSQL. Make sure Docker is running.
    pause
    exit /b 1
)

echo PostgreSQL started successfully!
echo Waiting for database to be ready...
timeout /t 10 /nobreak > nul

echo Testing database connection...
python manage.py test-db

if %errorlevel% neq 0 (
    echo Database connection test failed. Check your configuration.
    pause
    exit /b 1
)

echo Database is ready!
pause
