@echo off
set TEST_FILE=%1

if "%TEST_FILE%"=="" (
    echo Usage: run_test_report.bat [path_to_test_file]
    exit /b 1
)

echo Running tests in %TEST_FILE%...
pytest %TEST_FILE% --alluredir=./allure-results

if %ERRORLEVEL% NEQ 0 (
    echo Tests failed or encountered errors. Proceeding to generate report anyway...
)

echo Generating Allure Report...
call allure generate --single-file path/to/allure-results

echo Combining to Single File...
call allure-combine ./allure-report

echo.
echo Report generated at: %CD%\allure-report\complete.html
start allure-report\complete.html
