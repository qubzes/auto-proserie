@echo off
REM ProSeries W2 Automation Launcher for Windows
REM This batch file helps run the automation on Windows

echo ========================================
echo ProSeries W2 Form Automation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please copy .env.example to .env and add your API key
    pause
    exit /b 1
)

REM Check if requirements are installed
pip show pywinauto >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

echo.
echo Setup complete!
echo.
echo Usage:
echo   1. Make sure ProSeries is running
echo   2. Navigate to the W2 form in ProSeries
echo   3. Run: run_automation.py --json your_w2_data.json
echo.
echo To generate sample data:
echo   python run_automation.py --generate-sample sample.json
echo.
echo To run with sample data:
echo   python run_automation.py --json sample_w2_data.json
echo.

pause
