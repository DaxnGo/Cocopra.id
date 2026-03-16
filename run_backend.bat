@echo off
cd backend
echo Starting Cocopra.id Backend...
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
