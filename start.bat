@echo off
echo Starting Food Ordering System...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then activate it and install requirements.txt
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your settings
    echo.
    pause
)

REM Activate virtual environment and start the application
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting Flask application...
echo.
echo Customer Interface: http://localhost:5000/
echo Worker Dashboard:   http://localhost:5000/worker
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
