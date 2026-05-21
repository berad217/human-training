<#
.SYNOPSIS
    Installs the global Claude Code CLAUDE.md from this repo.

.DESCRIPTION
    Links (or copies) workflow/claude-code.md to ~/.claude/CLAUDE.md so the
    global instructions are available in every Claude Code session.

    Skills are NOT installed by this script anymore — they ship as a
    Claude Code plugin. Install them once with:

        /plugin install <this-repo-url>

    and Claude Code manages versioning and updates from there.

.PARAMETER RepoPath
    Path to the human-training repo. Defaults to parent of scripts folder.

.EXAMPLE
    ./scripts/setup-machine.ps1

.EXAMPLE
    # Run as Administrator to create a symlink that auto-syncs on git pull
    ./scripts/setup-machine.ps1
#>

param(
    [string]$RepoPath = (Split-Path -Parent $PSScriptRoot)
)

$ClaudeDir = Join-Path $env:USERPROFILE ".claude"

Write-Host "Claude Code Global Setup" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repo path:  $RepoPath" -ForegroundColor Gray
Write-Host "Claude dir: $ClaudeDir" -ForegroundColor Gray
Write-Host ""

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not (Test-Path $ClaudeDir)) {
    New-Item -ItemType Directory -Path $ClaudeDir | Out-Null
    Write-Host "Created: $ClaudeDir" -ForegroundColor Green
}

$ClaudeMdSource = Join-Path $RepoPath "workflow\claude-code.md"
$ClaudeMdTarget = Join-Path $ClaudeDir "CLAUDE.md"

if (Test-Path $ClaudeMdSource) {
    if (Test-Path $ClaudeMdTarget) {
        Remove-Item $ClaudeMdTarget -Force
    }
    if ($isAdmin) {
        New-Item -ItemType SymbolicLink -Path $ClaudeMdTarget -Target $ClaudeMdSource | Out-Null
        Write-Host "Symlinked: CLAUDE.md -> workflow/claude-code.md" -ForegroundColor Green
    } else {
        Copy-Item $ClaudeMdSource -Destination $ClaudeMdTarget -Force
        Write-Host "Copied: CLAUDE.md (re-run as Administrator for an auto-syncing symlink)" -ForegroundColor Yellow
    }
} else {
    Write-Host "NOTE: workflow/claude-code.md not found." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Done. To install the workflow skills, run in Claude Code:" -ForegroundColor Cyan
Write-Host "  /plugin install <this-repo-url>" -ForegroundColor Gray
