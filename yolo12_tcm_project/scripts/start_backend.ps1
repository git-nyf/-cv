param(
  [string]$HostAddress = "127.0.0.1",
  [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

$pythonExe = Join-Path ".venv" "Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
  throw "Virtual environment not found. Run .\scripts\setup_env.ps1 first."
}

& $pythonExe -m uvicorn backend.app.main:app --host $HostAddress --port $Port --reload

