<#
.SYNOPSIS
    Builds Claude Code plugin skills from two sources: model-agnostic workflow
    documents, and fully-formed session-authored skill packages.

.DESCRIPTION
    Produces skills/<name>/ for each skill the plugin ships. Two source tracks
    feed the same output directory:

      1. Generated skills — workflow/guides/<source>.md + an entry in the
         $skillDefinitions table below. The body is model-agnostic; the
         frontmatter is synthesized from $skillDefinitions.

      2. Session-authored skills — fully-formed skill packages dropped into
         skills-source/<name>/. These are copied through to skills/<name>/
         as-is (with line-ending normalization).

    Output is normalized to LF / no BOM so the two builders (this one and
    build-skills.sh) produce byte-identical output regardless of which one
    populated the committed skills/ tree.

.EXAMPLE
    ./scripts/build-skills.ps1

.EXAMPLE
    ./scripts/build-skills.ps1 -OutputDir ./skills -Verbose
#>

param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$OutputDir = "",
    [switch]$Verbose
)

if (-not $OutputDir) {
    $OutputDir = Join-Path $RepoRoot "skills"
}

$WorkflowDir = Join-Path $RepoRoot "workflow"
$GuidesDir = Join-Path $WorkflowDir "guides"
$TemplatesDir = Join-Path $WorkflowDir "templates"
$SkillsSourceDir = Join-Path $RepoRoot "skills-source"

# Skill definitions - maps source files to skill metadata
# Edit this to add/modify skills
$skillDefinitions = @{
    "lifecycle.md" = @{
        name = "lifecycle-manager"
        description = "Use when actively implementing features in Sprint 1-N: writing code, writing tests right after, updating the DEVLOG with decisions and rationale, checking the confidence bar before acting, orienting at the start of a session, or handling a mid-sprint context reset. The core test-code-document development loop."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "Bash", "TodoWrite")
        assets = @()
    }
    "handover-guide.md" = @{
        name = "handover-manager"
        description = "Use when the user requests a handover, the context window is getting full or laggy, at a natural pause point (end of sprint or milestone), or when stuck and a fresh perspective is needed. Creates a handover capturing the ephemeral conversation delta not already in the project files. Works with any AI agent."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob")
        assets = @("handover.md")
    }
    "onboarding-guide.md" = @{
        name = "onboarding-creator"
        description = "Use when setting up a new project, after the Sprint 0 spec is complete, or when an AI agent entry point is missing. Creates onboarding.md, the universal orientation doc that works across any environment (Cursor, VSCode, Claude Code, web) - the office tour, not the employee handbook."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob")
        assets = @("onboarding.md")
    }
    "genesis.md" = @{
        name = "project-genesis"
        description = "Use when starting a new project, brainstorming an idea, evaluating whether something is worth building, or turning a concept into a technical spec. Covers Sprint 0 end to end: ideation (challenge ideas, red-team, force scope) and spec writing (concrete specs for coding agents). Enter at brainstorming, enter at speccing, or flow through both."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "WebSearch", "WebFetch")
        assets = @("ideation-protocol.md", "spec-writing-guide.md", "spec.md", "testing-standards.md")
    }
    "workflow-orientation.md" = @{
        name = "workflow-orientation"
        description = "Use when entering a project to align it with the sprint-based workflow: empty project (scaffold rails), existing project with no workflow (propose onboarding), partial setup (gap report), canonical-healthy (drift check), or mature project with its own conventions (bridge mode via onboarding.md). Always audits read-only first, discusses, then acts non-destructively."
        allowedTools = @("Read", "Write", "Edit", "Grep", "Glob", "Bash")
        assets = @()
    }
}

Write-Host "Building Claude Code plugin skills from workflow docs..." -ForegroundColor Cyan
Write-Host "Source: $GuidesDir" -ForegroundColor Gray
Write-Host "Output: $OutputDir" -ForegroundColor Gray
Write-Host ""

# Start clean so skills removed from the definitions above don't linger.
Remove-Item -Recurse -Force $OutputDir -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
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

    $skillDir = Join-Path $OutputDir $skillName
    $assetsDir = Join-Path $skillDir "assets"

    try {
        New-Item -ItemType Directory -Force -Path $skillDir | Out-Null

        $sourceContent = Get-Content $sourcePath -Raw -Encoding UTF8

        # Build frontmatter with explicit LF. Ends with a blank line before
        # the body to match build-skills.sh's heredoc (which emits ---\n\n).
        $toolsList = ($def.allowedTools | ForEach-Object { $_ }) -join ", "
        $frontmatter = "---`n" +
            "name: $skillName`n" +
            "description: $($def.description)`n" +
            "allowed-tools: [$toolsList]`n" +
            "---`n`n"

        # Write SKILL.md: normalize to LF, write UTF-8 without BOM, end with
        # exactly one newline so the output is byte-identical to
        # build-skills.sh (its heredoc forces a single trailing newline).
        $skillContent = ($frontmatter + $sourceContent) -replace "`r`n", "`n"
        $skillContent = $skillContent.TrimEnd("`n") + "`n"
        [System.IO.File]::WriteAllText((Join-Path $skillDir "SKILL.md"), $skillContent, $utf8NoBom)

        # Copy asset files if any (normalized to LF / no BOM)
        if ($def.assets.Count -gt 0) {
            New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null
            foreach ($asset in $def.assets) {
                $assetSource = Join-Path $TemplatesDir $asset
                if (-not (Test-Path $assetSource)) {
                    $assetSource = Join-Path $GuidesDir $asset
                }
                if (Test-Path $assetSource) {
                    $assetText = [System.IO.File]::ReadAllText($assetSource) -replace "`r`n", "`n"
                    [System.IO.File]::WriteAllText((Join-Path $assetsDir $asset), $assetText, $utf8NoBom)
                    if ($Verbose) {
                        Write-Host "  Added asset: $asset" -ForegroundColor Gray
                    }
                } else {
                    Write-Warning "  Asset not found: $asset"
                }
            }
        }

        Write-Host "  -> $skillName/SKILL.md" -ForegroundColor Green
        $builtCount++
    }
    catch {
        Write-Error "Failed to build $skillName : $_"
        $errorCount++
    }
}

# Copy session-authored skills from skills-source/ into the output dir.
# These are fully-formed skill packages (their own SKILL.md + any
# assets/evals) — no transformation, just line-ending normalization so
# both builders produce byte-identical output.
$copiedCount = 0
if (Test-Path $SkillsSourceDir) {
    Get-ChildItem -Path $SkillsSourceDir -Directory | ForEach-Object {
        $srcDir = $_.FullName
        $skillName = $_.Name
        $destDir = Join-Path $OutputDir $skillName

        if (Test-Path $destDir) {
            Write-Warning "skills-source/$skillName collides with a generated skill of the same name — skipping pass-through."
            $errorCount++
            return
        }

        Write-Host "Copying:  $skillName (from skills-source/)" -ForegroundColor Yellow

        Get-ChildItem -Path $srcDir -Recurse -File | ForEach-Object {
            $relPath = $_.FullName.Substring($srcDir.Length).TrimStart('\','/')
            $outPath = Join-Path $destDir $relPath
            $outParent = Split-Path -Parent $outPath
            New-Item -ItemType Directory -Force -Path $outParent | Out-Null

            # Normalize line endings to LF for text files (matches sh builder's
            # tr -d '\r'). Binary files are byte-copied as-is.
            $textExtensions = @('.md', '.json', '.yml', '.yaml', '.txt', '.sh', '.ps1', '.py', '.js', '.ts', '.css', '.html')
            if ($textExtensions -contains $_.Extension.ToLower()) {
                $text = [System.IO.File]::ReadAllText($_.FullName) -replace "`r`n", "`n"
                [System.IO.File]::WriteAllText($outPath, $text, $utf8NoBom)
            } else {
                Copy-Item -LiteralPath $_.FullName -Destination $outPath -Force
            }
            if ($Verbose) {
                Write-Host "  -> $skillName/$relPath" -ForegroundColor Gray
            }
        }

        Write-Host "  -> $skillName/ (session-authored)" -ForegroundColor Green
        $copiedCount++
    }
}

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Cyan
Write-Host "  Generated skills: $builtCount" -ForegroundColor Green
Write-Host "  Session-authored skills: $copiedCount" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "  Errors: $errorCount" -ForegroundColor Red
}
Write-Host ""
Write-Host "Skills are distributed via the plugin manifest (.claude-plugin/plugin.json)." -ForegroundColor Yellow
Write-Host "For local development:  claude --plugin-dir ." -ForegroundColor Gray
