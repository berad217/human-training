#!/bin/bash
#
# build-skills.sh - Build Claude Code .skill files from workflow docs
#
# Usage: ./scripts/build-skills.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${OUTPUT_DIR:-$REPO_ROOT/claude-skills}"
WORKFLOW_DIR="$REPO_ROOT/workflow"
GUIDES_DIR="$WORKFLOW_DIR/guides"
TEMPLATES_DIR="$WORKFLOW_DIR/templates"

echo "Building Claude Code skills from workflow docs..."
echo "Source: $GUIDES_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

mkdir -p "$OUTPUT_DIR"

# Function to build a single skill
build_skill() {
    local source_file="$1"
    local skill_name="$2"
    local description="$3"
    local allowed_tools="$4"
    shift 4
    local assets=("$@")

    local source_path="$GUIDES_DIR/$source_file"

    if [[ ! -f "$source_path" ]]; then
        echo "WARNING: Source file not found: $source_path"
        return 1
    fi

    echo "Building: $skill_name"

    # Create temp directory
    local temp_dir=$(mktemp -d)
    local skill_dir="$temp_dir/$skill_name"
    local assets_dir="$skill_dir/assets"

    mkdir -p "$skill_dir"

    # Build SKILL.md with frontmatter. Strip CR so output is LF-only
    # regardless of the source file's line endings (CI compares with the
    # PowerShell builder's output, which also normalizes to LF).
    cat > "$skill_dir/SKILL.md" << SKILL_EOF
---
name: $skill_name
description: $description
allowed-tools: [$allowed_tools]
---

$(tr -d '\r' < "$source_path")
SKILL_EOF

    # Copy assets if any
    if [[ ${#assets[@]} -gt 0 ]]; then
        mkdir -p "$assets_dir"
        for asset in "${assets[@]}"; do
            if [[ -f "$TEMPLATES_DIR/$asset" ]]; then
                tr -d '\r' < "$TEMPLATES_DIR/$asset" > "$assets_dir/$asset"
            elif [[ -f "$GUIDES_DIR/$asset" ]]; then
                tr -d '\r' < "$GUIDES_DIR/$asset" > "$assets_dir/$asset"
            else
                echo "  WARNING: asset not found: $asset"
            fi
        done
    fi

    # Create .skill zip (POSIX forward-slash paths)
    local skill_file="$OUTPUT_DIR/$skill_name.skill"
    rm -f "$skill_file"
    (cd "$temp_dir" && zip -rq "$skill_file" "$skill_name")

    local file_size=$(du -h "$skill_file" | cut -f1)
    echo "  -> $skill_name.skill ($file_size)"

    # Cleanup
    rm -rf "$temp_dir"
}

# Build each skill
build_skill "lifecycle.md" "lifecycle-manager" \
    "Use when actively implementing features in Sprint 1-N: writing code, writing tests right after, updating the DEVLOG with decisions and rationale, checking the confidence bar before acting, orienting at the start of a session, or handling a mid-sprint context reset. The core test-code-document development loop." \
    "Read, Write, Edit, Grep, Glob, Bash, TodoWrite"

build_skill "handover-guide.md" "handover-manager" \
    "Use when the user requests a handover, the context window is getting full or laggy, at a natural pause point (end of sprint or milestone), or when stuck and a fresh perspective is needed. Creates a handover capturing the ephemeral conversation delta not already in the project files. Works with any AI agent." \
    "Read, Write, Edit, Grep, Glob" \
    "handover.md"

build_skill "onboarding-guide.md" "onboarding-creator" \
    "Use when setting up a new project, after the Sprint 0 spec is complete, or when an AI agent entry point is missing. Creates onboarding.md, the universal orientation doc that works across any environment (Cursor, VSCode, Claude Code, web) - the office tour, not the employee handbook." \
    "Read, Write, Edit, Grep, Glob" \
    "onboarding.md"

build_skill "genesis.md" "project-genesis" \
    "Use when starting a new project, brainstorming an idea, evaluating whether something is worth building, or turning a concept into a technical spec. Covers Sprint 0 end to end: ideation (challenge ideas, red-team, force scope) and spec writing (concrete specs for coding agents). Enter at brainstorming, enter at speccing, or flow through both." \
    "Read, Write, Edit, Grep, Glob, WebSearch, WebFetch" \
    "ideation-protocol.md" "spec-writing-guide.md" "project-spec-template.md" "spec.md" "testing-standards.md"

echo ""
echo "Build complete!"
echo ""
echo "To install globally:"
echo "  Extract each .skill to ~/.claude/skills/"
echo "  Or (Windows): ./scripts/setup-machine.ps1"
