#!/bin/bash
#
# build-skills.sh - Build Claude Code plugin skills from workflow docs
#
# Generates skills/<name>/SKILL.md (+ assets/) from the model-agnostic
# guides in workflow/. The workflow docs are the source of truth; the
# skills/ directory is a generated artifact bundled by the plugin
# (see .claude-plugin/plugin.json).
#
# Usage: ./scripts/build-skills.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${OUTPUT_DIR:-$REPO_ROOT/skills}"
WORKFLOW_DIR="$REPO_ROOT/workflow"
GUIDES_DIR="$WORKFLOW_DIR/guides"
TEMPLATES_DIR="$WORKFLOW_DIR/templates"

echo "Building Claude Code plugin skills from workflow docs..."
echo "Source: $GUIDES_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

# Start clean so skills removed from the build definitions don't linger.
rm -rf "$OUTPUT_DIR"
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

    local skill_dir="$OUTPUT_DIR/$skill_name"
    local assets_dir="$skill_dir/assets"
    mkdir -p "$skill_dir"

    # SKILL.md = Claude-specific frontmatter + the model-agnostic guide.
    # Strip CR so output is LF-only regardless of the source's line endings.
    cat > "$skill_dir/SKILL.md" << SKILL_EOF
---
name: $skill_name
description: $description
allowed-tools: [$allowed_tools]
---

$(tr -d '\r' < "$source_path")
SKILL_EOF

    # Copy assets (also CR-stripped) if any
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

    echo "  -> $skill_name/SKILL.md"
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
    "ideation-protocol.md" "spec-writing-guide.md" "spec.md" "testing-standards.md"

echo ""
echo "Build complete!"
echo ""
echo "Skills are distributed via the plugin manifest (.claude-plugin/plugin.json)."
echo "For local development:  claude --plugin-dir ."
