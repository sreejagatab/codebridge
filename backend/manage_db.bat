@echo off
REM Database management scripts for CodeBridge backend

echo CodeBridge Database Management
echo ===============================

:menu
echo.
echo 1. Start PostgreSQL (Docker)
echo 2. Run Migrations
echo 3. Seed Database
echo 4. Test Database Connection
echo 5. Initialize Database (Migrate + Seed)
echo 6. Reset Database
echo 7. Create New Migration
echo 8. Rollback Migration
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto start_postgres
if "%choice%"=="2" goto migrate
if "%choice%"=="3" goto seed
if "%choice%"=="4" goto test_db
if "%choice%"=="5" goto init_db
if "%choice%"=="6" goto reset_db
if "%choice%"=="7" goto create_migration
if "%choice%"=="8" goto rollback
if "%choice%"=="9" goto exit

echo Invalid choice. Please try again.
goto menu

:start_postgres
echo Starting PostgreSQL with Docker Compose...
docker-compose up -d postgres
if %errorlevel% neq 0 (
    echo Failed to start PostgreSQL. Make sure Docker is running.
    pause
    goto menu
)
echo PostgreSQL started successfully!
echo Waiting for database to be ready...
timeout /t 5 /nobreak > nul
goto menu

:migrate
echo Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Migration failed!
    pause
)
goto menu

:seed
echo Seeding database...
python manage.py seed
if %errorlevel% neq 0 (
    echo Seeding failed!
    pause
)
goto menu

:test_db
echo Testing database connection...
python manage.py test-db
pause
goto menu

:init_db
echo Initializing database...
python manage.py init-db
if %errorlevel% neq 0 (
    echo Database initialization failed!
    pause
)
goto menu

:reset_db
echo WARNING: This will delete all data in the database!
set /p confirm="Are you sure? (y/N): "
if /i not "%confirm%"=="y" goto menu
echo Resetting database...
python manage.py reset-db
if %errorlevel% neq 0 (
    echo Database reset failed!
    pause
)
goto menu

:create_migration
set /p message="Enter migration message: "
echo Creating migration: %message%
python manage.py makemigration "%message%"
if %errorlevel% neq 0 (
    echo Migration creation failed!
    pause
)
goto menu

:rollback
set /p revision="Enter revision to rollback to (-1 for previous): "
echo Rolling back to: %revision%
python manage.py rollback --revision "%revision%"
if %errorlevel% neq 0 (
    echo Rollback failed!
    pause
)
goto menu

:exit
echo Goodbye!
exit /b 0
