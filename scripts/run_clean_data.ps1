$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$anacondaPython = Join-Path $env:USERPROFILE "anaconda3\python.exe"

if (-not (Test-Path $anacondaPython)) {
    throw "Anaconda Python was not found at $anacondaPython"
}

Push-Location $repoRoot
try {
    & $anacondaPython -m src.clean_data
}
finally {
    Pop-Location
}
