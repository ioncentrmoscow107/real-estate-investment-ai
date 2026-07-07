$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PythonPath = Join-Path $RepoRoot ".venv\Scripts\python.exe"

Set-Location $RepoRoot

Write-Host "Запускаю backend..." -ForegroundColor Cyan
Write-Host "URL API: http://127.0.0.1:8000/api/v1/dashboard/properties" -ForegroundColor Green
Write-Host "Оставьте это окно открытым, пока backend нужен для работы." -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path -LiteralPath $PythonPath)) {
    Write-Host "Не найден Python виртуального окружения: $PythonPath" -ForegroundColor Red
    Write-Host "Создайте окружение командой: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

& $PythonPath -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
