@echo off
rem MoguMogu frontend launcher (development)
set "ROOT=%~dp0..\frontend"
cd /d "%ROOT%"
if not exist "node_modules" (
  echo [ERROR] node_modules not found. Run: npm install
  exit /b 1
)
call npm run dev >> "frontend-runtime.log" 2>&1