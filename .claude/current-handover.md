# Handover - Human-Training Workflow Project

## Quick Start

New AI: Start by reading `.claude/global-preferences.md` (communication style), then `.claude/onboarding.md` (if it exists - it may not for this meta-project), then come back here.

## Project Context

**Project**: Human-Training - Standardized workflow templates for AI-human hobby project collaboration

**Purpose**: Create reusable templates and guidance docs that optimize the workflow from idea → spec → implementation for projects where a non-professional developer works with AI coding agents.

**Phase**: Documentation creation - establishing foundational workflow documents

**No spec for this project** - This is a meta-project about creating the workflow itself. We're building the templates that future projects will use.

## Where We Are

**What exists in `.claude/` folder:**
- ✅ `global-preferences.md` - User's cognitive and communication preferences
- ✅ `ideation-protocol.md` - How to conduct brainstorming conversations
- ✅ `spec-writing-guide.md` - How to write specs from ideation conversations
- ✅ `handover-guide.md` - How to write/use handover documents (just completed)
- ✅ `current-handover.md` - This document

**What exists in root and `templates/` folder:**
- Various template files from previous session (user hasn't read them yet)
- `onboarding.md`, `handover-template.md`, `patterns-extracted.md`, etc.
- Templates folder with more detailed templates

**Git status**: All `.claude/` files committed and pushed to branch `claude/sce-workflow-docs-011CUxpgYUKeQe5LNzd6Qt2C`

## Conversation Context

**What we accomplished this session:**

1. **Established the pipeline phases:**
   - Ideation → Spec Creation → Implementation → DEVLOG Management → Handovers

2. **Created foundational guidance documents:**
   - Started with global preferences (user pasted theirs)
   - Built ideation protocol (how to brainstorm, challenge assumptions)
   - Built spec-writing guide (how to translate ideation → spec for LLM consumption)
   - Built handover guide (how to capture conversation context)

3. **Key design decisions:**
   - **Lean over comprehensive** - Keep docs digestible and adaptable
   - **LLM-targeted** - Primary audience is AI agents, not the human
   - **Continuous improvement** - Feedback loops built into each phase
   - **Living documents** - Nothing is frozen, everything evolves
   - **Show, don't tell** - Concrete examples over abstract descriptions

**Philosophy that emerged:**
- User is non-professional coder building hobby projects with AI agents
- Values: intellectual honesty, modularity, discovery through building
- Struggles with: mission creep, testing discipline
- Learns by: building, not reading documentation
- This is a partnership between human (systems design) and AI (implementation)

**Key tensions we're navigating:**
- Mission creep vs discovery through exploration
- Prescriptive guidance vs flexible adaptation
- Comprehensive docs vs lean/digestible
- Testing discipline vs not wanting to test manually

**What we haven't tackled yet:**
- Implementation phase guidance (how coding agents should work during sprints)
- DEVLOG management (lean maintenance, archiving old sprints)
- Review of existing templates in `templates/` folder (decide what to keep/refine/discard)

**User said:**
- Wants to dogfood the handover process (test context reset)
- Hasn't read the old template docs yet - started fresh from first principles
- After context reset, tackle remaining workflow phases

## Design Patterns Established

**Spec-for-LLM approach:**
- Success criteria (testable outcomes) instead of formal test definitions
- Concrete JSON examples, never just descriptions
- Flexible sprint granularity (context-reset friendly)
- Living document that evolves with implementation
- Meta-feedback mechanism for continuous improvement

**Handover philosophy:**
- Captures conversation context, not just state
- Adapts to what docs exist in project
- Focus on decisions in flight, what was tried, active discussions
- Incoming AI provides feedback if handover inadequate

**Communication style:**
- Direct, no hedging
- Challenge assumptions, especially uncomfortable ones
- "That won't work because X" > "That's an interesting approach..."
- Humor when it reveals insight
- Precise when it matters, casual when it doesn't

## Red Flags / Warnings

None for this project. It's documentation, low technical risk.

**Process concern:** User hasn't reviewed the old templates yet. When we tackle implementation/DEVLOG phases next, we should check if `templates/` folder has useful material or if we're reinventing wheels.

## Next Steps (After Context Reset)

**Immediate:**
1. New AI: Read `.claude/global-preferences.md` and this handover
2. Confirm understanding of where we are
3. User will decide: Continue with remaining workflow phases OR review existing templates first

**Remaining work:**
- Implementation phase guidance (sprint workflow for coding agents)
- DEVLOG management guide (archiving, keeping it lean)
- Review/refine existing templates in `templates/` folder
- Eventually: Create README or quick-start guide as entry point

**Files to be aware of:**
- `templates/` folder has old template docs (not yet reviewed)
- Root has `onboarding.md`, `handover-template.md`, `patterns-extracted.md`, `sidequest-collaboration-stack.md`

## Meta Notes

**This is the first handover using the guide we just created.**

Incoming AI: If this handover is inadequate, say so. We're dogfooding the process to see if the guide actually works. Feedback welcome.

---

**Resume point:** User will start fresh session, read this handover, and we'll continue building out the workflow pipeline.
