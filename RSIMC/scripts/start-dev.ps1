# DARSI-CS Development Startup (Windows)
# Usage: .\scripts\start-dev.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "=== DARSI-CS Development ===" -ForegroundColor Cyan
Write-Host ""

# Prefer Docker Compose when Docker Desktop is running
try {
    docker info *> $null
    Write-Host "Docker detected. Starting all services..." -ForegroundColor Green
    Set-Location $Root
    docker compose up -d --build
    Write-Host ""
    Write-Host "Services:" -ForegroundColor Yellow
    Write-Host "  Kiosk UI:         http://localhost:3000"
    Write-Host "  Admin Dashboard:  http://localhost:3001"
    Write-Host "  API + Swagger:    http://localhost:8000/docs"
    Write-Host ""
    Write-Host "Demo NIK: 3573010101010001 (Budi Santoso)"
    exit 0
} catch {
    Write-Host "Docker is not running. Use manual mode below." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Manual mode (3 terminals required):" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. PostgreSQL + Redis must be running (or start Docker Desktop and re-run this script)"
Write-Host "2. Backend:  cd backend; pip install -r requirements.txt; python main.py"
Write-Host "3. Kiosk:    cd kiosk-ui; npm install; npm run dev"
Write-Host "4. Admin:    cd admin-dashboard; npm install; npm run dev -p 3001"
Write-Host ""
Write-Host "Copy .env.example to .env and adjust DATABASE_URL if needed."
