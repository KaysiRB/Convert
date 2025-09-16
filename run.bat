@echo off
title Outfits converter

REM Go to the folder of the .bat file
cd /d "%~dp0"

echo.
echo ========================================
echo    Outfits converter - Launcher
echo ========================================
echo.
echo Working directory : %cd%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in the PATH.
    echo.
    echo Please install Python from : https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo Main.py file not found in this folder.
    echo.
    echo Make sure this .bat file is in the same folder as main.py.
    echo.
    pause
    exit /b 1
)

REM Run the Python script
echo Launching the converter...
echo.
python main.py

REM Pause at the end
echo.
echo ========================================
pause