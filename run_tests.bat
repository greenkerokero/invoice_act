@echo off
echo ===================================================
echo RUNNING UNIT AND INTEGRATION TESTS WITH COVERAGE...
echo ===================================================
call uv run pytest tests/ --cov=src --cov-report=html --cov-report=term --html=test_results.html --self-contained-html
echo.
echo ===================================================
echo DONE.
echo 1. Test Results: Open 'test_results.html'
echo 2. Code Coverage: Open 'htmlcov/index.html'
echo ===================================================
pause
