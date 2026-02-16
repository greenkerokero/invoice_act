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
echo Update completed
pause
exit /b 0
