<#
.SYNOPSIS
    Sets up Claude Code with global skills and configuration from this repo.

.DESCRIPTION
    This script creates symlinks from ~/.claude/ to this repository, making
    your workflow docs and skills available across all Claude Code sessions.

    Run this once per machine after cloning the repo.

.PARAMETER RepoPath
    Path to the human-training repo. Defaults to parent of scripts folder.

.PARAMETER Force
    Overwrite existing files/symlinks without prompting.

.EXAMPLE
    ./scripts/setup-machine.ps1

.EXAMPLE
    ./scripts/setup-machine.ps1 -Force
#>

param(
    [string]$RepoPath = (Split-Path -Parent $PSScriptRoot),
    [switch]$Force
)

$ClaudeDir = Join-Path $env:USERPROFILE ".claude"

Write-Host "Claude Code Global Setup" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repo path: $RepoPath" -ForegroundColor Gray
Write-Host "Claude dir: $ClaudeDir" -ForegroundColor Gray
Write-Host ""

# Check if running as admin (needed for symlinks on Windows)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "NOTE: Running without admin privileges." -ForegroundColor Yellow
    Write-Host "      Will copy files instead of creating symlinks." -ForegroundColor Yellow
    Write-Host "      Re-run as Administrator for symlinks (auto-sync on git pull)." -ForegroundColor Yellow
    Write-Host ""
}

# Ensure .claude directory exists
if (-not (Test-Path $ClaudeDir)) {
    New-Item -ItemType Directory -Path $ClaudeDir | Out-Null
    Write-Host "Created: $ClaudeDir" -ForegroundColor Green
}

# Build skills first if they don't exist
$SkillsSource = Join-Path $RepoPath "claude-skills"
if (-not (Test-Path "$SkillsSource\*.skill")) {
    Write-Host "Building skills first..." -ForegroundColor Yellow
    $buildScript = Join-Path $RepoPath "scripts\build-skills.ps1"
    if (Test-Path $buildScript) {
        & $buildScript
    } else {
        Write-Error "build-skills.ps1 not found. Run from repo root."
        exit 1
    }
}

# Extract skills to ~/.claude/skills/
$SkillsTarget = Join-Path $ClaudeDir "skills"
Write-Host "Installing skills to $SkillsTarget..." -ForegroundColor Yellow

# Create skills directory
New-Item -ItemType Directory -Force -Path $SkillsTarget | Out-Null

# Extract each .skill file (rename to .zip temporarily since PowerShell requires .zip extension)
Get-ChildItem -Path $SkillsSource -Filter "*.skill" | ForEach-Object {
    $skillFile = $_
    $skillName = $skillFile.BaseName
    $extractPath = Join-Path $SkillsTarget $skillName

    # Remove existing if Force or doesn't exist
    if (Test-Path $extractPath) {
        if ($Force) {
            Remove-Item -Recurse -Force $extractPath
        } else {
            Write-Host "  Skipping $skillName (exists, use -Force to overwrite)" -ForegroundColor Gray
            return
        }
    }

    # Copy to temp .zip file (PowerShell only supports .zip extension)
    $tempZip = Join-Path $env:TEMP "$skillName-$(Get-Random).zip"
    Copy-Item $skillFile.FullName -Destination $tempZip

    # Extract
    Expand-Archive -Path $tempZip -DestinationPath $SkillsTarget -Force
    Write-Host "  Installed: $skillName" -ForegroundColor Green

    # Cleanup temp file
    Remove-Item $tempZip -ErrorAction SilentlyContinue
}

# Create/update CLAUDE.md
$ClaudeMdSource = Join-Path $RepoPath "workflow\claude-code.md"
$ClaudeMdTarget = Join-Path $ClaudeDir "CLAUDE.md"

if (Test-Path $ClaudeMdSource) {
    if ($isAdmin) {
        # Create symlink
        if (Test-Path $ClaudeMdTarget) {
            Remove-Item $ClaudeMdTarget -Force
        }
        New-Item -ItemType SymbolicLink -Path $ClaudeMdTarget -Target $ClaudeMdSource | Out-Null
        Write-Host "Symlinked: CLAUDE.md -> workflow/claude-code.md" -ForegroundColor Green
    } else {
        # Copy file
        Copy-Item $ClaudeMdSource -Destination $ClaudeMdTarget -Force
        Write-Host "Copied: CLAUDE.md (re-run as admin for symlink)" -ForegroundColor Yellow
    }
} else {
    Write-Host "NOTE: workflow/claude-code.md not found. Create it for global instructions." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your global Claude Code configuration:" -ForegroundColor Yellow
Write-Host "  Skills: $SkillsTarget" -ForegroundColor Gray
Write-Host "  Config: $ClaudeMdTarget" -ForegroundColor Gray
Write-Host ""
Write-Host "These will be available in ALL Claude Code sessions on this machine." -ForegroundColor Green
Write-Host ""
Write-Host "To update after editing workflow docs:" -ForegroundColor Yellow
Write-Host "  1. Edit files in workflow/ (source of truth)" -ForegroundColor Gray
Write-Host "  2. Run: ./scripts/build-skills.ps1" -ForegroundColor Gray
Write-Host "  3. Run: ./scripts/setup-machine.ps1 -Force" -ForegroundColor Gray
