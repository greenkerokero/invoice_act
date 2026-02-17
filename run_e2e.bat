@echo off
echo ===================================================
echo RUNNING E2E TESTS WITH REPORT...
echo ===================================================

echo Creating reports directory...
if not exist "e2e_reports" mkdir e2e_reports

echo Starting backend on port 10000...
start /B uv run uvicorn src.main:app --host 127.0.0.1 --port 10000 > server.log 2>&1
echo Waiting for server to start...
timeout /t 5

echo Running E2E tests with report...
uv run pytest e2e/ --html=e2e_reports/e2e_report.html --self-contained-html --tb=short --log-cli-level=INFO -s

echo Stopping server...
taskkill /IM uvicorn.exe /F 2>nul

echo.
echo ===================================================
echo DONE.
echo Report saved to: e2e_reports/e2e_report.html
echo ===================================================
pause
