$ErrorActionPreference = "Continue"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PythonPath = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$NodeModulesPath = Join-Path $RepoRoot "frontend\node_modules"

Set-Location $RepoRoot

Write-Host "Проверка локального окружения" -ForegroundColor Cyan
Write-Host ""

Write-Host "Python:"
python --version

Write-Host ""
Write-Host "Node.js:"
node --version

Write-Host ""
Write-Host "npm.cmd:"
npm.cmd --version

Write-Host ""
Write-Host ".venv Python найден: $(Test-Path -LiteralPath $PythonPath)"
Write-Host "frontend/node_modules найден: $(Test-Path -LiteralPath $NodeModulesPath)"

Write-Host ""
foreach ($Port in @(8000, 3000)) {
    $Connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($Connection) {
        Write-Host "Порт $Port занят. Закройте старый процесс или выберите другой порт." -ForegroundColor Yellow
    } else {
        Write-Host "Порт $Port свободен." -ForegroundColor Green
    }
}
