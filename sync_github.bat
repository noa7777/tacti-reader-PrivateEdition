@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ========================================
echo   GitHub Sync Script
echo ========================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH.
    pause
    exit /b 1
)

if not exist ".git" (
    echo ERROR: Not a git repository.
    echo Please run "git init" and set up remote first.
    pause
    exit /b 1
)

git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ERROR: No remote 'origin' configured.
    echo Please set remote with: git remote add origin ^<url^>
    pause
    exit /b 1
)

echo [1/5] Checking git status...
git status --short
echo.

echo [2/5] Pulling latest changes from remote...
git pull origin
if errorlevel 1 (
    echo ERROR: Pull failed. Please resolve conflicts first.
    pause
    exit /b 1
)
echo.

echo [3/5] Staging all changes...
git add -A
echo.

echo [4/5] Committing changes...
set /p msg="Enter commit message: "
if "%msg%"=="" set msg=update

git commit -m "%msg%"
if errorlevel 1 (
    echo INFO: Nothing to commit. Working tree is clean.
    echo.
    echo Sync completed - already up to date.
    pause
    exit /b 0
)
echo.

echo [5/5] Pushing to origin...
git push -u origin
if errorlevel 1 (
    echo ERROR: Push failed.
    pause
    exit /b 1
)
echo.

echo ========================================
echo   Sync completed successfully!
echo ========================================
pause
