@echo off
echo ACTS - Accountability & Corruption Tracking System
echo Git Repository Setup Script
echo =====================================

REM Navigate to project directory
cd /d "c:\Users\My\OneDrive\Desktop\Learning_Project\ACTS"

REM Check if git is available
git --version
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Initialize git repository if not already done
if not exist ".git" (
    echo Initializing git repository...
    git init
)

REM Set git configuration
echo Setting git configuration...
git config user.name "nishan1314"
git config user.email "nishan1314@example.com"

REM Add all files
echo Adding files to git...
git add .

REM Create initial commit
echo Creating initial commit...
git commit -m "Initial commit: ACTS - Accountability & Corruption Tracking System for Bangladesh

Features implemented:
- Django backend with PostgreSQL support
- Dashboard with procurement data analysis
- Citizen reporting system with SHA-256 receipts
- Risk analysis algorithms
- Bangladesh district heatmaps
- AI-powered corruption detection
- Responsive web interface with Bangladesh theme
- Fixed navigation bar
- Montserrat typography
- Font Awesome icons"

REM Add remote repository
echo Adding remote repository...
git remote add origin https://github.com/nishan1314/acts-ict.git

REM Push to GitHub
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo SUCCESS: Project has been pushed to GitHub!
echo Repository URL: https://github.com/nishan1314/acts-ict.git
echo.
pause
