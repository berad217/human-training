<#
.SYNOPSIS
    Diagnose why this machine is running a stale version of the plugin.

.DESCRIPTION
    Claude Code serves plugins through a chain of local caches, and no layer in
    that chain can tell you it is stale. `claude plugin update` asks the local
    marketplace catalog, not GitHub; if the catalog has never refreshed, it
    answers "you are current" perfectly honestly, and the machine sits many
    versions behind indefinitely.

    This script asks the questions the plugin system does not ask itself:

      1. Is the plugin actually being LOADED?   (PID claims under .in_use)
      2. Is the installed version behind the catalog?
      3. Is the catalog itself behind GitHub?   (the failure that hides the rest)

    Question 3 is the important one. It runs `git ls-remote` against the real
    remote rather than trusting the clone's own remote-tracking ref, because a
    clone that has never fetched reports itself in sync with total confidence.

    A missing .git/FETCH_HEAD is the smoking gun: git writes that file on every
    fetch, so its absence proves the catalog has not refreshed since it was
    cloned.

    Read-only. Installs nothing, fetches nothing, writes nothing.

    Note this covers the terminal CLI only (~/.claude/plugins/). The Claude
    Desktop app unpacks its own bundle per session and is not visible here; it
    updates only on a full quit and relaunch.

.PARAMETER Plugin
    Plugin/marketplace name to report drift for. Defaults to human-training.

.EXAMPLE
    ./scripts/check-plugin-state.ps1

.EXAMPLE
    ./scripts/check-plugin-state.ps1 -Plugin some-other-plugin
#>

param(
    [string]$Plugin = 'human-training'
)

$PluginsDir = Join-Path $env:USERPROFILE ".claude\plugins"

Write-Host "Claude Code Plugin State" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

if (-not (Test-Path $PluginsDir)) {
    Write-Host ""
    Write-Host "No CLI plugin store at $PluginsDir." -ForegroundColor Yellow
    Write-Host "Either the terminal CLI is not installed, or no plugins have been added." -ForegroundColor Gray
    return
}

# --- 1. Installed versions, and whether anything is actually claiming them ---
# Each version dir holds .in_use/<pid> lockfiles written by live processes.
# That is what makes updating safe while a session runs, and why applying an
# update needs a restart: the running process still holds the old directory.

Write-Host ""
Write-Host "Installed versions and live claims" -ForegroundColor Cyan

$rows = Get-ChildItem (Join-Path $PluginsDir 'cache') -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $marketplace = $_.Name
    Get-ChildItem $_.FullName -Directory | ForEach-Object {
        $name = $_.Name
        Get-ChildItem $_.FullName -Directory | ForEach-Object {
            # Skip *.tmp.* — partial writes, not real claims.
            $marks = @(Get-ChildItem (Join-Path $_.FullName '.in_use') -Force -ErrorAction SilentlyContinue |
                       Where-Object { $_.Name -notlike '*.tmp.*' })
            [pscustomobject]@{
                Plugin    = "$name@$marketplace"
                Version   = $_.Name
                Claims    = $marks.Count
                LastClaim = if ($marks) { ($marks | Sort-Object LastWriteTime -Descending)[0].LastWriteTime } else { $null }
            }
        }
    }
}

if ($rows) {
    $rows | Sort-Object Plugin | Format-Table -AutoSize
} else {
    Write-Host "  (no plugins installed)" -ForegroundColor Gray
}

# --- 2 & 3. Drift: installed vs catalog vs GitHub ---------------------------

Write-Host "Version drift for '$Plugin'" -ForegroundColor Cyan

$installed = $null
$installedKey = $null
$installedFile = Join-Path $PluginsDir 'installed_plugins.json'
if (Test-Path $installedFile) {
    $all = (Get-Content $installedFile -Raw | ConvertFrom-Json).plugins
    # Match either a plugin named $Plugin, or any plugin from marketplace
    # $Plugin — the two share a name in this repo but need not in general.
    $installedKey = $all.PSObject.Properties.Name |
        Where-Object { $_ -like "$Plugin@*" -or $_ -like "*@$Plugin" } |
        Select-Object -First 1
    if ($installedKey) { $installed = $all.$installedKey[0].version }
}

# autoUpdate is a PER-MARKETPLACE opt-in, not a global setting, and it is not
# set for you when a marketplace is added. When it is off, nothing ever
# refreshes the catalog — this is the root cause of nearly every stale machine.
$autoUpdate = $null
$knownFile = Join-Path $PluginsDir 'known_marketplaces.json'
if (Test-Path $knownFile) {
    $known = Get-Content $knownFile -Raw | ConvertFrom-Json
    if ($known.PSObject.Properties.Name -contains $Plugin) {
        $entry = $known.$Plugin
        $autoUpdate = if ($entry.PSObject.Properties.Name -contains 'autoUpdate') {
            [bool]$entry.autoUpdate
        } else {
            $false   # absent means off
        }
    }
}

$clone = Join-Path $PluginsDir "marketplaces\$Plugin"
$catalog = $catalogVersion = $localHead = $remoteHead = $fetched = $null
$isGit = $false

if (Test-Path $clone) {
    # A single-plugin marketplace (this repo's shape) has plugin.json at the
    # root. Multi-plugin marketplaces do not, and there is no single version.
    $manifest = Join-Path $clone '.claude-plugin\plugin.json'
    if (Test-Path $manifest) {
        # Only a real version string is comparable against what is installed.
        $catalogVersion = (Get-Content $manifest -Raw | ConvertFrom-Json).version
        $catalog = $catalogVersion
    } else {
        $catalog = '(multi-plugin marketplace - no single version)'
    }

    # Not every marketplace is git-backed. Anthropic's official one ships as a
    # bundle (.gcs-sha, no .git), where the git drift check is meaningless.
    $isGit = Test-Path (Join-Path $clone '.git')

    if ($isGit) {
        $localHead = (git -C $clone rev-parse HEAD 2>$null)

        # Ask the remote directly. The clone's own origin/* ref is only as fresh
        # as its last fetch, so comparing against it would reproduce the very
        # blind spot this script exists to expose.
        $remoteHead = ((git -C $clone ls-remote origin HEAD 2>$null) -split '\s+') | Select-Object -First 1

        # .git is hidden on Windows, so Get-Item needs -Force.
        $fetchHead = Join-Path $clone '.git\FETCH_HEAD'
        $fetched = if (Test-Path $fetchHead) {
            (Get-Item $fetchHead -Force).LastWriteTime
        } else {
            'NEVER - no FETCH_HEAD; this clone has not fetched since it was created'
        }
    } else {
        $fetched = '(not git-backed - drift check does not apply)'
    }
} else {
    $catalog = '(marketplace not installed)'
}

$report = [ordered]@{
    'Installed version' = if ($installed) { $installed } else { '(not installed)' }
    'Catalog version'   = $catalog
}
if ($isGit) {
    $report['Catalog HEAD'] = if ($localHead)  { $localHead.Substring(0, 7) }  else { 'n/a' }
    $report['Remote HEAD']  = if ($remoteHead) { $remoteHead.Substring(0, 7) } else { 'n/a (offline?)' }
}
$report['Catalog fetched'] = if ($fetched) { $fetched } else { 'unknown' }
$report['autoUpdate']      = if ($null -eq $autoUpdate) { '(marketplace not registered)' }
                             elseif ($autoUpdate)       { 'true' }
                             else                       { 'FALSE - catalog will never refresh' }

[pscustomobject]$report | Format-List

$problem = $false

if ($autoUpdate -eq $false) {
    $problem = $true
    Write-Host "ROOT CAUSE: autoUpdate is off for this marketplace, so its catalog never refreshes." -ForegroundColor Red
    Write-Host "  Set it once in ~/.claude/settings.json under extraKnownMarketplaces.$Plugin :" -ForegroundColor Gray
    Write-Host '    "autoUpdate": true' -ForegroundColor Gray
}

if ($localHead -and $remoteHead -and $localHead -ne $remoteHead) {
    $problem = $true
    Write-Host "STALE CATALOG: it is behind GitHub, so 'plugin update' will report you are current." -ForegroundColor Red
}

if ($installed -and $catalogVersion -and $installed -ne $catalogVersion) {
    $problem = $true
    Write-Host "STALE INSTALL: installed $installed, catalog offers $catalogVersion." -ForegroundColor Yellow
}

if ($problem) {
    Write-Host ""
    Write-Host "Fix now (both lines - the first is the one that gets skipped):" -ForegroundColor Cyan
    Write-Host "  claude plugin marketplace update $Plugin" -ForegroundColor Gray
    if ($installedKey) {
        Write-Host "  claude plugin update $installedKey" -ForegroundColor Gray
    } else {
        Write-Host "  claude plugin update <plugin>@$Plugin" -ForegroundColor Gray
    }
    Write-Host "Then FULLY quit and relaunch - a new thread is not enough." -ForegroundColor Gray
} elseif ($localHead -and $remoteHead) {
    Write-Host "Up to date with the remote." -ForegroundColor Green
}

# A read-only diagnostic must never leave a failing exit code behind: internal
# git probes are allowed to fail (offline, non-git marketplace) without that
# meaning the check itself failed.
exit 0
