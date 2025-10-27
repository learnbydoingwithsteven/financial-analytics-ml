@echo off
echo ====================================
echo Financial Analytics Dashboard
echo ====================================
echo.

echo Starting Backend Server...
start "Backend" cmd /k "cd backend && python main.py"

timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo Dashboard is starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo ====================================
echo.
echo Press any key to open the dashboard in your browser...
pause >nul

start http://localhost:5173
