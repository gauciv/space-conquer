@echo off
echo Space Conquer Launcher
echo =====================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Run the launcher script
python run_game.py
if %errorlevel% neq 0 (
    echo Failed to run the game.
    pause
    exit /b 1
)

exit /b 0
