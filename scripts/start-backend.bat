@echo off
rem MoguMogu backend launcher (development)
set "ROOT=%~dp0..\backend"
cd /d "%ROOT%"
if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] .venv not found. Run: npm run setup:backend
  exit /b 1
)
".venv\Scripts\python.exe" -X utf8 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 >> "backend-runtime.log" 2>&1