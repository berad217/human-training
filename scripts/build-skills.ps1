<#
.SYNOPSIS
    Builds Claude Code .skill files from model-agnostic workflow documents.

.DESCRIPTION
    This script reads workflow guides from workflow/guides/ and packages them
    into Claude Code .skill files with appropriate frontmatter and assets.

    The workflow docs remain the SOURCE OF TRUTH (model-agnostic).
    The .skill files are GENERATED artifacts for Claude Code specifically.

.EXAMPLE
    ./scripts/build-skills.ps1

.EXAMPLE
    ./scripts/build-skills.ps1 -OutputDir ./claude-skills -Verbose
#>

param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputDir = "",
    [switch]$Verbose
)

if (-not $OutputDir) {
    $OutputDir = Join-Path $RepoRoot "claude-skills"
}

$WorkflowDir = Join-Path $RepoRoot "workflow"
$GuidesDir = Join-Path $WorkflowDir "guides"
$TemplatesDir = Join-Path $WorkflowDir "templates"

# Skill definitions - maps source files to skill metadata
# Edit this to add/modify skills
$skillDefinitions = @{
    "lifecycle.md" = @{
        name = "lifecycle-manager"
        description = "Active development workflow for Sprint 1-N. Handles orientation, the confidence bar for decision-making, testing approach, documentation, and context resets."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "Bash", "TodoWrite")
        assets = @()  # No specific template needed
    }
    "handover-guide.md" = @{
        name = "handover-manager"
        description = "Create handovers for smooth context resets between AI sessions. Captures ephemeral conversation context (the delta) not documented elsewhere. Works with any AI agent."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob")
        assets = @("handover.md")
    }
    "onboarding-guide.md" = @{
        name = "onboarding-creator"
        description = "Create onboarding.md - the universal entry point for AI agents in any environment (Cursor, VSCode, Claude Code, web). The office tour, not the employee handbook."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob")
        assets = @("onboarding.md")
    }
    "genesis.md" = @{
        name = "project-genesis"
        description = "Guide Sprint 0 from idea to spec. Challenge ideas, force scope definition, prevent mission creep, then create technical specification with concrete examples."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "WebSearch", "WebFetch")
        assets = @("project-spec-template.md", "spec.md")
    }
    "ideation-protocol.md" = @{
        name = "ideation-helper"
        description = "Brainstorm with the human effectively. Challenge assumptions, red-team ideas, check if solutions exist, force scope decisions. Help decide build vs park vs abandon."
        allowedTools = @("Read", "Write", "Grep", "Glob", "WebSearch", "WebFetch")
        assets = @()
    }
    "spec-writing-guide.md" = @{
        name = "spec-writer"
        description = "Write technical specifications using the 4-round process: info gathering, architecture, review, deliver. Create specs with concrete JSON examples, not vague descriptions."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob")
        assets = @("project-spec-template.md", "spec.md", "testing-standards.md")
    }
}

# Ensure output directory exists
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

Write-Host "Building Claude Code skills from workflow docs..." -ForegroundColor Cyan
Write-Host "Source: $GuidesDir" -ForegroundColor Gray
Write-Host "Output: $OutputDir" -ForegroundColor Gray
Write-Host ""

$builtCount = 0
$errorCount = 0

foreach ($sourceFile in $skillDefinitions.Keys) {
    $def = $skillDefinitions[$sourceFile]
    $skillName = $def.name
    $sourcePath = Join-Path $GuidesDir $sourceFile

    if (-not (Test-Path $sourcePath)) {
        Write-Warning "Source file not found: $sourcePath"
        $errorCount++
        continue
    }

    Write-Host "Building: $skillName" -ForegroundColor Yellow

    # Create temp directory for skill contents
    $tempDir = Join-Path $env:TEMP "skill-build-$skillName-$(Get-Random)"
    $skillDir = Join-Path $tempDir $skillName
    $assetsDir = Join-Path $skillDir "assets"

    try {
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
        New-Item -ItemType Directory -Force -Path $skillDir | Out-Null

        # Read source content
        $sourceContent = Get-Content $sourcePath -Raw -Encoding UTF8

        # Build frontmatter
        $toolsList = ($def.allowedTools | ForEach-Object { $_ }) -join ", "
        $frontmatter = @"
---
name: $skillName
description: $($def.description)
allowed-tools: [$toolsList]
---

"@

        # Write SKILL.md with frontmatter + source content
        $skillContent = $frontmatter + $sourceContent
        $skillMdPath = Join-Path $skillDir "SKILL.md"
        Set-Content -Path $skillMdPath -Value $skillContent -NoNewline -Encoding UTF8

        if ($Verbose) {
            Write-Host "  Created SKILL.md ($([math]::Round((Get-Item $skillMdPath).Length / 1024, 1)) KB)" -ForegroundColor Gray
        }

        # Copy asset files if any
        if ($def.assets.Count -gt 0) {
            New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null
            foreach ($asset in $def.assets) {
                $assetSource = Join-Path $TemplatesDir $asset
                if (Test-Path $assetSource) {
                    Copy-Item $assetSource -Destination $assetsDir
                    if ($Verbose) {
                        Write-Host "  Added asset: $asset" -ForegroundColor Gray
                    }
                } else {
                    Write-Warning "  Asset not found: $asset"
                }
            }
        }

        # Create .skill zip (PowerShell requires .zip extension, so we create then rename)
        $zipFile = Join-Path $OutputDir "$skillName.zip"
        $skillFile = Join-Path $OutputDir "$skillName.skill"
        Remove-Item $zipFile -ErrorAction SilentlyContinue
        Remove-Item $skillFile -ErrorAction SilentlyContinue

        # Zip the skill directory (from parent so folder name is preserved in archive)
        Compress-Archive -Path $skillDir -DestinationPath $zipFile -Force

        # Rename to .skill
        Rename-Item -Path $zipFile -NewName "$skillName.skill"

        $fileSize = [math]::Round((Get-Item $skillFile).Length / 1024, 1)
        Write-Host "  -> $skillName.skill ($fileSize KB)" -ForegroundColor Green

        $builtCount++
    }
    catch {
        Write-Error "Failed to build $skillName : $_"
        $errorCount++
    }
    finally {
        # Cleanup temp directory
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Cyan
Write-Host "  Skills built: $builtCount" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "  Errors: $errorCount" -ForegroundColor Red
}
Write-Host ""
Write-Host "To install globally:" -ForegroundColor Yellow
Write-Host "  1. Extract each .skill file to ~/.claude/skills/" -ForegroundColor Gray
Write-Host "  2. Or run: ./scripts/setup-machine.ps1" -ForegroundColor Gray
