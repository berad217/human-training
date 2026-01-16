# Global Workflow - Brad

This file provides baseline instructions for all Claude Code sessions.

## About This Human

See `workflow/global-preferences.md` for detailed communication style.

**Quick summary:**
- Thinks in systems, learns by building
- Values intellectual honesty over social comfort
- Direct feedback preferred - "That won't work because X" beats hedging
- Struggles with mission creep - help define clear "done" criteria

## Project Lifecycle

I use a sprint-based development workflow with clear phases:

### Phase 0: Project Genesis (New Projects)
Use the **project-genesis** skill when:
- Starting a new project from an idea
- Need to turn concept into actionable spec
- Want help with scope definition and mission creep prevention

**Key deliverables:** spec.md, onboarding.md, DEVLOG.md skeleton

### Phase 1-N: Active Development
Use the **lifecycle-manager** skill for the inner development loop:
1. Orient (read onboarding.md, DEVLOG.md, any handover)
2. Implement feature from spec
3. Write tests immediately
4. Update DEVLOG with decisions and rationale
5. Check confidence bar - continue, complete sprint, or flag blocker

### Context Resets
Use the **handover-manager** skill when:
- Context window getting full (laggy responses)
- Stuck and need fresh perspective
- Natural pause point (end of sprint, milestone)
- User requests handover

**Key concept:** Handovers capture *ephemeral delta* - conversation context NOT in files.

### Creating Onboarding Docs
Use the **onboarding-creator** skill to create onboarding.md - the universal entry point for AI agents that works across all tools (Cursor, VSCode, Claude Code, web).

## Document Hierarchy

**Look for these in any project (locations may vary):**

| Document | Purpose | Common Locations |
|----------|---------|------------------|
| **onboarding.md** | Agent entry point, "office tour" | `onboarding.md`, `docs/onboarding.md` |
| **spec.md** | What to build | `spec.md`, `SPEC.md`, `docs/spec.md` |
| **DEVLOG.md** | What was built + why | `DEVLOG.md`, `docs/devlog.md` |
| **HANDOVER.md** | Ephemeral context | `HANDOVER.md`, `docs/.agents/current-handover.md` |
| **global-preferences.md** | How this human works | `docs/.agents/global-preferences.md` |

## The Confidence Bar

Use this threshold for autonomous decision-making:

- **HIGH** (just do it): Routine task, follows spec, unambiguous
- **MODERATE** (do it + document): Slight ambiguity, clear best path, highlight in DEVLOG
- **LOW** (STOP and ask): Multiple valid paths, significant tradeoffs, affects future sprints

**When in doubt, ask.** Better to confirm than implement wrong approach.

## Code Quality Standards

For implementation work, follow these patterns:

- **Type hints:** Required on all function parameters and returns
- **Docstrings:** Google-style with Args, Returns, Raises sections
- **Error handling:** Try-except around all I/O operations
- **Logging:** Log start/completion/errors for user-facing operations
- **Windows compatibility:** ASCII characters only in console output (no Unicode emojis in logs)

## Anti-Patterns to Avoid

- Making changes without reading existing code first
- Skipping DEVLOG updates after significant work
- Continuing when blocked (after 3 failed attempts, STOP and flag)
- Letting scope creep happen silently
- Duplicating content between docs (reference instead)
- Dumping large files into context (reference, don't copy)

## Working with Multiple AI Tools

These workflow documents work across all AI assistants:
- Claude Code (CLI, Desktop, VS Code extension)
- Cursor / Windsurf
- Web Claude, GPT, Gemini
- Any tool with file access

The project docs (onboarding.md, spec.md, DEVLOG.md) are the source of truth, not tool-specific configurations.

## Project-Specific Overrides

Individual projects can override this baseline by having their own:
- `.claude/CLAUDE.md` - Project-specific instructions
- `.claude/skills/` - Project-specific skills
- `docs/.agents/` - Project-specific workflow docs

Project settings take precedence over these global defaults.
