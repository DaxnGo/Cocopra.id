@echo off
echo Starting Cocopra.id Application...

:: Start Backend in a new window
start "Backend Server" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Start Frontend (PROXO) in a new window
start "Frontend Server" cmd /k "cd PROXO && npm run dev"

echo Both servers are starting in new windows.
