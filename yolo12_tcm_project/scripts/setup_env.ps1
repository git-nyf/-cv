param(
  [string]$Python = "",
  [string]$Venv = ".venv"
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

function Invoke-ProjectPython {
  param([string[]]$Arguments)
  if ($Python) {
    & $Python @Arguments
    return
  }
  $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
  if ($pyLauncher) {
    & py -3 @Arguments
    return
  }
  & python @Arguments
}

Write-Host "Creating virtual environment: $Venv"
Invoke-ProjectPython -Arguments @("-m", "venv", $Venv)

$pip = Join-Path $Venv "Scripts\pip.exe"
$pythonExe = Join-Path $Venv "Scripts\python.exe"

& $pythonExe -m pip install --upgrade pip
& $pip install -r requirements.txt

Write-Host "Environment ready."
Write-Host "Activate with: .\$Venv\Scripts\Activate.ps1"
