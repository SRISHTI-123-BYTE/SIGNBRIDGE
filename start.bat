@echo off
setlocal
echo =========================================================================
echo  SignBridge: Continuous ISL Recognition & Bi-Directional Speech Translation
echo =========================================================================
echo.
echo Select Execution Mode:
echo   [1] Unified Production Server (Recommended - Port 8000, 1 window)
echo   [2] Dual Development Servers (Vite Port 5173 + FastAPI Port 8000)
echo   [3] Docker Container Deployment (Requires Docker Desktop)
echo.
set /p MODE="Enter choice [1, 2, or 3] (default is 1): "

if "%MODE%"=="2" goto DEV_MODE
if "%MODE%"=="3" goto DOCKER_MODE

:PROD_MODE
echo.
echo Launching Unified Production Server on http://localhost:8000 ...
call start_production.bat
goto END

:DEV_MODE
echo.
echo Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "SignBridge Backend (Dev)" cmd /c "cd backend && python main.py"
timeout /t 3 /nobreak > nul

echo Launching Vite React Frontend on http://localhost:5173 ...
start "SignBridge Frontend (Dev)" cmd /c "cd frontend && npm run dev"

echo.
echo SignBridge Development Servers are running!
echo Open your browser at: http://localhost:5173
goto END

:DOCKER_MODE
call docker_start.bat
goto END

:END
pause
