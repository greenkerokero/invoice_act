@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Repository clone script
echo ========================================

if exist ".git" (
    echo Repository already initialized
    goto :pull
)

git init
if errorlevel 1 (
    echo Error: failed to initialize git
    pause
    exit /b 1
)

git remote add origin https://github.com/greenkerokero/invoice_act.git
if errorlevel 1 (
    echo Error: failed to add remote origin
    echo Possibly remote already exists
    pause
    exit /b 1
)

git fetch origin
if errorlevel 1 (
    echo Error: failed to fetch from remote
    pause
    exit /b 1
)

git checkout -b main origin/main
if errorlevel 1 (
    echo Error: failed to checkout main branch
    pause
    exit /b 1
)

echo.
echo Repository successfully cloned
echo.
echo Use: git pull to update
pause
exit /b 0

:pull
echo.
echo Repository already configured
echo Running git pull...
echo.

git pull origin main
if errorlevel 1 (
    echo Error: failed to pull updates
    pause
    exit /b 1
)

echo.
echo ========================================
echo Restarting application
echo ========================================
echo.

echo Stopping uvicorn process...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)
timeout /t 2 /nobreak >nul

echo Starting application...
start "PIPISKA" cmd /c ".venv\Scripts\uvicorn.exe src.main:app --host 127.0.0.1 --port 8000"

echo.
echo Update completed and application restarted
echo ========================================
pause
exit /b 0
