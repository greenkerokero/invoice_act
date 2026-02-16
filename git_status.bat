@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Git Status
echo ========================================
echo.

echo --- Branch ---
git branch --show-current
echo.

echo --- Status ---
git status
echo.

echo --- Recent commits (last 5) ---
git log --oneline -5
echo.

echo --- Remote ---
git remote -v
echo.

echo --- Branches ---
git branch -a
echo.

echo ========================================
echo Done
echo ========================================

pause
