# Run the installed, pinned Story Skills CLI without adding game dependencies.
$ErrorActionPreference = 'Stop'
$pluginLock = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'community_plugins.lock.json') -Raw | ConvertFrom-Json
$storyPlugin = $pluginLock.plugins | Where-Object { $_.name -eq 'story-skills' }
$storyEntry = Join-Path $storyPlugin.installed_path 'skills/story-maintenance/scripts/story.js'
if (-not (Test-Path -LiteralPath $storyEntry -PathType Leaf)) {
    throw 'Story Skills is missing. See tools/COMMUNITY_PLUGINS.md to restore the pinned installation.'
}
& node $storyEntry @args
exit $LASTEXITCODE
