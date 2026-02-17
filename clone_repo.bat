@echo off
setlocal enabledelayedexpansion

:: --- НАСТРОЙКИ ---
set REPO_URL=https://github.com/greenkerokero/invoice_act.git
set BRANCH=main

echo ========================================================
echo   SMART UPDATE: Safe Mode + Auto Restart
echo   (Auto-fix uv.lock, preserve changes, restart app)
echo ========================================================
echo.

:: 1. ПРОВЕРКА GIT
where git >nul 2>nul
if %errorlevel% neq 0 goto :error_no_git

:: 2. ТОЧЕЧНЫЙ СБРОС UV.LOCK
:: Проверяем, есть ли изменения конкретно в uv.lock
git diff --name-only | findstr "uv.lock" >nul
if errorlevel 1 goto :check_stash
:: Если errorlevel 0, значит uv.lock найден в списке измененных
echo [INFO] Detected local changes in uv.lock.
echo        Discarding them to allow update...
git checkout -- uv.lock

:check_stash
:: 3. ОБРАБОТКА ОСТАЛЬНЫХ ИЗМЕНЕНИЙ (STASH)
set "STASH_NEEDED=0"
git diff --quiet HEAD
:: Если diff нашел изменения (код возврата 1), идем к созданию стэша
if errorlevel 1 goto :do_stash
goto :do_pull

:do_stash
echo [INFO] Other local changes detected (configs/code).
echo        Stashing them safely...
git stash push -m "Auto-save before smart update"
set STASH_NEEDED=1

:do_pull
:: 4. ОБНОВЛЕНИЕ С СЕРВЕРА
echo [INFO] Pulling from GitHub...
git pull origin %BRANCH%
if errorlevel 1 goto :error_pull

:: 5. ВОЗВРАТ ИЗМЕНЕНИЙ (Если прятали)
if "%STASH_NEEDED%"=="0" goto :sync_deps

echo [INFO] Restoring your custom changes...
git stash pop
if errorlevel 1 goto :warn_conflict

:sync_deps
:: 6. СИНХРОНИЗАЦИЯ ЗАВИСИМОСТЕЙ
echo.
echo [INFO] Updating dependencies with uv sync...
where uv >nul 2>nul
if errorlevel 1 goto :warn_no_uv

uv sync
if errorlevel 1 goto :warn_uv_fail

:: Все прошло успешно, переходим к перезапуску
goto :restart_app

:: --- БЛОК ПЕРЕЗАПУСКА ПРИЛОЖЕНИЯ ---
:restart_app
echo.
echo ========================================
echo Restarting application
echo ========================================
echo.

echo Stopping uvicorn process...
:: Ищем процесс на порту 8000 и убиваем его
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
)
:: Небольшая пауза, чтобы порт успел освободиться
timeout /t 2 /nobreak >nul

echo Starting application...
start "PIPISKA" cmd /c ".venv\Scripts\uvicorn.exe src.main:app --host 127.0.0.1 --port 8000"

echo.
echo Update completed and application restarted
echo ========================================
pause
exit /b 0

:: --- БЛОКИ ОБРАБОТКИ ОШИБОК ---

:error_no_git
echo.
echo [ERROR] Git not found.
pause
exit /b 1

:error_pull
echo.
echo [ERROR] Git pull failed.
if "%STASH_NEEDED%"=="1" (
    echo [INFO] Attempting to restore your files...
    git stash pop
)
pause
exit /b 1

:warn_conflict
echo.
echo [WARN] Merge conflict detected in your custom files.
echo        Please check them manually in your editor.
:: Даже если есть конфликт, пробуем перезапустить, вдруг заработает
goto :restart_app

:warn_no_uv
echo [WARN] 'uv' tool not found. Skipping dependency sync.
goto :restart_app

:warn_uv_fail
echo [WARN] 'uv sync' failed. Check your uv.lock or network.
goto :restart_app