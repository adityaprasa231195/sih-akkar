@echo off
setlocal
title AAKAR Cadastral Platform Launcher
echo ========================================================
echo Starting AAKAR Cadastral Platform Services...
echo ========================================================

:: Launch Backend
echo [1/2] Launching FastAPI Backend on port 8000...
start "AAKAR FastAPI Backend" /D "%~dp0AAKAR\backend" cmd /k python -m uvicorn app.main:app --port 8000 --reload

:: Launch Frontend
echo [2/2] Launching React Vite Frontend on port 3000...
start "AAKAR React Frontend" /D "%~dp0AAKAR\frontend" cmd /k npm run dev

echo.
echo ========================================================
echo Services launched successfully in separate windows!
echo - Web-GIS Application:    http://localhost:3000/
echo - Citizen Parcel Lookup:  http://localhost:3000/lookup
echo - FastAPI API Docs:       http://localhost:8000/docs
echo ========================================================
echo.
pause
