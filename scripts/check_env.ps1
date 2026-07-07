$ErrorActionPreference = "Continue"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PythonPath = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$NodeModulesPath = Join-Path $RepoRoot "frontend\node_modules"

Set-Location $RepoRoot

function Write-Check {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$Details = "",
        [string]$Fix = ""
    )

    if ($Ok) {
        Write-Host "[OK] $Name $Details" -ForegroundColor Green
    } else {
        Write-Host "[MISSING] $Name $Details" -ForegroundColor Yellow
        if ($Fix) {
            Write-Host "  Fix: $Fix" -ForegroundColor DarkYellow
        }
    }
}

Write-Host "Local environment check" -ForegroundColor Cyan
Write-Host ""

if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonVersion = & python --version 2>$null
    Write-Check "Python" ($LASTEXITCODE -eq 0) $PythonVersion "Install Python and make sure it is available in PATH."
} else {
    Write-Check "Python" $false "" "Install Python and make sure it is available in PATH."
}

$VenvExists = Test-Path -LiteralPath $PythonPath
Write-Check "venv Python" $VenvExists $PythonPath "Run: python -m venv .venv"

if ($VenvExists) {
    & $PythonPath -c "import uvicorn" 2>$null
    Write-Check "uvicorn in .venv" ($LASTEXITCODE -eq 0) "" "Run: .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
} else {
    Write-Check "uvicorn in .venv" $false "" "Create .venv first, then install requirements.txt."
}

if (Get-Command node -ErrorAction SilentlyContinue) {
    $NodeVersion = & node -v 2>$null
    Write-Check "Node.js" ($LASTEXITCODE -eq 0) $NodeVersion "Install Node.js and make sure node is available in PATH."
} else {
    Write-Check "Node.js" $false "" "Install Node.js and make sure node is available in PATH."
}

if (Get-Command npm.cmd -ErrorAction SilentlyContinue) {
    $NpmVersion = & npm.cmd -v 2>$null
    Write-Check "npm.cmd" ($LASTEXITCODE -eq 0) $NpmVersion "Install Node.js/npm or use npm.cmd from PowerShell."
} else {
    Write-Check "npm.cmd" $false "" "Install Node.js/npm or use npm.cmd from PowerShell."
}

$NodeModulesExists = Test-Path -LiteralPath $NodeModulesPath
Write-Check "frontend/node_modules" $NodeModulesExists $NodeModulesPath "Run: cd frontend; npm.cmd install"

Write-Host ""
foreach ($Port in @(8000, 3000)) {
    $Connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($Connection) {
        Write-Host "[BUSY] Port $Port is already in use." -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Port $Port is free." -ForegroundColor Green
    }
}
