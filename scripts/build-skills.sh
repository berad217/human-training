#!/bin/bash
#
# build-skills.sh - Build Claude Code plugin skills from two source tracks
#
# Produces skills/<name>/ from:
#   1) Generated skills: workflow/guides/<source>.md combined with metadata
#      in the build_skill calls below (model-agnostic body + synthesized
#      frontmatter).
#   2) Session-authored skills: fully-formed skill packages under
#      skills-source/<name>/, copied through as-is (text files have CRLF
#      stripped so output is byte-identical regardless of which builder ran).
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
SKILLS_SOURCE_DIR="$REPO_ROOT/skills-source"

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

build_skill "workflow-orientation.md" "workflow-orientation" \
    "Use when entering a project to align it with the sprint-based workflow: empty project (scaffold rails), existing project with no workflow (propose onboarding), partial setup (gap report), canonical-healthy (drift check), or mature project with its own conventions (bridge mode via onboarding.md). Always audits read-only first, discusses, then acts non-destructively." \
    "Read, Write, Edit, Grep, Glob, Bash"

# --- Pass-through: copy session-authored skills from skills-source/ ---
# These are fully-formed packages (their own SKILL.md + any assets/evals).
# Text files have CRLF stripped so output is byte-identical to the PS builder.
copy_session_skill() {
    local src_dir="$1"
    local skill_name="$2"
    local dest_dir="$OUTPUT_DIR/$skill_name"

    if [[ -d "$dest_dir" ]]; then
        echo "WARNING: skills-source/$skill_name collides with a generated skill of the same name — skipping pass-through."
        return 1
    fi

    echo "Copying:  $skill_name (from skills-source/)"

    while IFS= read -r -d '' file; do
        local rel="${file#$src_dir/}"
        local out="$dest_dir/$rel"
        mkdir -p "$(dirname "$out")"
        case "${file,,}" in
            *.md|*.json|*.yml|*.yaml|*.txt|*.sh|*.ps1|*.py|*.js|*.ts|*.css|*.html)
                tr -d '\r' < "$file" > "$out"
                ;;
            *)
                cp "$file" "$out"
                ;;
        esac
    done < <(find "$src_dir" -type f -print0)

    echo "  -> $skill_name/ (session-authored)"
}

if [[ -d "$SKILLS_SOURCE_DIR" ]]; then
    for src in "$SKILLS_SOURCE_DIR"/*/; do
        [[ -d "$src" ]] || continue
        name="$(basename "$src")"
        copy_session_skill "${src%/}" "$name"
    done
fi

echo ""
echo "Build complete!"
echo ""
echo "Skills are distributed via the plugin manifest (.claude-plugin/plugin.json)."
echo "For local development:  claude --plugin-dir ."
