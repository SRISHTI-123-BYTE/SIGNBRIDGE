@echo off
echo =========================================================================
echo  SignBridge: Unified Production Server (Port 8000)
echo  FastAPI + ST-GCN ONNX + WebSocket + Built React SPA
echo =========================================================================
echo.

REM Verify frontend distribution exists
if not exist "frontend\dist\index.html" (
    echo [SignBridge] Frontend build not detected. Building frontend assets now...
    cd frontend
    call npm run build
    cd ..
)

echo [SignBridge] Starting Unified FastAPI & Static Asset Server on http://localhost:8000 ...
echo [SignBridge] Press Ctrl+C in this terminal to stop the server.
echo.

REM Open browser after 2 seconds
start "" cmd /c "timeout /t 2 /nobreak > nul && start http://localhost:8000"

cd backend
python main.py
pause
