$ErrorActionPreference = 'Stop'
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\pythonw.exe'
if (Test-Path -LiteralPath $bundledPython) {
    $gamePython = $bundledPython
} else {
    $gamePython = (Get-Command pythonw.exe -ErrorAction Stop).Source
}
Start-Process -FilePath $gamePython -ArgumentList ('"' + (Join-Path $PSScriptRoot 'game.py') + '"') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden
