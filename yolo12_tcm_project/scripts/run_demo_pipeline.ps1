$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

$pythonExe = Join-Path ".venv" "Scripts\python.exe"
if (Test-Path $pythonExe) {
  $py = $pythonExe
} elseif (Test-Path "C:\Users\ROG\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe") {
  $py = "C:\Users\ROG\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  $py = "py"
} else {
  $py = "python"
}

if ($py -eq "py") {
  & py -3 scripts\create_demo_dataset.py --output data/demo_yolo --overwrite
  & py -3 scripts\validate_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt --output reports/demo_dataset_validation.json --markdown reports/demo_dataset_validation.md
  & py -3 scripts\split_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt --output data/demo_splits --overwrite
} else {
  & $py scripts\create_demo_dataset.py --output data/demo_yolo --overwrite
  & $py scripts\validate_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt --output reports/demo_dataset_validation.json --markdown reports/demo_dataset_validation.md
  & $py scripts\split_yolo_dataset.py --images data/demo_yolo/images --labels data/demo_yolo/labels --classes data/demo_yolo/classes.txt --output data/demo_splits --overwrite
}

Write-Host "Demo pipeline completed. This dataset is synthetic and only validates the engineering flow."
