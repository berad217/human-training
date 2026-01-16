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

    # Build SKILL.md with frontmatter
    cat > "$skill_dir/SKILL.md" << EOF
---
name: $skill_name
description: $description
allowed-tools: [$allowed_tools]
---

$(cat "$source_path")
EOF

    # Copy assets if any
    if [[ ${#assets[@]} -gt 0 ]]; then
        mkdir -p "$assets_dir"
        for asset in "${assets[@]}"; do
            if [[ -f "$TEMPLATES_DIR/$asset" ]]; then
                cp "$TEMPLATES_DIR/$asset" "$assets_dir/"
            fi
        done
    fi

    # Create .skill zip
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
    "Active development workflow for Sprint 1-N. Handles orientation, the confidence bar for decision-making, testing approach, documentation, and context resets." \
    "Read, Write, Edit, Grep, Glob, Bash, TodoWrite"

build_skill "handover-guide.md" "handover-manager" \
    "Create handovers for smooth context resets between AI sessions. Captures ephemeral conversation context (the delta) not documented elsewhere. Works with any AI agent." \
    "Read, Write, Edit, Grep, Glob" \
    "handover.md"

build_skill "onboarding-guide.md" "onboarding-creator" \
    "Create onboarding.md - the universal entry point for AI agents in any environment (Cursor, VSCode, Claude Code, web). The office tour, not the employee handbook." \
    "Read, Write, Edit, Grep, Glob" \
    "onboarding.md"

build_skill "genesis.md" "project-genesis" \
    "Guide Sprint 0 from idea to spec. Challenge ideas, force scope definition, prevent mission creep, then create technical specification with concrete examples." \
    "Read, Write, Edit, Grep, Glob, WebSearch, WebFetch" \
    "project-spec-template.md" "spec.md"

build_skill "ideation-protocol.md" "ideation-helper" \
    "Brainstorm with the human effectively. Challenge assumptions, red-team ideas, check if solutions exist, force scope decisions. Help decide build vs park vs abandon." \
    "Read, Write, Grep, Glob, WebSearch, WebFetch"

build_skill "spec-writing-guide.md" "spec-writer" \
    "Write technical specifications using the 4-round process: info gathering, architecture, review, deliver. Create specs with concrete JSON examples, not vague descriptions." \
    "Read, Write, Edit, Grep, Glob" \
    "project-spec-template.md" "spec.md" "testing-standards.md"

echo ""
echo "Build complete!"
echo ""
echo "To install globally:"
echo "  Extract each .skill to ~/.claude/skills/"
echo "  Or run: ./scripts/setup-machine.sh"
