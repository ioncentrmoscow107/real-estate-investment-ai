$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$FrontendRoot = Join-Path $RepoRoot "frontend"
$NodeModulesPath = Join-Path $FrontendRoot "node_modules"

if (-not (Test-Path -LiteralPath $FrontendRoot)) {
    Write-Host "Frontend folder was not found: $FrontendRoot" -ForegroundColor Red
    exit 1
}

Set-Location $FrontendRoot

Write-Host "Starting frontend..." -ForegroundColor Cyan
Write-Host "URL: http://localhost:3000" -ForegroundColor Green
Write-Host "Keep this window open while the frontend is running." -ForegroundColor Yellow
Write-Host ""

Write-Host "Checking Node.js..." -ForegroundColor Cyan
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js was not found in PATH. Install Node.js, then run this script again." -ForegroundColor Red
    exit 1
}
node -v

Write-Host "Checking npm.cmd..." -ForegroundColor Cyan
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    Write-Host "npm.cmd was not found in PATH. Install Node.js/npm, then run this script again." -ForegroundColor Red
    exit 1
}
npm.cmd -v

if (-not (Test-Path -LiteralPath $NodeModulesPath)) {
    Write-Host "frontend/node_modules was not found. Installing frontend dependencies..." -ForegroundColor Yellow
    npm.cmd install
}

Write-Host ""
Write-Host "Launching Next.js dev server..." -ForegroundColor Cyan
npm.cmd run dev
