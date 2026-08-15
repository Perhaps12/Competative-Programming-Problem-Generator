@echo off
echo ==========================================
echo Starting Leetcode Clone dev environment
echo ==========================================

echo.
echo [1/3] Starting Docker containers (Postgres + Piston)...
docker compose up -d

echo.
echo [2/3] Starting backend in a new window...
start "Backend" cmd /k "cd backend && ..\venv\Scripts\activate && python main.py"

echo.
echo [3/3] Starting frontend in a new window...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================
echo All services starting. Two new windows
echo have opened for the backend and frontend.
echo Docker is running in the background.
echo ==========================================