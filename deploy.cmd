@echo off
REM Cryptex Echo Bot Deployment Script for Windows
setlocal enabledelayedexpansion

echo [INFO] Starting Cryptex Echo Bot deployment...

REM Check Docker installation
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is required but not installed.
    exit /b 1
)

REM Check Docker Compose
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is required but not installed.
    exit /b 1
)

REM Setup environment
if not exist .env (
    copy .env.example .env
    echo [INFO] Created .env file from template. Please edit with your settings.
    echo [INFO] After editing .env, run this script again.
    exit /b 1
)

REM Create directories
if not exist logs\pearl mkdir logs\pearl
if not exist logs\royalty mkdir logs\royalty

REM Deploy application
echo [INFO] Deploying Cryptex Echo Bot...
docker compose pull
docker compose up -d --build

if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed. Check logs with: docker compose logs
    exit /b 1
)

REM Monitor deployment
echo [INFO] Monitoring deployment...
timeout /t 10 /nobreak >nul

REM Check service health
docker compose ps >temp.txt
findstr /i "healthy" temp.txt >nul
if %errorlevel% equ 0 (
    echo [SUCCESS] All services are healthy.
) else (
    echo [ERROR] Some services are not healthy. Check logs with: docker compose logs
    del temp.txt
    exit /b 1
)
del temp.txt

echo [SUCCESS] Deployment complete!
echo.
echo Important next steps:
echo 1. Configure your trading parameters in the dashboard
echo 2. Set up monitoring alerts
echo 3. Test with paper trading first
echo 4. Monitor the logs regularly
echo.
echo Dashboard: http://localhost:3000
echo API: http://localhost:5050
echo.
echo Thank you for choosing Cryptex Echo Bot!

endlocal