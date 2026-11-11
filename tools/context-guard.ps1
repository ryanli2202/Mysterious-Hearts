# Run the installed Context Guard diagnostic CLI. This does not trust hooks.
$ErrorActionPreference = 'Stop'
$pluginLock = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'community_plugins.lock.json') -Raw | ConvertFrom-Json
$guardPlugin = $pluginLock.plugins | Where-Object { $_.name -eq 'context-guard' }
$guardEntry = Join-Path $guardPlugin.installed_path 'scripts/run-context-guard.ps1'
if (-not (Test-Path -LiteralPath $guardEntry -PathType Leaf)) {
    throw 'Context Guard is missing. See tools/COMMUNITY_PLUGINS.md to restore the pinned installation.'
}
& $guardEntry @args
exit $LASTEXITCODE
