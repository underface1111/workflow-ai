# Local test script — run in PowerShell from repo root: .\scripts\test-local.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "=== 1. Unit tests (Jest) ===" -ForegroundColor Cyan
npm test
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python not found in PATH. Install Python 3.12+ and tick 'Add to PATH', then open a NEW terminal." -ForegroundColor Red
    exit 1
}

Write-Host "`n=== 2. Robot dependencies ===" -ForegroundColor Cyan
python -m pip install -r tests/e2e-robot/requirements.txt -q

Write-Host "`n=== 3. Start API (background) ===" -ForegroundColor Cyan
$job = Start-Job -ScriptBlock { Set-Location $using:Root; node src/server.js }
Start-Sleep -Seconds 2

try {
    $ready = $false
    for ($i = 1; $i -le 15; $i++) {
        try {
            Invoke-RestMethod -Uri "http://localhost:3000/health" -TimeoutSec 2 | Out-Null
            $ready = $true
            break
        } catch {
            Start-Sleep -Seconds 1
        }
    }
    if (-not $ready) { throw "API did not start on :3000" }

    Write-Host "`n=== 4. Robot E2E (@critical) ===" -ForegroundColor Cyan
    robot --outputdir robot-results --include critical tests/e2e-robot/suites/critical
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "`nAll local tests passed." -ForegroundColor Green
} finally {
    Stop-Job $job -ErrorAction SilentlyContinue
    Remove-Job $job -Force -ErrorAction SilentlyContinue
    Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*workflow-ai*" } | Stop-Process -Force -ErrorAction SilentlyContinue
}
