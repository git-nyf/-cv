$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

$bundledPython = "C:\Users\ROG\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path $bundledPython) {
  $py = $bundledPython
} elseif (Test-Path ".venv\Scripts\python.exe") {
  $py = ".venv\Scripts\python.exe"
} else {
  $py = "python"
}

& $py -m compileall scripts backend tests -q
npm run build --prefix frontend
& $py scripts\smoke_check.py

Write-Host "Static checks completed. See reports/smoke_check.md."

