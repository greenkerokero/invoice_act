@echo off
echo ===================================================
echo ЗАПУСК UNIT И INTEGRATION ТЕСТОВ С ПОКРЫТИЕМ...
echo ===================================================
call uv run pytest tests/ --cov=src --cov-report=html --cov-report=term --html=test_results.html --self-contained-html
echo.
echo ===================================================
echo ГОТОВ.
echo 1. Результаты тестов: Откройте 'test_results.html'
echo 2. Покрытие кода: Откройте 'htmlcov/index.html'
echo ===================================================
pause
