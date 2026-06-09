param(
  [int]$Port = 5173
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Join-Path (Split-Path -Parent $PSScriptRoot) "frontend")

if (-not (Test-Path "node_modules")) {
  npm install
}

npm run dev -- --host 0.0.0.0 --port $Port

