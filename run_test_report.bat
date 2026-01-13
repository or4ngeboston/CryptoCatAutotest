@echo off
set TEST_FILE=%1

if "%TEST_FILE%"=="" (
    echo No test file specified. Running ALL tests...
    pytest --alluredir=./allure-results
) else if /I "%TEST_FILE%"=="smoke" (
    echo Running SMOKE tests...
    pytest tests/test_smoke.py --alluredir=./allure-results
) else (
    echo Running tests in %TEST_FILE%...
    pytest %TEST_FILE% --alluredir=./allure-results
)

if %ERRORLEVEL% NEQ 0 (
    echo Tests failed or encountered errors. Proceeding to generate report anyway...
)

echo Generating Allure Report...
echo Generating Allure Report...
call npx -y allure-commandline generate ./allure-results -o ./allure-report --clean
if %ERRORLEVEL% NEQ 0 (
    echo Allure generation failed!
    exit /b 1
)

echo Combining to Single File...
call allure-combine ./allure-report
if %ERRORLEVEL% NEQ 0 (
    echo Allure combine failed!
    exit /b 1
)

echo.
echo Report generated at: %CD%\allure-report\complete.html
start allure-report\complete.html
