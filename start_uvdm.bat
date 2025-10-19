@echo off
REM Startup script for UVDM with API server (Windows)

echo ========================================
echo   UVDM Startup Script
echo ========================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Load configuration if exists
if exist "api_config.env" (
    echo Loading API configuration...
    for /f "delims== tokens=1,2" %%a in (api_config.env) do (
        if not "%%a"=="" if not "%%a:~0,1%"=="#" set %%a=%%b
    )
)

REM Check if we should start the API server
if "%1"=="--with-api-server" goto START_API
if "%1"=="-a" goto START_API
goto START_APP

:START_API
echo Starting API server in background...
start /b python api_server.py > api_server.log 2>&1
echo API server started
timeout /t 2 /nobreak > nul

REM Check if server is running
curl -s http://localhost:%UVDM_API_PORT%/ > nul 2>&1
if %errorlevel%==0 (
    echo API server is running at http://localhost:%UVDM_API_PORT%
) else (
    echo Warning: API server may not be running correctly
)
echo.

:START_APP
REM Start the main application
echo Starting UVDM application...
python main.py

REM Cleanup
echo.
echo ========================================
echo   UVDM Shutdown Complete
echo ========================================

exit /b
