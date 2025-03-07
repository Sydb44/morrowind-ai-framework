@echo off
REM Morrowind AI Framework - Server Startup Script for Windows

echo Starting Morrowind AI Framework Server...

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python not found. Please install Python 3.9 or later.
    goto :end
)

REM Remove existing virtual environment to ensure clean dependencies
if exist "%SCRIPT_DIR%venv" (
    echo Removing existing virtual environment...
    rmdir /s /q "%SCRIPT_DIR%venv"
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv "%SCRIPT_DIR%venv"
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment. Please ensure you have Python 3.9 or later installed.
    goto :end
)

REM Activate virtual environment
echo Activating virtual environment...
call "%SCRIPT_DIR%venv\Scripts\activate.bat"

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r "%SCRIPT_DIR%requirements.txt"
if %ERRORLEVEL% neq 0 (
    echo Failed to install dependencies.
    goto :deactivate
)

REM Create logs directory if it doesn't exist
if not exist "%SCRIPT_DIR%logs" mkdir "%SCRIPT_DIR%logs"

REM Start the server
echo Starting server...
cd "%SCRIPT_DIR%"
python run_server.py

:deactivate
REM Deactivate virtual environment
call "%SCRIPT_DIR%venv\Scripts\deactivate.bat"

:end
echo Press any key to exit...
pause >nul
