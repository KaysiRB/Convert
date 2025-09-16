@echo off
title Outfits Converter Launcher

REM Navigate to the folder of the .bat file
cd /d "%~dp0"

echo.
echo ========================================
echo       Outfits Converter - Launcher
echo ========================================
echo Working directory : %cd%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in the PATH.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if main.py exists in src\
if not exist "src\main.py" (
    echo [ERROR] main.py file not found in src\ directory.
    echo Make sure this .bat file is in the root directory and main.py is in src\.
    echo.
    pause
    exit /b 1
)

REM Run the Python script
echo Launching the converter...
echo.
python src\main.py
if errorlevel 1 (
    echo [ERROR] An error occurred while running main.py
    echo Check your Python script for issues.
    echo.
)

echo.
echo ========================================
pause