@echo off
echo Setting up ACTS Development Environment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Database migration failed
    pause
    exit /b 1
)

echo.
echo Creating superuser account...
echo Please enter superuser details:
python manage.py createsuperuser

echo.
echo Loading sample data...
python manage.py load_sample_data --tenders=50
if errorlevel 1 (
    echo WARNING: Sample data loading failed, but application should still work
)

echo.
echo ============================================
echo Setup completed successfully!
echo.
echo To start the development server:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Run server: python manage.py runserver
echo 3. Open browser: http://localhost:8000
echo.
echo Admin panel: http://localhost:8000/admin/
echo API docs: http://localhost:8000/api/docs/
echo ============================================
echo.
pause
