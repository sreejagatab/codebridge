@echo off
echo ==========================================
echo CodeBridge Steps 1 & 2 Validation
echo ==========================================

echo.
echo 1. Running comprehensive validation...
python validate_steps_1_2.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Validation failed! Please check the issues above.
    pause
    exit /b 1
)

echo.
echo 2. Running database demonstration...
python demo_step2.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Database demo failed! Please check the issues above.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ ALL VALIDATIONS PASSED!
echo ==========================================
echo.
echo Steps 1 & 2 are fully implemented and ready!
echo.
echo Next actions:
echo - Review the completion report: STEPS_1_2_COMPLETION_REPORT.md
echo - Check the updated README.md
echo - Start the server: start_server.bat
echo - View API docs: http://localhost:3047/docs
echo.
echo 🚀 Ready to proceed to Step 3!
echo.
pause
