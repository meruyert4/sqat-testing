@echo off
REM Aviasales Test Automation - Quick Start Script for Windows
REM This script helps you set up and run the tests quickly

echo ======================================
echo Aviasales Automation - Quick Start
echo ======================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Step 1: Cleaning previous builds...
call mvn clean

echo.
echo Step 2: Installing dependencies...
call mvn install -DskipTests

echo.
echo Step 3: Running tests...
call mvn test

echo.
echo ======================================
echo Test Execution Complete!
echo ======================================
echo.
echo View Reports:
echo    - Extent Report: test-output\ExtentReport.html
echo    - Logs: test-output\logs\automation.log
echo    - Screenshots: test-output\screenshots\
echo.
echo Open Extent Report:
echo    start test-output\ExtentReport.html
echo.

pause
