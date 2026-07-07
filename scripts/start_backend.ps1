$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PythonPath = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$RequirementsPath = Join-Path $RepoRoot "requirements.txt"

Set-Location $RepoRoot

Write-Host "Starting backend..." -ForegroundColor Cyan
Write-Host "API URL: http://127.0.0.1:8000/api/v1/dashboard/properties" -ForegroundColor Green
Write-Host "Keep this window open while the backend is running." -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path -LiteralPath $PythonPath)) {
    Write-Host "Virtual environment Python was not found: $PythonPath" -ForegroundColor Yellow
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "Python was not found in PATH. Install Python, then run this script again." -ForegroundColor Red
        exit 1
    }
    Write-Host "Creating virtual environment with: python -m venv .venv" -ForegroundColor Cyan
    python -m venv .venv
}

if (-not (Test-Path -LiteralPath $PythonPath)) {
    Write-Host "Could not create or find venv Python: $PythonPath" -ForegroundColor Red
    exit 1
}

& $PythonPath -c "import uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Backend dependencies are missing in .venv. Installing requirements..." -ForegroundColor Yellow
    & $PythonPath -m pip install --upgrade pip
    & $PythonPath -m pip install -r $RequirementsPath
}

Write-Host ""
Write-Host "Launching uvicorn..." -ForegroundColor Cyan
& $PythonPath -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
