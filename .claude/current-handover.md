# Handover - Human-Training Workflow Project

## Quick Start

New AI: Start by reading `.claude/global-preferences.md` (communication style), then come back here.

## Project Context

**Project**: Human-Training - Standardized workflow templates for AI-human hobby project collaboration

**Purpose**: Create reusable templates and guidance docs that optimize the workflow from idea → spec → implementation for projects where a non-professional developer works with AI coding agents.

**Phase**: Documentation refinement - NEW foundational docs complete, now cleaning up old docs and preparing for remaining phases

**No spec for this project** - This is a meta-project about creating the workflow itself. We're building the templates that future projects will use.

## Where We Are

**NEW foundational docs in `.claude/` folder (COMPLETE):**
- ✅ `global-preferences.md` - User's cognitive and communication preferences
- ✅ `ideation-protocol.md` - How to conduct brainstorming conversations
- ✅ `spec-writing-guide.md` - How to write specs from ideation conversations
- ✅ `handover-guide.md` - How to write/use handover documents
- ✅ `current-handover.md` - This document

**Old docs in root and `templates/` folder (PARTIALLY CLEANED):**
- ✅ `templates/best-practices-ai-human-collab.md` - Cleaned up (removed Phase 1 & 3)
- ⏳ `templates/testing-standards.md` - Not yet reviewed
- ⏳ `templates/sprint-checklist.md` - Not yet reviewed
- ⏳ `templates/devlog-entry-template.md` - Not yet reviewed
- ⏳ `templates/project-spec-template.md` - Complements NEW spec-writing-guide
- ⏳ Various other old templates - Not yet reviewed

**Git status**: All work committed and pushed to branch `claude/read-handover-notes-011CUzhvRDartRA4AZt6hf39`

## This Session's Accomplishments

**Context reset tested successfully** - User pasted beginning of previous conversation that I didn't have access to (context glitch).

**Cleaned up best-practices document:**
1. Reviewed which sections overlapped with NEW docs
2. Removed Phase 1 (Idea to Spec) - covered by NEW ideation-protocol.md and spec-writing-guide.md
3. Removed Phase 3 (Context Management) - covered by NEW handover-guide.md
4. Updated Table of Contents
5. What remains in best-practices: Phase 2 (Implementation), Phase 4 (Iteration), Common Pitfalls, Success Metrics

**Key decisions made:**
- Token-based context management guidance REJECTED - User manages context resets based on "open loops" not token counts
- Tech stack tables and checklists REJECTED - Already covered or not needed
- Lean/adaptive handover philosophy CONFIRMED over comprehensive/rigid approach
- global-preferences.md stays SEPARATE from onboarding.md (different purposes, different scopes)

**Philosophy reinforced:**
- Context management is HUMAN's responsibility
- Reset timing based on local minimum of "balls in the air"
- NEW docs are guide-level (how to think), templates provide structure (what to fill in)

## Design Patterns Established

**Spec-for-LLM approach:**
- Success criteria (testable outcomes) instead of formal test definitions
- Concrete JSON examples, never just descriptions
- Flexible sprint granularity (context-reset friendly)
- Living document that evolves with implementation
- Meta-feedback mechanism for continuous improvement

**Handover philosophy:**
- Lean and adaptive (not comprehensive and rigid)
- Captures conversation context, not just state
- Adapts to what docs exist in project
- Focus on decisions in flight, what was tried, active discussions
- Incoming AI provides feedback if handover inadequate

**Context management philosophy:**
- Human controls timing based on "open loops"
- NOT based on token percentages or automatic triggers
- AI doesn't suggest when to reset
- Opportunistic resets at natural pause points

**Communication style:**
- Direct, no hedging
- Challenge assumptions, especially uncomfortable ones
- "That won't work because X" > "That's an interesting approach..."
- Humor when it reveals insight
- Precise when it matters, casual when it doesn't

## What's Left to Build

**Still need NEW documents for:**
1. **`.claude/onboarding.md`** - How to onboard new AI agents to work with this user (distinct from global-preferences which is personality/style)
2. **Implementation guidance** - How coding agents should work during sprints
3. **Testing guidance** - Strategy and standards for testing

**BEFORE creating NEW docs, should review existing:**
- `templates/testing-standards.md` (12K file - substantial)
- `templates/best-practices-ai-human-collab.md` Phase 2 content (Implementation)
- `templates/sprint-checklist.md`
- `templates/devlog-entry-template.md`

**Process:** Review existing → Extract useful bits → Create NEW if needed OR keep/refine existing

## Important Context About This Session

**Mid-conversation context glitch:**
- I lost access to the beginning of the conversation
- User had to paste it back to me
- The lost content included the "rounds 1, 2, 3" review of best-practices sections
- This worked - showed handover can handle disruptions

**What the rounds covered:**
- Round 1: Ideation sections (Phase 1.1-1.2) - REJECTED
- Round 2: Spec writing section (Phase 1.3) - REJECTED
- Round 3: Context management (Phase 3) - REJECTED, especially token guidance

## Next Steps

**Immediate (in next session):**
1. New AI: Read `.claude/global-preferences.md` and this handover
2. User will direct: Review existing implementation/testing docs before creating NEW versions
3. After review, create `.claude/onboarding.md`

**Then:**
4. Create or refine implementation guidance
5. Create or refine testing guidance
6. Clean up any remaining old docs
7. Eventually: Create README or quick-start guide as entry point

## Red Flags / Warnings

None for this project. It's documentation, low technical risk.

**Process note:** User wants to consult existing docs but NOT dive deep into them in this session - wants fresh context for that work.

## Meta Notes

**This is the second handover using the guide we created.**

First handover worked well enough to enable context reset. This session demonstrated:
- Handover can survive mid-session context glitches
- Pasting conversation history back in works
- User comfortable with opportunistic resets

Incoming AI: Continue the pattern of direct communication, challenge assumptions, keep it lean.

---

**Resume point:** User will start fresh session to tackle the remaining workflow areas (onboarding, implementation, testing).
