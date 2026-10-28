@echo off
echo =========================================================================
echo  SignBridge: Docker Container Deployment (Port 8000)
echo =========================================================================
echo.

docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not in PATH.
    echo Please install Docker Desktop or run start_production.bat instead.
    pause
    exit /b 1
)

echo [SignBridge] Building and starting SignBridge container via Docker Compose...
docker compose up --build -d

echo.
echo [SignBridge] Container running at http://localhost:8000
echo [SignBridge] Checking container status...
docker ps --filter "name=signbridge_app"

echo.
echo Opening browser at http://localhost:8000 ...
timeout /t 3 /nobreak > nul
start http://localhost:8000
pause
