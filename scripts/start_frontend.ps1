$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$FrontendRoot = Join-Path $RepoRoot "frontend"

Set-Location $FrontendRoot

Write-Host "Запускаю frontend..." -ForegroundColor Cyan
Write-Host "URL: http://localhost:3000" -ForegroundColor Green
Write-Host "Оставьте это окно открытым, пока frontend нужен для работы." -ForegroundColor Yellow
Write-Host ""

& npm.cmd run dev
