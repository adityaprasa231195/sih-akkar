Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting AAKAR Cadastral Platform Services..." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$backendPath = Join-Path $PSScriptRoot "AAKAR\backend"
$frontendPath = Join-Path $PSScriptRoot "AAKAR\frontend"

Write-Host "[1/2] Launching FastAPI Backend on port 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$backendPath'; python -m uvicorn app.main:app --port 8000 --reload"

Write-Host "[2/2] Launching React Vite Frontend on port 3000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; npm run dev"

Write-Host "`nServices launched successfully!" -ForegroundColor Green
Write-Host "- Web-GIS Application:   http://localhost:3000/" -ForegroundColor White
Write-Host "- Citizen Parcel Lookup: http://localhost:3000/lookup" -ForegroundColor White
Write-Host "- FastAPI API Docs:      http://localhost:8000/docs" -ForegroundColor White
